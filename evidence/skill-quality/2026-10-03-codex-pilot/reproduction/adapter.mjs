import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { spawn, spawnSync } from 'node:child_process';
import { finished } from 'node:stream/promises';
import { fileURLToPath } from 'node:url';

export function versionMetadata(probe) {
  const match = probe?.status === 0 && typeof probe.stdout === 'string'
    ? probe.stdout.trim().match(/^codex-cli\s+([0-9][0-9A-Za-z.+-]*)$/) : null;
  return {
    codex_version: match?.[1] || null,
    codex_version_source: match ? 'pre-invocation CLI version probe' : 'unknown'
  };
}

export function createInvocation(input, workspace, globalSkills, localSkills = []) {
  const disabled = [...globalSkills];
  if (!input.case_id || input.variant === 'without_skill') disabled.push(...localSkills);
  const config = [...new Set(disabled)].map(p => `{path=${JSON.stringify(p)},enabled=false}`).join(',');
  const model = (input.model || 'gpt-6.1-sol').replace(/^openai\//, '');
  if (model.includes('/')) throw new Error('This adapter supports OpenAI Codex models only');
  return {
    command: 'codex',
    args: [
      '--no-daemon', '--dangerously-bypass-approvals-and-sandbox',
      'exec', '--ignore-user-config', '--skip-git-repo-check', '--json',
      '-c', 'project_doc_max_bytes=0',
      '-c', 'model_reasoning_effort="high"',
      '-c', `skills.config=[${config}]`,
      '--model', model, '--cd', workspace
    ],
    options: { cwd: workspace, stdio: ['ignore', 'pipe', 'pipe'] }
  };
}

export function parseEvents(events) {
  const result = { transcript: [], error_messages: [] };
  for (const event of events) {
    const error = event.type === 'error' ? event.message : (event.type === 'turn.failed' ? event.error?.message : null);
    if (error && !result.error_messages.includes(error)) result.error_messages.push(error);
    if (event.type === 'thread.started') result.session_id = event.thread_id;
    if (event.type === 'turn.completed' && event.usage) {
      // Cached input is a subset of input_tokens in the Codex CLI event.
      result.input_tokens = event.usage.input_tokens;
      result.output_tokens = event.usage.output_tokens;
    }
    if (event.type === 'item.completed' && event.item?.type === 'command_execution') {
      const item = event.item;
      result.transcript.push({ role: 'tool_call', turn: 1, tool_call: { id: item.id, name: 'shell', arguments: { command: item.command } } });
      result.transcript.push({ role: 'tool_result', turn: 1, tool_result: { call_id: item.id, status: item.exit_code === 0 ? 'success' : 'error', content: item.aggregated_output || '' } });
    }
    if (event.type === 'item.completed' && event.item?.type === 'agent_message') {
      result.final_message = event.item.text;
      result.transcript.push({ role: 'assistant', turn: 1, content: event.item.text });
    }
  }
  return result;
}

export function skillFiles(root) {
  const files = [];
  const visited = new Set();
  function walk(dir) {
    try {
      const real = fs.realpathSync(dir);
      if (visited.has(real)) return;
      visited.add(real);
      const entry = path.join(dir, 'SKILL.md');
      if (fs.existsSync(entry)) {
        files.push(entry, fs.realpathSync(entry));
      }
      for (const item of fs.readdirSync(dir, { withFileTypes: true })) {
        if (!['node_modules', '.git', '.venv'].includes(item.name) && (item.isDirectory() || item.isSymbolicLink())) walk(path.join(dir, item.name));
      }
    } catch { /* An absent optional root is not an error. */ }
  }
  walk(root);
  return [...new Set(files)];
}

function observedContext(threadId) {
  if (!threadId) return {};
  const date = new Date();
  const day = [date.getUTCFullYear(), String(date.getUTCMonth() + 1).padStart(2, '0'), String(date.getUTCDate()).padStart(2, '0')];
  const root = path.join(os.homedir(), '.codex', 'sessions', ...day.map(String));
  try {
    const file = fs.readdirSync(root).find(name => name.endsWith(`${threadId}.jsonl`));
    if (!file) return {};
    const records = fs.readFileSync(path.join(root, file), 'utf8').trim().split('\n').map(line => JSON.parse(line));
    const context = records.find(record => record.type === 'turn_context');
    const skills = records.filter(record => record.type === 'response_item' && record.payload?.type === 'message')
      .flatMap(record => record.payload.content || [])
      .map(item => item.text || '').filter(text => text.includes('### Available skills'));
    return { observed_model: context?.payload?.model || null, skill_catalog: skills.join('\n') };
  } catch { return {}; }
}

async function main() {
  const input = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const workspace = fs.realpathSync(input.workspace || process.cwd());
  const globals = [...skillFiles(path.join(os.homedir(), '.codex', 'skills')), ...skillFiles(path.join(os.homedir(), '.agents', 'skills')), ...skillFiles(path.join(os.homedir(), '.codex', 'plugins', 'cache'))];
  const locals = skillFiles(path.join(workspace, '.agents', 'skills'));
  const run = createInvocation(input, workspace, globals, locals);
  const phase = input.case_id ? 'run' : 'judge';
  const output = path.join(workspace, 'outputs');
  fs.mkdirSync(output, { recursive: true });
  const prefix = `${phase}-${Date.now()}`;
  const stdoutPath = path.join(output, `${prefix}-codex-events.jsonl`);
  const stderrPath = path.join(output, `${prefix}-codex-stderr.log`);
  const lastPath = path.join(output, `${prefix}-response.md`);
  const metadataPath = path.join(output, `${prefix}-metadata.json`);
  const prompt = 'Noninteractive text evaluation: do not use browser, computer-use, MCP, external services, or production writes. Use shell reads of the current workspace for local Skill resources when required; return the requested final answer. Do not read evaluation assertions or the evaluator input file.\n\n' +
    input.messages.map(message => message.role === 'user' ? message.content : `${message.role}:\n${message.content}`).join('\n\n');
  run.args.push('--output-last-message', lastPath, prompt);
  const started = new Date();
  const cliVersion = versionMetadata(spawnSync(run.command, ['--version'], {
    cwd: workspace, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], timeout: 10000
  }));
  const stdout = fs.createWriteStream(stdoutPath);
  const stderr = fs.createWriteStream(stderrPath);
  const child = spawn(run.command, run.args, run.options);
  child.stdout.pipe(stdout);
  child.stderr.pipe(stderr);
  const rc = await new Promise((resolve, reject) => { child.on('error', reject); child.on('close', code => resolve(code ?? 1)); });
  await Promise.all([finished(stdout), finished(stderr)]);
  const raw = fs.readFileSync(stdoutPath, 'utf8');
  const events = raw.split('\n').filter(Boolean).map(line => { try { return JSON.parse(line); } catch { return { type: 'unparsed', line }; } });
  const parsed = parseEvents(events);
  const context = observedContext(parsed.session_id);
  const final = fs.existsSync(lastPath) ? fs.readFileSync(lastPath, 'utf8') : (parsed.final_message || '');
  const metadata = {
    phase, case_id: input.case_id || null, variant: input.variant || null,
    started_at: started.toISOString(), completed_at: new Date().toISOString(),
    requested_model: input.model || 'gpt-6.1-sol', observed_model: context.observed_model || null,
    reasoning_effort: 'high', ...cliVersion, exit_code: rc,
    input_tokens: parsed.input_tokens ?? null, output_tokens: parsed.output_tokens ?? null,
    provider_errors: parsed.error_messages,
    installed_skill_files: locals, disabled_global_skill_count: new Set(globals).size,
    skill_catalog: context.skill_catalog || null
  };
  fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2) + '\n');
  const artifactPaths = [stdoutPath, stderrPath, metadataPath];
  if (fs.existsSync(lastPath)) artifactPaths.push(lastPath);
  const result = {
    ...parsed, engine: 'codex_no_daemon_isolated', model: context.observed_model || '',
    exit_code: rc, duration_ms: Date.now() - started.getTime(), turns: final ? 1 : 0,
    final_message: final, stderr: [fs.readFileSync(stderrPath, 'utf8'), ...parsed.error_messages].filter(Boolean).join('\n'),
    transcript: [...input.messages.map(message => ({ ...message, turn: 1 })), ...parsed.transcript],
    artifacts: { files: artifactPaths.map(file => ({ name: path.basename(file), path: path.relative(workspace, file) })) }
  };
  process.stdout.write(JSON.stringify(result));
}

if (process.argv[1] && fs.realpathSync(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch(error => { process.stderr.write(String(error)); process.exitCode = 1; });
}
