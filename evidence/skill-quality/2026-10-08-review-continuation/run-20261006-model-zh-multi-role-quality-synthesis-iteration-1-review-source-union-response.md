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
        "qa-1": {"version": "v1", "severity": "P0"},
        "tech-1": {"version": "v2", "severity": "P1"}
      },
      "evidence_by_source": {
        "qa-1": {"version": "v1", "evidence": ["run-R1"]},
        "tech-1": {"version": "v2", "evidence": ["diff-D1"]}
      }
    },
    {
      "id": "S-2",
      "input_finding_ids": ["F-product"],
      "sources": ["product-1"],
      "severity": "P2",
      "original_severities": {
        "product-1": {"version": "v3", "severity": "P2"}
      },
      "evidence_by_source": {
        "product-1": {"version": "v3", "evidence": ["req-Q7"]}
      }
    }
  ],
  "blockers": ["S-1"],
  "disagreements": [
    {
      "sources": ["qa-1", "tech-1"],
      "topic": "S-1（refund / retry after commit / duplicate debit）严重度分歧：qa-1@v1=P0；tech-1@v2=P1。汇总保守取输入最高紧急度 P0，分歧仍保留。"
    },
    {
      "sources": ["qa-1", "tech-1"],
      "topic": "S-1 阻塞判断分歧：qa-1@v1 blocking=true；tech-1@v2 blocking=false。保留 qa-1@v1 明确声明的阻塞。"
    }
  ]
}
