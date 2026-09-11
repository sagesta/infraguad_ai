# Historical figure-generation notice

`generate.py` is the figure generator for the 13 August 2026 manuscript snapshot. A full run would reproduce several superseded evaluation-status graphics, so full generation is blocked by default and this script is excluded from the submission package.

The current `fig_5_1_acceptance.png` and its Mermaid sources represent the
29 August post-review software-verification result: 180 tests passed with 45
warnings; overall line coverage was 89% across 1,655 statements with 190 missed.
Six selected modules reached 100%, while `store` reached 94% and `orchestrator`
reached 95%. These are controlled local test results, not production-validation
evidence.

The authoritative figures are the embedded figures in
`../InfraGuard_AI_Masters_Project_FINAL_REVISED_AFTER_29_AUGUST_REVIEW.docx`.
