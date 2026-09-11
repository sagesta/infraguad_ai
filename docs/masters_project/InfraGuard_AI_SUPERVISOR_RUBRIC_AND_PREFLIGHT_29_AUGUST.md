# InfraGuard AI Supervisor Rubric and Final Preflight

Date: 29 August 2026  
Basis: the new 44-page supervisor review, the prior major-revision review, the current manuscript, retained evaluation artefacts, both assessor reports, and repository inspection.

## Bottom-line interpretation

The supervisor applies a non-compensatory review model: strong architecture and implementation do not offset weak or non-recomputable research evidence. The new review rates the artefact highly but returns **Major Revision** because human evaluation, statistical rigour, gold-label provenance, and security assurance do not meet the evidential threshold.

The next submission must therefore pass every evidence gate. More features cannot substitute for provenance, recomputability, calibrated claims, and a clear novelty boundary.

## Inferred review domains

The review does not publish numeric weights. The following weights are an analytical reconstruction, not an institutional marking scheme.

| Domain | Inferred emphasis | What triggers another revision |
|---|---:|---|
| Empirical benchmark, RAG, and gold-label validity | High | Treating researcher labels as objective truth; conflating retrieval with correctness or safety |
| Human evaluation, SUS, reproducibility, and statistics | High | Reporting means, rankings, agreement, or kappa without assessor-by-item records |
| Literature, theory, DSR traceability, and novelty | High | Technology catalogue without synthesis; novelty asserted rather than bounded |
| Technical artefact and software verification | Medium | Confusing passing tests or coverage with operational validation |
| LLM security and data governance | Medium | Listing controls without a threat model or evidence boundary |
| Editorial quality, APA 7, figures, tables, and navigation | Medium | Broken links, stale pages, dense tables, inconsistent references, unreadable diagrams |
| Problem relevance and scope discipline | Lower but mandatory | Production, population, causal, or cross-model claims beyond the evidence |

## Hard pass/fail gates

1. Every quantitative human finding must be recomputable from genuine retained assessor-by-item records, or it must be excluded from primary evidence.
2. Gold labels must disclose author, timing, policy, independent-review status, ambiguity handling, and the meaning of agreement.
3. Software verification, controlled model evaluation, qualitative practitioner interpretation, and descriptive SUS evidence must remain distinct.
4. Retrieval relevance, grounding or traceability, answer correctness, and actionable safety must be reported separately.
5. The thesis must not imply diagnostic reliability, causal improvement, production effectiveness, population usability, or cross-model equivalence.
6. The novelty claim must distinguish conceptual, architectural, engineering, implemented-construct, and empirical contributions.
7. The LLM threat model must cover direct and indirect prompt injection, exfiltration, poisoned evidence, unsafe output, acknowledgement poisoning, privileged integrations, and supply-chain drift.
8. Interface support must not be presented as evaluated provider/model performance.
9. Tests and coverage verify exercised software behaviour; they do not prove attack resistance, diagnostic correctness, resilience, or production suitability.
10. TOC, lists, page numbers, bookmarks, captions, internal/external hyperlinks, appendices, citations, references, and final PDF layout must all pass final inspection.

## Assessor-report evidence decision

The user-supplied DevOps and SRE assessor reports are byte-for-byte identical to the repository copies:

- DevOps SHA-256: `741B5446C8DFFAABFEAC20823AA7A4427A4A61C058B1B9E9C619000C641D6720`
- SRE SHA-256: `7C91DFD735A4A070CE4E6053C5ADDCFB70CEC2D67002B199B43F22F21133EFDB`

The reports contain aggregate means, agreement percentages, kappa coefficients, and qualitative observations. They do not contain the original 72 item-level ratings per assessor for the incident set and 72 item-level ratings per assessor for the RAG/no-RAG set. The public A/B worksheets contain identifiers but blank score cells.

The SRE report contains a randomisation-seed inconsistency: its opening record and executive summary state `2026082412`, while the Assessment Method table states `2026081902`. The user confirmed `2026082412` as correct, and the retained `CORRECTION_NOTICE.md` plus `manifest.json` already preserve that value as authoritative while leaving the hashed report binary unchanged.

Decision for the final manuscript:

- retain the two reports and hashes as provenance-qualified qualitative material;
- retain their engineering themes as hypotheses for future tests;
- exclude their means, rankings, agreement percentages, and kappas from primary findings, RQ answers, objectives, contributions, and conclusions;
- make no quantitative human RAG-versus-no-RAG claim;
- restore quantitative practitioner findings only if genuine item-level sheets are recovered and independently recomputed.

## Statistical interpretation rules

