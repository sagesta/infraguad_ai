const { p, pCenter, chapterLabel, h2, h3, h4, bullet, num, blank, pageBreak, buildTable, tableCaption } = require('../helpers');

function chapter2() {
  const b = [];

  b.push(chapterLabel('CHAPTER TWO: LITERATURE REVIEW AND TECHNOLOGY CONTEXT'));
  b.push(blank());

  // 2.1 CONCEPTUAL REVIEW
  b.push(h2('2.1  Conceptual Review'));
  b.push(p('Six concepts frame the design: cloud-native observability, site reliability engineering, AIOps, large language models and agents, retrieval-augmented generation, and acknowledgement memory. The discussion below defines each concept and states how it affects the implementation.'));

  b.push(h3('2.1.1  Cloud-Native Observability and the Three Pillars'));
  b.push(p('Observability is the ability to infer a system\'s internal state from its outputs. Common telemetry types include metrics, logs, traces, and service events. Prometheus is widely used for metrics, Grafana Loki for logs, and OpenTelemetry for instrumentation. These tools make signals available for investigation, but an operator must still determine what the signals mean in the context of a particular service. InfraGuard AI consumes logs and metrics directly, supplemented by HTTP probes and optional Docker telemetry.'));

  b.push(h3('2.1.2  Site Reliability Engineering and Incident Management'));
  b.push(p('Site reliability engineering uses telemetry, service-level objectives, and operational automation to improve reliability. Beyer et al. (2016) use the term toil for repetitive manual work that scales with service growth. Alert review and repeated handling of known conditions are relevant examples. InfraGuard AI addresses a limited part of this work by generating a first-pass verdict and recording operator acknowledgements.'));

  b.push(h3('2.1.3  AIOps: Artificial Intelligence for IT Operations'));
  b.push(p('AIOps applies machine learning and analytics to operations data for tasks such as anomaly detection, event correlation, fault diagnosis, and remediation support. Chen et al. (2025) present AIOpsLab as a reproducible environment for deploying cloud systems, injecting faults, exporting telemetry, and evaluating LLM agents across operational tasks. Their results also show that agent capability depends on the task and evaluation setting. InfraGuard AI does not train an anomaly detector or claim autonomous remediation. It asks a general-purpose LLM to interpret a bounded set of collected evidence and returns the result for operator review.'));

  b.push(h3('2.1.4  Large Language Models and Agentic AI'));
  b.push(p('Large language models generate text from a supplied context and can be connected to tools that retrieve additional evidence. ReAct interleaves model reasoning with tool actions (Yao et al., 2023), while Reflexion studies the use of verbal feedback across attempts (Shinn et al., 2023). InfraGuard AI uses LangGraph to define a bounded workflow and offers an optional LangChain mode in which the configured model selects from a small telemetry tool set. These mechanisms do not guarantee a correct diagnosis, so the system keeps the operator responsible for action.'));

  b.push(h3('2.1.5  Retrieval-Augmented Generation'));
  b.push(p('Retrieval-augmented generation (RAG) retrieves relevant documents and supplies them as context to a language model at inference time (Lewis et al., 2020). In an operations setting, the retrieved material can come from the organisation\'s runbooks. This gives the model relevant local context and source titles, although the answer still requires operator review. InfraGuard AI loads local Markdown runbooks, embeds them on the host, stores the vectors in ChromaDB, and exposes retrieval through the dashboard.'));

  b.push(h3('2.1.6  Statelessness, Alert Deduplication, and Agent Memory'));
  b.push(p('A scheduled triage loop can show the same condition on successive cycles even after it has been reviewed. Alert grouping and log-template research show why the identity used for matching matters. A broad key can merge different conditions, while exact raw text often fails to match because timestamps, identifiers, and values change. Drain, for example, derives stable log templates by separating fixed and variable tokens (He et al., 2017). InfraGuard AI applies a related idea at verdict level: it combines a condition signature with the prompt version and model to produce a fingerprint. A matching acknowledgement marks an ok or warning verdict as suppressed in the API and dashboard. It does not prevent the model call on the next heartbeat.'));

  // 2.2 EXISTING SYSTEMS / SOLUTIONS
  b.push(h2('2.2  Review of Existing Systems and Solutions'));
  b.push(p('The review covers thirteen studies on site reliability engineering, AIOps, log parsing, retrieval, and LLM-assisted operations. Each study is compared by method, evidence, limitation, and relevance to InfraGuard AI. Current product documentation is used separately for the commercial and open-source tools.'));

  b.push(h3('2.2.1  Comparative Table of Thirteen Recent and Related Studies'));
  b.push(p('Table 2.1 compares thirteen studies covering site reliability engineering, AIOps, LLM-based incident analysis, log parsing, tool use, and retrieval. The selection emphasises work published from 2020 to 2025, established research venues, and direct relevance to the implemented design.'));
  b.push(blank());

  const colWidths = [750, 1500, 1300, 1150, 1350, 1500, 1476];
  const headers = [
    '#', 'Study (author, year)', 'Method', 'Tools / models',
    'Reported result', 'Limitation', 'Use in InfraGuard AI'
  ];

  const litRows = [
    [
      '1',
      'Beyer, Jones, Petoff & Murphy (2016). “Site Reliability Engineering.” O’Reilly / Google.',
      'Foundational practitioner text codifying SRE practice: service-level objectives, error budgets, on-call, and incident response.',
      'Operational framework; no software artefact.',
      'Defines telemetry-driven operations and describes repetitive manual work that grows with service scale as toil.',
      'Predates the LLM era; assumes a human performs the interpretation of telemetry into action.',
      'Implements a first-pass telemetry summary as a structured verdict. Its effect on operator workload still requires a field study.'
    ],
    [
      '2',
      'Chen, Shetty, Somashekar et al. (2025). “AIOpsLab: A Holistic Framework to Evaluate AI Agents for Enabling Autonomous Clouds.” MLSys.',
      'Builds a framework that deploys cloud environments, injects faults, generates workloads, exports telemetry, and evaluates operational agents.',
      'Open AIOpsLab framework, agent-cloud interface, benchmark environments, and LLM agents.',
      'Provides a reproducible benchmark and reports that current agents have uneven capability across complex operational tasks.',
      'Focuses on benchmarked agent evaluation rather than a small operator-facing deployment with persistent acknowledgement memory.',
      'Motivates reproducible evaluation while InfraGuard AI supplies an inspectable single-host implementation and states which live-model tests remain outstanding.'
    ],
    [
      '3',
      'He, Zhu, Zheng & Lyu (2017). “Drain: An Online Log Parsing Approach with Fixed Depth Tree.” IEEE ICWS.',
      'Streaming log parser that abstracts raw log lines into templates by stripping variable tokens via a fixed-depth parse tree.',
      'The Drain algorithm.',
      'Enables stable grouping of semantically identical log events despite volatile parameters such as timestamps and identifiers.',
      'Provides parsing only; no reasoning over the parsed events and no operator-facing memory of judgements.',
      'The verdict-memory applies the same volatile-token-normalisation principle so that the same condition fingerprints stably across heartbeats, enabling reliable acknowledgement.'
    ],
    [
      '4',
      'Yao, Zhao, Yu, Du, Shafran, Narasimhan & Cao (2023). “ReAct: Synergizing Reasoning and Acting in Language Models.” ICLR.',
      'Introduces an interleaved reasoning-and-acting prompting paradigm allowing an LLM to alternate chain-of-thought with tool invocations.',
      'GPT-3 / PaLM with external tool environments.',
      'Outperforms the reported reasoning-only and acting-only baselines on the study’s knowledge and decision tasks.',
      'Domain-agnostic foundational technique with no operations application or production evaluation.',
      'Adopted in the LangChain multi-tool mode, where Gemini interleaves reasoning with calls to the Loki, Prometheus, and HTTP-probe tools before producing a verdict.'
    ],
    [
      '5',
      'Shinn, Cassano, Gopinath, Narasimhan & Yao (2023). “Reflexion: Language Agents with Verbal Reinforcement Learning.” NeurIPS.',
      'Self-improving agent loop in which the model reflects on failed actions through verbal critique and revises its plan.',
      'GPT-4 with a reflection memory.',
      'Outperforms the reported single-shot baselines on the study’s multi-step tasks.',
      'Demonstrated on toy code and QA tasks; no integration with telemetry or operations systems.',
      'Provides a contrast with InfraGuard AI: the project stores operator acknowledgements, not a model-generated reflection memory.'
    ],
    [
      '6',
      'Yuan, Tang, Liu et al. (2025). “Incident Diagnosing and Reporting System Based on Retrieval Augmented Large Language Model.” AAAI.',
      'RAIDR retrieves system documents and similar incident records, then uses an LLM to diagnose IoT anomalies and draft incident reports.',
      'Incident signatures, relationship-aware anomaly analysis, retrieval, and an LLM report generator.',
      'Demonstrates a retrieval-augmented incident diagnosis and reporting workflow over IoT sensor data.',
      'Short demonstration paper focused on IoT incidents; it does not evaluate the single-host observability and acknowledgement workflow used here.',
      'Supports the use of organisation-specific documents for incident assistance; InfraGuard AI applies retrieval to runbooks and returns source titles.'
    ],
    [
      '7',
      'Ahmed, Ghosh, Bansal, Zimmermann, Zhang and Rajmohan (2023). “Recommending Root-Cause and Mitigation Steps for Cloud Incidents Using Large Language Models.” ICSE.',
      'Prompts and fine-tunes LLMs to recommend root cause and mitigation steps from production incident data at scale.',
      'GPT-3.0 and GPT-3.5 models on more than 40,000 Microsoft incidents.',
      'Reports zero-shot, fine-tuned, and multi-task results, followed by evaluation with incident owners.',
      'Operates inside a proprietary hyperscale cloud; not self-hostable; no operator-facing memory; no open implementation.',
      'Brings grounded root-cause and recommended-action verdicts to a self-hosted, open reference system sized for small teams, with an operator acknowledgement memory layered on top.'
    ],
    [
      '8',
      'Jin, Zhang, Ma et al. (2023). “Assess and Summarize: Improve Outage Understanding with Large Language Models.” ESEC/FSE.',
      'Oasis groups incidents to assess outage impact and uses a fine-tuned model to generate an outage summary.',
      'Fine-tuned GPT-3.x models on data from 18 Microsoft cloud systems.',
      'Reports an empirical evaluation and a human evaluation with outage owners; a prototype entered experimental adoption.',
      'Evaluates outage summarisation after evidence has been collected; the data and deployment are proprietary.',
      'Runs on a scheduled heartbeat and stores each structured verdict for later review and acknowledgement.'
    ],
    [
      '9',
      'Chen, Xie, Ma et al. (2024). “Automatic Root Cause Analysis via Large Language Models for Cloud Incidents.” EuroSys.',
      'RCACopilot matches incidents to handlers by alert type, gathers diagnostic information, predicts a root-cause category, and generates an explanation.',
      'Incident matching and diagnostic collection with an LLM-generated explanation over Microsoft incident data.',
      'Reports root-cause accuracy up to 0.766; its diagnostic collection component had been used at Microsoft for more than four years.',
      'Targets hyperscale operations; heavyweight; not bounded for, or deployable by, small single-host estates.',
      'Restricts collection to selected sources on one host and exposes the implementation for inspection.'
    ],
    [
      '10',
      'Roy, Zhang, Bhave et al. (2024). “Exploring LLM-Based Agents for Root Cause Analysis.” FSE Companion.',
      'Investigates autonomous LLM agents for root-cause analysis and the interface and grounding choices that make them effective.',
      'Tool-augmented LLM agents on incident datasets.',
      'Reports that tool and grounding choices affect root-cause-analysis performance.',
      'Uses Microsoft incident data and diagnostic services; it does not present a general self-hosted deployment or an acknowledgement feature.',
      'Contributes the self-hosted, human-in-the-loop, memory-equipped variant: operator-approved threat response and a stateful acknowledgement memory.'
    ],
    [
      '11',
      'Xu, Zhang, Zhong et al. (2025). “OpenRCA: Can Large Language Models Locate the Root Cause of Software Failures?” ICLR.',
      'Introduces a benchmark for locating software-failure root causes from heterogeneous logs, metrics, traces, and dependency information.',
      'OpenRCA: 335 failures from three enterprise systems and more than 68 GB of telemetry; evaluated LLMs and an RCA agent.',
      'The best reported configuration, an RCA agent using Claude 3.5, solved 11.34 percent of the benchmark cases.',
      'Offline benchmark rather than a deployed incident workflow; results show that current models remain unreliable on difficult cases.',
      'Supports the project’s human-review boundary and the decision not to claim diagnostic accuracy from software tests alone.'
    ],
    [
      '12',
      'Hou, Zhao, Liu et al. (2024). “Large Language Models for Software Engineering: A Systematic Literature Review.” ACM TOSEM.',
      'Systematic review of 395 studies on LLM applications across the software lifecycle.',
      'Meta-analysis.',
      'Catalogues models, data practices, evaluation methods, and software-engineering tasks, and identifies uneven coverage across the field.',
      'Reviews the gap but does not provide an operations implementation; it also identifies hallucination and reproducibility concerns.',
      'Provides an inspectable implementation of one LLM-assisted operations workflow and documents its output constraints.'
    ],
    [
      '13',
      'Guo, Yang, Lu et al. (2024). “OWL: A Large Language Model for IT Operations.” ICLR.',
      'Develops a domain-specialised LLM and benchmark for IT-operations question answering.',
      'Domain-tuned LLM; IT-ops benchmark.',
      'Domain specialisation improves operations question-answering performance over general models.',
      'Model-centric; no end-to-end agent, no live telemetry loop, and the bespoke model raises cost and operational complexity.',
      'Uses a configurable general-purpose provider with bounded telemetry context instead of training a domain-specific model.'
    ],
  ];

  const rows = [headers, ...litRows];
  b.push(buildTable(colWidths, rows, 'D9E2F3', true));
  b.push(blank());
  b.push(tableCaption('Table 2.1: Comparative Review of Thirteen Studies in AIOps and LLM-Assisted Operations.'));
  b.push(blank());

  b.push(h3('2.2.2  Synthesis of the Reviewed Studies'));
  b.push(p('Ahmed et al. (2023), Jin et al. (2023), Chen et al. (2024), and Roy et al. (2024) evaluate LLMs for incident recommendations, outage summaries, or tool-assisted root-cause analysis, largely with proprietary cloud data. More recent open work addresses reproducible evaluation and exposes the remaining difficulty: AIOpsLab evaluates agents in controlled cloud environments, while OpenRCA reports that its best configuration solved 11.34 percent of 335 benchmark failures (Chen et al., 2025; Xu et al., 2025). RAIDR applies retrieval to incident diagnosis and reporting in an IoT setting (Yuan et al., 2025). InfraGuard AI uses related tool and retrieval patterns over a small telemetry surface, but keeps the operator responsible for action and does not claim diagnostic accuracy from software tests.'));

  b.push(h3('2.2.3  Commercial and Open-Source State of the Art'));
  b.push(p('The following products provide related observability or incident-analysis functions. Their descriptions are limited to features stated in current product documentation.'));
  b.push(h4('Datadog Bits AI and Watchdog'));
  b.push(p('Datadog Bits AI supports investigations using Datadog telemetry, runbooks, environment context, feedback, and investigation memories (Datadog, n.d.). It is part of Datadog\'s managed commercial platform.'));
  b.push(h4('New Relic AI'));
  b.push(p('New Relic AI provides natural-language access to telemetry held in the New Relic platform and can return explanations, summaries, charts, and troubleshooting guidance (New Relic, n.d.). It is a managed platform feature rather than an operator-hosted reference implementation.'));
  b.push(h4('PagerDuty AIOps'));
  b.push(p('PagerDuty AIOps provides alert grouping, noise reduction, triage, root-cause features, event orchestration, and automation within PagerDuty\'s managed incident platform (PagerDuty, n.d.). Its event-grouping functions are related to, but not identical with, the acknowledgement memory studied here.'));
  b.push(h4('k8sgpt (Open Source)'));
  b.push(p('k8sgpt is an open-source tool that analyses Kubernetes resources and sends selected information to a configured AI backend for explanation (k8sgpt, n.d.). Its primary scope is Kubernetes diagnosis rather than the multi-source heartbeat implemented by InfraGuard AI.'));

  b.push(h3('2.2.4  Capability Comparison'));
  b.push(p('Table 2.2 compares the main emphasis and deployment model of the reviewed systems. It avoids binary capability scores because commercial features change and are not fully observable from public documentation.'));
  b.push(blank());

  const capColWidths = [1800, 2000, 2000, 3226];
  const capHeaders = ['System', 'Deployment', 'Primary Scope', 'Relevant Distinction'];
  const capRows = [
    capHeaders,
    ['InfraGuard AI', 'Operator-hosted reference implementation', 'Scheduled triage over selected telemetry sources', 'Condition-and-ruleset acknowledgement; human-approved CrowdSec action'],
    ['Datadog Bits AI', 'Managed commercial platform', 'Investigation over Datadog telemetry and knowledge sources', 'Runbooks, environment context, feedback, and investigation memories'],
    ['New Relic AI', 'Managed commercial platform', 'Natural-language analysis of New Relic telemetry', 'Platform-integrated explanations, queries, summaries, and charts'],
    ['PagerDuty AIOps', 'Managed commercial platform', 'Event grouping, triage, RCA support, and orchestration', 'Noise reduction and event-processing automation'],
    ['k8sgpt', 'Open-source tool run by the user', 'Kubernetes resource analysis', 'Kubernetes-specific analyzers with a selectable AI backend'],
  ];
  b.push(buildTable(capColWidths, capRows));
  b.push(blank());
  b.push(tableCaption('Table 2.2: Deployment and Scope Comparison of Representative Systems.'));
  b.push(blank());

  // 2.3 TOOLS AND FRAMEWORKS
  b.push(h2('2.3  Review of Relevant Technologies, Tools, and Frameworks'));
  b.push(p('The selected technologies are grouped by architectural layer. Selection considered maintenance status, licensing, support for self-hosting, and fit with a small single-host deployment.'));

  b.push(h3('2.3.1  Programming Language and Runtime'));
  b.push(p('Python 3.11+ was selected because the required model-provider, LangChain, and LangGraph libraries are available for Python. The FastAPI service and heartbeat loop also use asyncio, while aiosqlite, httpx, and ChromaDB cover persistence, HTTP access, and retrieval. The dashboard uses one HTML file with CSS and JavaScript, so deployment does not require a separate frontend build service.'));

  b.push(h3('2.3.2  Web and API Framework'));
  b.push(p('FastAPI supports the asynchronous routes used by the application and generates an OpenAPI description of the API. Its dependency mechanism is used for route-level controls. The same application serves the dashboard and its JSON endpoints, with both using the session cookie for authentication. This avoids a separate dashboard service.'));

  b.push(h3('2.3.3  LLM Orchestration and Provider'));
  b.push(p('LangGraph was selected because its explicit graph maps to the collect, analyse, decide, and notify workflow (LangChain, n.d.). LangChain is retained for the optional multi-tool mode and the ChromaDB integration. The implementation defaults to Gemini through the Gemini Developer API, while the provider abstraction also supports Anthropic, OpenAI, and local Ollama backends. Provider and model names can be changed through environment variables.'));

  b.push(h3('2.3.4  Observability and Telemetry Sources'));
  b.push(p('Prometheus and Grafana Loki are the primary metric and log sources and are queried through their HTTP APIs. The deployment expects those services to be configured separately; it does not deploy a log shipper or monitoring backend. HTTP probes provide endpoint checks, the Docker Engine API provides optional local-container telemetry, and CrowdSec is available for operator-approved IP bans. Distributed tracing is outside the project scope.'));

  b.push(h3('2.3.5  Data Stores'));
  b.push(p('SQLite, accessed asynchronously through aiosqlite, is the persistence layer for verdict records and operator acknowledgements; its single-file, zero-administration profile suits a self-hosted single-host deployment, and an automatic retention policy bounds its growth. ChromaDB is the vector store for the runbook RAG corpus, which uses local ONNX embeddings. No external relational database server is required.'));

  b.push(h3('2.3.6  Security and Deployment'));
  b.push(p('Application controls include signed timestamped session cookies, rate limiting, response headers, output escaping, and request logging. Docker Compose packages the API and agent, Terraform provisions a Google Compute Engine host, and GitHub Actions runs tests before the deployment job builds and publishes images. A production deployment still requires HTTPS termination, restricted firewall rules, and protected secret handling.'));

  b.push(h3('2.3.7  Relevant Standards and Specifications'));
  b.push(p('Table 2.3 lists the standards and specifications referenced in the design.'));
  b.push(blank());

  const stdColWidths = [2400, 1900, 4726];
  const stdHeaders = ['Standard / Specification', 'Source', 'Role in InfraGuard AI'];
  const stdRows = [
    stdHeaders,
    ['Prometheus Exposition Format', 'Prometheus Authors (n.d.)', 'Metric data format consumed by the metrics-collection tool.'],
    ['Loki HTTP API (LogQL)', 'Grafana Labs (n.d.)', 'Log query interface used to retrieve recent log lines over an explicit time window.'],
    ['OpenAPI 3.1', 'OpenAPI Initiative (2025)', 'Automatic description of the control-plane REST surface generated by FastAPI.'],
    ['System Usability Scale (SUS)', 'Brooke (1996)', 'Standardised instrument used in the usability evaluation of the dashboard.'],
    ['ISO/IEC 27001:2022', 'International Organization for Standardization (2022)', 'Information-security management reference informing audit-trail and access-control design.'],
    ['Nigeria Data Protection Act 2023', 'Federal Republic of Nigeria (2023)', 'Regional legal context for access control, accountability, and responsible processing.'],
    ['Risk-Based Cybersecurity Framework for DMBs and PSBs', 'Central Bank of Nigeria (2024)', 'Sector-specific context for monitoring, reporting, and resilience controls.'],
    ['NIST AI 600-1', 'National Institute of Standards and Technology (2024)', 'Generative-AI risk reference for grounding, output validation, human oversight, and post-deployment monitoring.'],
    ['OWASP Top Ten', 'OWASP Foundation (2025)', 'Reference for the dashboard’s security-header, session, and threat-handling choices.'],
  ];
  b.push(buildTable(stdColWidths, stdRows));
  b.push(blank());
  b.push(tableCaption('Table 2.3: Relevant Standards and Specifications.'));

  // 2.4 GAP ANALYSIS
  b.push(h2('2.4  Gap Analysis'));
  b.push(p('Seven gaps in the reviewed work shaped the design decisions described below.'));

  b.push(h3('2.4.1  Grounding and response validation'));
  b.push(p('An LLM can infer an unsupported cause or return malformed output. The NIST Generative AI Profile identifies confabulation, information security, human oversight, and post-deployment monitoring as risk-management concerns (National Institute of Standards and Technology, 2024). InfraGuard AI supplies selected telemetry, tells the model not to treat absent integrations as faults, and checks the response fields and severity. These controls constrain the interface, but they do not establish diagnostic accuracy.'));
  b.push(h3('2.4.2  Deployment control'));
  b.push(p('The commercial platforms reviewed are vendor-managed services. InfraGuard AI keeps the API, dashboard, database, and runbook index on the operator\'s host. A prompt still leaves the host when the operator selects a cloud LLM provider.'));
  b.push(h3('2.4.3  Inspectable entry point'));
  b.push(p('A small reference implementation allows the collection and reasoning paths to be inspected without adopting a full observability platform. This does not imply lower operating cost; cost depends on the host, provider, prompt size, and request rate.'));
  b.push(h3('2.4.4  Recurring-condition acknowledgement'));
  b.push(p('A scheduled triage loop needs a durable distinction between a reviewed low-risk condition and a new finding. InfraGuard AI stores a fingerprinted acknowledgement and suppresses the matching ok or warning verdict in the default view. A change to the signature, prompt version, or model produces a different fingerprint.'));
  b.push(h3('2.4.5  Operator approval for enforcement'));
  b.push(p('IP bans can interrupt legitimate traffic. InfraGuard AI therefore applies a CrowdSec ban only after an operator approves the detected threat. Acknowledgement rules also prevent high and critical findings from being hidden.'));
  b.push(h3('2.4.6  Organisation-specific runbooks'));
  b.push(p('Generic advice may conflict with an organisation\'s procedures. The runbook assistant retrieves from locally maintained Markdown documents and returns the source titles used for its answer.'));
  b.push(h3('2.4.7  Reproducibility'));
  b.push(p('Private datasets and managed infrastructure limit direct reproduction of several reviewed systems. InfraGuard AI keeps the collection, matching, persistence, and API logic in one repository so another evaluator can inspect those decisions.'));

  b.push(p('Together, these gaps define the implementation boundary. Chapter Three explains how they were translated into requirements and design decisions.'));

  return b;
}

module.exports = { chapter2 };
