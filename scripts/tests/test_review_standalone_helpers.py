from pathlib import Path
import json
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from scripts.tests.test_review_parser_fidelity import ROOT
from scripts.check_review_resource_copies import main


class StandaloneHelperTests(unittest.TestCase):
    def test_shared_copies_match_canonical_sources(self):
        self.assertEqual(main(),0)

    def test_router_snapshot_is_complete_and_availability_is_unknown(self):
        expected={p.parent.name for p in (ROOT/'skills/en').rglob('SKILL.md')}
        for lang in ('en','zh'):
            p=ROOT/'skills'/lang/'testing-workflows/discover-testing/references/skill-capability-inventory.json'
            data=json.loads(p.read_text());rows=data['skills']
            self.assertEqual({r['name'] for r in rows},expected);self.assertEqual(len(rows),len(expected))
            self.assertTrue(all(r['availability']=='UNKNOWN' for r in rows))

    def test_plus_cli_exports_remain_explicitly_unassessed(self):
        packages=[('requirements-analysis-plus','run_analysis.py',['--input','source.md']),('testcase-writer-plus','run_writer.py',['--requirement','source.md','--analysis','analysis.md']),('test-case-reviewer-plus','run_review.py',['--requirement','source.md','--testcase','analysis.md']),('test-strategy-plus','run_strategy.py',['--requirement','source.md'])]
        for lang in ('en','zh'):
            for name,script,args in packages:
                formats=['markdown'] if name=='requirements-analysis-plus' else ['markdown','json','excel','word']
                for fmt in formats:
                    with self.subTest(skill=name,lang=lang,format=fmt),TemporaryDirectory() as folder:
                        base=Path(folder);shutil.copytree(ROOT/'skills'/lang/'testing-types'/name,base/'leaf')
                        (base/'source.md').write_text('Password must be 12..64 characters; user_id >= -1.')
                        (base/'analysis.md').write_text('TC1: 11 rejected, 12 accepted, 64 accepted, 65 rejected.')
                        output=base/('output.docx' if fmt=='word' else 'output.txt')
                        cmd=[sys.executable,str(base/'leaf/scripts'/script),*args,'--output',str(output)]
                        if name!='requirements-analysis-plus':cmd+=['--output-format',fmt]
                        result=subprocess.run(cmd,cwd=base,capture_output=True,text=True)
                        self.assertEqual(result.returncode,0,result.stderr)
                        if fmt=='word':
                            import zipfile
                            with zipfile.ZipFile(output) as z:text=z.read('word/document.xml').decode()
                        else:text=output.read_text()
                        self.assertIn('NOT_ASSESSED',text);self.assertIn('user_id',text);self.assertIn('SHA',text.upper() if name in {'requirements-analysis-plus','testcase-writer-plus'} else text.replace('source_hash','SHA'))

if __name__=='__main__':unittest.main()
