import json
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from scripts.tests.test_review_parser_fidelity import ROOT,load


class PackagedGraderTests(unittest.TestCase):
    def test_domain_graders_survive_script_up_isolation_and_valid_markdown(self):
        paths=list((ROOT/'skills').rglob('evals/fixtures/check_domain_decisions.py'))
        self.assertEqual(len(paths),118)
        for p in paths:
            oracle=json.loads(p.with_name('domain-oracle.json').read_text())
            message='| ID | DECISION | Evidence |\n| --- | --- | --- |\n'+'\n'.join(f'| {k} | {v} | declared source |' for k,v in oracle['decisions'].items())
            if oracle.get('calculations'):
                message+='\n\n| METRIC | VALUE | Evidence |\n| --- | --- | --- |\n'+'\n'.join(f'| {k} | {v} | declared units |' for k,v in oracle['calculations'].items())
            message+='\n'+'\n'.join(oracle.get('required_details',[]))
            with self.subTest(grader=str(p)),TemporaryDirectory() as folder:
                isolated=Path(folder)/'grader.py';isolated.write_bytes(p.read_bytes())
                env={**os.environ,'EVAL_EXIT_CODE':'0','EVAL_FINAL_MESSAGE':message}
                result=subprocess.run([sys.executable,str(isolated)],cwd=folder,env=env,capture_output=True,text=True)
                self.assertEqual(result.returncode,0,result.stderr)
                module=load(p);self.assertEqual(module.ORACLE,oracle)
                module.check('\n'.join(l.strip().strip('|').strip() for l in message.splitlines()),oracle)
                first=next(iter(oracle['decisions']));row=f'| {first} | {oracle["decisions"][first]} | declared source |'
                for broken in (message.replace(row,row+'\n'+row),message.replace(row,''),message.replace(row,f'| {first} | __MUTANT__ | declared source |')):
                    with self.assertRaises(ValueError):module.check(broken,oracle)

    def test_root_graders_accept_standard_tables_and_reject_mutations(self):
        paths=[p for p in (ROOT/'skills').rglob('evals/graders/review-*.py') if 'EXPECTED = ' in p.read_text()]
        self.assertEqual(len(paths),32)
        for p in paths:
            module=load(p)
            message='ID | DECISION | Evidence\n--- | --- | ---\n'+'\n'.join(f'{k} | {v} | source' for k,v in module.EXPECTED.items())
            with self.subTest(grader=str(p)):
                module.grade(message,0)
                with self.assertRaises(ValueError):module.grade(message+'\n'+message,0)
                with self.assertRaises(ValueError):module.grade(message,1)

    def test_structured_result_graders_reject_boolean_counts_and_duplicate_json_keys(self):
        paths=[p for p in (ROOT/'skills').rglob('evals/graders/*.py') if 'def equal(actual, expected):' in p.read_text()]
        self.assertEqual(len(paths),22)
        for p in paths:
            with self.subTest(grader=str(p)):
                module=load(p)
                module.equal({'counts':[1,0], 'approved':False}, {'counts':[1,0], 'approved':False})
                with self.assertRaises(AssertionError):
                    module.equal({'counts':[True,0]}, {'counts':[1,0]})
                with self.assertRaises(ValueError):
                    json.loads('{"count":1,"count":0}', object_pairs_hook=module.unique_object)

    def test_prose_trim_grader_preserves_fixture_bytes_and_document_lines(self):
        for lang in ('en', 'zh'):
            leaf=ROOT/'skills'/lang/'skill-engineering/skill-prose-trim'
            case=(leaf/'evals/cases/review-authorized-trim.yaml').read_text()
            blocks=re.findall(r'^    "([^"]+)": \|-\n((?:      .*\n)+)',case,re.M)
            source={path:'\n'.join(line[6:] for line in body.splitlines()) for path,body in blocks}
            self.assertEqual(set(source),{'contract.md','fixtures/recorded.json'})
            cleaned=source['contract.md'].replace('This PR fixed the reviewer concern and now we should keep it.\n','')
            with self.subTest(language=lang),TemporaryDirectory() as folder:
                work=Path(folder);(work/'fixtures').mkdir()
                script=work/'grader.py';script.write_bytes((leaf/'evals/graders/review-authorized-trim.py').read_bytes())
                protected=work/'fixtures/recorded.json';protected.write_bytes(source['fixtures/recorded.json'].encode())
                env={**os.environ,'EVAL_EXIT_CODE':'0','EVAL_FINAL_MESSAGE':'{"mode":"edited"}'}
                def run():return subprocess.run([sys.executable,str(script)],cwd=work,env=env,capture_output=True,text=True)
                for ending in ('','\n'):
                    (work/'contract.md').write_text(cleaned+ending)
                    result=run();self.assertEqual(result.returncode,0,result.stderr)
                protected.write_bytes((source['fixtures/recorded.json']+'\n').encode())
                self.assertNotEqual(run().returncode,0,'immutable fixture bytes changed')
                protected.write_bytes(source['fixtures/recorded.json'].encode())
                (work/'contract.md').write_text(cleaned.replace('Never send production writes.\n',''))
                self.assertNotEqual(run().returncode,0,'durable prohibition disappeared')

    def test_source_union_accepts_versioned_provenance_and_rejects_altered_evidence(self):
        versions={'qa-1':'v1','tech-1':'v2','product-1':'v3'}
        flat={
            'source_register':[{'source_id':source,'version':version} for source,version in versions.items()],
            'findings':[
                {'id':'S-1','input_finding_ids':['F-qa','F-tech'],'sources':['qa-1','tech-1'],
                 'severity':'P0','original_severities':{'qa-1':'P0','tech-1':'P1'},
                 'evidence_by_source':{'qa-1':['run-R1'],'tech-1':['diff-D1']}},
                {'id':'S-2','input_finding_ids':['F-product'],'sources':['product-1'],
                 'severity':'P2','original_severities':{'product-1':'P2'},
                 'evidence_by_source':{'product-1':['req-Q7']}}
            ],
            'blockers':['S-1'],'disagreements':[{'sources':['qa-1','tech-1'],'topic':'severity'}]
        }
        rich=json.loads(json.dumps(flat))
        for finding in rich['findings']:
            for field,value_key in (('original_severities','severity'),('evidence_by_source','evidence')):
                finding[field]={source:{'version':versions[source],value_key:value} for source,value in finding[field].items()}
        mutants=[]
        for field,key,replacement in (('original_severities','version','v9'),('original_severities','severity','P2'),
                                      ('evidence_by_source','version','v9'),('evidence_by_source','evidence',['invented'])):
            mutant=json.loads(json.dumps(rich));mutant['findings'][0][field]['qa-1'][key]=replacement;mutants.append(mutant)
        missing=json.loads(json.dumps(rich));del missing['findings'][0]['original_severities']['tech-1'];mutants.append(missing)
        for lang in ('en','zh'):
            leaf=ROOT/'skills'/lang/'testing-workflows/multi-role-quality-synthesis'
            with self.subTest(language=lang),TemporaryDirectory() as folder:
                script=Path(folder)/'grader.py';script.write_bytes((leaf/'evals/graders/review-source-union.py').read_bytes())
                def run(data):
                    env={**os.environ,'EVAL_EXIT_CODE':'0','EVAL_FINAL_MESSAGE':json.dumps(data)}
                    return subprocess.run([sys.executable,str(script)],cwd=folder,env=env,capture_output=True,text=True)
                for valid in (flat,rich):
                    result=run(valid);self.assertEqual(result.returncode,0,result.stderr)
                for mutant in mutants:
                    self.assertNotEqual(run(mutant).returncode,0,'changed provenance must fail')

if __name__=='__main__':unittest.main()
