# Skill Benchmark: functional-testing

**Date**: 2026-10-03T11:23:02Z
**Evals**: Functional testing: executable plan with context, Functional testing: draft despite missing docs, Functional testing: cut scope for a short window (1 runs each per configuration)

## Summary

| Metric | With Skill |
|--------|------------|
| Pass Rate | 100% ± 0% |

## Per-Case Results

### Functional testing: executable plan with context (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[(?i)Task Understanding (?i)(Risk|Priority) (?i)(boundary|edge|limit) (?i)(negative|failure|exception|abnormal)]} | ✅ | output satisfies all regex checks (all:[(?i)Task Understanding (?i)(Risk|Priority) (?i)(boundary|edge|limit) (?i)(negative|failure|exception|abnormal)]) |

### Functional testing: draft despite missing docs (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[(?i)(assumption|assumptions|assumed|working assumptions|\[assumption\]) (?i)(open questions|information gaps|missing information|gaps|what I need|must-have information)]} | ✅ | output satisfies all regex checks (all:[(?i)(assumption|assumptions|assumed|working assumptions|\[assumption\]) (?i)(open questions|information gaps|missing information|gaps|what I need|must-have information)]) |

### Functional testing: cut scope for a short window (with_skill)

- **Pass Rate**: 100% (4/4)

| Expectation | Result | Evidence |
|-------------|--------|----------|
| expect.must_contain | ✅ | all checks passed |
| expect.must_not_contain | ✅ | all checks passed |
| expect.exit_code | ✅ | all checks passed |
| output_matches{all:[P0 (?i)(critical path|critical scenario|core flow|release gate) (?i)(defer|deferred|deferral|out of scope|not in this pass) (?i)risk]} | ✅ | output satisfies all regex checks (all:[P0 (?i)(critical path|critical scenario|core flow|release gate) (?i)(defer|deferred|deferral|out of scope|not in this pass) (?i)risk]) |

