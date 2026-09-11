# InfraGuard AI Frozen v1 Benchmark Record - Objective Results and Archived Human-Report Provenance

> **FROZEN EVIDENCE BOUNDARY:** This record describes the qwen2.5:3b v1 run
> generated on 18 August 2026. The current source contains post-benchmark
> hardening and has not been rerun as v2, so these model results must not be
> transferred to the revised implementation. Only automatically derived
> objective measures are adopted quantitatively. Practitioner-report aggregates
> are excluded because the assessor-by-item ratings required to recompute them
> are not retained in the inspected evidence package.

- Benchmark version: 1.0.0
- Specification SHA-256: `7936721040238a95c57d51ec6fa86b9ee104b6b4021df83efdf903604ab58fee`
- Model: `qwen2.5:3b`
- Model digest: `357c53fb659c5076de1d65ccb0b397446227b71a42be9d1603d46168015c9e4b`
- Ollama version: `0.30.11`
- Temperature: 0.0
- Generated: 2026-08-18T17:12:04.813531+00:00

## Evidence boundary

The controlled run produced objective automated measurements for one local-model
configuration. Two unchanged DevOps and SRE role reports subsequently recorded
aggregate values and qualitative observations, but no populated assessor-by-item
ratings are retained in the inspected public evidence package. Those aggregates
are therefore archived rather than adopted as quantitative human findings; the
reports may support qualitative engineering hypotheses only. The run does not
establish results for Gemini, Anthropic, OpenAI-compatible cloud models, or
DeepSeek. Local Ollama has no metered API charge; electricity and hardware cost
were not measured.

## Incident benchmark

- Runs: 72 across 24 scenarios
- Schema-valid output rate: 100.0%
- Exact agreement with researcher-defined primary severity labels: 40.3%
- Gold-label boundary: labels were constructed by the researcher and were not independently adjudicated; agreement is not real-world diagnostic accuracy
- Macro F1: 0.383
- False positives: 0
- False negatives: 6
- Signature-format pass rate: 100.0%
- Signature-stability rate by scenario: 41.7%
- Expected-signature exact rate: 40.0%
- Latency p50 / p95: 9.933219 s / 14.53215 s
- Mean input / output tokens: 823.916667 / 136.222222

## RAG benchmark

- Generation runs: 72 (72 successful)
- Frozen relevant runbook present in the top four: 12/12 questions
- RAG latency p50 / p95: 10.070817 s / 35.652615 s
- No-RAG latency p50 / p95: 9.906291 s / 24.494734 s
- Human-rated correctness, grounding quality, and actionable safety: unresolved because assessor-by-item ratings are unavailable
- Traceability boundary: the no-RAG condition had no supplied source documents; this establishes lack of supplied-source traceability only, not factual incorrectness or a RAG-effectiveness result

## Practitioner role-report provenance - qualitative use only

- Retained records: two unchanged reports using separate DevOps and SRE role lenses
- Reported scope: the reports state that each role reviewed 72 incident responses and 72 RAG/no-RAG responses; populated assessor-by-item ratings are not retained for independent verification
- Authoritative public reports: `../../practitioner_confirmation/InfraGuard_DevOps_Assessment_Report.docx` and `../../practitioner_confirmation/InfraGuard_SRE_Assessment_Report.docx`
- Report SHA-256 values: `741b5446c8dffaabfeac20823aa7a4427a4a61c058b1b9e9c619000c641d6720` and `7c91dfd735a4a070ce4e6053c5addcfb70cec2d67002b199b43f22f21133efdb`
- Canonical role-package seeds: A1/DevOps `2026082405`; A2/SRE `2026082412`
- Quantitative-use decision: report means, rankings, agreement percentages, kappas, and RAG/no-RAG comparisons are excluded from primary findings because they cannot be recomputed from retained assessor-by-item records
- Permitted use: provenance-qualified qualitative engineering hypotheses only; no diagnostic-reliability, RAG-effectiveness, usability, or production-effectiveness conclusion

The SRE report's method table contains `2026081902`, while its opening record
and executive summary both state `2026082412`. The former is the seed found in
excluded historical assessment material. The preserved report remains
unchanged for hash integrity; `../../practitioner_confirmation/CORRECTION_NOTICE.md`
is authoritative for this field.

### Public item-level scoring limitation

The four public A/B assessor CSV files are uncompleted templates. Each contains
72 evidence rows and zero populated human score cells. The unchanged role
reports contain report-level aggregate statements and qualitative observations,
while original email provenance is researcher-reported as retained
confidentially outside the public repository. No completed item-level human
scoring file is present in the inspected public evidence directories. Therefore,
the report means, rankings, agreement percentages, kappas, and human RAG/no-RAG
comparisons cannot be independently recomputed and are not adopted as
quantitative findings. No item-level score should be inferred or reconstructed.

## Separate human SUS study

The separate System Usability Scale study received 11 consented submissions and
analysed 10 complete responses after excluding one incomplete response without
imputation. Its mean score was 79.25. This supports favourable perceived
usability within the evaluated group only; it does not establish population-level
usability, reduced workload, task performance, diagnostic correctness, or
production effectiveness.

## Retained evidence

- `incident_runs.jsonl`: prompts, raw outputs, parsed outputs, timings, and token counts.
- `rag_runs.jsonl`: RAG/no-RAG prompts, raw answers, sources, timings, and token counts.
- `retrieval.json`: frozen top-four retrieval results.
- `assessor_*_worksheet_A.csv` and `assessor_*_worksheet_B.csv`: retained blinded assessment templates.
- `assessor_*_key.csv`: protocol answer keys retained for traceability; their presence does not establish completed independent scoring.
- `../../practitioner_confirmation/InfraGuard_DevOps_Assessment_Report.docx` and `../../practitioner_confirmation/InfraGuard_SRE_Assessment_Report.docx`: unchanged role-specific reports containing aggregate statements and qualitative observations; quantitative aggregates are excluded from thesis findings.
- `../../practitioner_confirmation/manifest.json` and `../../practitioner_confirmation/CORRECTION_NOTICE.md`: authoritative public provenance classification and SRE seed correction.
- `HISTORICAL_NON_EVIDENTIAL_NOTICE.md`: exclusion record for the two preserved historical assessment binaries; neither file is admissible evidence for the defence/submission package.
