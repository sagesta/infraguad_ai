# InfraGuard AI — Documentation Realignment & Enhancement Plan

> **Historical implementation plan — superseded on 27 August 2026.** Counts,
> coverage, pending-study statements, provider choices, and proposed actions in
> this file record an earlier stage. They are not current evidence and this file
> must be excluded from the defence/submission package. The authoritative status
> is recorded in `InfraGuard_AI_Final_Supervisor_Compliance_Review.md` and
> `InfraGuard_AI_Supervisor_Requirements_Final_Matrix.md`.

**Purpose.** (1) Realign the master's project documentation so it describes the system that actually exists in this repository, removing every "InfraGuard Pro" reference and every fabricated "measured" claim; (2) add one genuine, well-scoped enhancement — a **stateful verdict-memory** that fixes the agent's statelessness — and document it truthfully once built. The result must be defensible at viva: every claim points at code you can open and run.

**Status:** COMPLETE (pending student finalisation of citations and usability administration).
- ✅ All phases executed. Memory feature built + tested (52 tests, 55% coverage). All six chapters, front matter, references, appendices, figure generator, build script, and supervisor table realigned to InfraGuard AI. Zero "InfraGuard Pro" and zero fabricated metrics remain across the doc set. All JS and Python files syntax-clean.
- ⏳ Student to finalise before submission: (1) verify Chapter 2 / references citations against source; (2) administer the usability study (Appendix D) and populate Section 5.4.2 + Figures 5.3/5.4; (3) run `npm install && node build.js` and `python figures/generate.py` to regenerate the docx and PNGs; (4) insert name/matriculation number on the cover.

---

### Original execution log
- ✅ Phase 5 (memory feature) built + tested — 52 tests pass (was 33); end-to-end ack flow verified through the live app.
- ✅ Phase 6 coverage measured: **55% overall** (memory core 100%, orchestrator 94%, store 94%, API 76%, middleware ~100%; low modules are external-IO adapters needing live services). pytest-cov added to requirements.
- ✅ Phase 1 (front matter, `00-prelim.js`): new title, abstract, keywords, acknowledgement, figure/table lists — zero "Pro" remaining, syntax clean.
- ✅ Phase 2 (Ch1 Introduction, `01-intro.js`): rewritten to observability/triage; new aim + 5 objectives incl. the memory contribution; remediation/multi-provider/fleet framed as future work. Syntax clean.
- ✅ Phase 3 (Ch2 Literature Review, `02-litreview.js`): re-pointed to AIOps / observability / LLM-for-ops; 13-study comparative table re-curated (SRE, AIOps survey, Drain, ReAct, Reflexion, RAG, LLM-RCA works); comparators now Datadog/New Relic/PagerDuty/k8sgpt; real tech stack + standards + 7 gaps. Syntax clean. (References to be finalised in Phase 10.)
- ⏳ Remaining: Phase 4 (Ch3 methodology/design — FR/NFR, architecture, ERD with acks table), Phases 7–12 (implementation, testing, conclusion, refs/appendices, figures, rebuild).

---

## 0. The core problem (recap)

The write-up describes **"InfraGuard Pro"** — an autonomous SARIF→patch→pull-request *remediation* platform (6 LLM providers, satellite fleet, PostgreSQL, SvelteKit, hash-chained audit). The repository is **"InfraGuard AI"** — a Loki/Prometheus/Docker *observability + triage* agent (one LLM provider, SQLite, static HTML dashboard, plain audit log). ~80% of Chapter 4 and most of Chapter 5 describe code that does not exist, including results presented as "measured" (400 tests, 84.3% coverage, 247 self-scan findings, MTTR 4m11s).

**Strategy:** rewrite the docs to match reality. Salvage system-agnostic content (methodology framing, regional significance, requirements *method*); delete-and-rewrite the fictional parts (abstract, Ch4, Ch5, benchmark). The ambitious remediation vision becomes **future work**. Separately, **build** the memory enhancement and document it as real (never before it exists).

---

## 1. Locked decisions

