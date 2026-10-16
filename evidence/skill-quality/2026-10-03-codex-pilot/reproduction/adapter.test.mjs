import test from 'node:test';
import assert from 'node:assert/strict';
import { fileURLToPath } from 'node:url';
import { createInvocation, parseEvents, skillFiles } from './adapter.mjs';

test('Codex stdin is closed and user configuration cannot leak into a run', () => {
  const run = createInvocation({ model: 'openai/gpt-6.1-sol' }, '/tmp/work', ['/tmp/global/SKILL.md']);
  assert.equal(run.options.stdio[0], 'ignore');
  assert.ok(run.args.includes('--ignore-user-config'));
  assert.ok(run.args.includes('project_doc_max_bytes=0'));
  assert.ok(run.args.includes('gpt-6.1-sol'));
  assert.ok(run.args.some(a => a.includes('enabled=false') && a.includes('/tmp/global/SKILL.md')));
});

test('without-skill and judge invocations cannot load locally installed run Skills', () => {
  const local = '/tmp/work/.agents/skills/target/SKILL.md';
  for (const input of [{ variant: 'without_skill', case_id: 'basic' }, {}]) {
    const run = createInvocation(input, '/tmp/work', [], [local]);
    assert.ok(run.args.some(a => a.includes(local) && a.includes('enabled=false')));
  }
  const run = createInvocation({ variant: 'with_skill', case_id: 'basic' }, '/tmp/work', [], [local]);
  assert.ok(!run.args.some(a => a.includes(local) && a.includes('enabled=false')));
});

test('Codex usage and shell reads are retained as real evidence', () => {
  const result = parseEvents([
    { type: 'thread.started', thread_id: 'test-thread' },
    { type: 'item.completed', item: { id: 'cmd1', type: 'command_execution', command: "sed -n '1,90p' .agents/skills/target/SKILL.md", aggregated_output: 'skill text', exit_code: 0 } },
    { type: 'item.completed', item: { type: 'agent_message', text: 'done' } },
    { type: 'turn.completed', usage: { input_tokens: 100, cached_input_tokens: 20, output_tokens: 40 } }
  ]);
  assert.equal(result.session_id, 'test-thread');
  assert.equal(result.input_tokens, 100);
  assert.equal(result.output_tokens, 40);
  assert.equal(result.final_message, 'done');
  assert.equal(result.transcript[0].role, 'tool_call');
  assert.match(result.transcript[0].tool_call.arguments.command, /SKILL.md/);
});

test('missing usage is unknown rather than measured zero', () => {
  const result = parseEvents([]);
  assert.equal(result.input_tokens, undefined);
  assert.equal(result.output_tokens, undefined);
});

test('nested fixture Skills are disabled alongside their parent Skill', () => {
  const files = skillFiles(fileURLToPath(new URL('./fixture-skills', import.meta.url)));
  assert.ok(files.some(file => file.endsWith('/parent/SKILL.md')));
  assert.ok(files.some(file => file.endsWith('/parent/fixtures/nested/SKILL.md')));
});

test('provider errors in JSONL are retained even when stderr is uninformative', () => {
  const result = parseEvents([{ type: 'error', message: 'Content blocked by provider' }, { type: 'turn.failed', error: { message: 'Content blocked by provider' } }]);
  assert.deepEqual(result.error_messages, ['Content blocked by provider']);
});
