## 1. Task understanding and scope

Compare the four fixture cases using Human hours to decide whether the supplied automation assumptions break even. The success criteria are a three-month net labor saving and whole-month break-even for the first case, plus one supported decision per case.

This is a static fixture comparison. No real tests or external actions were performed, and no monetary return is inferred.

## 2. Input audit

- **Known:** Build is 12 h; manual work is 1 h/run; automation plus review is 0.2 h/run. The prompt supplies run frequency and maintenance for the first three cases, and a three-month horizon for the first. Source: current-turn fixture. The skill’s [sanitized calibration example](../../../skills/en/testing-types/automation-roi-analysis/evals/cases/domain-method-regression.yaml) confirms the fixture oracle; it is not real project evidence.
- **Missing:** The fourth case lacks frequency and a case-specific maintenance value. The second and third cases have no stated horizon, but their recurring net labor is nonpositive under the supplied assumptions. Candidate workflow details and measured time records are also absent.
- **Conflicting:** No conflicts found among the supplied figures.
- **Stale:** The fixture has no underlying period or version, so its real-world recency cannot be assessed.
- **Out of scope:** Live-system behavior, test execution, business acceptance, and currency conversion.
- **Assumptions:** Build is one-time; run and maintenance values recur monthly and remain stable over the stated horizon. The 0.2 h/run is combined automation and review effort.

## 3. ROI analysis and priorities

All quantities are Human hours. The observable oracle is:

- Recurring monthly net = runs × (1 − 0.2) − monthly maintenance.
- Net over a stated horizon = months × recurring monthly net − 12 h build.
- Whole-month break-even = ceiling of build hours divided by positive recurring monthly net. If recurring net is zero or negative, there is no break-even under steady inputs.

For a labor-only ROI ratio, the numerator would be net Human hours saved after build, run/review, and maintenance; the denominator would be total automation-side Human hours over the same horizon. No ratio or monetary conversion is reported.

The supplied cases provide a base scenario and a change-driven maintenance scenario, but no low/base/high range. The local arithmetic cross-check reproduced the first case’s net and break-even figures, the second case’s zero recurring net, and the third case’s negative recurring net. This validates only the arithmetic, not any real automation outcome.

## 4. Candidate validation and residual risk

The smallest useful real-world validation would record eligible run count, manual time, automation-plus-review time, and maintenance time for a representative monthly window, then apply the same oracle. Stop or escalate if measured recurring net is nonpositive, or if exceptions require human risk acceptance.

Residual risk remains because the fixture’s time and frequency inputs are unmeasured. A human owner must confirm the window is representative and decide whether non-labor benefits justify investment where labor savings do not break even.

### Requested calculations

| METRIC | VALUE | Unit/evidence |
|---|---:|---|
| net_saving_h | 24 | Human hours; three months × (20 runs/month × 0.8 h/run − 4 h/month maintenance) − 12 h build |
| break_even_months | 1 | Whole months; ceiling of 12 h build ÷ 12 h recurring net labor/month |

### Decision table — fixture comparison only

| ID | DECISION | Evidence |
|---|---|---|
| R-1 | POSITIVE | Source: current-turn fixture. Trigger: 20 runs/month, 4 h/month maintenance, three-month horizon. Oracle: positive recurring net and positive horizon net; calculation is shown above. Evidence state: static calculation only. Priority P2: favorable labor case, with 12 h build exposure; likelihood of input drift is unmeasured and detectable from run/time logs. Owner: QA automation lead with process owner. Close condition: confirm representative run count, manual time, automation-plus-review time, and maintenance. Stop or escalate if measured recurring net is nonpositive or exceptions require human risk acceptance. |
| R-2 | NO_BREAK_EVEN | Source: current-turn fixture. Trigger: 5 runs/month and 4 h/month maintenance. Oracle: 5 × 0.8 − 4 = 0 h recurring net, so the one-time build is not recovered under steady inputs. Evidence state: static calculation only. Priority P1: build labor has no labor payback under these assumptions; likelihood is unmeasured and the arithmetic is directly checkable. Owner: QA automation lead with process owner. Close condition: validate frequency and maintenance from records; if recurring net remains nonpositive, stop the labor-only case unless a human owner accepts a non-labor objective. |
| R-3 | NO_BREAK_EVEN | Source: current-turn fixture. Trigger: 20 runs/month after maintenance rises to 20 h/month. Oracle: 20 × 0.8 − 20 = −4 h recurring net/month; no break-even under steady inputs. Evidence state: static change scenario only. Priority P1: the supplied change case produces recurring labor loss; real likelihood and persistence are unmeasured but observable in post-change maintenance and run records. Owner: QA automation lead with the maintainer or process owner. Close condition: remeasure post-change frequency and maintenance; stop scaling while recurring net is nonpositive and escalate any non-labor case for human judgment. |
| R-4 | UNKNOWN | Source: current-turn fixture. Trigger: frequency is missing, and no case-specific maintenance value is supplied. Oracle: recurring net and break-even cannot be calculated. Evidence state: incomplete static input. Priority P1: decision blocker; exposure cannot be bounded, and the missing fields are directly detectable. Owner: process owner with QA automation lead. Close condition: supply a sourced monthly run count and maintenance estimate, then apply the stated oracle; hold the ROI decision until those inputs are available. |