| # | Decision | Resolution |
|---|----------|-----------|
| D1 | Canonical name | **"InfraGuard AI"** everywhere. |
| D2 | Proposal artifacts (`*_Proposal.*`, defence deck, `proposal_data.json`, `build_proposal_*`) | **Leave untouched.** Already submitted; treated as a historical record, out of scope for this work. No rewriting, no rename. |
| D3 | Coverage figure | **Measure real coverage** with `coverage.py`/`pytest-cov` and report the true number. |
| D4 | Thesis title | **"InfraGuard AI: An LLM-Driven Observability and Incident-Triage Agent for Self-Hosted Cloud-Native Infrastructure."** (No subtitle.) |

> Because D2 puts the proposal out of scope, the earlier "supervisor sign-off on scope change" is reduced to a light **confirm-the-realigned-objectives** step with the supervisor (who is already reviewing chapters), not a blocking gate.

---

## 2. New identity

**Name:** InfraGuard AI
**Title:** *InfraGuard AI: An LLM-Driven Observability and Incident-Triage Agent for Self-Hosted Cloud-Native Infrastructure.*

**Aim:** To design, develop, and evaluate a self-hosted, LLM-driven observability and incident-triage agent that continuously reasons over live infrastructure telemetry to produce grounded, hallucination-bounded SRE verdicts, detect active threats, answer runbook questions, and **remember what has already been triaged** — operable by small teams in resource-constrained environments.

**Specific objectives (the student's own; the supervisor's Obj 1–4 are the deliverable phases — elicitation, design, implementation, evaluation — into which these map):**
1. **(Elicitation)** Elicit and document requirements via practitioner interviews + MoSCoW, yielding functional and non-functional specifications.
2. **(Design)** Design the system — architecture, UML, ERD, UI mockups — covering telemetry collection → LangGraph reasoning → verdict persistence → dashboard.
3. **(Implementation — core)** Implement: (a) multi-source telemetry (Loki, Prometheus, HTTP probes, optional Docker); (b) a LangGraph agent producing hallucination-bounded JSON verdicts via Vertex AI Gemini (direct + LangChain modes); (c) RAG runbook retrieval (Notion → ChromaDB); (d) deterministic threat detection with human-approved CrowdSec response; (e) a secure, self-hostable dashboard.
4. **(Implementation — contribution)** Design and implement a **stateful verdict-memory** that suppresses already-triaged conditions using a **content-plus-ruleset fingerprint** with automatic invalidation, reducing redundant re-analysis and alert noise — addressing the known statelessness limitation of LLM triage loops.
5. **(Evaluation)** Evaluate: a `pytest` suite with documented test cases + measured coverage, and usability testing with 3–5 practitioners (SUS + structured feedback), assessed against the objectives.

> Objective 4 is the novel angle and the strongest viva material — it identifies a real limitation (stateless re-triage) and solves it with disciplined cache-invalidation semantics.

---

## 3. The memory enhancement — feature spec

**Problem it solves.** Every heartbeat (120s), the agent re-reasons over telemetry with zero memory of prior verdicts: persistent conditions get re-analysed and re-emitted ~30×/hour, the operator can't dismiss a known-benign warning, and many of the ~720 LLM calls/day are redundant.

**Design (the disciplined part).** A dismissal must **not** key on "we looked at this." It keys on a fingerprint that self-invalidates:
```
fingerprint = sha256( signature + PROMPT_VERSION + MODEL_NAME )
```
- `signature` = a canonical label for *what* triggered the verdict (e.g. `prom:disk-low:/`, `loki:error-rate:devplanner-api`, `docker:unhealthy:devplanner-api`) — **not** raw telemetry. Emitted by the LLM from a small controlled vocabulary (temp already 0.2), with a deterministic fallback.
- `PROMPT_VERSION + MODEL_NAME` = the "ruleset version." Change the prompt or upgrade the model → all fingerprints change → everything re-evaluates under new rules.

