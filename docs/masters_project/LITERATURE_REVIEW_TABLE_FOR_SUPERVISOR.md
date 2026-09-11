# HISTORICAL / SUPERSEDED DRAFT - Literature Review Table

> **Do not submit or cite this draft as current evidence.** It predates the verified 29 August manuscript, contains an explicit unresolved citation-verification note, and includes claims that were later narrowed or removed. The authoritative literature review and Table 2.1 are in `InfraGuard_AI_Masters_Project_FINAL_REVISED_AFTER_29_AUGUST_REVIEW.docx`. This file is retained only as revision history.

**Project:** InfraGuard AI: An LLM-Driven Observability and Incident-Triage Agent for Self-Hosted Cloud-Native Infrastructure
**Programme:** Professional Master of Information Technology (MIT) — Miva Open University Abuja, Nigeria

---

## Introduction to the Table

The table below provides a structured comparative review of thirteen recent and closely related studies spanning site reliability engineering, AIOps, LLM-based incident and root-cause analysis, log parsing, and the agentic and retrieval-augmentation techniques on which the present system is built. The studies were selected on the basis of (i) recency, with emphasis on 2020–2025 publications; (ii) publication venue credibility — peer-reviewed top-tier conferences and journals, with a small number of widely-cited industry-research works; and (iii) direct topical relevance to grounded, LLM-assisted operations.

Each row identifies the study, summarises its approach, lists the tools or models employed, captures its principal findings, identifies the limitations or gaps it leaves open, and explicitly states how the InfraGuard AI project addresses those gaps.

> **Note for the supervisor:** the citations below are to be finalised against source during the references pass; author lists and venues should be verified before final submission.

---

## Table 2.1 — Comparative Review of Thirteen Recent and Related Studies

