# InfraGuard AI diagram sources

This folder contains editable Mermaid reference sources for the architecture,
workflow, data-model, and chart figures in the master's project. The embedded
figures in `InfraGuard_AI_Masters_Project_FINAL_REVISED_AFTER_29_AUGUST_REVIEW.docx`
are the current authoritative versions. Each source file should identify the
thesis figure number, caption, and corresponding PNG filename; the source file
itself remains editable reference material rather than submission evidence.

## How to render a clean replacement

1. Open [Mermaid Live](https://mermaid.live).
2. Open the required `.mmd` file from this folder and paste its complete content
   into the editor.
3. Export as SVG for review. For the thesis, export a PNG at 3x scale or at least
   2400 pixels wide, with a white background.
4. Save the PNG in `docs/masters_project/figures/` using the exact output name in
   the table below, then inspect the exported image independently.

Do not rebuild or overwrite the authoritative manuscript from the
historical JavaScript content tree. Its guarded builder is retained only for
traceability and does not represent the final reviewed manuscript.

Do not rename the output PNGs unless the corresponding `image()` call in the
chapter source is also changed.

## Figure index

| Figure | Stable ID | Exact thesis caption | Mermaid source | Required output PNG |
|---|---|---|---|---|
| 3.1 | `FIG-3.1` | High-Level Architecture of InfraGuard AI | `figure_3_1_high_level_architecture.mmd` | `fig_3_1_architecture.png` |
| 3.2 | `FIG-3.2` | Intended Single-VPS Topology for DevPlanner and InfraGuard AI | `figure_3_2_single_host_topology.mmd` | `fig_3_2_topology.png` |
| 3.3 | `FIG-3.3` | Heartbeat Pipeline and Remediation Boundary | `figure_3_3_heartbeat_pipeline.mmd` | `fig_3_3_remediation_flow.png` |
| 3.4 | `FIG-3.4` | InfraGuard AI Use-Case Model | `figure_3_4_use_case.mmd` | `fig_3_4_usecase.png` |
| 3.5 | `FIG-3.5` | Sequence of One Heartbeat Cycle | `figure_3_5_heartbeat_sequence.mmd` | `fig_3_5_sequence.png` |
| 3.6 | `FIG-3.6` | Verdict and Acknowledgement Data Model | `figure_3_6_verdict_erd.mmd` | `fig_3_6_erd.png` |
| 3.7 | `FIG-3.7` | LangGraph Agent State Machine | `figure_3_7_langgraph_state_machine.mmd` | `fig_3_7_state_machine.png` |
| 4.1 | `FIG-4.1` | Repository Layout of the Reference Implementation | `figure_4_1_repository_structure.mmd` | `fig_4_1_folder.png` |
| 4.2 | `FIG-4.2` | Verdict-Memory Fingerprint and Acknowledgement Flow | `figure_4_2_verdict_memory_flow.mmd` | `fig_4_2_llm_classes.png` |
| 4.3 | `FIG-4.3` | InfraGuard AI Operations Dashboard | No Mermaid source; see `figure_4_3_screenshot_guide.md` | `fig_4_3_dashboard.png` |
| 4.4 | `FIG-4.4` | Local Runbook Indexing and Retrieval Process | `../figures/mermaid/fig_4_4_runbook_retrieval.mmd` | `fig_4_4_runbook_retrieval.png` |
| 4.5 | `FIG-4.5` | Cloud-LLM Data Boundary and Local Retention Points | `figure_4_5_cloud_llm_data_boundary.mmd` | `fig_4_5_cloud_llm_data_boundary.png` |
| 5.1 | `FIG-5.1` | Selected-Module Coverage after Post-Review Verification on 29 August 2026 | `figure_5_1_module_coverage.mmd` | `fig_5_1_acceptance.png` |
| 5.2 | `FIG-5.2` | Deterministic 30-Cycle Illustration of Default-View Duplicate Presentation | `figure_5_2_duplicate_warnings.mmd` | `fig_5_2_mttr.png` |
| 5.3 | `FIG-5.3` | Proposed Five-Case Practitioner Usability Workflow | `../figures/mermaid/fig_5_3_practice_evaluation.mmd` | `fig_5_3_practice_evaluation.png` |

Figure 3.4 uses Mermaid's flowchart syntax to approximate a UML use-case
diagram. If formal stick-figure UML notation is required, use the existing
`docs/masters_project/figures/mermaid/fig_3_4_usecase.drawio` source instead.
