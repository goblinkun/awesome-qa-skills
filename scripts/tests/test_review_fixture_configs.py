import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[2]


@unittest.skipUnless(shutil.which('skill-up'), 'skill-up is needed to validate the embedded eval configuration')
class ReviewFixtureConfigurationTests(unittest.TestCase):
    def fixture_files(self, language, name):
        case = ROOT/'skills'/language/'skill-engineering/skill-quality-review/evals/cases'/(name+'.yaml')
        blocks = re.findall(r'^    "([^"]+)": \|-\n((?:(?:      .*)?\n)+)', case.read_text(), re.M)
        return {path: '\n'.join(line[6:] for line in body.splitlines()) for path, body in blocks}

    def test_defect_controls_keep_the_declared_resource_missing(self):
        for language in ('en', 'zh'):
            for name, missing in (
                ('review-missing-prompt', 'sample/prompts/review.md'),
                ('review-missing-bare-resource', 'sample/references/contracts.md'),
            ):
                with self.subTest(language=language, case=name):
                    files = self.fixture_files(language, name)
                    self.assertNotIn(missing, files)
                    self.assertIn(missing.removeprefix('sample/'), files['sample/SKILL.md'])
            valid = self.fixture_files(language, 'review-valid-package')
            self.assertIn('sample/prompts/review.md', valid)

    def test_quality_review_embedded_cases_are_valid_skill_up_inputs(self):
        names = ('basic-success', 'review-valid-package', 'review-missing-prompt',
                 'review-missing-bare-resource', 'review-bilingual-schema')
        for language in ('en', 'zh'):
            for name in names:
                files = self.fixture_files(language, name)
                with self.subTest(language=language, case=name), TemporaryDirectory() as directory:
                    work = Path(directory)
                    self.assertIn('sample/evals/eval.yaml', files)
                    for path, content in files.items():
                        target = work/path
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_text(content)
                    config = work/'sample/evals/eval.yaml'
                    def validate():
                        return subprocess.run(['skill-up', 'validate', str(config)],
                                              cwd=work/'sample', capture_output=True, text=True)
                    result = validate()
                    self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
                    success = work/'sample/evals/cases/success.yaml'
                    success.write_text('id: success\ninput:\n  prompt: Review invoice: total=10\n')
                    self.assertNotEqual(validate().returncode, 0, 'invalid embedded YAML must fail')

    def test_sample_graders_reject_wrong_results_and_invoice_edits(self):
        expected = {
            'success': {'invoice_id': 'I-1', 'status': 'PASS', 'source_id': 'R1', 'total': 10},
            'incomplete': {'invoice_id': 'I-1', 'status': 'MISSING_SOURCE', 'source_id': None, 'total': None},
            'boundary': {'invoice_id': 'I-1', 'status': 'READ_ONLY_BLOCKED', 'source_id': 'R1', 'total': 10},
        }
        for language in ('en', 'zh'):
            files = self.fixture_files(language, 'review-valid-package')
            for name, result in expected.items():
                case = files['sample/evals/cases/'+name+'.yaml']
                match = re.search(r"^    invoice\.json: ('[\s\S]*?')(?=\n\S)", case, re.M)
                self.assertIsNotNone(match, 'the declared invoice fixture must be materialized')
                source = ' '.join(line.strip() for line in match.group(1)[1:-1].splitlines()).replace("''", "'")
                record = json.loads(source)
                self.assertEqual(record['invoice_id'], 'I-1')
                with self.subTest(language=language, scenario=name), TemporaryDirectory() as directory:
                    work = Path(directory)
                    invoice = work/'invoice.json';invoice.write_text(source)
                    script = work/'grader.py';script.write_text(files['sample/evals/graders/'+name+'.py'])
                    def grade(message):
                        return subprocess.run([sys.executable, str(script)], cwd=work,
                                              env={**os.environ, 'EVAL_EXIT_CODE': '0', 'EVAL_FINAL_MESSAGE': message},
                                              capture_output=True, text=True)
                    good = grade(json.dumps(result))
                    self.assertEqual(good.returncode, 0, good.stderr)
                    wrong = {**result, 'total': 999}
                    for bad in ('Summary Findings', json.dumps(wrong), '{"total":999,'+json.dumps(result)[1:]):
                        self.assertNotEqual(grade(bad).returncode, 0, 'wrong behavior must fail')
                    invoice.write_text(source+'\n')
                    self.assertNotEqual(grade(json.dumps(result)).returncode, 0, 'changed invoice bytes must fail')


if __name__ == '__main__':
    unittest.main()
