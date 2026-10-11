Compare the supplied memory fixture against M-v3, covering reads, preference updates, deletion, isolation, provenance, and retention. **FAIL/PASS describe static fixture comparisons only.** No external actions or runtime tests were performed.

Facts and input audit: the user’s fixture supplies the policy and observations. The [main prompt](../../../skills/en/testing-types/agent-memory-testing/prompts/agent-memory-testing.md) supplies the procedure; the [domain example](../../../skills/en/testing-types/agent-memory-testing/references/domain-decision-example.md) supplies calibration, not execution evidence.

Known facts include tenant ownership, the two valid preference versions, deletion acknowledgment, and the permitted read control. Missing evidence includes write and expiry timestamps, source provenance beyond the named records, ordered retrieval traces, cache behavior, and backup policy. The observations conflict with three policy requirements; the policy definitions themselves are consistent. Runtime recency and staleness cannot be assessed. Live access and system changes are outside scope. The deletion observation is interpreted as the post-acknowledgment retrieval described by the fixture; a replay would require timestamps to establish that ordering.

Evidence-backed inferences and domain steps follow. P1 denotes a stated policy violation; P2 denotes an unresolved policy or evidence gap.

- **P1 — Isolation and contamination risk.** Source/evidence: static fixture showing a foreign tenant’s record. Preconditions: separate synthetic tenant stores. Stimulus: issue the same preference query under each identity. Oracle: every returned record belongs to the querying tenant; the valid own-tenant read supplies a positive control. Capture tenant, memory ID, version, and origin. Stop on any foreign record. Owner: retrieval engineer. Close with traces satisfying isolation and permitted retrieval. Downstream answer contamination remains unproven.
- **P1 — Preference update precedence.** Source/evidence: static fixture with two valid versions and an answer using the older one. Preconditions: retain both supplied versions. Stimulus: query the preference. Oracle: select v2 and answer email. Capture validity, selected version, and response; write times do not override the supplied version rule. Stop on selection of v1. Owner: memory resolution engineer. Close when selection and response both follow the highest valid version.
- **P1 — Deletion and forgetting.** Source/evidence: static fixture showing an acknowledged deletion followed by an index return. Preconditions: record acknowledgment and query ordering. Stimulus: retrieve immediately afterward. Oracle: the deleted record is absent, with no invented grace period. Capture acknowledgment and retrieval timestamps, record ID, and index/cache traces. Stop on a returned deleted record. Owner: memory storage engineer. Close with absence across the defined retrieval scope; backup expiry requires separate evidence.
- **P2 — Retention and lifecycle provenance.** Source/evidence: the fixture supplies no backup retention policy. Preconditions: obtain the policy and backup inventory. Stimulus: inspect a masked backup at a policy-defined expiry boundary. Oracle: apply the approved expiry rule. Require write/expiry timestamps, provenance, deletion status, and expiry evidence. Stop the assessment while the rule is undefined. Owner: data platform and policy owners. Close with an explicit rule and supporting observations.

Candidate recommendations: review tenant filtering, version selection, and deletion visibility against these observable failures without asserting a root cause. The smallest future validation is an isolated synthetic replay of the preference, isolation/control, and post-deletion queries with one ordered provenance trace. Backup validation remains pending its policy. Write correctness, cache propagation, complete backup forgetting, and production behavior remain unverified.

Human decision: the policy owner must define backup retention scope, expiry criteria, and any deletion obligations before backup compliance can be assessed.

Minimal static validation confirmed five unique supplied IDs, three nonempty cells per row, and one allowed decision enum per row. No calculation keys were supplied or introduced.

| ID | DECISION | Evidence |
| --- | --- | --- |
| M-1 | FAIL | Fixture: tenant A's query retrieves B/m9; M-v3 requires strict tenant isolation. |
| M-2 | FAIL | Fixture: both versions are valid, v2=email outranks v1=SMS, but the response uses v1; M-v3 requires the highest valid version. |
| M-3 | FAIL | Fixture: deletion of A/m2 is acknowledged, yet the index returns m2; M-v3 forbids retrieval immediately after acknowledgment. |
| M-4 | PASS | Fixture: A retrieves its own valid m3 v2 with no B records; this supplied read is a permitted isolation control. |
| M-5 | UNKNOWN | Fixture: no backup retention policy is supplied, so no backup expiry deadline or observable compliance criterion can be established. |
