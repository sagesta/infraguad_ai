const { p, chapterLabel, h2, h3, num, blank } = require('../helpers');

function chapter6() {
  const b = [];

  b.push(chapterLabel('CHAPTER SIX: SUMMARY, CONCLUSION AND RECOMMENDATIONS'));
  b.push(blank());

  b.push(h2('6.1  Summary of the Project'));
  b.push(p('This project addressed the delay between collecting operational telemetry and interpreting it. InfraGuard AI was implemented as a single-host reference system with a scheduled agent, FastAPI service, browser dashboard, SQLite persistence, and optional runbook and threat-response integrations. The agent collects configured Loki, Prometheus, HTTP, and Docker evidence, then uses a LangGraph workflow to request a structured verdict from the selected LLM provider.'));
  b.push(p('The provider abstraction supports the direct Gemini Developer API, Anthropic, OpenAI, and local Ollama. The returned object is parsed into severity, summary, root cause, recommended action, and a condition signature. High and critical results follow the notification path. The dashboard provides current status, history, integration state, threat review, runbook retrieval, and acknowledgement controls.'));
  b.push(p('The acknowledgement feature computes a fingerprint from the condition signature, prompt version, and model. An active match can mark an ok or warning verdict as suppressed in the API and dashboard. A changed input produces a different fingerprint, and high or critical verdicts are never suppressed. The workflow continues to call the LLM and store a verdict on every heartbeat, so the feature reduces repeated display rather than inference.'));
  b.push(p('The final verification run contained 80 passing tests and 66 percent overall line coverage. The results support the implemented software rules, especially the memory and orchestration paths. They do not establish live-model diagnostic accuracy, cost, latency, or practitioner usability.'));

  b.push(h2('6.2  Conclusion'));
  b.push(p('The completed system connects an LLM-assisted triage workflow to Loki, Prometheus, HTTP probes, and optional Docker telemetry on one host. It records structured verdicts and keeps acknowledgement and threat-response actions under operator control.'));
  b.push(p('The acknowledgement design provides a practical way to label repeated low-risk conditions without hiding high-risk results. Its safety depends on the quality and stability of the condition signature. The severity safeguard and expiry rules reduce risk, but they do not remove the need for operator review.'));
  b.push(p('The evidence is sufficient to describe the system as a tested reference implementation. It is not sufficient to claim that prompt constraints prevent hallucinations, that the system reduces model cost, or that operators find the dashboard usable. Those questions require separate live-model and participant studies.'));

  b.push(h2('6.3  Professional Contributions'));
  b.push(h3('6.3.1  Reproducible Reference Implementation'));
  b.push(p('The repository shows how telemetry adapters, a provider-independent LLM interface, LangGraph orchestration, persistence, an authenticated API, a dashboard, and automated tests can be assembled for a single-host operations use case.'));
  b.push(h3('6.3.2  Acknowledgement Pattern'));
  b.push(p('The content-and-ruleset fingerprint links an acknowledgement to the observed condition and the active reasoning configuration. A similar design may suit other systems that must separate reviewed low-risk results from new findings, provided they also enforce an independent severity safeguard.'));
  b.push(h3('6.3.3  Documented Limits'));
  b.push(p('The report states where the evidence ends. Live provider behaviour, RAG integrations, usability, and deployment hardening are not presented as completed evaluations. Another evaluator can therefore distinguish the implemented controls from the outcomes that still need to be measured.'));

  b.push(h2('6.4  Recommendations for Future Work'));
  b.push(h3('6.4.1  Evaluation'));
  b.push(num('Create a labelled set of healthy, degraded, and failing telemetry scenarios. Measure severity accuracy, root-cause accuracy, evidence support, false positives, false negatives, schema-valid output rate, latency, and cost for each provider and model version.'));
  b.push(num('Administer the Appendix D tasks and System Usability Scale to an approved participant group. Report participant characteristics, task outcomes, times, errors, SUS calculations, interview themes, and interface changes.'));
  b.push(num('Run a longer field evaluation to measure operator-facing duplicate reduction, acknowledgement errors, and the effect of signature changes. Do not use stored-verdict suppression as a proxy for reduced inference cost.'));

  b.push(h3('6.4.2  Test and Security Coverage'));
  b.push(num('Add integration tests for the live provider clients, LangChain multi-tool path, ChromaDB store, notification adapter, CrowdSec adapter, and heartbeat entry point.'));
  b.push(num('Place the API behind an HTTPS reverse proxy, publish only the HTTPS port, restrict Prometheus, Loki, and administration ports to trusted networks, set secure cookies, and move credentials to a managed secret store.'));
  b.push(num('Replace inline dashboard scripts and styles so the content-security policy no longer requires unsafe-inline. Send audit events to a protected external store if tamper evidence is required.'));

  b.push(h3('6.4.3  Architecture'));
  b.push(num('Evaluate deterministic condition signatures derived before the LLM call. If reliable, they could allow some acknowledged conditions to bypass model analysis, after appropriate severity and freshness checks.'));
  b.push(num('Evaluate the supplied Ollama path where data-control requirements prohibit cloud inference. Compare model quality, latency, and resource cost with the configured cloud providers; equivalence must be measured rather than assumed.'));
  b.push(num('Treat autonomous remediation and multi-host operation as separate projects with their own threat models, approval policies, rollback mechanisms, and evaluations.'));

  return b;
}

module.exports = { chapter6 };
