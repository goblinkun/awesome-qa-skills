{
  "source_register": [
    {"source_id": "qa-1", "version": "v1"},
    {"source_id": "tech-1", "version": "v2"},
    {"source_id": "product-1", "version": "v3"}
  ],
  "findings": [
    {
      "id": "S-1",
      "input_finding_ids": ["F-qa", "F-tech"],
      "sources": ["qa-1", "tech-1"],
      "severity": "P0",
      "original_severities": {
        "qa-1": "P0",
        "tech-1": "P1"
      },
      "evidence_by_source": {
        "qa-1": ["run-R1"],
        "tech-1": ["diff-D1"]
      }
    },
    {
      "id": "S-2",
      "input_finding_ids": ["F-product"],
      "sources": ["product-1"],
      "severity": "P2",
      "original_severities": {
        "product-1": "P2"
      },
      "evidence_by_source": {
        "product-1": ["req-Q7"]
      }
    }
  ],
  "blockers": ["S-1"],
  "disagreements": [
    {
      "sources": ["qa-1", "tech-1"],
      "topic": "Refund retry after commit: qa-1/v1 reports P0 and blocking; tech-1/v2 reports P1 and non-blocking. Synthesized P0 follows conservative highest-input urgency (P0 > P1 > P2 > P3); the disagreement remains unresolved."
    }
  ]
}
