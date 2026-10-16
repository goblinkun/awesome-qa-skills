import fs from 'node:fs';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const input = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
if (input.case_id) {
  const goldens = JSON.parse(fs.readFileSync(new URL('./goldens.json', import.meta.url), 'utf8'));
  if (!Object.hasOwn(goldens, input.case_id)) throw new Error('Unknown calibration fixture');
  process.stdout.write(JSON.stringify({ engine: 'synthetic-answer-fixture', exit_code: 0, turns: 1, final_message: goldens[input.case_id] }));
} else {
  const run = spawnSync(process.execPath, [fileURLToPath(new URL('../adapter.mjs', import.meta.url)), process.argv[2]], { stdio: ['ignore', 'inherit', 'inherit'] });
  process.exitCode = run.status ?? 1;
}
