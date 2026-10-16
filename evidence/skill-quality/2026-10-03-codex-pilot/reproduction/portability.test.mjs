import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import * as adapter from './adapter.mjs';

const source = fileURLToPath(new URL('.', import.meta.url));

test('CLI version metadata is derived from the actual version probe', () => {
  assert.deepEqual(adapter.versionMetadata?.({ status: 0, stdout: 'codex-cli 0.160.0\n' }), {
    codex_version: '0.160.0', codex_version_source: 'pre-invocation CLI version probe'
  });
});

test('missing or unsuccessful version probes remain unknown', () => {
  for (const probe of [{ status: 1, stdout: 'codex-cli 0.160.0' }, { status: 0, stdout: '' }, { status: 0, stdout: 'unrecognized version' }, {}]) {
    assert.deepEqual(adapter.versionMetadata?.(probe), { codex_version: null, codex_version_source: 'unknown' });
  }
});

test('adapter fixture discovery survives spaces and Unicode in the checkout path', () => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'sqet-portability-'));
  try {
    const moved = path.join(temp, '资料 with spaces');
    fs.mkdirSync(moved);
    for (const name of ['adapter.mjs', 'adapter.test.mjs', 'fixture-skills']) {
      fs.cpSync(path.join(source, name), path.join(moved, name), { recursive: true });
    }
    const childEnv = { ...process.env };
    delete childEnv.NODE_TEST_CONTEXT;
    const run = spawnSync(process.execPath, ['--test', path.join(moved, 'adapter.test.mjs')], { encoding: 'utf8', timeout: 15000, env: childEnv });
    assert.equal(run.status, 0, run.stdout + run.stderr);
    assert.match(run.stdout, /nested fixture Skills are disabled alongside their parent Skill/);
  } finally {
    fs.rmSync(temp, { recursive: true, force: true });
  }
});

test('calibration delegates the original input through a decoded adapter path', () => {
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'sqet-calibration-path-'));
  try {
    const moved = path.join(temp, '资料 with spaces');
    const calibration = path.join(moved, 'calibration');
    fs.mkdirSync(calibration, { recursive: true });
    fs.copyFileSync(path.join(source, 'calibration/fixture-agent.mjs'), path.join(calibration, 'fixture-agent.mjs'));
    // The offline child isolates path delegation; no Codex/model process is started.
    fs.writeFileSync(path.join(moved, 'adapter.mjs'), 'import fs from "node:fs"; process.stdout.write(fs.readFileSync(process.argv[2], "utf8"));\n');
    const input = path.join(moved, '评审 input.json');
    const body = JSON.stringify({ messages: [{ role: 'user', content: 'offline delegation fixture' }] });
    fs.writeFileSync(input, body);
    const run = spawnSync(process.execPath, [path.join(calibration, 'fixture-agent.mjs'), input], { encoding: 'utf8', timeout: 15000 });
    assert.equal(run.status, 0, run.stderr);
    assert.equal(run.stdout, body);
  } finally {
    fs.rmSync(temp, { recursive: true, force: true });
  }
});
