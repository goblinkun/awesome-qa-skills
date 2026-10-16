import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const localPath = /\/Users\/[A-Za-z0-9._-]+|\/(?:private\/)?var\/folders(?:\/|\b)/;
const credentialPattern = /sk-(?:proj-|ant-)?[A-Za-z0-9_-]{25,}|gh[pousr]_[A-Za-z0-9]{30,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/;

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