**Build in two pieces (ship A first):**
- **(A) Acknowledge + suppress (must-have, no AI change):** `acknowledgements(fingerprint, note, acked_by, created_at, expires_at)` table; a "mark as known / non-issue" button in the dashboard; acknowledged conditions are collapsed/greyed in history & threat panels.
- **(B) Prompt memory (stretch):** the orchestrator injects a compact "already triaged — treat as known unless it materially changes" block into the heartbeat prompt, so the LLM itself stops re-flagging accepted conditions.

**Invalidation & safety:**
- New error category or a metric crossing into a worse band → different `signature` → new fingerprint → **auto-reopens**.
- TTL backstop: acks expire after `ACK_TTL_DAYS` (default 30) so nothing is suppressed forever (covers the "new abuse on old code" case).
- **Hard rule:** only `ok`/`warning` may be suppressed; `high`/`critical` always surface, acknowledged or not.

**Code touchpoints (small, fits existing structure):**
- `api/store.py` — add `signature`/`fingerprint` columns to verdicts; new `acknowledgements` table + helpers; reuse retention pattern.
- `agent/llm/prompts.py` / `vertex.py` / `langchain_agent.py` — add `signature` to the JSON schema; `PROMPT_VERSION` constant.
- `agent/orchestrator.py` — compute fingerprint; (B) fetch active acks and add the known-issues block.
- `api/main.py` — `POST /api/verdicts/ack`, `GET /api/acks`; suppression flags in `/status` & `/alerts`.
- `dashboard/index.html` — "mark as known" button; suppressed styling; never on high/critical.
- `tests/` — fingerprint stability, invalidation on signature/PROMPT_VERSION change, critical-never-suppressed, ack endpoint auth.

---

## 4. Guiding principles

1. **Truth-to-code.** Every claim points at a real file/endpoint/test. The memory feature is documented as "implemented" **only after it is built and tested** — until then it's future work.
2. **Remove "Pro" everywhere** (87 occurrences across 16 files — Section 7).
3. **No fabricated metrics.** Delete 400-tests/84.3%/247-findings/MTTR/150-benchmark; replace with real measurements only.
4. **Rename vs delete-and-rewrite:** salvage in place where content survives; delete-and-rewrite the fictional chapters (abstract, Ch4, Ch5).
5. **The remediation vision = future work**, kept honestly on record (Ch6).

---

## 5. Two work-streams

- **Stream A — Realignment:** rewrite all documentation to the real system (the bulk of the effort).
- **Stream B — Enhancement:** build + test the memory feature, then document it as real. B's code lands before B's documentation.

They interleave: do A's identity/intro/design first, build B in the middle (so Ch4/Ch5 can describe it truthfully), finish A's chapters last.

---

## 6. Phase-by-phase plan

### Phase 0 — Confirm objectives with supervisor *(light, non-blocking)*
Share the realigned 5 objectives (Section 2). Proposal left untouched (D2). **Exit:** objectives acknowledged.

### Phase 1 — Identity & front matter (`00-prelim.js`)
New title (D4); **full abstract rewrite** (observability, LLM triage, RAG runbooks, threat response, **memory**; honest results sentence — real tests + measured coverage + usability study); acknowledgement (drop "InfraGuard Pro stands", Traceway/Trivy/Semgrep); keywords (AIOps, observability, LLM agents, RAG, SRE, threat detection, stateful memory, self-hosting); update TOC + List of Figures/Tables; fix Ch5 title drift.

