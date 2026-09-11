# Project figures

The editable sources in `mermaid/` and `../diagram_sources/` are source-controlled
references. Export them manually to PNG and insert the images into the refined
Word document. Existing PNGs in this directory are outputs and may be older
than their Mermaid sources; the figures embedded in the current authoritative
manuscript remain the submission versions.

Do not run generate.py for the architecture diagrams unless you also update that script: it is a legacy renderer and can overwrite PNGs with older wording and metrics.

## Manual workflow

1. Open the required .mmd file from figures/mermaid.
2. Paste it into Mermaid Live Editor: https://mermaid.live.
3. Check that no node is clipped and export a PNG at 3× scale with a light background.
4. Save it in this directory using the exact filename stated in the source comment and inventory.
5. In Word, use **Insert → Pictures → This Device**, centre the image, and size it to the page width without stretching it.
6. Use **References → Insert Caption** so Word controls figure numbering. Put the source immediately below the caption where required by the university format.
7. Update the List of Figures, save as PDF, and inspect the relevant pages at 100% zoom before submission.

The newer sources include `fig_4_4_runbook_retrieval.mmd`, which shows how 20
whole local Markdown runbooks are indexed and how the top four retrieved
documents condition a bounded response as explicitly untrusted context. This
retrieval evidence does not by itself establish answer correctness or
groundedness. `fig_5_3_practice_evaluation.mmd` documents a proposed five-case
practitioner usability workflow; it is a study-design figure, not a claim that
the workflow was completed or that results were obtained.

The current authoritative embedded figures are in
`../InfraGuard_AI_Masters_Project_FINAL_REVISED_AFTER_29_AUGUST_REVIEW.docx`.

For Figure 5.1, the current controlled local verification record is 180 tests
passed with 45 warnings and 89% line coverage across 1,655 statements with 190
missed. Six selected modules reached 100%; `store` reached 94% and
`orchestrator` reached 95%. These results do not establish live or production
validation.

See mermaid/README.md for the complete inventory, suggested captions, and exact output filenames.
