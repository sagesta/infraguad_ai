# InfraGuard AI Practitioner Role-Report Provenance

This folder preserves the two unchanged role-specific reports supplied for the
exploratory practitioner-confirmation stage:

- `InfraGuard_DevOps_Assessment_Report.docx`
- `InfraGuard_SRE_Assessment_Report.docx`

## Evidence boundary

The reports state that two human operations practitioners reviewed the frozen
controlled benchmark: A1 using a DevOps role lens and A2 using an SRE role lens.
They contain aggregate values and qualitative observations, but the populated
assessor-by-item ratings required to reproduce those values are not retained in
the inspected public evidence package. The report means, rankings, agreement
percentages, kappas, and RAG/no-RAG comparisons are therefore archived and
excluded from quantitative thesis findings. The reports may support
provenance-qualified qualitative engineering hypotheses only; they do not
establish diagnostic reliability, RAG effectiveness, production effectiveness,
or generalisable findings.

The separate System Usability Scale (SUS) study is not contained in this folder.
That study received 11 consented submissions and analysed 10 complete responses.
Its findings are descriptive and do not establish population-level usability,
reduced workload, task performance, diagnostic correctness, or production
effectiveness.

The researcher reports that the original email submissions, full assessor
names, and confidential assessor identity mapping are retained outside the
public repository for supervisor verification. Personal email addresses are
not stored here. The A-series assessor codes are distinct from the P-series
participant codes used for the separate SUS study.

## Integrity record

| File | Role | Assessment date stated in report | Canonical role-package seed | SHA-256 |
|---|---|---|---:|---|
| `InfraGuard_DevOps_Assessment_Report.docx` | DevOps / A1 | 24 August 2026 | `2026082405` | `741b5446c8dffaabfeac20823aa7a4427a4a61c058b1b9e9c619000c641d6720` |
| `InfraGuard_SRE_Assessment_Report.docx` | SRE / A2 | 24 August 2026 | `2026082412` | `7c91dfd735a4a070ce4e6053c5addcfb70cec2d67002b199b43f22f21133efdb` |

The source reports are preserved unchanged so their hashes remain verifiable.
The SRE report states `2026082412` in both its opening record and executive
summary. Its method table contains `2026081902`, which is the seed found in the
excluded historical assessment material rather than the human SRE role package.
The authoritative correction is therefore `2026082412`. See
`CORRECTION_NOTICE.md` for the exact field-level correction and evidence basis.

## Public item-level scoring limitation

The public files `assessor_incident_worksheet_A.csv`,
`assessor_incident_worksheet_B.csv`, `assessor_rag_worksheet_A.csv`, and
`assessor_rag_worksheet_B.csv` under `evaluation/results/qwen2.5-3b-v1/` are
uncompleted assessment templates. All 72 rows are present in each file, but the
human score columns contain no populated values. They must not be presented as
completed human score sheets.

The unchanged DevOps and SRE reports preserve report-level aggregate statements
and qualitative observations. Original email submissions and the confidential
identity mapping are researcher-reported as retained outside the public
repository. No completed item-level human scoring file is present in the
inspected public evidence directories. Consequently, the report means,
rankings, agreement percentages, kappas, and human RAG/no-RAG comparisons cannot
be independently recomputed and are excluded from quantitative findings. This
is a provenance and reproducibility limitation; it must not be repaired by
reconstructing or fabricating item-level scores.

## Defence-package exclusion

The two files whose names begin
`InfraGuard_AI_AI_Simulated_DevOps_SRE_Assessment` in
`evaluation/results/qwen2.5-3b-v1/` are preserved only as historical development
artefacts. They are non-evidential, are not the source of the human practitioner
claims, and are explicitly excluded from the defence/submission package. See
`../results/qwen2.5-3b-v1/HISTORICAL_NON_EVIDENTIAL_NOTICE.md`.
