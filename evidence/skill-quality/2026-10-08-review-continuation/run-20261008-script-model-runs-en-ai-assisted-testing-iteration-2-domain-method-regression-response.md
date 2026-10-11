**1. Task Understanding**

This is a static comparison of the same 10 checkout cases. Sanitization, timings, execution, and acceptance are fixture statements, not independently verified records. Allowed use: local analysis only; no external actions or checkout tests were performed.

**2. Recommended AI-Assisted Work Split**

AI can draft cases and assertions, summarize review feedback, and maintain provenance and labor records. Humans approve business expectations, assertions, privacy, adoption, and acceptance. QA R1 is the supplied assertion reviewer.

The 35-minute rework stage is the largest potential improvement opportunity; savings have not been demonstrated.

**3. High-Risk Areas Needing Human Review**

Highest priority: adoption without human review. Business oracles, privacy, and high-risk tradeoffs also require named human owners; those owners are unspecified. Unreviewed artifacts remain drafts, and missing execution evidence remains unknown.

**4. Draft Outputs or Prompts to Use**

The supplied provenance record is:

Sanitized input → **input snapshot and model/prompt versions unspecified** → D1 → QA R1 reviews assertions → V2 → fixture-reported execution → 10/10 acceptance.

D2 has an adoption label but no human review. A review checklist, versioned provenance record, full labor log, and acceptance record are needed for auditable real use.

**5. Execution Order**

Classify and sanitize input → record input/model/prompt versions → generate draft → human review and rework → adopt a version → execute → human acceptance.

These are domain gates; the fixture supplies only partial provenance.

**6. Checks Before Final Use**

Observable oracles: adoption requires review linked to the adopted artifact and acceptance evidence; productivity improvement requires complete AI-assisted labor below a comparable manual baseline.

Calculations:

- `manual_total`: **60 minutes** — supplied baseline for the same 10 cases.
- `ai_total`: **80 minutes** — generation 10 + review 25 + rework 35 + acceptance 10.
- `labor_increase`: **20 minutes** — 80 − 60.
- `labor_increase_percent`: **33.33% of manual labor** — (80 − 60) ÷ 60 × 100.

Gaps include version identifiers, acceptance signer, underlying execution/review logs, defect counts, and confirmation of equivalent complexity and measurement windows. Rework time is recorded separately; defect counts cannot be inferred.

Sources: the user-supplied fixture, the [main prompt](../../../skills/en/testing-types/ai-assisted-testing/prompts/ai-assisted-testing.md), and the [domain reference](../../../skills/en/testing-types/ai-assisted-testing/references/domain-decision-example.md). Minimal local validation checked arithmetic, unique IDs and calculation keys, allowed enums, three-cell rows, and nonempty evidence. Decisions apply only to this fixture.

| ID | DECISION | Evidence |
| --- | --- | --- |
| I-1 | ACCEPTED | Sanitized input → D1 → QA R1 assertion review → adopted V2 → fixture-reported execution and 10/10 acceptance satisfy the supplied oracle; version metadata and acceptance signer remain unspecified. |
| I-2 | DRAFT | D2 is called adopted without human review, so the adoption gate is unmet; execution and acceptance evidence are unspecified. |
| I-3 | UNSUPPORTED | Generation alone takes 10 minutes, but complete AI-assisted labor is 80 minutes versus the 60-minute manual baseline: 20 minutes more labor. |
