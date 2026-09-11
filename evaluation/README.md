# InfraGuard AI Controlled Evaluation

This directory contains the frozen, reproducible benchmark defined in Appendix E of the revised master's manuscript.

## Evidence boundary

The harness records model outputs and computes only objective measures
automatically: schema validity, exact severity, confusion-matrix measures,
signature format/stability, retrieval success, latency, token counts, and
metered provider cost. Root-cause correctness, recommended-action quality,
evidence grounding, and RAG answer quality are reported separately from the
human practitioner assessment.

Two human operations practitioners completed separate exploratory DevOps and
SRE role-lens assessments. The authoritative public records are the unchanged
reports and hashes under `practitioner_confirmation/`. Original email
submissions and the confidential identity mapping are researcher-reported as
retained outside the public repository. The four public A/B assessor CSVs are
uncompleted templates, not completed human score sheets: each contains 72
evidence rows and zero populated score cells. No completed item-level human
scoring file is present in the inspected public evidence directories, so the
published aggregate scores and agreement statistics cannot be independently
recomputed from this public package alone.

The current local run uses Ollama. A local run has no metered API charge, but that does not mean the system has zero economic cost: electricity and hardware depreciation are outside this measurement.

## Frozen inputs

- `benchmark_v1.json` contains 24 incident fixtures, gold severities, reference answers, and 12 labelled RAG questions.
- The runner records the specification SHA-256, production prompt hash, model digest, Ollama version, temperature, timestamps, raw responses, parsed responses, latency, and token counts.
- Three repeated runs are mandatory. The runner refuses a different repeat count.
- Checkpoint JSONL files are append-only and resumable. Existing results are rejected if the model, temperature, or frozen specification differs.

## Execution

The benchmark is designed to run in the project's API image so it uses the same Python dependencies and production modules as InfraGuard AI. The model must already be present in the project's Ollama service.

Example from WSL:

```bash
docker run --rm \
  --network infraguad_ai_default \
  -v "$PWD:/workspace" \
  -v infraguad_ai_embedding_cache:/root/.cache \
  -w /tmp/benchmark \
  -e PYTHONPATH=/workspace \
  -e RUNBOOKS_DIR=/workspace/runbooks \
  <api-image> \
  python /workspace/evaluation/run_benchmark.py \
    --phase all \
    --model qwen2.5:3b \
    --base-url http://ollama:11434/v1 \
    --output-dir /workspace/evaluation/results/qwen2.5-3b-v1
```

Use `--phase retrieval`, `--phase incident`, `--phase rag`, or `--phase score` for individual/resumed stages.

## Generated evidence

- `manifest.json`: run configuration and model metadata.
- `incident_runs.jsonl`: complete incident prompts, raw outputs, parsed outputs, timings, and token usage.
- `rag_runs.jsonl`: complete RAG/no-RAG prompts, answers, retrieved sources, timings, and token usage.
- `retrieval.json`: top-four retrieval results for each labelled question.
- `summary.json` and `report.md`: objective results, exploratory aggregate human results, provenance classification, and limitations.
- `incident_objective_scores.csv`: per-run objective scores.
- `assessor_incident_worksheet_A.csv`, `assessor_incident_worksheet_B.csv`, `assessor_rag_worksheet_A.csv`, and `assessor_rag_worksheet_B.csv`: uncompleted assessment templates without model identity or gold labels; each has 72 rows and zero populated human score cells.
- `assessor_incident_key.csv` and `assessor_rag_key.csv`: held-back keys used only after initial independent scoring.
- `results/qwen2.5-3b-v1/HISTORICAL_NON_EVIDENTIAL_NOTICE.md`: exclusion record for the two preserved historical assessment binaries that are not admissible defence/submission evidence.

## Human evidence provenance

- A1/DevOps report: `practitioner_confirmation/InfraGuard_DevOps_Assessment_Report.docx`, SHA-256 `741b5446c8dffaabfeac20823aa7a4427a4a61c058b1b9e9c619000c641d6720`, canonical role-package seed `2026082405`.
- A2/SRE report: `practitioner_confirmation/InfraGuard_SRE_Assessment_Report.docx`, SHA-256 `7c91dfd735a4a070ce4e6053c5addcfb70cec2d67002b199b43f22f21133efdb`, canonical role-package seed `2026082412`.
- The SRE method-table value `2026081902` is a legacy transcription from excluded historical assessment material. `practitioner_confirmation/CORRECTION_NOTICE.md` is authoritative for that field while the source DOCX remains unchanged for hash integrity.

The two-assessor results remain exploratory and do not establish population-level
diagnostic reliability or production effectiveness. The absence of public
completed item-level human scoring is a provenance and reproducibility
limitation. Do not infer, reconstruct, or fabricate item-level values.
