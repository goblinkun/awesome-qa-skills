from __future__ import annotations
import ast
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from scripts.tests.test_review_parser_fidelity import load, ROOT


class GeneratedApiCorrectnessTests(unittest.TestCase):
    def module(self,name,script,lang='zh'):
        return load(ROOT/'skills'/lang/'testing-types'/name/'scripts'/script)

    def test_unknown_expectations_block_instead_of_accepting_4xx(self):
        for lang in ('zh','en'):
            p=self.module('api-test-pytest','generate_pytest_tests.py',lang)._case_block('GET','/orders','orders')
            self.assertIn('pytest.fail',p);self.assertNotIn('api_client.request',p)
            r=self.module('api-test-restassure','generate_restassured_tests.py',lang).build_java_class([{'method':'GET','path':'/orders'}])
            self.assertIn('Assertions.fail',r);self.assertNotIn('is(404)',r)
            s=self.module('api-test-supertest','generate_supertest_tests.py',lang)._to_test('GET','/orders','orders')
            self.assertIn('throw new Error',s);self.assertNotIn('request(app).get',s)
            b=self.module('api-test-bruno','generate_bruno_requests.py',lang)._to_bru('GET','/orders','orders')
            self.assertIn('url: {{baseUrl}}/orders',b);self.assertIn('script:pre-request',b);self.assertIn('Incomplete contract',b)

    def test_empty_inputs_fail_generation_not_a_tautology(self):
        for lang in ('zh','en'):
            with self.assertRaisesRegex(ValueError,'No endpoints'):
                self.module('api-test-restassure','generate_restassured_tests.py',lang).build_java_class([])
            with TemporaryDirectory() as folder:
                p=Path(folder);(p/'input.json').write_text('{"endpoints":[]}')
                for name,script,outputarg in [('api-test-pytest','generate_pytest_tests.py','--output'),('api-test-supertest','generate_supertest_tests.py','--output-dir'),('api-test-bruno','generate_bruno_requests.py','--output-dir')]:
                    command=[sys.executable,str(ROOT/'skills'/lang/'testing-types'/name/'scripts'/script),'--input',str(p/'input.json'),outputarg,str(p/'generated')]
                    result=subprocess.run(command,capture_output=True,text=True)
                    self.assertNotEqual(result.returncode,0,(name,result.stdout));self.assertIn('No endpoints',result.stderr)

    def test_pytest_generated_assertions_detect_bad_status_and_body(self):
        ep={'method':'POST','path':'/orders','body':{'qty':1},'body_encoding':'json','headers':{'Content-Type':'application/json'},'expected_statuses':[201],'expected_json':{'qty':1}}
        for lang in ('zh','en'):
            module=self.module('api-test-pytest','generate_pytest_tests.py',lang)
            code=module._case_block('POST','/orders','orders',ep);ast.parse(code)
            namespace={};exec(code,namespace)
            calls=[]
            def client(status,body):
                def request(method,path,**kwargs):
                    calls.append((method,path,kwargs));return SimpleNamespace(status_code=status,json=lambda:body)
                return SimpleNamespace(request=request)
            namespace['test_orders'](client(201,{'qty':1}));self.assertEqual(calls[-1][2]['json'],{'qty':1})
            with self.assertRaises(AssertionError):namespace['test_orders'](client(404,{'qty':1}))
            with self.assertRaises(AssertionError):namespace['test_orders'](client(201,{'qty':2}))
            self.assertNotIn('elapsed',code)

    def test_request_payloads_and_status_are_preserved_in_all_formats(self):
        ep={'method':'POST','path':'/orders','body':{'qty':1},'body_encoding':'json','headers':{'Content-Type':'application/json'},'expected_statuses':[201]}
        for lang in ('zh','en'):
            r=self.module('api-test-restassure','generate_restassured_tests.py',lang).build_java_class([ep]);self.assertIn('is(201)',r);self.assertNotIn('is(404)',r);self.assertIn('qty',r);self.assertNotIn('3000',r)
            s=self.module('api-test-supertest','generate_supertest_tests.py',lang)._to_test('POST','/orders','orders',ep);self.assertIn('qty',s);self.assertIn('[201]',s);self.assertNotIn('404',s)
            b=self.module('api-test-bruno','generate_bruno_requests.py',lang)._to_bru('POST','/orders','orders',ep);self.assertIn('"qty": 1',b);self.assertNotIn('"sample"',b);self.assertIn('[201]',b);self.assertNotIn('404',b)

    def test_required_data_and_unresolved_schema_remain_incomplete(self):
        module=self.module('api-test-pytest','generate_pytest_tests.py')
        for ep in [{'expected_statuses':[201],'body_required':True}, {'expected_statuses':[200],'response_schema':{'$ref':'#/missing'}}]:
            code=module._case_block('POST','/orders','orders',ep)
            self.assertIn('pytest.fail',code);self.assertNotIn('api_client.request',code)

    def test_unresolved_file_and_request_refs_are_blocked(self):
        for lang in ('zh','en'):
            m=self.module('api-test-pytest','generate_pytest_tests.py',lang)
            for ep in [{'expected_statuses':[200],'unresolved_input_files':['@body.json']}, {'expected_statuses':[200],'unresolved_request':{'$ref':'https://example.test/request'}}]:
                code=m._case_block('POST','/orders','orders',ep)
                self.assertIn('pytest.fail',code);self.assertNotIn('api_client.request',code)

if __name__=='__main__':unittest.main()