- The 72 incident responses are three repeated observations within 24 purposively designed synthetic scenarios, not 72 independent production incidents.
- Severity results are agreement with a researcher-defined policy, not an estimate of real-world diagnostic truth.
- Do not use a simple binomial confidence interval or significance test that treats the 72 repeats as independent and representative.
- The RAG set is a paired 12-question repeated design. Without item-level human ratings, no inferential comparison or kappa recomputation is supportable.
- A no-RAG grounding value of zero is structurally induced by the absence of supplied sources; it demonstrates lack of traceability, not factual incorrectness.
- SUS `n = 10` is a convenience sample. Mean, median, sample standard deviation, range, and completion rate may be reported descriptively; subgroup means remain descriptive only.
- Do not infer reduced workload, fewer errors, faster diagnosis, population usability, or causality from SUS.

## Mandatory wording boundaries

Use:

- `configuration-specific`
- `controlled benchmark`
- `researcher-defined labels`
- `exploratory qualitative role reports`
- `descriptive convenience-sample SUS result`
- `reference implementation`
- `retrievability under the frozen corpus and top-four setting`

Avoid as result claims unless new evidence exists:

- `validated`
- `proven`
- `effective`
- `reliable`
- `significantly improved`
- `production-ready`
- `reduces workload`
- `RAG improved grounding`
- `provider-independent performance`

## Submission preflight

### Evidence and claims

- [ ] All unrecomputable practitioner means, rankings, agreement percentages, and kappas are absent from primary findings.
- [ ] The two reports are described only as qualitative, provenance-limited material.
- [ ] The SRE seed correction is disclosed through the authoritative sidecar; the hashed report remains unchanged.
- [ ] Gold-label origin, policy, review status, and C20 sensitivity are explicit.
- [ ] Verification and validation are defined once at the start of Chapter Five.
- [ ] RAG dimensions are separated; only top-four retrieval is claimed quantitatively.
- [ ] qwen2.5:3b is the only controlled retained model result.
- [ ] DeepSeek remains an unretained convenience pilot.
- [ ] Gemini, Anthropic, OpenAI-compatible, and other Ollama paths remain interface claims only.
- [ ] SUS is limited to favourable perceived usability in the evaluated convenience group.
- [ ] No production, fleet, longitudinal, workload, fatigue, task-time, task-error, energy, full-cost, or population claim appears.

### Research argument

- [ ] Five clean RQs are used consistently in Chapters One, Three, Five, and Six.
- [ ] DSR is the primary methodology; governance-by-design is the primary governance foundation.
- [ ] Human-AI reliance and trustworthy AI are supporting lenses.
- [ ] Observability, SRE, AIOps, incident management, and RAG are domain/technical foundations rather than theory.
- [ ] The named novelty subsection distinguishes five contribution categories and answers “What is new?” directly.
- [ ] Requirements are consistently described as researcher-derived, not stakeholder-elicited.
- [ ] Model-generated condition identity is explicitly identified as insufficiently stable for dependable acknowledgement semantics.

### Security and implementation

- [ ] Untrusted telemetry/runbook content is separated from model instructions.
- [ ] Acknowledgement free text does not enter the model prompt.
- [ ] Acknowledgement never instructs the model to downgrade current severity.
- [ ] Prompt/ruleset changes invalidate earlier acknowledgement fingerprints.
- [ ] Verdict parsing rejects malformed, incomplete, duplicate-key, non-canonical, oversized, or severity/signature-contradictory output.
- [ ] Provider/parser failure creates a visible, non-acknowledgeable pipeline alert.
- [ ] CrowdSec action is rebuilt from fresh server-side detection rather than client assertions.
- [ ] The cloud/local data-flow diagram labels egress, return, local storage, provider exposure, and deployment obligations.
- [ ] The manuscript states that these controls have software-test evidence only; no penetration test or live adversarial model run is claimed.
- [ ] Frozen benchmark v1 remains immutable and is not reparsed or overwritten under the hardened v2 contract.

### Editorial and artifact QA

- [ ] Abstract contains approximately five headline results and no assessor comparison.
- [ ] Table 2.1 is concise and followed by critical synthesis.
- [ ] Every figure/table is introduced and interpreted in the narrative.
- [ ] Figure and table captions, lists, and numbering are sequential.
- [ ] Every table header row is marked and every image has meaningful alt text.
- [ ] British English and project terminology are consistent.
- [ ] Citation keys reconcile with reference entries; DOI/URL targets are valid.
- [ ] TOC and list page numbers match the final PDF.
- [ ] All bookmarks and PDF hyperlinks resolve.
- [ ] Every rendered page is visually inspected for clipping, overlap, blank-page anomalies, table wrapping, and figure legibility.

## Residual evidence item that cannot be manufactured

The only defensible way to reinstate the practitioner means and kappas is to obtain the genuine original assessor-by-item records or have both assessors rescore the frozen anonymised packages under a documented protocol. Aggregate report values cannot be reverse-engineered into authentic item-level evidence.
