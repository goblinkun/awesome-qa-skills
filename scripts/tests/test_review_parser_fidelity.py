from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
API_NAMES = ('api-test-bruno', 'api-test-pytest', 'api-test-restassure', 'api-test-supertest')
NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'


def load(path):
    spec = importlib.util.spec_from_file_location('review_' + str(path).replace('/', '_').replace('-', '_'), path)
    module = importlib.util.module_from_spec(spec)
    with patch.object(sys, 'path', [str(path.parent), *sys.path]):
        spec.loader.exec_module(module)
    return module


def workbook(path):
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('xl/workbook.xml', '<workbook xmlns="'+NS+'" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Rules" sheetId="1" r:id="rId1"/><sheet name="Errors" sheetId="2" r:id="rId2"/></sheets></workbook>')
        z.writestr('xl/_rels/workbook.xml.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Target="worksheets/sheet1.xml"/><Relationship Id="rId2" Target="/xl/worksheets/sheet2.xml"/></Relationships>')
        z.writestr('xl/sharedStrings.xml', '<sst xmlns="'+NS+'"><si><t>user_id &gt;= -1</t></si></sst>')
        z.writestr('xl/worksheets/sheet1.xml', '<worksheet xmlns="'+NS+'"><sheetData><row r="1"><c r="A1" t="inlineStr"><is><t>REQ-1</t></is></c><c r="C1"><v>42</v></c></row><row r="3"><c r="B3" t="s"><v>0</v></c></row></sheetData></worksheet>')
        z.writestr('xl/worksheets/sheet2.xml', '<worksheet xmlns="'+NS+'"><sheetData><row r="1"><c r="A1" t="inlineStr"><is><t>ERR-2</t></is></c></row></sheetData></worksheet>')


class WorkbookFidelityTests(unittest.TestCase):
    def test_row_coordinates_are_inferred_or_rejected_when_conflicting(self):
        with TemporaryDirectory() as folder:
            path=Path(folder)/'row.xlsx'
            for row,expected in [('<row><c r="A3" t="inlineStr"><is><t>r3</t></is></c></row>',3),('<row r="1"><c r="A3"><v>1</v></c></row>',None)]:
                with zipfile.ZipFile(path,'w') as z:z.writestr('xl/worksheets/sheet1.xml','<worksheet xmlns="'+NS+'"><sheetData>'+row+'</sheetData></worksheet>')
                reader=load(ROOT/'scripts/skill_resources/xlsx_reader.py')
                if expected is None:
                    with self.assertRaisesRegex(ValueError,'row'):reader.read_workbook(path)
                else:self.assertEqual(reader.read_workbook(path)[0]['row_numbers'],[expected])

    def test_plus_excel_rows_are_unambiguous_json(self):
        with TemporaryDirectory() as folder:
            path=Path(folder)/'pipes.xlsx'
            with zipfile.ZipFile(path,'w') as z:z.writestr('xl/worksheets/sheet1.xml','<worksheet xmlns="'+NS+'"><sheetData><row r="1"><c r="A1" t="inlineStr"><is><t>a | b</t></is></c><c r="C1" t="inlineStr"><is><t>x&#10;y</t></is></c></row></sheetData></worksheet>')
            for lang in ('zh','en'):
                for name in ('requirements-analysis-plus','test-case-reviewer-plus','test-strategy-plus','testcase-writer-plus'):
                    data=load(ROOT/'skills'/lang/'testing-types'/name/'scripts/common_parser.py').parse_excel(path)
                    raw=next(l for l in data.splitlines() if l.startswith('row 1: '))[7:]
                    self.assertEqual(json.loads(raw),['a | b','','x\ny'])

    def test_inline_strings_and_sparse_columns_in_existing_parsers(self):
        with TemporaryDirectory() as folder:
            path = Path(folder)/'rules.xlsx'; workbook(path)
            for lang in ('zh', 'en'):
                for name in ('functional-testing', 'performance-testing'):
                    for script in ('parse_formats.py', 'convert_formats.py'):
                        p=ROOT/'skills'/lang/'testing-types'/name/'scripts'/script
                        with self.subTest(path=str(p)):
                            data=load(p).parse_xlsx(path)
                            rows=data.get('rows',data.get('sample_rows'))
                            self.assertEqual(rows[0], ['REQ-1', '', '42'])
                            self.assertIn('Errors', [s['name'] for s in data['sheets']])
                            self.assertEqual(data['sheets'][0]['row_numbers'], [1,3])
                            self.assertEqual(data['sheets'][1]['rows'], [['ERR-2']])

    def test_all_packaged_excel_readers_keep_supplied_values(self):
        with TemporaryDirectory() as folder:
            path=Path(folder)/'rules.xlsx';workbook(path)
            readers=list((ROOT/'skills').glob('*/*/*/scripts/convert_formats.py')) + list((ROOT/'skills').glob('*/*/*/scripts/common_parser.py'))
            tested=0
            for p in readers:
                mod=load(p); fn=getattr(mod,'parse_xlsx',None) or getattr(mod,'parse_excel',None)
                if fn is None:continue
                with self.subTest(path=str(p)):
                    text=json.dumps(fn(path),ensure_ascii=False)
                    self.assertIn('REQ-1',text);self.assertIn('ERR-2',text);self.assertIn('user_id >= -1',text)
                tested+=1
            self.assertEqual(tested,48)

    def test_markdown_preserves_rule_identifiers_and_operators(self):
        raw='user_id >= -1; retry-count > 3; REQ-001'
        with TemporaryDirectory() as folder:
            path=Path(folder)/'rule.md';path.write_text(raw)
            for lang in ('zh','en'):
                p=ROOT/'skills'/lang/'testing-types'/'requirements-analysis-plus'/'scripts/common_parser.py'
                self.assertEqual(load(p).parse_markdown(path),raw)