| # | Study (Author, Year) | Approach / Methodology | Tools and Models Used | Key Findings | Identified Limitations / Gaps | How InfraGuard AI Addresses the Gap |
|---|---|---|---|---|---|---|
| 1 | Beyer, Jones, Petoff & Murphy (2016). "Site Reliability Engineering." *O'Reilly / Google.* | Foundational practitioner text codifying SRE practice: SLOs, error budgets, on-call, incident response. | Operational framework; no software artefact. | Establishes telemetry-driven operations and identifies repetitive manual interpretation ("toil") as the central scaling constraint. | Predates the LLM era; assumes a human performs the interpretation of telemetry into action. | Automates the first-pass interpretation of telemetry into structured verdicts, reducing the manual triage toil SRE identifies. |
| 2 | Notaro, Cardoso & Gerndt (2021). "A Survey of AIOps Methods for Failure Management." *ACM TIST.* | Systematic survey of AIOps techniques across the failure-management lifecycle. | Meta-analysis of supervised and statistical methods. | Maps the AIOps landscape; finds most methods are narrow models requiring heavy labelled data and producing numeric scores rather than explanations. | Pre-LLM; no grounded natural-language reasoning; surveyed methods rarely open or self-hostable. | Uses a general LLM for explainable, natural-language verdicts grounded in live telemetry, delivered as an open, self-hostable artefact. |
| 3 | He, Zhu, Zheng & Lyu (2017). "Drain: An Online Log Parsing Approach with Fixed Depth Tree." *IEEE ICWS.* | Streaming log parser abstracting raw log lines into templates by stripping variable tokens. | The Drain algorithm. | Enables stable grouping of semantically identical log events despite volatile parameters. | Parsing only; no reasoning and no operator-facing memory. | The verdict-memory applies the same volatile-token-normalisation principle so the same condition fingerprints stably across heartbeats. |
| 4 | Yao et al. (2023). "ReAct: Synergizing Reasoning and Acting in Language Models." *ICLR.* | Interleaved reasoning-and-acting prompting allowing an LLM to alternate reasoning with tool invocations. | GPT-3 / PaLM with external tool environments. | Significant accuracy gains on knowledge-intensive and decision-making tasks. | Domain-agnostic; no operations application or production evaluation. | Adopted in the LangChain multi-tool mode, where Gemini interleaves reasoning with calls to the Loki, Prometheus, and HTTP-probe tools. |
| 5 | Shinn et al. (2023). "Reflexion: Language Agents with Verbal Reinforcement Learning." *NeurIPS.* | Self-improving agent loop with verbal self-critique on failure. | GPT-4 with a reflection memory. | Substantial gains over single-shot baselines on multi-step tasks. | Demonstrated on toy code and QA tasks; no operations integration. | Informs the agent's bounded structured-retry posture on malformed output, with an explicit iteration cap. |
| 6 | Lewis et al. (2020). "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks." *NeurIPS.* | RAG as a hybrid parametric–non-parametric architecture with a dense retriever feeding a generator. | BART generator with a DPR retriever. | Establishes RAG as the canonical grounding mechanism for generative output. | Foundational only; static corpus; no operations specialisation. | Applied to a dynamic, organisation-specific runbook corpus in ChromaDB surfaced through the runbook assistant with citations. |
| 7 | Ahmed et al. (2023). "Recommending Root-Cause and Mitigation Steps for Cloud Incidents using LLMs." *IEEE/ACM ICSE.* | Prompts/fine-tunes LLMs to recommend root cause and mitigation from production incidents. | GPT-3.5 / GPT-4 on enterprise incident records. | LLMs produce useful root-cause and mitigation recommendations; positive human evaluation. | Proprietary hyperscale cloud; not self-hostable; no operator memory; no open implementation. | Brings grounded root-cause and recommended-action verdicts to a self-hosted, open reference system with operator acknowledgement memory. |
| 8 | Jin et al. (2023). "Assess and Summarize: Improve Outage Understanding with LLMs." *ACM ESEC/FSE.* | LLM assessment and summarisation of ongoing outages. | GPT-family models on outage records. | Improves on-call comprehension speed. | Post-hoc summarisation; proprietary; no live reasoning loop. | Produces live, structured verdicts on a continuous heartbeat and persists them for history and memory. |
| 9 | Chen et al. (2024). "Automatic Root Cause Analysis via LLMs for Cloud Incidents (RCACopilot)." *ACM EuroSys.* | An LLM agent orchestrating diagnostic collectors for root-cause analysis. | LLM agent with tool-augmented diagnostic handlers. | Improves root-cause coverage and accuracy in production. | Hyperscale; heavyweight; not bounded for small single-host estates. | A deliberately bounded, single-host-scale triage agent grounded only in present telemetry. |
| 10 | Roy et al. (2024). "Exploring LLM-based Agents for Root Cause Analysis." *ACM FSE (Industry).* | Investigates autonomous LLM agents for root-cause analysis and the grounding choices that make them effective. | Tool-augmented LLM agents on incident datasets. | Confirms agentic LLMs can perform credible root-cause analysis given the right tools and grounding. | Cloud-internal; no self-hosted, human-in-the-loop, or memory-equipped variant. | Contributes the self-hosted, human-in-the-loop, memory-equipped variant with operator-approved threat response. |
| 11 | Yang et al. (2024). "SWE-agent: Agent–Computer Interfaces Enable Automated Software Engineering." *NeurIPS.* | Designs an agent–computer interface for an LLM to navigate, edit, and test code. | GPT-4 with a constrained tool interface. | Careful interface and tool design substantially improves task-resolution rate. | Code-editing tasks rather than operations; no telemetry grounding. | Borrows the interface principle to design a small, well-scoped telemetry tool surface (Loki, Prometheus, HTTP probe). |
| 12 | Hou et al. (2024). "Large Language Models for Software Engineering: A Systematic Literature Review." *ACM TOSEM.* | Systematic review of several hundred primary studies on LLM applications across the software lifecycle. | Meta-analysis. | Code generation and bug fixing are the most-studied activities; LLM-for-operations is strikingly under-represented. | Confirms rather than fills the gap; no implementation. | Directly addresses the under-represented LLM-for-operations category with a reproducible open-source implementation and explicit hallucination-bounding. |
| 13 | Guo et al. (2024). "OWL: A Large Language Model for IT Operations." *ICLR.* | Develops a domain-specialised LLM and benchmark for IT-operations question answering. | Domain-tuned LLM; IT-ops benchmark. | Domain specialisation improves operations question answering. | Model-centric; no end-to-end agent or live telemetry; bespoke model raises cost and complexity. | Pairs a general low-cost model (Gemini 2.5 Flash) with strict grounding and RAG instead of a bespoke model. |

---

## Synthesis of the Reviewed Studies

**First**, the capability question is largely settled: recent work (entries 7–10) demonstrates that LLMs, suitably grounded and tool-augmented, can perform credible root-cause analysis and produce useful operational recommendations. The open questions are no longer whether an LLM can reason about operations, but how to do so safely, cheaply, and reproducibly outside a hyperscale environment.

**Second**, almost all of the operations-specific work (entries 7–10) is conducted inside large proprietary clouds and is neither open nor deployable by a small team — the accessibility and sovereignty gap that the self-hosted, open-source design of InfraGuard AI addresses.

**Third**, the foundational agentic and retrieval techniques (entries 4–6, 11) are individually well-validated but have not been composed specifically for grounded, bounded operations triage. InfraGuard AI composes ReAct-style tool use, RAG grounding, and a bounded state machine.

**Fourth**, the systematic reviews (entries 2, 12) confirm that the LLM-for-operations intersection remains under-represented relative to LLM-for-code, justifying the present work as a research contribution.

**Fifth**, none of the reviewed systems equips its triage loop with an operator-facing, self-invalidating memory: every one of them, run continuously, would re-emit verdicts for conditions a human had already accepted. The content-plus-ruleset verdict-memory introduced in this work is, to the best of the author's knowledge, a novel treatment of statelessness in an LLM operations agent.

---

*This table is reproduced from Section 2.2.1 of the full project report.*
