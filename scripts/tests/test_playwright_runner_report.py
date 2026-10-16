from __future__ import annotations

import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class PlaywrightRunnerReportTests(unittest.TestCase):
    def test_bilingual_runners_write_the_announced_json_report(self) -> None:
        for language in ("zh", "en"):
            with self.subTest(language=language), tempfile.TemporaryDirectory() as tmp:
                temp_root = Path(tmp)
                script_dir = (
                    temp_root
                    / "skills"
                    / language
                    / "testing-types"
                    / "ui-test-playwright"
                    / "scripts"
                )
                script_dir.mkdir(parents=True)
                runner = script_dir / "run-tests.sh"
                source_runner = (
                    ROOT
                    / "skills"
                    / language
                    / "testing-types"
                    / "ui-test-playwright"
                    / "scripts"
                    / "run-tests.sh"
                )
                runner.write_text(source_runner.read_text(encoding="utf-8"), encoding="utf-8")

                fake_bin = temp_root / "bin"
                fake_bin.mkdir()
                fake_npx = fake_bin / "npx"
                fake_npx.write_text(
                    "#!/bin/sh\n"
                    "[ \"$1\" = playwright ] || exit 17\n"
                    "[ \"$2\" = test ] || exit 18\n"
                    "[ \"$3\" = --reporter=list,html,json ] || exit 19\n"
                    "[ -n \"${PLAYWRIGHT_JSON_OUTPUT_FILE:-}\" ] || exit 20\n"
                    "printf '{\\\"ok\\\":true}\\n' > \"$PLAYWRIGHT_JSON_OUTPUT_FILE\"\n",
                    encoding="utf-8",
                )
                fake_npx.chmod(0o755)

                result = subprocess.run(
                    ["bash", str(runner)],
                    env={**os.environ, "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}"},
                    capture_output=True,
                    text=True,
                    check=False,
                )

                self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
                match = re.search(r"^Report path: (.+)$", result.stdout, re.MULTILINE)
                self.assertIsNotNone(match, result.stdout)
                report_path = Path(match.group(1))
                self.assertTrue(report_path.is_file(), str(report_path))
                self.assertEqual(json.loads(report_path.read_text(encoding="utf-8")), {"ok": True})


if __name__ == "__main__":
    unittest.main()
