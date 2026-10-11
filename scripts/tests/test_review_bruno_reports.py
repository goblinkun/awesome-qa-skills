import unittest
from scripts.tests.test_review_parser_fidelity import ROOT,load


class BrunoReportTests(unittest.TestCase):
    def checker(self):
        return load(ROOT/'skills/en/testing-types/api-test-bruno/scripts/check_bruno_report.py').validate_report

    def report(self):
        return [{'iterationIndex':0,'results':[{'status':'pass','response':{'status':201},'testResults':[{'status':'pass'}],'assertionResults':[],'error':None}], 'summary':{'totalRequests':1,'passedRequests':1,'failedRequests':0,'errorRequests':0,'skippedRequests':0,'totalTests':1,'passedTests':1,'failedTests':0,'totalAssertions':0,'failedAssertions':0}}]

    def test_valid_executed_request_and_assertion(self):
        self.checker()(self.report())

    def test_empty_skipped_and_zero_assertion_reports_fail(self):
        for change in ('empty','skipped','no-tests','missing-response'):
            r=self.report()
            if change=='empty':r=[]
            if change=='skipped':r[0]['results'][0]['skipped']=True;r[0]['summary']['skippedRequests']=1
            if change=='no-tests':r[0]['results'][0]['testResults']=[];r[0]['summary']['totalTests']=0;r[0]['summary']['passedTests']=0
            if change=='missing-response':del r[0]['results'][0]['response']
            with self.subTest(change=change),self.assertRaises(ValueError):self.checker()(r)

    def test_failed_test_is_not_hidden_by_pass_request_status(self):
        r=self.report();r[0]['results'][0]['testResults'][0]['status']='fail'
        with self.assertRaises(ValueError):self.checker()(r)

if __name__=='__main__':unittest.main()
