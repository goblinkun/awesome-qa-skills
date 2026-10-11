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

    def test_openapi_security_requires_a_matching_environment_header(self):
        endpoint={'method':'GET','path':'/orders','expected_statuses':[200],
                  'security_requirements':[{'ApiKeyAuth':[]}],
                  'security_schemes':{'ApiKeyAuth':{'type':'apiKey','in':'header','name':'X-API-Key'}}}
        generators={
            'api-test-restassure':('generate_restassured_tests.py','build_java_class'),
            'api-test-pytest':('generate_pytest_tests.py','_case_block'),
            'api-test-supertest':('generate_supertest_tests.py','_to_test'),
            'api-test-bruno':('generate_bruno_requests.py','_to_bru'),
        }
        for lang in ('zh','en'):
            for name,(script,entrypoint) in generators.items():
                with self.subTest(language=lang, generator=name):
                    module=self.module(name,script,lang)
                    if entrypoint=='build_java_class':
                        blocked=module.build_java_class([endpoint])
                        allowed=module.build_java_class([{**endpoint,'headers_env':{'X-API-Key':'API_TOKEN'}}])
                    elif entrypoint=='_case_block':
                        blocked=module._case_block('GET','/orders','orders',endpoint)
                        allowed=module._case_block('GET','/orders','orders',{**endpoint,'headers_env':{'X-API-Key':'API_TOKEN'}})
                    elif entrypoint=='_to_test':
                        blocked=module._to_test('GET','/orders','orders',endpoint)
                        allowed=module._to_test('GET','/orders','orders',{**endpoint,'headers_env':{'X-API-Key':'API_TOKEN'}})
                    else:
                        blocked=module._to_bru('GET','/orders','orders',endpoint)
                        allowed=module._to_bru('GET','/orders','orders',{**endpoint,'headers_env':{'X-API-Key':'API_TOKEN'}})
                    unsupported={**endpoint,'security_schemes':{'ApiKeyAuth':{'type':'apiKey','in':'query','name':'api_key'}},'headers_env':{'X-API-Key':'API_TOKEN'}}
                    collision={'method':'GET','path':'/orders','expected_statuses':[200],
                               'security_requirements':[{'ApiKeyAuth':[]}],
                               'security_schemes':{'ApiKeyAuth':{'type':'apiKey','in':'header','name':'X-Custom-Key'}},
                               'headers':{'X-Custom-Key':'HARDCODED'},'headers_env':{'X-Custom-Key':'API_TOKEN'}}
                    if entrypoint=='build_java_class':
                        unsupported_code=module.build_java_class([unsupported])
                        collision_code=module.build_java_class([collision])
                    elif entrypoint=='_case_block':
                        unsupported_code=module._case_block('GET','/orders','orders',unsupported)
                        collision_code=module._case_block('GET','/orders','orders',collision)
                    elif entrypoint=='_to_test':
                        unsupported_code=module._to_test('GET','/orders','orders',unsupported)
                        collision_code=module._to_test('GET','/orders','orders',collision)
                    else:
                        unsupported_code=module._to_bru('GET','/orders','orders',unsupported)
                        collision_code=module._to_bru('GET','/orders','orders',collision)
                    self.assertTrue(any(token in blocked for token in ('Assertions.fail','pytest.fail','throw new Error','stopExecution')))
                    self.assertTrue(any(token in allowed for token in ('requiredEnv("API_TOKEN")','os.environ[v]','process.env["API_TOKEN"]','bru.getProcessEnv("API_TOKEN")')))
                    self.assertTrue(any(token in unsupported_code for token in ('Assertions.fail','pytest.fail','throw new Error','stopExecution')))
                    self.assertTrue(any(token in collision_code for token in ('Assertions.fail','pytest.fail','throw new Error','stopExecution')))

    def test_openapi_security_mapping_respects_alternatives_and_combined_schemes(self):
        requirements=[{'BearerAuth':[],'ApiKeyAuth':[]},{'FallbackKey':[]}]
        schemes={'BearerAuth':{'type':'http','scheme':'bearer'},
                 'ApiKeyAuth':{'type':'apiKey','in':'header','name':'X-API-Key'},
                 'FallbackKey':{'type':'apiKey','in':'header','name':'X-Fallback-Key'}}
        endpoint={'method':'GET','path':'/orders','expected_statuses':[200],
                  'security_requirements':requirements,'security_schemes':schemes}
        for lang in ('zh','en'):
            for name in ('api-test-bruno','api-test-pytest','api-test-restassure','api-test-supertest'):
                with self.subTest(language=lang, package=name):
                    contract=self.module(name,'api_case_contract.py',lang)
                    partial={**endpoint,'headers_env':{'X-API-Key':'API_TOKEN'}}
                    complete={**endpoint,'headers_env':{'X-API-Key':'API_TOKEN','Authorization':'TEST_AUTHORIZATION'}}
                    alternative={**endpoint,'headers_env':{'X-Fallback-Key':'FALLBACK_TOKEN'}}
                    collision={'method':'GET','path':'/orders','expected_statuses':[200],
                               'security_requirements':[{'CustomKey':[]}],
                               'security_schemes':{'CustomKey':{'type':'apiKey','in':'header','name':'X-Custom-Key'}},
                               'headers':{'X-Custom-Key':'HARDCODED'},'headers_env':{'X-Custom-Key':'API_TOKEN'}}
                    duplicate_header={'method':'GET','path':'/orders','expected_statuses':[200],
                                      'security_requirements':[{'BasicAuth':[],'BearerAuth':[]}],
                                      'security_schemes':{'BasicAuth':{'type':'http','scheme':'basic'},
                                                          'BearerAuth':{'type':'http','scheme':'bearer'}},
                                      'headers_env':{'Authorization':'AUTH_TOKEN'}}
                    digest={'method':'GET','path':'/orders','expected_statuses':[200],
                            'security_requirements':[{'DigestAuth':[]}],
                            'security_schemes':{'DigestAuth':{'type':'http','scheme':'digest'}},
                            'headers_env':{'Authorization':'DIGEST_AUTH'}}
                    missing_http_scheme={'method':'GET','path':'/orders','expected_statuses':[200],
                                         'security_requirements':[{'CustomHttpAuth':[]}],
                                         'security_schemes':{'CustomHttpAuth':{'type':'http'}},
                                         'headers_env':{'Authorization':'CUSTOM_AUTH'}}
                    self.assertTrue(any('headers_env' in error for error in contract.contract_errors('GET','/orders',partial)))
                    self.assertEqual(contract.contract_errors('GET','/orders',complete),[])
                    self.assertEqual(contract.contract_errors('GET','/orders',alternative),[])
                    anonymous={**endpoint,'security_requirements':[{}],'security_schemes':{}}
                    self.assertEqual(contract.contract_errors('GET','/orders',anonymous),[])
                    self.assertTrue(any('credential' in error.lower() for error in contract.contract_errors('GET','/orders',collision)))
                    self.assertTrue(contract.contract_errors('GET','/orders',duplicate_header))
                    self.assertTrue(contract.contract_errors('GET','/orders',digest))
                    self.assertTrue(contract.contract_errors('GET','/orders',missing_http_scheme))

    def test_malformed_normalized_security_requirements_fail_closed(self):
        malformed_values=(None,{},False,0,[None,{}],[{'BearerAuth':None}],[{'BearerAuth':[1]}])
        for lang in ('zh','en'):
            for name in ('api-test-bruno','api-test-pytest','api-test-restassure','api-test-supertest'):
                contract=self.module(name,'api_case_contract.py',lang)
                endpoint={'method':'GET','path':'/orders','expected_statuses':[200]}
                self.assertEqual(contract.contract_errors('GET','/orders',endpoint),[])
                for value in malformed_values:
                    with self.subTest(language=lang,package=name,value=value):
                        self.assertTrue(contract.contract_errors('GET','/orders',{**endpoint,'security_requirements':value}))

    def test_malformed_openapi_security_blocks_generated_requests(self):
        source={'openapi':'3.0.3','security':[{'BearerAuth':[]}],
                'components':{'securitySchemes':{'BearerAuth':{'type':'http','scheme':'bearer'}}},
                'paths':{'/invalid':{'get':{'security':None,'responses':{'200':{'description':'OK'}}}},
                         '/bad-alternative':{'get':{'security':[None,{}],'responses':{'200':{'description':'OK'}}}}}}
        generators={
            'api-test-restassure':('generate_restassured_tests.py','build_java_class'),
            'api-test-pytest':('generate_pytest_tests.py','_case_block'),
            'api-test-supertest':('generate_supertest_tests.py','_to_test'),
            'api-test-bruno':('generate_bruno_requests.py','_to_bru'),
        }
        for lang in ('zh','en'):
            for name,(script,entrypoint) in generators.items():
                parser=self.module(name,'parse_api_sources.py',lang)
                endpoints=parser._parse_openapi(source,'fixture')
                module=self.module(name,script,lang)
                with self.subTest(language=lang,generator=name):
                    for endpoint in endpoints:
                        if entrypoint=='build_java_class':
                            generated=module.build_java_class([endpoint])
                        elif entrypoint=='_case_block':
                            generated=module._case_block('GET',endpoint['path'],endpoint['path'].strip('/'),endpoint)
                        elif entrypoint=='_to_test':
                            generated=module._to_test('GET',endpoint['path'],endpoint['path'].strip('/'),endpoint)
                        else:
                            generated=module._to_bru('GET',endpoint['path'],endpoint['path'].strip('/'),endpoint)
                        self.assertTrue(any(token in generated for token in ('Assertions.fail','pytest.fail','throw new Error','stopExecution')))

    def test_restassured_preserves_fractional_response_limits(self):
        for lang in ('zh','en'):
            module=self.module('api-test-restassure','generate_restassured_tests.py',lang)
            for limit,expected in ((0.5,'500000L'),(250.9,'250900000L'),(250,'250000000L'),(1e308,'9223372036854775807L')):
                with self.subTest(language=lang, limit=limit):
                    code=module.build_java_class([{'method':'GET','path':'/orders','expected_statuses':[200],'max_response_ms':limit}])
                    self.assertIn(f'lessThanOrEqualTo({expected}), java.util.concurrent.TimeUnit.NANOSECONDS',code)

if __name__=='__main__':unittest.main()
