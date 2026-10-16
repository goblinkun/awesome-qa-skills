# Skill Benchmark: testability-analysis

**Date**: 2026-10-03T11:36:41Z
**Evals**: Testability Analysis: domain-complete scenario, Testability Analysis: bounded first pass with incomplete input, Testability Analysis: high-risk boundary and tradeoffs, Architecture testability review: seams and environment reproduction, Architecture testability review: incomplete architecture material (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 100% ± 0% |

## Per-Case Results

### Testability Analysis: domain-complete scenario (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[(?i)task understanding (?i)input audit (?i)risks? P0 (?i)(expected|decision criterion|acceptance)]} | ✅ | output satisfies all regex checks (all:[(?i)task understanding (?i)input audit (?i)risks? P0 (?i)(expected|decision criterion|acceptance)]) |

### Testability Analysis: bounded first pass with incomplete input (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[(?i)working assumptions (?i)open questions (?i)evidence (?i)(next actions|next steps|immediate requests|smallest next actions)]} | ✅ | output satisfies all regex checks (all:[(?i)working assumptions (?i)open questions (?i)evidence (?i)(next actions|next steps|immediate requests|smallest next actions)]) |

### Testability Analysis: high-risk boundary and tradeoffs (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[P0 P1 (?i)(residual risk|remaining risk|unverified.*risk)]} | ✅ | output satisfies all regex checks (all:[P0 P1 (?i)(residual risk|remaining risk|unverified.*risk)]) |

### Architecture testability review: seams and environment reproduction (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[(?i)(input audit|input evidence|evidence (basis|quality)|evidence is limited|confirmed facts) (?i)isolation (?i)(validation|verification|verify)]} | ✅ | output satisfies all regex checks (all:[(?i)(input audit|input evidence|evidence (basis|quality)|evidence is limited|confirmed facts) (?i)isolation (?i)(validation|verification|verify)]) |

### Architecture testability review: incomplete architecture material (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[(?i)Input Audit (?i)(open questions|missing|gaps) (?i)evidence]} | ✅ | output satisfies all regex checks (all:[(?i)Input Audit (?i)(open questions|missing|gaps) (?i)evidence]) |

