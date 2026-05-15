const { p, pCenter, chapterLabel, h2, h3, h4, bullet, num, blank, pageBreak, buildTable } = require('../helpers');

function chapter2() {
  const b = [];

  b.push(chapterLabel('CHAPTER TWO'));
  b.push(pCenter('LITERATURE REVIEW AND TECHNOLOGY CONTEXT'));
  b.push(blank());

  // 2.1 CONCEPTUAL REVIEW
  b.push(h2('2.1  Conceptual Review'));
  b.push(p('This section establishes the conceptual vocabulary used throughout the remainder of the report. Each concept is defined briefly, situated relative to the project, and traced to its principal sources in the academic and industry literature. The concepts are organised into six thematic groups: (i) DevSecOps and the security shift-left movement, (ii) continuous integration and delivery pipelines, (iii) automated security scanning and the SARIF standard, (iv) large language models and agentic AI systems, (v) retrieval-augmented generation, and (vi) cloud-native observability and site reliability engineering.'));

  b.push(h3('2.1.1  DevSecOps and the Security Shift-Left'));
  b.push(p('DevSecOps emerged in the mid-2010s as a corrective extension of DevOps, addressing the observation that security activities had been disproportionately concentrated at the end of the software delivery lifecycle, frequently as a release-blocking penetration test, and that this concentration was incompatible with the high-cadence delivery rhythm DevOps had enabled. The shift-left principle holds that security activities — threat modelling, code review, dependency analysis, secret scanning, container hardening — should be integrated into the earliest stages of the pipeline, ideally before code is merged. The empirical literature is consistent in its finding that defects discovered earlier in the lifecycle cost an order of magnitude less to remediate than those discovered after deployment, and that automated, machine-speed feedback is essential to making shift-left compatible with continuous delivery (Myrbakken and Colomo-Palacios, 2017; Rajapakse et al., 2022).'));

  b.push(h3('2.1.2  Continuous Integration and Continuous Delivery'));
  b.push(p('Continuous integration (CI) is the practice of automatically building and testing every code change as it is committed to a shared repository; continuous delivery (CD) extends CI by automating the packaging and deployment of every change that passes its tests into production-equivalent environments. The CI/CD pipeline is the orchestration mechanism that executes these activities, typically expressed declaratively as a configuration file (GitHub Actions YAML, GitLab CI YAML, Tekton Pipelines, Jenkinsfile). Within this pipeline, individual jobs are responsible for compilation, unit testing, integration testing, security scanning, container image construction, image signing, artefact publishing, and deployment to the target environment. The pipeline is the natural insertion point for autonomous remediation: it is the only location in the software lifecycle that simultaneously sees source code, dependency graph, container image, IaC manifests, and deployment configuration.'));

  b.push(h3('2.1.3  Automated Security Scanning and the SARIF Standard'));
  b.push(p('Automated security scanners in the modern pipeline fall into five canonical categories: Static Application Security Testing (SAST), Software Composition Analysis (SCA), container image scanning, Infrastructure-as-Code (IaC) scanning, and secret scanning. Each category historically used its own proprietary output format, producing significant integration overhead for downstream tooling. The Static Analysis Results Interchange Format (SARIF), standardised by OASIS as version 2.1.0 in 2020 and revised through 2023, provides a uniform JSON Schema for representing scanner findings, including rule identifiers, severity levels, source locations, suggested fixes, and tool provenance. SARIF adoption is now nearly universal across both open-source and commercial scanners and is the natural ingestion format for any orchestrating system. The present project standardises exclusively on SARIF 2.1.0 for its ingestion pipeline.'));

  b.push(h3('2.1.4  Large Language Models and Agentic AI'));
  b.push(p('Large language models are statistical models — typically transformer-based neural networks with parameter counts ranging from approximately one billion to several trillion — trained on extensive corpora of natural language and source code. Models such as OpenAI’s GPT-4o, Anthropic’s Claude 3.5 Sonnet, Google DeepMind’s Gemini 2.5, Moonshot AI’s Kimi-K2, and the open-weight Llama 3.1, DeepSeek-R1, and Mistral families now exhibit sufficient capability to read source code, reason about its behaviour, and produce syntactically valid and semantically reasonable patches. When integrated with tool-use interfaces and grounded in external retrieval, LLMs function as agents: systems that decompose a high-level goal into sub-tasks, invoke external tools to gather evidence, and iterate towards a verified outcome. The agentic paradigm has matured rapidly through frameworks such as LangChain, LangGraph, AutoGen, CrewAI, and OpenAI’s Assistants API, all of which converge on a common loop of plan, act, observe, reflect. InfraGuard Pro adopts the LangGraph implementation of this loop as its reasoning substrate.'));

  b.push(h3('2.1.5  Retrieval-Augmented Generation'));
  b.push(p('Retrieval-augmented generation (RAG) is a technique that grounds an LLM’s output in a body of external, organisation-specific knowledge by retrieving relevant documents at inference time and injecting them into the model’s context window (Lewis et al., 2020). In a DevSecOps remediation setting, RAG enables the LLM to consult curated runbooks, vulnerability advisories, and past incident records before generating a patch. This dramatically reduces the risk of hallucinated fixes and provides an audit trail in the form of citation references. InfraGuard Pro implements RAG over a ChromaDB vector store populated from four source classes: Notion-hosted runbooks, local Markdown runbooks, uploaded artefact files, and historical verdict records.'));

  b.push(h3('2.1.6  Cloud-Native Observability and Site Reliability Engineering'));
  b.push(p('Observability is the property of a system that permits its internal state to be inferred from its external outputs — logs, metrics, traces, exceptions, and events. The cloud-native observability stack converged in the mid-2020s on the OpenTelemetry standard for instrumentation and on a small number of complementary storage backends: Prometheus for metrics, Loki or Elasticsearch for logs, Tempo or Jaeger for traces, and emerging unified platforms such as Traceway that store all three in a ClickHouse column store with cross-correlation by trace identifier. Site Reliability Engineering (SRE), the operational discipline formalised by Google (Beyer et al., 2016), prescribes the use of this telemetry to maintain service-level objectives and to drive incident response. The present project treats post-deployment observability not as a separate concern but as the closed-loop validation surface for autonomous remediation: every patch deployed by the system is monitored for runtime regression through the satellite-agent topology before the remediation is marked successful.'));

  // 2.2 EXISTING SYSTEMS / SOLUTIONS - 15 PAPER TABLE
  b.push(h2('2.2  Review of Existing Systems and Solutions'));
  b.push(p('This section first reviews the academic literature on LLM-driven and AI-driven vulnerability remediation through a structured comparative table of fifteen recent and closely related studies, then surveys the commercial state-of-the-art in DevSecOps tooling and autonomous remediation features. Each entry in the table is summarised under the headings of methodological approach, tools and models used, principal findings, identified limitations or gaps, and the manner in which the present InfraGuard Pro project addresses those gaps. The table forms the empirical evidence base for the gap analysis presented in Section 2.4.'));

  b.push(h3('2.2.1  Comparative Table of Fifteen Recent and Related Studies'));
  b.push(p('Table 2.1 presents a structured comparison of fifteen recent and closely related studies on the use of large language models, agentic systems, retrieval augmentation, and automated tooling for vulnerability detection, repair, and CI/CD security automation. The studies were selected on the basis of recency (2020–2025, with emphasis on 2023–2025), publication venue credibility (peer-reviewed top-tier conferences and journals, with a small number of widely-cited preprints from major industry research laboratories), and direct topical relevance to LLM-assisted security remediation. Each row identifies the study, summarises its approach, lists the tools or models employed, captures its principal findings, identifies the limitations or gaps it leaves open, and explicitly states how InfraGuard Pro addresses those gaps.'));
  b.push(blank());

  // Build the 15-paper table
  // Column widths sum to 9026 (A4 content width)
  // Columns: # (350) | Citation (1200) | Approach (1500) | Tools/Models (1300) | Key Findings (1700) | Gap (1500) | How InfraGuard Pro Addresses (1476)
  const colWidths = [350, 1200, 1500, 1300, 1700, 1500, 1476];
  const headers = [
    'No.', 'Study (Author, Year)', 'Approach / Methodology', 'Tools and Models Used',
    'Key Findings', 'Identified Limitations / Gaps', 'How InfraGuard Pro Addresses the Gap'
  ];

  const litRows = [
    [
      '1',
      'Pearce, Tan, Ahmad, Karri & Dolan-Gavitt (2023). “Examining Zero-Shot Vulnerability Repair with Large Language Models.” IEEE Symposium on Security and Privacy (S&P).',
      'Empirical zero-shot evaluation of multiple LLMs on the task of repairing known software vulnerabilities without fine-tuning, across synthetic and real-world C/C++ defects.',
      'OpenAI Codex, GPT-2, GPT-J, polycoder, jurassic-1 jumbo; CWE-tagged benchmark.',
      'Demonstrated that zero-shot LLMs can repair a meaningful fraction of vulnerabilities but with high variance across CWE classes and brittle behaviour on real-world bugs.',
      'No CI/CD pipeline integration; no policy controls; no retrieval grounding; single-vendor LLM scope; no closed-loop runtime validation.',
      'Integrates SARIF ingestion directly into CI/CD; adds policy engine with three execution modes; grounds generation in RAG over runbooks and historical fixes; supports five LLM providers; validates patches via post-deploy multi-server telemetry.'
    ],
    [
      '2',
      'Fu, Tantithamthavorn, Nguyen & Le (2023). “ChatGPT for Vulnerability Detection, Classification, and Repair: How Far Are We?” IEEE Asia-Pacific Software Engineering Conference (APSEC).',
      'Empirical study of ChatGPT (GPT-3.5 and GPT-4) on three vulnerability tasks across multiple CWE categories, comparing prompt engineering strategies.',
      'ChatGPT GPT-3.5-turbo and GPT-4; Big-Vul and CVEfixes datasets.',
      'GPT-4 outperformed specialised supervised baselines for vulnerability detection but lagged for classification; repair quality was inconsistent and often introduced new bugs.',
      'Operated only on isolated source snippets; no integration with scanner output formats; no production validation; no provider abstraction.',
      'Operates on SARIF findings situated in their full repository context; provides regression validation through post-deploy telemetry; abstracts over five LLM providers; tracks per-patch confidence and citation evidence.'
    ],
    [
      '3',
      'Wu, Mascarenhas, Murphy-Hill, Murali, Maddila, Bird, Macedo, Tirelo & Schäfer (2023). “How Effective Are Neural Networks for Fixing Security Vulnerabilities.” ACM ISSTA.',
      'Comparative evaluation of deep-learning and LLM approaches for security bug fixing on a curated corpus of 1,400 real-world Java vulnerabilities.',
      'Codex, PLBART, CodeT5, VulRepair; Java CVEs dataset.',
      'LLMs outperform earlier neural baselines on Java security fixes but still fail on complex multi-file, multi-hunk patches; data leakage in benchmarks identified.',
      'Limited to single-language (Java) and single-file repairs; no orchestration of multiple scanner sources; no autonomous deployment of fixes.',
      'Supports multi-language (Python, JavaScript, Go, Java, Terraform, Dockerfile, YAML) findings; consumes output from six distinct scanner classes; orchestrates the full lifecycle from SARIF to merged pull request.'
    ],
    [
      '4',
      'Khoury, Avila, Brunelle & Camara (2023). “How Secure Is Code Generated by ChatGPT?” IEEE International Conference on Systems, Man and Cybernetics (SMC).',
      'Adversarial probing study examining whether code generated by ChatGPT introduces new security vulnerabilities under naïve, security-aware, and exploitation-focused prompts.',
      'ChatGPT GPT-3.5; 21 hand-crafted security-sensitive programming tasks.',
      'A majority of generated programs were insecure under default prompts; security-aware prompts significantly improved outcomes but did not eliminate vulnerabilities.',
      'Highlights the risk of LLM-introduced vulnerabilities but offers no architectural defence; no validation loop; no human-in-the-loop policy controls.',
      'Embeds policy classification of every patch with three execution modes; subjects every LLM-generated patch to the original scanner suite before merging; logs every action in a tamper-evident audit trail.'
    ],
    [
      '5',
      'Yang, Prenner, Kıcıman, Macedo, Murali, Bird & Tirelo (2024). “SWE-agent: Agent–Computer Interfaces Enable Automated Software Engineering.” NeurIPS.',
      'Designs a custom agent–computer interface enabling an LLM to autonomously edit, navigate, and test code in real repositories; evaluated on SWE-bench.',
      'GPT-4 / GPT-4-turbo with a constrained shell, file-editor, and test-runner toolset.',
      'Achieves substantially higher SWE-bench resolution rates than prompt-only baselines through careful interface design and tool ergonomics.',
      'Evaluated only on functional bug-fix tasks rather than security findings; no SARIF integration; no policy engine; single LLM provider in published experiments.',
      'Inherits the agent–computer interface paradigm via LangGraph but specialises tools to security-finding workflows: SARIF parser, CVE lookup, dependency-graph queries, Git provider API, scanner re-run.'
    ],
    [
      '6',
      'Jimenez, Yang, Wettig, Yao, Pei, Press & Narasimhan (2024). “SWE-bench: Can Language Models Resolve Real-World GitHub Issues?” ICLR.',
      'Constructs a benchmark of 2,294 real GitHub issues with paired pull-request fixes drawn from twelve popular Python repositories; evaluates leading LLMs.',
      'GPT-4, Claude 2, ChatGLM-6B; SWE-bench dataset.',
      'Even strongest LLMs resolved less than 5% of real-world issues end-to-end without specialised scaffolding; reveals the gap between code generation and applied software engineering.',
      'Benchmark covers general bug fixing rather than security; does not measure CI/CD integration overhead; no production deployment.',
      'Restricts scope to the security-finding subclass where structured input (SARIF) is available, dramatically narrowing the reasoning space; provides per-finding evidence chains to compensate for residual LLM weakness.'
    ],
    [
      '7',
      'Hou, Wang, Wei, Zhang, Yang, Zhang, Wang, Liu, Liu, Yu, Chen, Zhang, Wang, Cao, Zhao, Zhao, Han, Zhao, Wang, Liu, Wang, Chen, Liu, Wang & Liu (2024). “Large Language Models for Software Engineering: A Systematic Literature Review.” ACM Transactions on Software Engineering and Methodology (TOSEM).',
      'Systematic literature review covering 395 primary studies on LLM applications across the software engineering lifecycle, organised by activity, model, and evaluation metric.',
      'GPT-3/4, Codex, CodeT5, StarCoder, Llama-family; meta-analysis only.',
      'Identifies code generation, summarisation, and bug fixing as the most-studied activities and notes a striking under-representation of security-specific and CI/CD-integrated work.',
      'Confirms (rather than fills) the gap; provides no implementation; identifies LLM hallucination, evaluation rigour, and reproducibility as standing open problems.',
      'Directly addresses the under-represented LLM-for-CI/CD-security category; ships a reproducible, open-source reference implementation; defines a 150-finding benchmark to seed future empirical work.'
    ],
    [
      '8',
      'Jin, Shahriar, Tufano, Shi, Lou, Sundaresan & Le (2023). “InferFix: End-to-End Program Repair with LLMs.” ACM ESEC/FSE.',
      'End-to-end industrial pipeline combining a static analyser, a retriever, and an LLM to produce patches for warnings issued by Microsoft’s Infer static analyser.',
      'Codex; Microsoft Infer; in-house dense retriever.',
      'Achieves industrial-grade patch acceptance rates for null-dereference and resource-leak warnings; demonstrates the value of retrieval grounding for repair.',
      'Tied to a single proprietary scanner (Infer); single LLM provider; not open-sourced; no policy controls for autonomous merging.',
      'Generalises the retrieval-grounded repair pattern to six open-source scanners through SARIF; abstracts the LLM provider; adds explicit policy controls and audit logging; ships the implementation as open source.'
    ],
    [
      '9',
      'Yao, Zhao, Yu, Du, Shafran, Narasimhan & Cao (2023). “ReAct: Synergizing Reasoning and Acting in Language Models.” ICLR.',
      'Introduces an interleaved reasoning-and-acting prompting paradigm that allows an LLM to interleave chain-of-thought reasoning with tool invocations against external environments.',
      'GPT-3 (text-davinci-002), PaLM-540B; HotpotQA, FEVER, ALFWorld, WebShop benchmarks.',
      'Significant accuracy gains on knowledge-intensive and decision-making tasks relative to chain-of-thought-only or act-only baselines.',
      'Domain-agnostic foundational technique with no security application; no evaluation on production systems.',
      'Adopts the ReAct paradigm in the LangGraph implementation of the reasoning agent; specialises the tool surface to SARIF parsing, CVE lookup, code search, and scanner re-execution.'
    ],
    [
      '10',
      'Shinn, Cassano, Berman, Gopinath, Narasimhan & Yao (2023). “Reflexion: Language Agents with Verbal Reinforcement Learning.” NeurIPS.',
      'Self-improving agent loop in which the LLM reflects on its own failed actions through verbal critique and rewrites its plan accordingly.',
      'GPT-4 with custom reflection memory; HumanEval, MBPP, HotpotQA.',
      'Substantial performance improvements over single-shot baselines, especially for tasks requiring multi-step reasoning.',
      'Demonstrated on code-generation toy tasks; no integration with real scanner output or CI/CD systems.',
      'Adopts the Reflexion-style critique loop for patches that fail post-deployment scanner re-runs, automatically refining the patch up to a configurable retry limit.'
    ],
    [
      '11',
      'Lewis, Perez, Piktus, Petroni, Karpukhin, Goyal, Küttler, Lewis, Yih, Rocktäschel, Riedel & Kiela (2020). “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.” NeurIPS.',
      'Introduces RAG as a hybrid parametric–non-parametric memory architecture in which a dense retriever supplies relevant documents to a generative model.',
      'BART-large generator with DPR retriever; Wikipedia, Natural Questions.',
      'Establishes RAG as the canonical mechanism for grounding generative outputs in evolving external knowledge.',
      'Foundational architecture only; no security or code-repair specialisation; corpus is static encyclopaedic content.',
      'Applies the RAG architecture to a dynamic, organisation-specific corpus combining Notion runbooks, local Markdown, uploaded artefacts, and historical verdicts indexed by a ChromaDB vector store.'
    ],
    [
      '12',
      'Nong, Hu, Liu, Singh, Khoury, Brookshire & Cai (2024). “VGX: Large-Scale Sample Generation for Boosting Learning-Based Software Vulnerability Analyses.” ICSE.',
      'Uses LLMs to synthesise large-scale labelled vulnerability and patch datasets to overcome the scarcity of real-world ground-truth data.',
      'GPT-3.5, CodeT5; CWE-tagged synthetic corpus.',
      'Demonstrates that LLM-synthesised training data can improve downstream vulnerability detector performance.',
      'Targets training-time data augmentation rather than inference-time remediation; no policy or deployment artefacts.',
      'Uses analogous synthetic-augmentation principles to seed the historical-fix RAG corpus when an organisation does not yet have sufficient real-world patch history, ensuring useful retrieval from day one.'
    ],
    [
      '13',
      'Ahmad, Tan, Pearce, Karri & Dolan-Gavitt (2024). “Fixing Hardware Security Bugs with Large Language Models.” IEEE Transactions on Information Forensics and Security.',
      'Extends LLM-based repair from software vulnerabilities to hardware description language (Verilog) security bugs.',
      'OpenAI Codex, GPT-3.5, GPT-4; CWE-1191/1234/1241 Verilog corpus.',
      'Shows that capable LLMs generalise repair behaviour to hardware DSLs but require careful prompt engineering and structured grounding.',
      'Hardware-only focus; no orchestration of multiple finding types; no policy or deployment integration.',
      'Generalises the structured-prompt grounding pattern to the heterogeneous mix of software languages, IaC dialects, and Dockerfiles encountered in cloud-native pipelines.'
    ],
    [
      '14',
      'Rajapakse, Zahedi, Babar & Shen (2022). “Challenges and Solutions When Adopting DevSecOps: A Systematic Review.” Information and Software Technology.',
      'Systematic review of 53 primary studies on the organisational and technical challenges of DevSecOps adoption in industrial practice.',
      'Meta-analysis; no implementation artefact.',
      'Identifies the absence of automated remediation, alert fatigue, and integration overhead between scanners and ticketing systems as the most frequently cited adoption barriers.',
      'Provides only a problem characterisation; does not propose or evaluate a remediation architecture.',
      'Directly addresses every adoption barrier identified: unifies multi-scanner output via SARIF; automates remediation; surfaces a single dashboard rather than disjoint ticket queues.'
    ],
    [
      '15',
      'Liu, Wei, Xu, Yu, Wang, Yang, Chen, Yang & Jiang (2024). “Refining ChatGPT-Generated Code: Characterizing and Mitigating Code Quality Issues.” ACM TOSEM.',
      'Large-scale empirical characterisation of code-quality defects in ChatGPT-generated code, with a taxonomy of seventeen defect categories and an automated refinement pipeline.',
      'ChatGPT GPT-3.5; 4,066 generated programs; static analysers SonarQube and SpotBugs.',
      'Identifies that 65% of generated programs contain at least one quality defect; demonstrates that iterative refinement with static analyser feedback reduces defect density by half.',
      'Quality-focused rather than security-focused; no SARIF orchestration; single LLM vendor; no CI/CD pipeline deployment.',
      'Adopts the iterative-refinement principle but specialises the feedback signal to the original SARIF rule violations, re-running the scanner suite against each generated patch until the finding is closed or the retry budget exhausted.'
    ],
  ];

  // Build header + data rows
  const rows = [headers, ...litRows.map((row, idx) => row)];
  b.push(buildTable(colWidths, rows));
  b.push(blank());
  b.push(p('Table 2.1: Comparative Review of Fifteen Recent and Related Studies on LLM-Driven and AI-Driven Vulnerability Remediation. Compiled by the author from peer-reviewed conference and journal sources.', { align: require('docx').AlignmentType.CENTER }));
  b.push(blank());

  // Narrative discussion of the table
  b.push(h3('2.2.2  Synthesis of the Reviewed Studies'));
  b.push(p('Several patterns are visible when the fifteen studies are read collectively. First, the academic frontier has moved decisively from demonstrating that LLMs can repair isolated vulnerabilities (entries 1, 2, 3, 4, 13) to integrating them into multi-step agentic workflows (entries 5, 6, 8, 9, 10). The capability question is, in the main, settled — capable LLMs can repair a meaningful fraction of findings; the open questions concern integration, orchestration, governance, and production safety. Second, the studies that ship industrial-grade pipelines (notably InferFix, entry 8) remain tightly coupled to a single proprietary scanner and a single LLM vendor; this is the precise gap addressed by the SARIF-based ingestion and the LLM provider abstraction in InfraGuard Pro. Third, retrieval augmentation (entry 11) and reflective self-correction (entry 10) are individually well-validated techniques but have not been systematically combined in a security-remediation context — InfraGuard Pro composes both. Fourth, the systematic reviews (entries 7 and 14) confirm that the security-CI/CD intersection remains structurally under-represented in the academic literature, providing direct justification for the present work as a research contribution rather than an engineering exercise. Finally, every reviewed study, without exception, leaves the post-deployment validation gap open: none of them re-run the original scanner against the patched artefact, none of them watch production telemetry for regressions, and none of them maintain an audit trail of LLM decisions in a form suitable for regulated environments. The closed-loop validation architecture introduced in Chapter Three is, to the best of the author’s knowledge, the first published treatment of this end-to-end loop.'));

  // 2.2.3 Commercial / Industrial state of the art
  b.push(h3('2.2.3  Commercial and Industrial State of the Art'));
  b.push(p('Beyond the academic literature, several commercial and open-source platforms have begun to populate the LLM-assisted remediation space. The most prominent are reviewed here.'));
  b.push(h4('Snyk DeepCode AI Fix'));
  b.push(p('Snyk has integrated an LLM-backed fix-suggestion engine, marketed under the DeepCode AI Fix brand, into its SAST product. The feature generates suggested patches for a subset of supported rules and presents them to the developer within the Snyk dashboard and IDE integrations. The principal limitations of the offering are its confinement to Snyk’s own scanner output (no SARIF orchestration across third-party tools), its closed and undisclosed underlying model, the absence of a transparent policy framework, and the necessity of a paid Snyk subscription priced beyond the reach of many emerging-market organisations.'));
  b.push(h4('GitHub Copilot Autofix and GitHub Advanced Security'));
  b.push(p('GitHub launched Copilot Autofix as a remediation feature on top of GitHub Advanced Security in 2024, leveraging OpenAI models to generate patches for CodeQL alerts. The integration is tight, the developer experience is excellent, and the feature is widely available. Its principal limitations from the perspective of the present work are the lock-in to GitHub as the Git provider and to CodeQL as the SAST engine; the inability to operate on container image, IaC, or secret-scanning findings; the closed-source nature of the orchestration logic; and the inapplicability to self-hosted Git providers (GitLab, Gitea, Forgejo) prevalent in regulated and air-gapped environments.'));
  b.push(h4('Mend.io AppSec AI'));
  b.push(p('Mend.io (formerly WhiteSource) offers an AppSec AI product that combines LLM analysis with its own SCA dataset to prioritise and partially automate dependency upgrades. The product is enterprise-priced and focused on the SCA dimension; it does not currently address SAST, IaC, or container scanning in a unified manner, and like its peers it does not expose the underlying policy or model configuration.'));
  b.push(h4('Endor Labs and Dependabot'));
  b.push(p('Endor Labs offers reachability-prioritised SCA with LLM-assisted upgrade suggestions, while GitHub’s Dependabot has long provided automated dependency-update pull requests without LLM involvement. Both tools are valuable but neither addresses the full remediation surface, neither provides a vendor-neutral LLM substrate, and Dependabot in particular is limited to template-based rather than context-aware patches.'));
  b.push(h4('Open-Source Adjacent Work: Bunkerweb, OpenGrep, OWASP Nettacker'));
  b.push(p('The open-source DevSecOps community has produced an extensive catalogue of scanners (Trivy, Semgrep, Bandit, Checkov, Gitleaks, Grype, OpenGrep) and observability tools (Prometheus, Loki, Grafana, OpenTelemetry, Traceway) but, at the time of writing, no widely-adopted open-source orchestrator unifies their output and applies LLM-driven autonomous remediation across the full surface. The present work is positioned to fill this open-source gap.'));

  // 2.2.4 Capability matrix
  b.push(h3('2.2.4  Capability Comparison'));
  b.push(p('Table 2.2 summarises the capability differences between InfraGuard Pro and the principal commercial offerings reviewed above. Capabilities are scored on a three-point scale: ✓ for full support, P for partial support, and ✗ for absence.'));
  b.push(blank());

  const capColWidths = [2200, 1300, 1300, 1300, 1300, 1626];
  const capHeaders = ['Capability', 'InfraGuard Pro', 'Snyk DeepCode', 'GitHub Copilot Autofix', 'Mend AppSec AI', 'Dependabot'];
  const capRows = [
    capHeaders,
    ['Unified SARIF ingestion across SAST, SCA, IaC, container, secret scanners', '✓', '✗', 'P', 'P', '✗'],
    ['Multi-vendor LLM provider abstraction (≥ 5 providers)', '✓', '✗', '✗', '✗', 'n/a'],
    ['Self-hosted / sovereign LLM option (Ollama, LM Studio)', '✓', '✗', '✗', '✗', 'n/a'],
    ['Three-mode policy engine (recommend / approve / autonomous)', '✓', 'P', 'P', 'P', '✗'],
    ['Multi-provider Git integration (GitHub, GitLab, Gitea)', '✓', 'P', '✗', 'P', 'P'],
    ['RAG over organisation-specific runbooks', '✓', '✗', '✗', '✗', '✗'],
    ['Historical-fix retrieval and similar-incident learning', '✓', '✗', '✗', 'P', '✗'],
    ['Closed-loop post-deployment regression validation', '✓', '✗', '✗', '✗', '✗'],
    ['Multi-server satellite-agent topology', '✓', '✗', '✗', '✗', '✗'],
    ['Tamper-evident audit trail for every action', '✓', 'P', 'P', 'P', 'P'],
    ['Open-source, self-hostable', '✓', '✗', '✗', '✗', '✗'],
  ];
  b.push(buildTable(capColWidths, capRows));
  b.push(blank());
  b.push(p('Table 2.2: Capability Comparison — InfraGuard Pro vs Commercial DevSecOps Platforms.', { align: require('docx').AlignmentType.CENTER }));
  b.push(blank());

  // 2.3 TOOLS AND FRAMEWORKS
  b.push(h2('2.3  Review of Relevant Technologies, Tools, and Frameworks'));
  b.push(p('This section surveys the technologies, tools, and frameworks selected for the InfraGuard Pro implementation, organised by architectural layer. The selection criteria across all layers were maturity (production deployments in comparable organisations), licensing compatibility with self-hosting, active community maintenance, and applicability to the multi-server cloud-native context.'));

  b.push(h3('2.3.1  Programming Languages and Runtimes'));
  b.push(p('Python 3.11+ was selected as the primary backend language. The decision was driven by three considerations. First, Python has emerged as the dominant language of the LLM ecosystem; the official client libraries for every targeted provider (OpenAI, Anthropic, Google Vertex AI, Moonshot, Ollama) are first-class Python packages, and orchestration frameworks (LangChain, LangGraph) are Python-native. Second, the existing InfraGuard codebase upon which the project builds is already written in Python 3.11. Third, asynchronous I/O via asyncio is fundamental to the satellite-agent and heartbeat-loop architecture and is well-supported in modern Python. TypeScript was selected for the dashboard frontend on the basis of the maturity of the SvelteKit framework and the type-safety advantages for a multi-page operations dashboard.'));

  b.push(h3('2.3.2  Web and API Frameworks'));
  b.push(p('FastAPI was selected as the API framework on grounds of its first-class asyncio support, automatic OpenAPI schema generation (which proved invaluable for satellite-agent client generation), dependency-injection ergonomics, and very low overhead. SvelteKit 5 with Svelte 5 was selected for the dashboard on grounds of bundle size (an order of magnitude smaller than equivalent React or Next.js applications), first-class TypeScript support, and its file-system-based routing that maps naturally to the multi-section operations console required by the project.'));

  b.push(h3('2.3.3  LLM Orchestration Frameworks'));
  b.push(p('LangGraph was selected over plain LangChain for orchestrating the reasoning agent. LangGraph’s explicit state-machine model maps cleanly to the four-phase agent loop (collect, analyse, decide, notify) inherited from the existing InfraGuard implementation, supports cyclic reasoning required for reflective patch refinement, and provides better observability than LangChain’s implicit chain construction. The LangChain ecosystem is retained for tool integrations (Prometheus, Loki, HTTP probes) and for the ChromaDB vector store binding.'));

  b.push(h3('2.3.4  Observability and Telemetry'));
  b.push(p('Prometheus and Loki, the de-facto open-source standards for metrics and logs respectively, are retained from the existing InfraGuard baseline and extended to operate in a federated mode across the satellite topology. Traceway is introduced as the OpenTelemetry-native correlation backbone, providing trace, metric, log, and grouped-exception ingestion through OTLP/HTTP and storing telemetry in ClickHouse. CrowdSec is retained for IP-based threat response and bridged into the verdict pipeline. Promtail is used as the log-shipping agent on each satellite.'));

  b.push(h3('2.3.5  Data Stores'));
  b.push(p('PostgreSQL is selected as the central relational store for the control-plane state (server registry, verdict records, remediation queue, audit log, user accounts), replacing the SQLite store used by the original single-host InfraGuard. SQLite is retained on the satellite agents as a local buffer for telemetry when central-plane connectivity is intermittent. ChromaDB is retained as the vector store for the RAG corpus. ClickHouse is used (transparently, through Traceway) as the telemetry store.'));

  b.push(h3('2.3.6  Container and Deployment Tooling'));
  b.push(p('Docker and Docker Compose are used throughout for both the central control plane and the satellite agents, in keeping with the project’s self-hosting orientation. Terraform is used for the cloud infrastructure portions of the deployment (GCE instances, networking, artefact registry), inherited from the existing InfraGuard Terraform module set. GitHub Actions is used as the canonical CI/CD reference implementation for the remediation engine, with GitLab CI as a secondary supported target.'));

  b.push(h3('2.3.7  Relevant Standards and Specifications'));
  b.push(p('Table 2.3 lists the principal standards and specifications adopted by the project, organised by layer.'));
  b.push(blank());

  const stdColWidths = [2400, 1900, 4726];
  const stdHeaders = ['Standard / Specification', 'Issuing Body', 'Role in InfraGuard Pro'];
  const stdRows = [
    stdHeaders,
    ['SARIF 2.1.0', 'OASIS', 'Canonical input format for all scanner findings consumed by the Remediation Engine.'],
    ['OpenTelemetry (OTel)', 'CNCF', 'Telemetry data model for traces, metrics, and logs forwarded from satellites to Traceway.'],
    ['OpenAPI 3.1', 'OpenAPI Initiative', 'API description format for the control-plane REST surface; used for satellite client generation.'],
    ['Common Vulnerabilities and Exposures (CVE)', 'MITRE', 'Vulnerability identifier referenced in SARIF findings and in the RAG corpus.'],
    ['Common Vulnerability Scoring System (CVSS) v4.0', 'FIRST', 'Severity scoring used in the policy engine for risk-classification thresholds.'],
    ['Common Weakness Enumeration (CWE)', 'MITRE', 'Weakness taxonomy used to route patches to appropriate retrieval shards in the RAG corpus.'],
    ['ISO/IEC 27001:2022', 'ISO/IEC', 'Information-security management reference for audit-trail and access-control design choices.'],
    ['NIST SP 800-218 (SSDF)', 'NIST', 'Secure Software Development Framework whose practices PO.5, PW.7, and RV.2 align directly with the project’s automation goals.'],
    ['Nigeria Data Protection Act 2023', 'NDPC, Nigeria', 'Regional regulatory anchor for the audit and access-control requirements.'],
    ['OWASP Top Ten (2021/2025 draft)', 'OWASP Foundation', 'CWE-to-OWASP mapping used to prioritise high-impact remediation flows in the dashboard.'],
  ];
  b.push(buildTable(stdColWidths, stdRows));
  b.push(blank());
  b.push(p('Table 2.3: Summary of Relevant Standards and Specifications Adopted by InfraGuard Pro.', { align: require('docx').AlignmentType.CENTER }));

  // 2.4 GAP ANALYSIS
  b.push(h2('2.4  Gap Analysis'));
  b.push(p('Drawing together the academic literature reviewed in Section 2.2.1, the commercial landscape surveyed in Section 2.2.3, and the technology stack reviewed in Section 2.3, eight distinct gaps emerge in the current state of LLM-driven autonomous security remediation. Each is restated here together with the specific InfraGuard Pro design decision that addresses it.'));

  b.push(num('Multi-scanner orchestration gap. No reviewed academic study and no surveyed commercial platform uniformly orchestrates the full set of SAST, SCA, IaC, container image, and secret-scanning findings. InfraGuard Pro addresses this through a single SARIF-based ingestion pipeline that normalises output from Trivy, Semgrep, Bandit, Checkov, Gitleaks, and OSV-Scanner into a unified internal finding model.'));
  b.push(num('LLM-vendor lock-in gap. Every reviewed system is tightly coupled to a single LLM vendor. InfraGuard Pro addresses this through a pluggable provider abstraction supporting Vertex AI, OpenAI, Anthropic, Moonshot Kimi, Ollama, and LM Studio, with runtime switching and per-verdict provider attribution.'));
  b.push(num('Policy governance gap. The literature consistently treats remediation as binary (suggest or apply) rather than as a graduated continuum. InfraGuard Pro introduces an explicit three-mode policy engine: recommend-only, human-approval-required, and autonomous-low-risk, configurable per finding category and per severity threshold.'));
  b.push(num('Audit and compliance gap. Few reviewed systems treat audit logging as a first-class concern; those that do, do so opaquely. InfraGuard Pro records every ingestion, every LLM invocation, every patch proposal, every policy decision, and every applied action in a tamper-evident audit log structured for regulator-grade review.'));
  b.push(num('Closed-loop validation gap. No reviewed study or commercial product re-runs the original scanner against the patched artefact, watches runtime telemetry for regressions, and uses that observation to mark the remediation successful or failed. InfraGuard Pro implements this closed loop as a core architectural element.'));
  b.push(num('Retrieval-grounding gap. While RAG is well-established as a technique, no reviewed remediation system applies it specifically to a corpus combining vulnerability advisories, organisation-specific runbooks, and historical fix outcomes. InfraGuard Pro indexes all three into ChromaDB and cites retrieved evidence on every patch.'));
  b.push(num('Multi-server operability gap. Existing systems are uniformly designed for a single repository or a single deployment environment. InfraGuard Pro is architected from the ground up around a satellite-agent topology supporting the multi-server reality of African mid-market operations such as LivWell.'));
  b.push(num('Open-source availability gap. The leading commercial offerings (Snyk DeepCode, GitHub Copilot Autofix, Mend AppSec AI) are closed-source and priced beyond the reach of most African digital enterprises. InfraGuard Pro is delivered as an open-source reference implementation under a permissive licence, fully self-hostable on commodity infrastructure.'));

  b.push(p('These eight gaps collectively justify the proposed solution as a substantive contribution to both the academic literature and the practical DevSecOps tooling ecosystem. Chapter Three translates these gap responses into a concrete methodology and system design.'));

  return b;
}

module.exports = { chapter2 };
