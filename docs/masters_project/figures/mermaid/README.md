# Canonical editable figure sources

These Mermaid files describe the current implementation: local Markdown runbooks, local ONNX embeddings, Gemini/Anthropic/OpenAI or optional Ollama, the shared DevPlanner VPS, Cloudflare Tunnel, Grafana Alloy, Loki, Prometheus, CrowdSec, and the actual human-approval boundary.

The PNG files one directory above are outputs, not source files. Regenerate a PNG whenever its .mmd source changes.

## Export each diagram

1. Open https://mermaid.live and paste the full contents of one .mmd file.
2. Resolve any parser warning before export.
3. Use a light theme and export PNG at 3× scale. Aim for at least 1800 pixels on the long edge.
4. Save it in docs/masters_project/figures using the exact PNG name below.
5. Open the PNG and check small labels before inserting it into Word.

Figures 3.1 and 3.2 contain more components than the others. If their labels become too small on a portrait page, place only that figure on a landscape page and return to portrait orientation afterwards.

## Figure inventory

| Figure | Source | Output PNG | Suggested caption |
|---|---|---|---|
| 3.1 | fig_3_1_architecture.mmd | fig_3_1_architecture.png | High-Level Architecture of InfraGuard AI |
| 3.2 | fig_3_2_topology.mmd | fig_3_2_topology.png | Deployed Single-VPS Topology for DevPlanner and InfraGuard AI |
| 3.3 | fig_3_3_remediation_flow.mmd | fig_3_3_remediation_flow.png | Heartbeat Pipeline and Remediation Boundary |
| 3.4 | fig_3_4_usecase.mmd | fig_3_4_usecase.png | InfraGuard AI Use-Case Model |
| 3.5 | fig_3_5_sequence.mmd | fig_3_5_sequence.png | Sequence of One Heartbeat Cycle |
| 3.6 | fig_3_6_erd.mmd | fig_3_6_erd.png | Verdict and Acknowledgement Data Model |
| 3.7 | fig_3_7_state_machine.mmd | fig_3_7_state_machine.png | LangGraph Agent State Machine |
| 4.1 | fig_4_1_folder.mmd | fig_4_1_folder.png | Repository Layout of the Reference Implementation |
| 4.2 | fig_4_2_llm_classes.mmd | fig_4_2_llm_classes.png | Verdict-Memory Fingerprint and Acknowledgement Flow |
| 4.3 | Running dashboard screenshot | fig_4_3_dashboard.png | InfraGuard AI Operations Dashboard |
| 4.4 | fig_4_4_runbook_retrieval.mmd | fig_4_4_runbook_retrieval.png | Local Runbook Indexing and Retrieval Process |
| 5.1 | fig_5_1_acceptance.mmd | fig_5_1_acceptance.png | Selected Module Coverage from the Verification Run |
| 5.2 | fig_5_2_mttr.mmd | fig_5_2_mttr.png | Visible Duplicate Warnings With and Without Acknowledgement |
| 5.3 | fig_5_3_practice_evaluation.mmd | fig_5_3_practice_evaluation.png | Five-Case Practice Evaluation Workflow |

Figure 4.3 must be a real screenshot from the running application. Crop browser chrome if it distracts from the interface, but do not edit status values or fabricate activity.

Figures 4.4 and 5.3 are new. Add them only if the surrounding text explains them and the List of Figures is updated. Figure 5.3 is a study-design figure, not a results chart.

## Insert into the refined Word document

1. Put the cursor after the paragraph that first refers to the figure.
2. Insert the PNG as an inline image and centre it.
3. Keep the aspect ratio locked. Use a width of roughly 15 to 16 centimetres for a full-width diagram.
4. Select **References → Insert Caption**, choose the Figure label, and use the suggested caption.
5. Add Source: Researcher's design (2026). on the next centred line if the university template requires figure sources.
6. Use Word cross-references in the body rather than typing figure numbers by hand.
7. Update the List of Figures and inspect the exported PDF for clipped labels, split captions, and figures stranded on a different page from their introduction.

## Accuracy notes

- InfraGuard recommends remediation for normal incidents; it does not run service restart, rollback, cleanup, scaling, database, or configuration commands.
- The only application-exposed corrective action is an operator-approved CrowdSec IP ban. Without CrowdSec configuration it is a dry run.
- Mark known affects how matching low-risk verdicts are displayed. It does not skip later model calls or stop verdict storage.
- Runbook retrieval uses the top four whole Markdown documents and returns source titles. Commands remain for the operator to review and execute.
- Do not add or refresh result charts unless the underlying dataset, protocol, configuration, and analysis are retained. Keep the frozen v1 model benchmark separate from the later source hardening, and describe the SUS result as descriptive perceived usability only.

The companion fig_3_4_usecase.drawio is retained as an optional UML-style alternative. The Mermaid source is the maintained version for the current architecture.