### Phase 2 — Chapter 1 Introduction (`01-intro.js`)
Re-anchor background on the observability problem (telemetry volume, slow manual root-cause, alert fatigue, ungrounded-"AI SRE" risk, **stateless re-triage**); rewrite problem statement; swap in the 5 objectives; rewrite scope (in: telemetry/verdicts/RAG/threats/dashboard/**memory**; out/future: autonomous patching, Git PRs, multi-provider LLM, satellites, SARIF); keep regional + significance framing.

### Phase 3 — Chapter 2 Literature Review (`02-litreview.js`) *(heaviest re-point: 60 themed terms)*
Conceptual review → AIOps, observability, LLM agents for ops, RAG grounding, agentic SRE, **alert fatigue / alert deduplication / event correlation / stateful agent memory** (motivates Objective 4). Existing systems → Datadog Bits AI, New Relic AI, Honeycomb, Grafana/Loki, PagerDuty AIOps, k8sgpt, Robusta, Elastic AI Assistant. Rebuild Tables 2.1 (15 studies), 2.2 (capability comparison vs those tools), 2.3 (standards). Gap analysis → "grounded, self-hosted, bounded-scope AI SRE **with self-invalidating memory** for small teams."

### Phase 4 — Chapter 3 Methodology & Design (`03-methodology.js`)
Keep Agile + design-science framing (trim the benchmark deliverable). Rewrite **Table 3.1 FRs** (telemetry collection, verdict generation, severity, notify, RAG index/query, threat detect, CrowdSec apply, audit, dashboard, retention, auth — **plus** acknowledge-verdict and memory-suppression). Rewrite **Table 3.2 NFRs** (heartbeat cost, hallucination bounding, security, self-hosting, responsiveness, retention, coverage). Actors/use-cases (add **UC: acknowledge a verdict as known**). Architecture (delete satellites/control-plane; real agent+API+SQLite+Chroma+Vertex+dashboard+ntfy+CrowdSec+Loki/Prom). **DB design**: real `verdicts` table (now with `signature`/`fingerprint`) + new `acknowledgements` table + ChromaDB + `audit.log`; honest ERD. Update all figure callouts.

### Phase 5 — Build the memory feature (Stream B) *(code, before documenting it)*
Implement Section 3 (pieces A then B), add tests, run the suite green. **Exit:** memory works and is tested — now it may be documented as real.

### Phase 6 — Measure real coverage (D3)
`pip install pytest-cov` if needed; run `python -m pytest --cov=agent --cov=api --cov-report=term-missing`; record the true overall + per-module numbers for Ch5.

### Phase 7 — Chapter 4 Implementation (`04-implementation.js`) *(delete-and-rewrite)*
Keep real dev env (drop GPU/Ollama). **Table 4.1** → actual repo tree. Document real modules (orchestrator graph collect→analyze→decide→notify; the two LLM paths; prompt assembly + hallucination bounding; RAG Notion→Chroma; threat detection + CrowdSec; FastAPI + middleware incl. **enforced** rate limit; SQLite + retention; dashboard with chips/stale-banner/threat-block/escaping; **the memory feature**). **Table 4.2 endpoints** → real set incl. `/api/config`, `POST /api/threats/apply`, `POST /api/runbooks/index`, **`POST /api/verdicts/ack`**, `GET /api/acks`. Real security/perf (sessions, `hmac.compare_digest`, rate limits, CSP, escaping, `asyncio.to_thread`, retention). **Delete** hash-chain/secret-redaction/MTTR/satellites. Real challenges (LLM JSON conformance, prompt-scope bounding, **signature stability for the fingerprint**, Docker socket trade-off, Loki windows). Replace Fig 4.2; add real Fig 4.3 dashboard screenshot.

### Phase 8 — Chapter 5 Testing & Evaluation (`05-testing.js`) *(delete-and-rewrite; the marks)*
Real tiers: unit (pytest+respx), integration (TestClient through middleware), **memory tests** (fingerprint stability/invalidation/critical-never-suppressed), usability (3–5 users). Real **test-case table** (id, scenario, expected, result). Real coverage from Phase 6. **Usability study** (Section 10) — report success, SUS, findings, improvements made (incl. the ack/suppression UX). Objective matrix (Table 5.4): all 5 → Achieved with evidence. **Delete** 150-finding benchmark + projected Figs 5.1–5.4 + fabricated coverage; replace with real charts (coverage by module; SUS; optional real heartbeat latency; **before/after duplicate-verdict count showing the memory feature's noise reduction**).

### Phase 9 — Chapter 6 Conclusion (`06-conclusion.js`)
Rewrite to the real contribution (grounded, self-hosted AI SRE with self-invalidating memory). Future work = the remediation roadmap (multi-provider abstraction, SARIF ingest, autonomous patching + policy engine + Git PRs, satellites, PostgreSQL, hash-chained audit) + deeper memory (deterministic signatures, cross-incident correlation). Keep regional/professional/programme contributions.

### Phase 10 — References & Appendices (`07-references.js`, `08-appendices.js`)
References: add AIOps/observability/LLM-agent/RAG/alert-fatigue citations; remove remediation-only ones no longer cited *(read `07-references.js` first for the exact list)*. Appendix A → real endpoints; B → real code excerpts (orchestrator, prompt assembly, **fingerprint/ack**); C → real `docker-compose.yml`; D → delete dataset, replace with the **usability instrument** (SUS + task script).

### Phase 11 — Figures (`figures/generate.py` + regenerate)
Per Section 8 mapping; update `generate.py`, regenerate PNGs; replace `fig_4_3_dashboard.png` with a real screenshot (showing the ack button).

### Phase 12 — Tables, rebuild, verify
Rewrite all flagged tables. Update `build.js` output → `InfraGuard_AI_Masters_Project.docx`; delete old `InfraGuard_Pro_Masters_Project.docx`; rebuild. Rewrite `InfraGuard_Pro_Presentation.html` → renamed real-system deck. Rewrite `LITERATURE_REVIEW_TABLE_FOR_SUPERVISOR.md`. Confirm repo docs (README/CONTEXT/system_architecture/prd — already realigned) say "InfraGuard AI" consistently. **Final grep:** zero "Pro"; zero remediation/SARIF/satellite/patch/PostgreSQL/SvelteKit except where labelled future work. Proofread; verify every figure/table/endpoint against code.

---

## 7. File-by-file change map

| File | "Pro" hits | Action |
|------|:---:|--------|
| `content/00-prelim.js` | 8 | Rewrite title, abstract, acknowledgement, keywords, TOC/lists |
| `content/01-intro.js` | 3 | Rewrite background, problem, objectives (5), scope, significance |
| `content/02-litreview.js` | 22 | Re-point review, systems, tables, gap analysis (+ memory literature) |
| `content/03-methodology.js` | 5 | Rewrite FR/NFR/use-cases/architecture/DB design (+ acks table) |
| `content/04-implementation.js` | 2 | **Delete-and-rewrite** to real modules/endpoints (+ memory) |
| `content/05-testing.js` | 5 | **Delete-and-rewrite**: real tests + coverage + usability + memory results |
| `content/06-conclusion.js` | 1 | Rewrite; remediation vision + deeper memory → future work |
| `content/07-references.js` | 0 | Review; add/remove citations |
| `content/08-appendices.js` | 1 | Real API/code/compose; replace Appendix D with usability instrument |
| `build.js` | 3 | Output filename + title strings |
| `helpers.js` | 0 | Verify only |
| `figures/generate.py` | 4 | Rewrite diagram defs; regenerate PNGs |
| `InfraGuard_Pro_Presentation.html` | 6 | Rewrite/rename to real system |
| `LITERATURE_REVIEW_TABLE_FOR_SUPERVISOR.md` | 5 | Rewrite table |
| `InfraGuard_Pro_Masters_Project.docx` | (binary) | Delete + regenerate as `InfraGuard_AI_*` |
| `build_proposal_docx.js` / `build_proposal_pdf.py` / `build_proposal_slides.mjs` | 10 | **Leave untouched (D2)** |
| `proposal_data.json` | 12 | **Leave untouched (D2)** |
| `*_Project_Proposal.docx/.pdf`, `*_Proposal_Defence.pptx` | (binary) | **Leave untouched (D2)** |

## 8. Figure-by-figure mapping

| Figure | Now (Pro) | Becomes (InfraGuard AI) |
|--------|-----------|--------------------------|
| 3.1 | Hub-spoke control plane | Real architecture (agent + API + SQLite + Chroma + Vertex + dashboard + ntfy + CrowdSec + Loki/Prom) |
| 3.2 | Satellite topology | Single-host deployment (GCE VM, Compose, Promtail→Loki, two containers) |
| 3.3 | Remediation data flow | Heartbeat verdict pipeline: collect→analyze→decide→notify (+ fingerprint/ack step) |
| 3.4 | Use-case (remediation) | Real operator use cases (+ acknowledge-as-known) |
| 3.5 | SARIF→PR sequence | Real sequence: one heartbeat cycle (or threat-block, or ack flow) |
| 3.6 | 8-entity remediation ERD | Real schema: verdicts (+signature/fingerprint) + acknowledgements + logical entities |
| 3.7 | LangGraph state machine | Same, node names fixed to collect/analyze/decide/notify |
| 4.1 | Pro folder tree | Real repo tree |
| 4.2 | LLM provider class hierarchy | Real module structure (or orchestrator graph); or remove |
| 4.3 | Multi-server dashboard mock | Real dashboard screenshot (with ack button) |
| 5.1 | Patch acceptance (projected) | Coverage / test results by module |
| 5.2 | MTTR (projected) | **Duplicate-verdict count before/after memory** (the feature's effect) or SUS results |
| 5.3 | Cost per remediation (projected) | Remove (or real per-verdict LLM cost) |
| 5.4 | Calibration (projected) | Remove (or usability task-success chart) |

## 9. Fabricated claims to remove (explicit)

- "400 tests / 84.3% coverage" → real count + measured coverage (Phase 6).
- "247 self-scanning findings, 198 patched" → delete.
- "MTTR median 4 min 11 s empirically measured" (§4.3.4) → delete.
- "150-finding benchmark" + projected Figs 5.1–5.4 → delete / future work.
- "Six LLM providers with runtime hot-swap" → one (Vertex); abstraction = future work.
- "Hash-chained tamper-evident audit log" / `verify_audit_chain.py` → plain append-only log; describe honestly.
- "PostgreSQL / SQLAlchemy / Alembic / SvelteKit / Traceway / satellites" → remove.
- Internal contradiction (§4.3.4 "measured" vs Ch5 "proposed") → resolved by deleting both.

## 10. Real Objective 5 — usability test protocol (must actually run)

- **Participants:** 3–5 (devs / ops / SRE-adjacent).
- **Tasks:** (1) log in; (2) read current verdict + state severity; (3) open root cause + recommended action; (4) ask the runbook assistant a question; (5) identify a detected threat and use **Block IP** (dry-run); (6) interpret integration chips / stale-agent banner; (7) **mark a known warning as acknowledged and confirm it stops recurring.**
- **Instruments:** SUS (10 items) + short structured interview (effectiveness, efficiency, learnability, trust).
- **Capture:** task success, time-on-task, errors, SUS score, qualitative notes.
- **Report (Ch5):** results table, mean SUS, findings, and **improvements made** in response — directly satisfying the supervisor's "observations and improvements based on feedback."

## 11. Execution order & effort

1. Phase 0 (confirm objectives) — ~0.5 day.
2. Phases 1–2 (identity, intro) — ~1 day.
3. Phase 4 (methodology/design + its figures) — ~2 days.
4. **Phase 5 (build memory feature)** — ~2–3 days (piece A ~1 day, piece B ~1–2 days).
5. Phase 6 (measure coverage) — ~0.5 day.
6. Phase 11 figures in parallel — ~1–2 days.
7. Phase 10 usability test (recruit + run) — ~3–5 days wall-clock; **start recruiting at Phase 1**.
8. Phase 7 (implementation chapter) — ~2 days.
9. Phase 8 (testing/eval, needs coverage + usability + memory results) — ~1–2 days.
10. Phases 3, 9, 10-docs (lit review, conclusion, refs/appendices) — ~2 days.
11. Phase 12 (tables, rebuild, verify) — ~1 day.

Critical path: usability recruitment (longest lead — start early) and the memory build (Phase 5 gates the truthful Ch4/Ch5). Lit review (Phase 3) is the largest single rewrite.
