{
  "source_register": [
    {"source_id": "qa-1", "version": "v1"},
    {"source_id": "tech-1", "version": "v2"},
    {"source_id": "product-1", "version": "v3"}
  ],
  "findings": [
    {
      "id": "F-1",
      "target": "refund",
      "condition": "retry after commit",
      "problem": "duplicate debit",
      "input_finding_ids": ["F-qa", "F-tech"],
      "sources": ["qa-1", "tech-1"],
      "source_versions": {"qa-1": "v1", "tech-1": "v2"},
      "severity": "P0",
      "severity_rule": "conservative highest-input urgency (P0 > P1 > P2 > P3)",
      "original_severities": {"qa-1": "P0", "tech-1": "P1"},
      "evidence_by_source": {
        "qa-1": ["run-R1"],
        "tech-1": ["diff-D1"]
      }
    },
    {
      "id": "F-2",
      "target": "invoice-import",
      "condition": "same invoice uploaded twice",
      "problem": "duplicate debit",
      "input_finding_ids": ["F-product"],
      "sources": ["product-1"],
      "source_versions": {"product-1": "v3"},
      "severity": "P2",
      "original_severities": {"product-1": "P2"},
      "evidence_by_source": {
        "product-1": ["req-Q7"]
      }
    }
  ],
  "blockers": ["F-1"],
  "disagreements": [
    {
      "sources": ["qa-1", "tech-1"],
      "topic": "F-1 severity: qa-1@v1 supplies P0; tech-1@v2 supplies P1. Both are preserved; synthesized P0 follows conservative highest-input urgency."
    },
    {
      "sources": ["qa-1", "tech-1"],
      "topic": "F-1 blocking status: qa-1@v1 supplies blocking=true; tech-1@v2 supplies blocking=false. F-1 remains in blockers because QA explicitly declares it blocking."
    }
  ]
}
