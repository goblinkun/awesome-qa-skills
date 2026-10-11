# Free QA Skills: Learning Opportunities (2026-10-09)

[中文](./2026-10-09-free-qa-skills-learning-review.md)

## Scope and evidence

Reviewed the current `main` tree of `Quality-Max/free-qa-skills`, source SHA `b0f94a6bf1b50a1c124b4735f46e5b8cf6826b89`, and read selected Skill files alongside local counterparts. This is a static review; it does not claim that upstream Skills were run or that their browser checks were validated.

## Highest-priority skills to study

| Priority | Upstream Skill | What to learn | Relationship to this repository |
| --- | --- | --- | --- |
| 1 | [evidence-code-audit](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/evidence-code-audit/SKILL.md) and its [audit dimensions](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/evidence-code-audit/references/dimensions.md) | Select incremental, focused, or broad scope; trace a trigger to a concrete failure; keep severity, confidence, and coverage separate; preserve Not assessed. | Local [code-review](../../skills/en/testing-types/code-review/SKILL.md) focuses on PRs and diffs. Learn its broad-audit mode and coverage matrix without replacing the existing PR-review contract. |
| 2 | [script-quality-review](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/script-quality-review/SKILL.md) | Catch false-green tests: skips counted as passes, generic 4xx checks, assertions that miss the titled case, unknown routes/selectors, and writes without cleanup. | Local [ai-generated-test-review](../../skills/en/testing-types/ai-generated-test-review/SKILL.md) and [test-code-review](../../skills/en/testing-types/test-code-review/SKILL.md) are more systematic. Reuse its counterexamples in Evals instead of adding a duplicate Skill. |
| 3 | [flaky-selector-scan](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/flaky-selector-scan/SKILL.md) | Map absolute XPath, positional selectors, generated classes, deep descendants, copy-coupled text, and index-based locators to stable alternatives. | Local [ui-test-selector-review](../../skills/en/testing-types/ui-test-selector-review/SKILL.md) has stronger semantic and evidence constraints; borrow the compact taxonomy and examples. |
| 4 | [responsive-screenshots](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/responsive-screenshots/SKILL.md) | Use a fixed 375/768/1280/1920/2560px viewport set, capture screenshots, and report overflow, text size, touch targets, and navigation behavior. | Local [visual-regression-testing](../../skills/en/testing-types/visual-regression-testing/SKILL.md) defines baselines and comparison conditions. Its concrete run steps and screenshot outputs are complementary. |

## Candidates if expanding web coverage

- [i18n-rtl-audit](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/i18n-rtl-audit/SKILL.md): long-string overflow, RTL layout, hardcoded copy, and `lang` / `dir` attributes. A local filename/content search found no direct site-audit counterpart. Worth a small pilot if expanding multilingual web QA. It temporarily changes page text and `dir`, so constrain it to a test environment and restore state.
- [cookie-privacy-scan](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/cookie-privacy-scan/SKILL.md): pre-consent network requests, third-party trackers, and cookie attributes; complements local [session-security-testing](../../skills/en/testing-types/session-security-testing/SKILL.md), which focuses more on session lifecycle. Redact cookie values, and leave legal conclusions to known jurisdictional and project rules instead of hard-coding severity as compliance verdicts.
- [core-web-vitals](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/core-web-vitals/SKILL.md): browser-based page metrics and an explicit “INP not measured” state when no interaction occurs. It can complement local load-modeling and performance-analysis Skills. Do not treat one browser sample or its A–F aggregate grade as a stable baseline, production acceptance, or release verdict.

## Avoid duplicate Skills

Upstream [test-quality-review](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/test-quality-review/SKILL.md), [diff-risk-review](https://github.com/Quality-Max/free-qa-skills/blob/main/skills/diff-risk-review/SKILL.md), accessibility-check, and agentic-app-risk-review overlap with local test-code review, code review, accessibility, and AI-safety coverage. Their main value is short triggers, a fast check path, and compact report examples; local Skills already have more detailed evidence states, input boundaries, and Eval contracts.

## Recommendation

Read `evidence-code-audit` and `script-quality-review` first. Then consider folding the concise taxonomy and visible outputs from `flaky-selector-scan` and `responsive-screenshots` into neighboring Skills' examples or Evals. Evaluate i18n/RTL, cookie privacy, and Core Web Vitals only if web-product auditing is an intended coverage area. Upstream browser Skills require Playwright MCP; this review did not execute them.

`evidence-code-audit` attributes part of its audit framework to XiNian-dada's repository and retains MIT terms. Preserve source and license requirements if copying specific text or assets; this note only extracts methods.
