# Figure sources (Mermaid + draw.io)

Editable diagram sources for the project figures. Render each to a PNG and place it
in `docs/masters_project/figures/` under the **Render-to** filename — `build.js`
embeds whatever PNG is at that path, so no chapter edits are needed.

**Rendering:** paste a `.mmd` into [mermaid.live](https://mermaid.live) → export PNG at
3× scale for print quality. Open the `.drawio` file at [app.diagrams.net](https://app.diagrams.net)
→ File ▸ Export as ▸ PNG (300 DPI).

> The render-to PNG names keep their original (sometimes legacy) base names so
> `build.js` and the chapter `image()` calls work unchanged.

| Fig | Appears in | Source file | Render-to PNG |
|-----|------------|-------------|---------------|
| 3.1 Architecture | **Ch 3 · §3.3.4** High-Level Architecture | `fig_3_1_architecture.mmd` | `fig_3_1_architecture.png` |
| 3.2 Deployment Topology | **Ch 3 · §3.3.5** Deployment Topology | `fig_3_2_topology.mmd` | `fig_3_2_topology.png` |
| 3.3 Heartbeat Pipeline | **Ch 3 · §3.3.6** Heartbeat Verdict Pipeline | `fig_3_3_remediation_flow.mmd` | `fig_3_3_remediation_flow.png` |
| 3.4 Use-Case | **Ch 3 · §3.4.2** Use-Case Model | `fig_3_4_usecase.mmd` *or* `fig_3_4_usecase.drawio` | `fig_3_4_usecase.png` |
| 3.5 Sequence | **Ch 3 · §3.4.3** Sequence Diagram | `fig_3_5_sequence.mmd` | `fig_3_5_sequence.png` |
| 3.6 ERD | **Ch 3 · §3.4.4** Entity-Relationship Model | `fig_3_6_erd.mmd` | `fig_3_6_erd.png` |
| 3.7 State Machine | **Ch 3 · §3.4.6** State Machine (LangGraph) | `fig_3_7_state_machine.mmd` | `fig_3_7_state_machine.png` |
| 4.1 Folder Structure | **Ch 4 · §4.2.1** Repository Layout | `fig_4_1_folder.mmd` | `fig_4_1_folder.png` |
| 4.2 Verdict-Memory Flow | **Ch 4 · §4.2.5** The Verdict-Memory | `fig_4_2_llm_classes.mmd` | `fig_4_2_llm_classes.png` |
| 4.3 Dashboard | **Ch 4 · §4.2.11** The Dashboard | — *(real screenshot of the running dashboard)* | `fig_4_3_dashboard.png` |
| 5.1 Coverage by Module | **Ch 5 · §5.2.1** Coverage by Module | `fig_5_1_acceptance.mmd` *or* `generate.py` | `fig_5_1_acceptance.png` |
| 5.2 Duplicate-Verdict Reduction | **Ch 5 · §5.3** Evaluation of the Verdict-Memory | `fig_5_2_mttr.mmd` *or* `generate.py` | `fig_5_2_mttr.png` |
| 5.3 SUS Results | **Ch 5 · §5.4.2** Results | — *(`generate.py` template; fill from sessions)* | `fig_5_3_cost.png` |
| 5.4 Severity Distribution | **Ch 5 · §5.5** Evaluation of Objectives | — *(`generate.py` template; fill from run)* | `fig_5_4_calibration.png` |

**Two non-Mermaid figures:**
- **4.3 Dashboard** — take an actual screenshot of the running dashboard (most honest and best-looking); no diagram source.
- **5.3 / 5.4** — data charts that need your real usability scores and verdict counts; keep them in `../generate.py` and populate after the evaluation.
