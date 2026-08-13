const { p, pCenter, chapterLabel, chapterTitle, h2, h3, bullet, num, blank, pageBreak } = require('../helpers');

function chapter1() {
  const b = [];

  b.push(chapterLabel('CHAPTER ONE: INTRODUCTION'));
  b.push(blank());

  // 1.1 BACKGROUND
  b.push(h2('1.1  Background to the Project'));
  b.push(p('Organisations increasingly operate containerised services that produce logs, metrics, and service events throughout the day. These signals are useful, but their volume and distribution make incident review difficult for a small operations team. An engineer may need to compare several sources before deciding whether a service is healthy, degraded, or failing.'));
  b.push(p('Observability is the ability to infer a system\'s internal state from its outputs. Prometheus, Grafana Loki, OpenTelemetry, and related tools provide established ways to collect and inspect telemetry. They support detection, but they do not remove the need for a person to interpret the evidence and choose an appropriate response.'));
  b.push(p('Site reliability engineering treats repetitive operational work as toil and recommends automation where the work is predictable and reviewable (Beyer et al., 2016). Initial incident triage fits this description in part: the inputs are available as telemetry, but a useful judgement still depends on context and experience. The purpose of this project is to assist that first review, not to replace the operator who remains responsible for action.'));
  b.push(p('Large language models can summarise structured and unstructured technical material, and tool-using agents can retrieve additional evidence before producing an answer. These capabilities make LLM-assisted triage worth testing. They also create risks. A model may infer facts that are not present, misread an optional integration as a failure, or produce a response that does not match the expected structure. Prompt constraints, output validation, and human approval can reduce these risks, but they do not prove that every verdict is correct.'));
  b.push(p('Nigerian organisations that operate digital services must also account for data-protection and sector-specific cybersecurity obligations. The Nigeria Data Protection Act 2023 sets duties for responsible processing of personal data. For institutions within its scope, the Central Bank of Nigeria\'s 2024 cybersecurity framework includes monitoring, reporting, and resilience controls (Central Bank of Nigeria, 2024; Federal Republic of Nigeria, 2023). Local deployment keeps the application records and access controls on the operator\'s host, but any prompt sent to a cloud LLM provider leaves that host.'));
  b.push(p('LivWell (Integrated Wellness Inc.) provided the operational setting that informed the requirements: several environments, containerised workloads, a small team, and a need for clear incident records. These constraints led to a single-host design, bounded telemetry collection, request auditing, operator-approved threat response, and an acknowledgement feature for recurring conditions. The result is a working reference implementation called InfraGuard AI.'));

  // 1.2 PROBLEM STATEMENT
  b.push(h2('1.2  Statement of the Problem'));
  b.push(p('Monitoring tools can collect and display system signals, but an operator must still relate those signals to the service context and decide what action is justified. This project addresses five practical parts of that problem:'));
  b.push(num('Triage time. When several telemetry sources report a problem, a responder must compare the evidence before stating the likely cause and next action. This work tests whether a bounded first-pass summary can support that review.'));
  b.push(num('Repeated low-risk findings. A known condition may appear on successive heartbeat cycles and occupy the same dashboard space as an unreviewed finding.'));
  b.push(num('Ungrounded model output. An LLM can infer a cause that is not supported by the supplied telemetry or treat an optional integration as a fault. Its response therefore needs scope constraints, structured parsing, and operator review.'));
  b.push(num('Deployment and data handling. Managed platforms and cloud model APIs differ in cost, hosting model, and the telemetry they receive. A small team needs a design whose data boundary can be inspected and configured.'));
  b.push(num('Limited operator memory. A recurring condition may appear on every heartbeat even after an operator has reviewed it. Without an acknowledgement mechanism, the dashboard provides no durable way to distinguish a known low-risk condition from an unreviewed one.'));
  b.push(p('The research problem is therefore to design and implement a bounded, self-hostable triage system that turns available telemetry into a reviewable verdict, provides runbook retrieval and operator-approved threat response, and records acknowledgements without hiding high-risk findings.'));

  // 1.3 AIM AND OBJECTIVES
  b.push(h2('1.3  Aim and Objectives of the Project'));
  b.push(h3('1.3.1  Aim'));
  b.push(p('The aim of this research is to design, develop, and evaluate InfraGuard AI, an LLM-assisted observability and incident-triage system that produces structured verdicts from available telemetry, supports operator-approved threat response and runbook retrieval, and records acknowledgements for recurring low-risk conditions.'));
  b.push(h3('1.3.2  Specific Objectives'));
  b.push(p('The study pursued five objectives:'));
  b.push(num('To design and implement a multi-source telemetry-collection layer that uniformly gathers application and system logs (via Grafana Loki), infrastructure metrics (via Prometheus), endpoint health (via HTTP probes), and optional container state (via the Docker Engine API), and normalises them into a bounded context suitable for downstream LLM reasoning.'));
  b.push(num('To develop a LangGraph reasoning workflow following a collect, analyse, decide, and notify cycle that requests a structured JSON verdict from a configured LLM provider and sends notifications for high and critical verdicts.'));
  b.push(num('To implement retrieval-augmented runbook assistance, grounded in organisation-specific Markdown runbooks loaded from the local filesystem and embedded locally into a ChromaDB vector store, together with deterministic detection of brute-force and port-scan patterns in logs and an operator-approved CrowdSec response for confirmed threats.'));
  b.push(num('To implement an acknowledgement memory keyed by a fingerprint of the condition signature, prompt version, and model, so matching low-risk verdicts can be marked and hidden by default while high and critical verdicts remain visible.'));
  b.push(num('To package the system for single-host deployment through Docker Compose and evaluate the implemented behaviour through automated tests and measured code coverage. A practitioner usability protocol is also defined for later administration.'));

  // 1.4 SCOPE
  b.push(h2('1.4  Scope of the Project'));
  b.push(h3('1.4.1  Within Scope'));
  b.push(bullet('Collection of application/system logs (Loki), infrastructure metrics (Prometheus), endpoint health (HTTP probes), and optional Docker container telemetry, on a configurable heartbeat interval.'));
  b.push(bullet('LLM-assisted generation of structured site-reliability verdicts through direct Gemini, Anthropic, or OpenAI APIs, or a local Ollama model, using direct-call or LangChain multi-tool modes.'));
  b.push(bullet('Push notification of high- and critical-severity verdicts via the ntfy.sh service.'));
  b.push(bullet('Deterministic detection of HTTP/SSH brute-force and port-scan patterns in logs, with operator-approved CrowdSec IP banning (operating in dry-run mode when CrowdSec is not configured).'));
  b.push(bullet('A retrieval-augmented runbook assistant over local Markdown runbooks indexed in ChromaDB with local embeddings.'));
  b.push(bullet('A stateful acknowledgement memory with condition-and-ruleset fingerprinting and a configurable time-to-live. A changed signature, prompt version, or model produces a different fingerprint.'));
  b.push(bullet('A single-page operations dashboard with session authentication, rate limiting, security headers, request auditing, and output escaping. Production deployment requires HTTPS termination and restricted network access.'));
  b.push(h3('1.4.2  Out of Scope (Identified as Future Work)'));
  b.push(bullet('Autonomous code remediation, including ingesting security-scanner output such as SARIF, generating code or configuration patches, and opening pull requests. The agent diagnoses and recommends; it does not modify application code.'));
  b.push(bullet('Fully offline inference is optional rather than automatic. The provider layer defaults to the direct Gemini Developer API and can switch to Anthropic Claude, OpenAI, or a local Ollama model through environment variables.'));
  b.push(bullet('Multi-server fleet operation. The present work targets a single host monitoring its co-located workloads; a distributed control-plane-and-satellite topology is future work.'));
  b.push(bullet('Custom training, fine-tuning, or distillation of the underlying LLMs; all models are treated as black-box providers accessed via their public APIs.'));
  b.push(bullet('Identity and access-management federation with external single-sign-on providers; the system uses cookie-based session authentication only.'));
  b.push(bullet('Native mobile or desktop client applications; the dashboard is delivered exclusively as a responsive web application.'));
  b.push(bullet('Formal security certification (e.g. SOC 2 or an ISO 27001 audit). The deliverable is a reference implementation and architectural blueprint, not a certified product.'));

  // 1.5 SIGNIFICANCE
  b.push(h2('1.5  Significance of the Project'));
  b.push(h3('1.5.1  Significance to Industry'));
  b.push(p('Practitioners can inspect how the implementation connects existing telemetry sources to an LLM-assisted review loop. The repository exposes the collection boundary, acknowledgement rule, threat-response approval step, and provider interface. It does not claim superiority over commercial platforms.'));
  b.push(h3('1.5.2  Significance to Organisations'));
  b.push(p('A small organisation can deploy, test, and modify InfraGuard AI on one host without first adopting a large observability platform. Whether that arrangement is suitable depends on the organisation\'s scale and controls. Running cost also depends on the LLM provider, heartbeat interval, prompt size, and surrounding infrastructure.'));
  b.push(h3('1.5.3  Significance to Policy and Society'));
  b.push(p('The Nigeria Data Protection Act 2023 and the Central Bank of Nigeria cybersecurity framework are relevant to organisations handling personal or financial data (Central Bank of Nigeria, 2024; Federal Republic of Nigeria, 2023). InfraGuard AI records verdicts, acknowledgements, and API requests, which an organisation may retain as part of its monitoring records. These records do not prove compliance. Use of a cloud LLM also requires an appropriate data-protection assessment.'));
  b.push(h3('1.5.4  Significance to Professional Practice'));
  b.push(p('Students and practitioners can trace a complete path from telemetry adapters through the LLM workflow, API, persistence layer, dashboard, and tests. The report also identifies the live-model and field evaluations that have not yet been carried out.'));
  b.push(h3('1.5.5  Significance to the Master of Information Technology Programme'));
  b.push(p('For the Master of Information Technology programme, the work links an operational problem to a software artefact, automated tests, measured coverage, and stated limits. The report distinguishes completed verification from evaluation proposed for later work.'));

  return b;
}

module.exports = { chapter1 };
