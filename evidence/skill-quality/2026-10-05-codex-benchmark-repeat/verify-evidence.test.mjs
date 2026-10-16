import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('.', import.meta.url));
const parent = path.resolve(root, '../2026-10-03-codex-pilot');
const digest = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
function target(rel) {
  const file = path.resolve(root, rel);
  assert.ok([root.slice(0, -1), parent].some(base => file.startsWith(`${base}${path.sep}`)), 'Evidence reference escaped its allowed roots');
  return file;
}
const read = rel => JSON.parse(fs.readFileSync(target(rel), 'utf8'));
function files(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(entry => {
    assert.equal(entry.isSymbolicLink(), false, 'Unexpected evidence symlink');
    return entry.isDirectory() ? files(path.join(dir, entry.name)) : [path.join(dir, entry.name)];
  });
}
const results = read('results.json');
const ledger = read('cost-ledger.json');
const manifest = read('artifact-manifest.json');

test('export hashes, source-copy identity, and manifest uniqueness are valid', () => {
  assert.equal(manifest.file_count, manifest.files.length);
  assert.equal(new Set(manifest.files.map(file => file.path)).size, manifest.file_count);
  for (const file of manifest.files) {
    assert.ok(!file.path.startsWith('/') && !file.path.split('/').includes('..'));
    assert.equal(digest(fs.readFileSync(target(file.path))), file.archived_sha256, file.path);
  }
  const source = read('source-identity.json');
  assert.equal(source.files.length, 80);
  for (const file of source.files) assert.equal(digest(fs.readFileSync(target(file.source))), file.sha256);
  assert.equal(digest(fs.readFileSync(target(source.adapter.source))), source.adapter.sha256);
});

test('paired summaries match original/native reports without turning skipped semantics into a score', () => {
  assert.equal(results.new_complete_pairs, 6);
  assert.equal(results.benchmarks.length, 3);
  for (const benchmark of results.benchmarks) {
    assert.equal(benchmark.samples_per_variant, 3);
    assert.equal(benchmark.samples.length, 3);
    for (const sample of benchmark.samples) {
      const native = read(sample.report);
      assert.equal(native.case_results.length, 2);
      for (const trial of sample.trials) {
        const actual = native.case_results.find(item => item.configuration === trial.configuration);
        assert.equal(actual.status, trial.status);
        assert.equal(Boolean(actual.grading.judge_context), trial.semantic_judge_executed);
        assert.deepEqual(actual.grading.assertion_results.filter(assertion => !assertion.text.startsWith('expect.')), trial.semantic_assertions);
        if (!trial.semantic_judge_executed) {
          assert.equal(trial.semantic_assertions.length, 0);
          assert.ok(actual.grading.assertion_results.some(assertion => assertion.text.startsWith('expect.') && !assertion.passed));
        }
      }
    }
    for (const variant of ['with_skill', 'without_skill']) assert.equal(benchmark.pass_counts[variant], benchmark.samples.filter(sample => sample.trials.find(trial => trial.configuration === variant).status === 'PASS').length);
  }
  assert.equal(results.claims.quality_score, 'NOT_SCORED');
  assert.equal(results.claims.formal_test_level, 'UNASSESSED');
  assert.equal(results.claims.business_acceptance, 'NOT_RUN');
  assert.equal(results.claims.natural_selection, 'BLOCKED');
});

