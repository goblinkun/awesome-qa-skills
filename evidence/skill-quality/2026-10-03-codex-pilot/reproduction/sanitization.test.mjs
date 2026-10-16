import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const localPath = /\/Users\/[A-Za-z0-9._-]+|\/(?:private\/)?var\/folders(?:\/|\b)/;
const credentialPattern = /sk-(?:proj-|ant-)?[A-Za-z0-9_-]{25,}|gh[pousr]_[A-Za-z0-9]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/;
const tutorialPath = 'reproduction/packages/performance-testing-zh/tutorial.md';

function files(dir) {
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(entry => {
    const target = path.join(dir, entry.name);
    return entry.isDirectory() ? files(target) : [target];
  });
}

test('ancestor AGENTS probes in the captured architecture trace are sanitized', () => {
  const file = path.join(root, 'artifacts/core/testability-analysis-zh/iteration-1/architecture-success/with_skill/outputs/agent/run/run-1791027004408-codex-events.jsonl');
  const text = fs.readFileSync(file, 'utf8');
  assert.equal(localPath.test(text), false, 'Captured trace still contains a local user or macOS temporary path');
  for (const line of text.trim().split('\n')) assert.doesNotThrow(() => JSON.parse(line));
});

test('the entire evidence package passes local-path and standard credential-pattern checks', () => {
  for (const file of files(root)) {
    const text = fs.readFileSync(file, 'utf8');
    assert.equal(localPath.test(text), false, `Local path remains in ${path.relative(root, file)}`);
    // Report only the filename and boolean, never a possible secret value.
    assert.equal(credentialPattern.test(text), false, `Possible credential requires manual review in ${path.relative(root, file)}`);
  }
});

test('the archived k6 tutorial reads login passwords from the environment', () => {
  const text = fs.readFileSync(path.join(root, tutorialPath), 'utf8');
  const example = text.match(/group\('用户登录', function \(\) \{([\s\S]*?)\n\s*check\(loginRes,/);
  assert.ok(example, 'The captured k6 login example must remain available');
  const bindings = [...example[1].matchAll(/\bpassword\s*:\s*([^\r\n,}]+)/g)];
  assert.ok(bindings.length > 0, 'The login example must remain covered');
  // Do not include a possibly hardcoded value in assertion output.
  assert.equal(bindings.every(match => match[1].trim() === '__ENV.TEST_PASSWORD'), true,
    'Archived k6 password bindings must use __ENV.TEST_PASSWORD, not literals');
});

test('example sanitization preserves original provenance and valid export hashes', () => {
  const manifest = JSON.parse(fs.readFileSync(path.join(root, 'artifact-manifest.json'), 'utf8'));
  assert.equal(manifest.file_count, manifest.files.length);
  assert.equal(new Set(manifest.files.map(file => file.path)).size, manifest.file_count);
  const entry = manifest.files.find(file => file.path === tutorialPath);
  const original = '3032eb32d7e797b16d38c74a36b72a4a91148a1316dbb13fe15b90c886710551';
  assert.equal(entry.original_sha256, original);
  assert.notEqual(entry.archived_sha256, original);
  assert.equal(entry.byte_identical, false);
  assert.equal(entry.sanitized_example_occurrences, 1);
  assert.equal(entry.delivery_revision.date, '2026-10-16');
  assert.equal(entry.delivery_revision.previous_archived_sha256, original);
  const source = JSON.parse(fs.readFileSync(path.join(root, 'source-manifest.json'), 'utf8'));
  const collected = source.files.find(file => file.path === 'skills/zh/testing-types/performance-testing/tutorial.md');
  assert.equal(collected.sha256, original, 'Historical source identity must not be rewritten');
  for (const file of manifest.files) {
    assert.ok(!path.isAbsolute(file.path) && !file.path.split('/').includes('..'));
    const bytes = fs.readFileSync(path.join(root, file.path));
    assert.equal(crypto.createHash('sha256').update(bytes).digest('hex'), file.archived_sha256, file.path);
  }
});