class ApiParsingFidelityTests(unittest.TestCase):
    def modules(self):
        for lang in ('zh','en'):
            for name in API_NAMES:
                yield lang+'/'+name,load(ROOT/'skills'/lang/'testing-types'/name/'scripts/parse_api_sources.py')

    def test_curl_inferred_method_body_headers_and_query(self):
        source='curl --url "https://example.test/orders?mode=check" -H "Content-Type: application/json" --data-raw \'{"qty":1}\''
        for name,m in self.modules():
            with self.subTest(package=name):
                ep=m._parse_curl(source,'fixture')[0]
                self.assertEqual(ep['method'],'POST');self.assertEqual(ep['path'],'/orders?mode=check')
                self.assertEqual(ep['body'],{'qty':1});self.assertEqual(ep['headers']['Content-Type'],'application/json')
                self.assertEqual(m._parse_curl('curl -G -d "q=a" https://example.test/search','fixture')[0]['path'],'/search?q=a')
                self.assertEqual(m._parse_curl('curl -I https://example.test/health','fixture')[0]['method'],'HEAD')

    def test_variable_url_and_postman_payload_are_not_lost(self):
        obj={'item':[{'request':{'method':'POST','url':'{{baseUrl}}/orders','header':[{'key':'Content-Type','value':'application/json'}],'body':{'mode':'raw','raw':'{"qty":1}'}}}]}
        for name,m in self.modules():
            with self.subTest(package=name):
                ep=m._parse_postman(obj,'fixture')[0];self.assertEqual(ep['path'],'/orders');self.assertEqual(ep['body'],{'qty':1})
                self.assertEqual(ep['raw_url'],'{{baseUrl}}/orders')
                b=m._parse_bruno('get {\n url: {{baseUrl}}/orders\n}', 'fixture')[0]
                self.assertEqual(b['path'],'/orders');self.assertEqual(b['raw_url'],'{{baseUrl}}/orders')

    def test_openapi_preserves_declared_example_and_success_contract(self):
        obj={'openapi':'3.0.3','paths':{'/orders':{'post':{'requestBody':{'required':True,'content':{'application/json':{'schema':{'type':'object'},'example':{'qty':1}}}},'responses':{'201':{'description':'Created'},'400':{'description':'Invalid'}}}}}}
        for name,m in self.modules():
            with self.subTest(package=name):
                ep=m._parse_openapi(obj,'fixture')[0]
                self.assertEqual(ep['body'],{'qty':1});self.assertEqual(ep['expected_statuses'],[201]);self.assertTrue(ep['body_required'])

    def test_wsdl_preserves_service_address_and_does_not_invent_rest_path(self):
        xml='<definitions xmlns="http://schemas.xmlsoap.org/wsdl/" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"><binding><operation name="CreateOrder"><soap:operation soapAction="urn:CreateOrder"/></operation></binding><service><port><soap:address location="https://example.test/service"/></port></service></definitions>'
        for name,m in self.modules():
            with self.subTest(package=name):
                ep=m._parse_wsdl(xml,'fixture')[0]
                self.assertEqual(ep['path'],'/service');self.assertEqual(ep['operation'],'CreateOrder');self.assertEqual(ep['soap_action'],'urn:CreateOrder')

    def test_wsdl_operations_follow_their_port_binding(self):
        xml='<definitions xmlns="http://schemas.xmlsoap.org/wsdl/" xmlns:tns="urn:demo" targetNamespace="urn:demo" xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"><binding name="OrderBinding"><operation name="CreateOrder"><soap:operation soapAction="urn:create"/></operation></binding><binding name="QuoteBinding"><operation name="Quote"><soap:operation soapAction="urn:quote"/></operation></binding><service><port binding="tns:OrderBinding"><soap:address location="https://example.test/orders"/></port><port binding="tns:QuoteBinding"><soap:address location="https://example.test/quotes"/></port></service></definitions>'
        for name,m in self.modules():
            with self.subTest(package=name):
                self.assertEqual([(e['path'],e['operation']) for e in m._parse_wsdl(xml,'fixture')],[('/orders','CreateOrder'),('/quotes','Quote')])

    def test_missing_yaml_dependency_is_an_explicit_error(self):
        for name,m in self.modules():
            with self.subTest(package=name), patch.object(m,'yaml',None):
                with self.assertRaisesRegex(RuntimeError,'PyYAML'):
                    m.parse_file(Path('api.yaml'),'openapi: 3.0.3\npaths: {}')

    def test_dedupe_keeps_distinct_request_scenarios(self):
        for name,m in self.modules():
            with self.subTest(package=name):
                eps=[{'method':'POST','path':'/orders','source':'fixture','body':{'qty':v}} for v in (1,0,1)]
                self.assertEqual(len(m.dedupe(eps)),2)

    def test_normalized_contract_can_enter_the_run_pipeline(self):
        endpoint={'method':'POST','path':'/orders','body':{'qty':1},'expected_statuses':[201],'expected_json':{'qty':1}}
        for name,m in self.modules():
            with self.subTest(package=name):
                actual=m.parse_file(Path('contract.json'),json.dumps({'endpoints':[endpoint]}))[0]
                self.assertEqual(actual['body'],endpoint['body']);self.assertEqual(actual['expected_statuses'],[201]);self.assertEqual(actual['expected_json'],{'qty':1})

    def test_integer_openapi_response_keys_do_not_drop_schema(self):
        obj={'openapi':'3.0.3','paths':{'/orders':{'get':{'responses':{200:{'content':{'application/json':{'schema':{'type':'object'}}}},202:{'content':{'application/json':{'schema':{'type':'array'}}}}}}}}}
        for name,m in self.modules():
            with self.subTest(package=name):
                actual=m._parse_openapi(obj,'fixture')[0]
                self.assertEqual(actual['response_schema'],{'type':'object'})
                self.assertEqual(set(actual['response_contracts']),{'200','202'})

if __name__=='__main__':unittest.main()
