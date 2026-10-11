from pathlib import Path
import json
import unittest
from scripts.tests.test_review_parser_fidelity import ROOT, load


class PlusScaffoldTests(unittest.TestCase):
    def module(self, lang, name, script):
        return load(ROOT/'skills'/lang/'testing-types'/name/'scripts'/script)

    def test_writer_preserves_password_rule_without_inventing_business_cases(self):
        req='Password must have at least 12 characters; user_id >= -1.\nNo password may exceed 64 characters.'
        for lang in ('en','zh'):
            cases=self.module(lang,'testcase-writer-plus','run_writer.py').generate_test_cases(req,'Analysis is pending.')
            data=json.dumps(cases,ensure_ascii=False)
            self.assertIn('user_id >= -1',data);self.assertIn('64 characters',data)
            self.assertNotIn('礼品',data);self.assertNotIn('活动页',data);self.assertNotIn('与规则一致',data)
            self.assertTrue(all(c['priority']=='NOT_ASSESSED' and c['status']=='NOT_ASSESSED' for c in cases))
            self.assertTrue(all('source_line' in c and 'source_hash' in c for c in cases))

    def test_review_is_not_a_fabricated_conclusion_on_correct_calculator_cases(self):
        docs=[('requirement','1 + 1 must equal 2.'),('testcases','TC-1: enter 1 + 1; expected display 2.')]
        for lang in ('en','zh'):
            result=self.module(lang,'test-case-reviewer-plus','run_review.py').build_review('review policy',docs)
            self.assertEqual(result['analysis_status'],'NOT_ASSESSED')
            self.assertIn('pending_human_decisions',result)
            data=json.dumps(result,ensure_ascii=False);self.assertNotIn('库存',data);self.assertNotIn('T+1',data)
            self.assertIn('1 + 1 must equal 2.',data);self.assertIn('source_hash',data)

    def test_strategy_does_not_invent_topology_thresholds_or_scope(self):
        for domain in ('Calculator: 1 + 1 must equal 2.','Text editor must preserve UTF-8.','温度转换：0摄氏度应转换为32华氏度。'):
            for lang in ('en','zh'):
                result=self.module(lang,'test-strategy-plus','run_strategy.py').build_strategy('policy',[('requirement',domain)])
                self.assertEqual(result['analysis_status'],'NOT_ASSESSED')
                data=json.dumps(result,ensure_ascii=False);self.assertIn(domain,data)
                for invented in ('库存','95%','网关','资格'):self.assertNotIn(invented,data)

    def test_analysis_preserves_all_lines_and_does_not_claim_testability(self):
        raw='\n'.join(f'Rule {i}: user_id >= -{i}; must preserve retry-count > 3.' for i in range(1,56))
        for lang in ('en','zh'):
            result=self.module(lang,'requirements-analysis-plus','run_analysis.py').build_analysis('policy',raw,Path('rules.md'),'markdown')
            self.assertIn('NOT_ASSESSED',result);self.assertIn('Rule 55:',result)
            self.assertIn('user_id >= -1;',result);self.assertNotIn('partially testable',result)
            self.assertNotIn('eligibility, inventory',result)

    def test_empty_required_sources_fail(self):
        for lang in ('en','zh'):
            with self.assertRaisesRegex(ValueError,'Empty'):
                self.module(lang,'testcase-writer-plus','run_writer.py').generate_test_cases('','analysis')
            with self.assertRaisesRegex(ValueError,'Empty'):
                self.module(lang,'test-case-reviewer-plus','run_review.py').build_review('policy',[('requirement','')])
            with self.assertRaisesRegex(ValueError,'Empty'):
                self.module(lang,'test-strategy-plus','run_strategy.py').build_strategy('policy',[('requirement','')])
            with self.assertRaisesRegex(ValueError,'Empty'):
                self.module(lang,'requirements-analysis-plus','run_analysis.py').build_analysis('policy','',Path('r.md'),'markdown')

if __name__=='__main__':unittest.main()