test('unique call ledger preserves native usage and actual Skill catalog isolation', () => {
  assert.equal(ledger.calls.length, 26);
  assert.equal(new Set(ledger.calls.map(call => call.session_id)).size, ledger.calls.length);
  const sum = calls => ({ calls: calls.length, input_tokens: calls.reduce((sum, call) => sum + call.input_tokens, 0), output_tokens: calls.reduce((sum, call) => sum + call.output_tokens, 0), cached_input_tokens: calls.reduce((sum, call) => sum + (call.cached_input_tokens ?? 0), 0), unknown_usage_calls: calls.filter(call => call.input_tokens == null || call.output_tokens == null).length });
  assert.deepEqual(sum(ledger.calls), ledger.all_followup_calls);
  assert.deepEqual(sum(ledger.calls.filter(call => call.cohort === 'complete_repeat')), ledger.complete_repeat);
  assert.deepEqual(sum(ledger.calls.filter(call => call.cohort !== 'complete_repeat')), ledger.interrupted);
  for (const call of ledger.calls) {
    const meta = read(call.artifact);
    const events = fs.readFileSync(target(call.artifact.replace(/-metadata\.json$/, '-codex-events.jsonl')), 'utf8').trim().split('\n').map(line => JSON.parse(line));
    const completed = events.find(event => event.type === 'turn.completed');
    assert.equal(events.find(event => event.type === 'thread.started').thread_id, call.session_id);
    assert.equal(completed.usage.input_tokens, call.input_tokens);
    assert.equal(completed.usage.output_tokens, call.output_tokens);
    assert.equal(completed.usage.cached_input_tokens ?? null, call.cached_input_tokens);
    assert.equal(meta.exit_code, 0);
    assert.equal(meta.observed_model, call.phase === 'run' ? 'gpt-6.1-sol' : 'gpt-6-sol');
    const catalog = [...(meta.skill_catalog || '').matchAll(/^- ([^\n:]+):/gm)].map(match => match[1]);
    if (call.phase === 'run' && call.variant === 'with_skill') {
      assert.equal(catalog.length, 1);
      assert.equal(meta.installed_skill_files.length, 1);
    } else {
      assert.deepEqual(catalog, []);
      if (call.phase === 'run') assert.deepEqual(meta.installed_skill_files, []);
      const targetReads = events.filter(event => event.type === 'item.completed' && event.item?.type === 'command_execution' && /(?:cat|sed|head)\b[\s\S]*\.agents\/skills\/[\s\S]*SKILL\.md/.test(event.item.command));
      assert.equal(targetReads.length, 0, 'Baseline/Judge must not read target Skill instructions');
    }
  }
});

test('package redaction and curated bilingual links remain valid', () => {
  const localPath = /\/Users\/|\/(?:private\/)?var\/folders(?:\/|\b)|\/private\/tmp\/sqet-/;
  const credential = /sk-(?:proj-|ant-)?[A-Za-z0-9_-]{25,}|gh[pousr]_[A-Za-z0-9]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/;
  for (const file of files(root)) {
    const text = fs.readFileSync(file, 'utf8');
    assert.equal(localPath.test(text), false, `Unredacted path in ${path.relative(root, file)}`);
    assert.equal(credential.test(text), false, `Possible credential requires manual review in ${path.relative(root, file)}`);
  }
  const docs = [path.join(root, 'README.md'), path.join(root, 'README_EN.md'), path.join(parent, 'README.md'), path.join(parent, 'README_EN.md')];
  for (const skill of ['functional-testing', 'testability-analysis', 'skill-evaluation']) for (const suffix of ['.md', '_EN.md']) docs.push(path.join(parent, 'profiles', skill + suffix));
  for (const file of docs) {
    const content = fs.readFileSync(file, 'utf8');
    const sibling = file.endsWith('_EN.md') ? file.replace(/_EN\.md$/, '.md') : file.replace(/\.md$/, '_EN.md');
    assert.ok(fs.existsSync(sibling) && content.includes(path.basename(sibling)));
    for (const match of content.matchAll(/(?<!!)\[[^\]]*\]\(([^)]+)\)/g)) {
      if (/^[a-z]+:/i.test(match[1]) || match[1].startsWith('#')) continue;
      assert.ok(fs.existsSync(path.resolve(path.dirname(file), match[1].split('#')[0])), `Broken link in ${path.basename(file)}`);
    }
  }
});
