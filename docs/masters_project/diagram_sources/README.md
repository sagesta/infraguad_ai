# InfraGuard AI diagram sources

This folder contains editable Mermaid source for every architecture, workflow,
data-model, and chart figure in the current master's project. Each source file
starts with the thesis figure number, a stable figure ID, the exact caption, and
the PNG filename expected by the Word-document builder.

## How to render a clean replacement

1. Open [Mermaid Live](https://mermaid.live).
2. Open the required `.mmd` file from this folder and paste its complete content
   into the editor.
3. Export as SVG for review. For the thesis, export a PNG at 3x scale or at least
   2400 pixels wide, with a white background.
4. Save the PNG in `docs/masters_project/figures/` using the exact output name in
   the table below.
5. Run `node build.js InfraGuard_AI_Masters_Project_Human_Edited.docx` from
   `docs/masters_project/` to rebuild the document.

Do not rename the output PNGs unless the corresponding `image()` call in the
chapter source is also changed.

## Figure index

| Figure | Stable ID | Exact thesis caption | Mermaid source | Required output PNG |
|---|---|---|---|---|
| 3.1 | `FIG-3.1` | InfraGuard AI High-Level System Architecture | `figure_3_1_high_level_architecture.mmd` | `fig_3_1_architecture.png` |
| 3.2 | `FIG-3.2` | Single-Host Deployment Topology | `figure_3_2_single_host_topology.mmd` | `fig_3_2_topology.png` |
| 3.3 | `FIG-3.3` | Heartbeat Verdict Pipeline: Collect, Analyse, Store, Present | `figure_3_3_heartbeat_pipeline.mmd` | `fig_3_3_remediation_flow.png` |
| 3.4 | `FIG-3.4` | Use-Case Diagram: Operator and Agent | `figure_3_4_use_case.mmd` | `fig_3_4_usecase.png` |
| 3.5 | `FIG-3.5` | Sequence Diagram: One Heartbeat Cycle | `figure_3_5_heartbeat_sequence.mmd` | `fig_3_5_sequence.png` |
| 3.6 | `FIG-3.6` | Entity-Relationship Diagram of the Verdict and Acknowledgement Schema | `figure_3_6_verdict_erd.mmd` | `fig_3_6_erd.png` |
| 3.7 | `FIG-3.7` | State Machine of the LangGraph Reasoning Agent | `figure_3_7_langgraph_state_machine.mmd` | `fig_3_7_state_machine.png` |
| 4.1 | `FIG-4.1` | Folder Structure of the InfraGuard AI Reference Implementation | `figure_4_1_repository_structure.mmd` | `fig_4_1_folder.png` |
| 4.2 | `FIG-4.2` | Verdict-Memory Fingerprint and Acknowledgement Flow | `figure_4_2_verdict_memory_flow.mmd` | `fig_4_2_llm_classes.png` |
| 4.3 | `FIG-4.3` | Dashboard Overview Page | No Mermaid source; see `figure_4_3_screenshot_guide.md` | `fig_4_3_dashboard.png` |
| 5.1 | `FIG-5.1` | Selected Module Coverage from the Verification Run | `figure_5_1_module_coverage.mmd` | `fig_5_1_acceptance.png` |
| 5.2 | `FIG-5.2` | Visible Duplicate Warnings with and without an Acknowledgement | `figure_5_2_duplicate_warnings.mmd` | `fig_5_2_mttr.png` |

Figure 3.4 uses Mermaid's flowchart syntax to approximate a UML use-case
diagram. If formal stick-figure UML notation is required, use the existing
`docs/masters_project/figures/mermaid/fig_3_4_usecase.drawio` source instead.
