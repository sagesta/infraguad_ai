# InfraGuard AI Defence Submission Checklist

**Status date:** 29 August 2026

**Current revised manuscript:** `docs/masters_project/InfraGuard_AI_Masters_Project_FINAL_REVISED_AFTER_29_AUGUST_REVIEW.docx`

**Submission status:** final quality assurance is still required. This checklist is
an internal evidence gate, not a supervisor-acceptance or defence-readiness
decision.

## Current bounded verification

- [x] The manuscript states the knowledge, design/technology, engineering, and empirical-evaluation gaps separately.
- [x] The fingerprint-based condition-and-ruleset acknowledgement pattern is identified as the principal design contribution.
- [x] Human-factors theory covers automation bias, calibrated trust, human control, alert fatigue, and trustworthy systems.
- [x] The frozen qwen2.5:3b benchmark is reported as **40.3% agreement with researcher-defined severity labels**, not independently adjudicated diagnostic accuracy, and the manuscript rejects unattended triage for that configuration.
- [x] The unchanged practitioner role reports are retained as provenance-limited qualitative material only. Their unrecomputable means, rankings, agreement percentages, kappas, and human RAG comparison are excluded from primary findings. The separate ten-complete-response SUS result remains descriptive perceived-usability evidence only.
- [x] The 29 August source-scoped software-verification run completed with **180 tests passed, 0 failed, 45 dependency warnings, and 89% overall line coverage** across 1,655 statements with 190 missed.
- [x] Six selected modules reached **100% line coverage**; the orchestrator reached 95% and the store reached 94%. These figures verify exercised software behaviour only.
- [x] Terraform has no ingress by default; HTTPS is opt-in and CIDR-gated; port 80 is redirect-only; management ports require trusted ranges; the dashboard/API is bound to `127.0.0.1:8080` in Docker Compose.
- [x] The README prominently requires HTTPS, private telemetry/admin binding, managed secrets, least privilege, and independent production-security verification.
- [ ] Re-export the final 29 August DOCX, refresh navigation, inspect every rendered page, and record the final page/reference/caption/link counts after the last layout correction.
- [ ] Reconcile the presentation with the 29 August manuscript before treating it as submission-ready; the existing deck predates this review cycle.

## Student actions before upload or defence

- [ ] Obtain all required signatures and dates on the approval pages.
- [ ] Confirm the University portal's filename, page-layout, file-size, and upload-format requirements.
- [ ] Open the final DOCX and any refreshed PPTX on the presentation computer and confirm fonts, links, and presenter notes display correctly.
- [ ] If a live provider demonstration is required, place the credential only in the private runtime environment, verify that no secret enters the repository or submission archive, and retain the operator-approval boundary.
- [ ] Rehearse the evidence boundaries: 40.3% agreement with researcher-defined labels; practitioner aggregates excluded because assessor-by-item ratings are unavailable; ten complete convenience-sample SUS responses; mocked external dependencies; and no diagnostic-reliability, RAG-effectiveness, or production-effectiveness claim.

## Include in the defence package

- `docs/masters_project/InfraGuard_AI_Masters_Project_FINAL_REVISED_AFTER_29_AUGUST_REVIEW.docx`, after the final QA gate passes.
- A presentation only after its claims and source notes have been reconciled with the 29 August manuscript.
- A newly rebuilt, credential-free source archive only if source submission is required.
- The assessor-report correction sidecar and manifests only when the supervisor requests the human-evidence provenance package.

## Exclude from the defence package

- Earlier manuscript and presentation versions, including the 28 August defence-ready-labelled artefacts.
- Historical revision matrices, realignment plans, and superseded document-generation sources.
- Legacy simulated-assessment artefacts; they are non-evidential.
- `tmp/`, caches, local databases, logs, credentials, `.env` files, and other runtime artefacts.
- Existing defence-ready source ZIPs unless they are rebuilt and independently checked against the current hardened source.

## Remaining limitations to state, not conceal

- The controlled tests use mocks for external providers, Docker/socket behaviour, and vector-store dependencies; they do not prove live or field reliability.
- TLS termination and managed-secret integration must be supplied by the deployment environment.
- The current model result does not support unattended triage.
- The role reports contain no retained assessor-by-item ratings, so their aggregate human results are excluded; SUS supports only descriptive perceived usability in the evaluated convenience group.
