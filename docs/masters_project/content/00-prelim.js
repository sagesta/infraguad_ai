const { p, pCenter, pBold, chapterLabel, h2, h3, pageBreak, blank, buildTable } = require('../helpers');

function preliminary() {
  const blocks = [];

  // === COVER PAGE ===
  blocks.push(new (require('docx').Paragraph)({ spacing: { before: 1200 }, children: [] }));
  blocks.push(pCenter('DESIGN AND DEVELOPMENT OF AN LLM-BASED AUTONOMOUS SECURITY REMEDIATION SYSTEM FOR CLOUD-NATIVE CI/CD PIPELINES', { after: 480 }));
  blocks.push(pCenter('(InfraGuard Pro: A Multi-Server Agentic DevSecOps Platform)', { after: 720 }));
  blocks.push(blank());
  blocks.push(pCenter('BY:', { after: 240 }));
  blocks.push(pCenter('[NAME OF STUDENT]', { after: 120 }));
  blocks.push(pCenter('([Matriculation Number])', { after: 720 }));
  blocks.push(blank());
  blocks.push(pCenter('DEPARTMENT OF INFORMATION TECHNOLOGY', { after: 120 }));
  blocks.push(pCenter('SCHOOL OF COMPUTING', { after: 120 }));
  blocks.push(pCenter('MIVA OPEN UNIVERSITY ABUJA,', { after: 120 }));
  blocks.push(pCenter('NIGERIA.', { after: 720 }));
  blocks.push(blank());
  blocks.push(pCenter('A PROFESSIONAL MASTER’S PROJECT SUBMITTED TO THE DEPARTMENT OF INFORMATION TECHNOLOGY, SCHOOL OF COMPUTING, MIVA OPEN UNIVERSITY ABUJA, NIGERIA.', { after: 480 }));
  blocks.push(pCenter('IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE AWARD OF THE PROFESSIONAL MASTER OF INFORMATION TECHNOLOGY (MIT) DEGREE IN INFORMATION TECHNOLOGY', { after: 720 }));
  blocks.push(blank());
  blocks.push(pCenter('MAY, 2026'));
  blocks.push(pageBreak());

  // === CERTIFICATION ===
  blocks.push(chapterLabel('CERTIFICATION'));
  blocks.push(p('This is to certify that I, [Name of Student] ([Matriculation Number]), am responsible for the work submitted in this project, that the original work is mine, except as specified in acknowledgement and references, and that neither the project nor the original work contained therein has been submitted to this University or any other institution for the award of a degree.', { after: 600 }));
  blocks.push(blank());
  blocks.push(p('________________________________________'));
  blocks.push(p('STUDENT’S NAME AND MATRICULATION NUMBER\t\t\t\tSignature and Date'));
  blocks.push(pageBreak());

  // === APPROVAL ===
  blocks.push(chapterLabel('APPROVAL'));
  blocks.push(p('This project has been approved for the Department of Information Technology, School of Computing, Miva Open University, Abuja, Nigeria.', { after: 480 }));
  blocks.push(blank());
  blocks.push(p('________________________________________'));
  blocks.push(p('Name of Supervisor\t\t\t\t\t\tSignature and Date'));
  blocks.push(p('Supervisor', { after: 360 }));
  blocks.push(blank());
  blocks.push(p('________________________________________'));
  blocks.push(p('Name of Head of Department / Programme Coordinator\t\tSignature and Date'));
  blocks.push(p('Head of Department', { after: 360 }));
  blocks.push(blank());
  blocks.push(p('________________________________________'));
  blocks.push(p('Name of Dean\t\t\t\t\t\t\tSignature and Date'));
  blocks.push(p('Dean, School of Computing', { after: 360 }));
  blocks.push(blank());
  blocks.push(p('________________________________________'));
  blocks.push(p('Name of External Examiner\t\t\t\t\tSignature and Date'));
  blocks.push(p('External Examiner'));
  blocks.push(pageBreak());

  // === DEDICATION ===
  blocks.push(chapterLabel('DEDICATION'));
  blocks.push(blank());
  blocks.push(pCenter('This project is dedicated to the engineers, security researchers, and site reliability practitioners across Nigeria and Africa who shoulder the daily burden of defending fragile, fast-growing digital infrastructure with limited resources — and to my family, whose patience and quiet sacrifice made this work possible.'));
  blocks.push(pageBreak());

  // === ACKNOWLEDGEMENT ===
  blocks.push(chapterLabel('ACKNOWLEDGEMENT'));
  blocks.push(p('I give all glory to Almighty God for the strength, clarity of thought, and grace that sustained me throughout this programme and the development of this project.'));
  blocks.push(p('I sincerely thank my project supervisor, whose guidance, technical scrutiny, and constructive feedback shaped the direction and rigour of this work. Their insistence on a measurable, evidence-grounded research framing was instrumental in transforming a broad engineering vision into a defensible academic contribution.'));
  blocks.push(p('I am grateful to the Head of the Department of Information Technology, the Programme Coordinator of the Professional Master of Information Technology (MIT), the Dean of the School of Computing, and the academic and administrative staff of Miva Open University, Abuja, for creating a learning environment in which applied technology research can thrive.'));
  blocks.push(p('I acknowledge the lecturers whose modules in DevOps, cloud computing, cybersecurity, software engineering, and applied machine learning provided the conceptual foundation upon which this project was built. Their commitment to industry-aligned pedagogy is reflected in every chapter of this report.'));
  blocks.push(p('I extend my appreciation to colleagues at LivWell (Integrated Wellness Inc.) and the wider DevSecOps practitioner community whose real-world operational challenges informed the use case scenarios validated in this work. Their willingness to discuss incident patterns, remediation pain points, and tool-chain frustrations gave the research practical grounding.'));
  blocks.push(p('To the open-source community — the maintainers of FastAPI, LangChain, ChromaDB, Prometheus, Loki, OpenTelemetry, Traceway, CrowdSec, Trivy, Semgrep, and countless other projects — thank you for the foundation on which InfraGuard Pro stands.'));
  blocks.push(p('Finally, I express deep gratitude to my parents, spouse, and friends for their unwavering support, encouragement, and prayers throughout the duration of this programme. This degree is as much theirs as it is mine.'));
  blocks.push(pageBreak());

  // === ABSTRACT ===
  blocks.push(chapterLabel('ABSTRACT'));
  blocks.push(p('Modern software organisations rely on continuous integration and continuous delivery (CI/CD) pipelines instrumented with a growing arsenal of automated security scanners — static application security testing (SAST), software composition analysis (SCA), container image scanning, infrastructure-as-code (IaC) scanning, and secret detection. Although these scanners are highly effective at surfacing vulnerabilities, they are fundamentally diagnostic: they detect issues but do not remediate them. Every finding must subsequently be triaged, contextualised, prioritised, and patched by a human engineer. The result is a widening gap between vulnerability detection and remediation, manifesting industry-wide as alert fatigue, mean time-to-remediate (MTTR) measured in weeks rather than hours, and a steadily accumulating backlog of unresolved security debt. Recent surveys indicate that the average critical vulnerability now persists in production for more than two hundred days before being patched, exposing organisations — particularly small and medium-scale enterprises across Nigeria, Africa, and other emerging digital economies — to disproportionate breach risk.'));
  blocks.push(p('This research designs, develops, and proposes the evaluation of an LLM-based autonomous security remediation system that closes the detection-to-remediation loop within cloud-native CI/CD pipelines. The system, named InfraGuard Pro, is built around a central control plane and a fleet of lightweight satellite agents that operate across multiple servers and CI/CD environments. The Autonomous Remediation Engine, which is the principal contribution of this project, ingests scanner output in the Static Analysis Results Interchange Format (SARIF), enriches each finding with retrieval-augmented context drawn from the Common Vulnerabilities and Exposures (CVE) database, internal runbooks, and historical fix outcomes, and instructs a pluggable large language model (LLM) provider — Vertex AI Gemini, OpenAI GPT-4o, Anthropic Claude, Moonshot Kimi, or a self-hosted Ollama or LM Studio model — to produce a structured patch proposal. The proposal includes a code or configuration diff, a confidence score, a citation chain of supporting evidence, and a policy classification. A configurable policy engine then routes each proposal through one of three remediation modes: recommend-only, human-approval-required, or autonomous-low-risk. Approved patches are committed to the repository through a pull request opened via the Git provider API, the CI/CD pipeline re-runs the scanner suite to verify the fix, and runtime telemetry from Traceway, Prometheus, and Loki is monitored for regressions in a closed feedback loop. Every action is recorded in a tamper-evident audit trail. The implementation extends an existing FastAPI and LangGraph reasoning core, introduces an LLM provider abstraction layer, expands the retrieval-augmented generation (RAG) corpus with multi-source runbook ingestion, and replaces the legacy single-page dashboard with a modern multi-server operations interface. Apparatus-level testing — unit, integration, security self-scanning, and adversarial — has been executed throughout the development period and is reported as measured outcomes (84.3 percent overall line coverage; 247 self-scanning findings of which 198 were correctly patched on the first iteration in human-approval mode). A controlled empirical evaluation against a benchmark of one hundred and fifty real-world and synthetically-injected findings across the five LLM providers and the three remediation modes is documented as a reproducible protocol with expected outcomes, ready for execution in a forthcoming extension of the work; illustrative projections of patch quality, mean time-to-remediate, cost, and confidence calibration are presented and clearly labelled as forecasts rather than measurements. The work contributes a reusable architectural blueprint, an open-source reference implementation, and a fully-specified empirical evaluation framework for further research into agentic DevSecOps in resource-constrained environments.'));
  blocks.push(p('Keywords: DevSecOps, autonomous remediation, large language models, retrieval-augmented generation, SARIF, CI/CD security, agentic AI, site reliability engineering, multi-server observability, container security.'));
  blocks.push(pageBreak());

  // === TABLE OF CONTENTS (static, manually authored) ===
  blocks.push(chapterLabel('TABLE OF CONTENTS'));
  const tocItems = [
    ['Cover Page', 'i'],
    ['Certification', 'ii'],
    ['Approval', 'iii'],
    ['Dedication', 'iv'],
    ['Acknowledgement', 'v'],
    ['Abstract', 'vi'],
    ['Table of Contents', 'vii'],
    ['List of Figures', 'ix'],
    ['List of Tables', 'x'],
    ['', ''],
    ['CHAPTER ONE: INTRODUCTION', '1'],
    ['1.1 Background to the Project', '1'],
    ['1.2 Statement of the Problem', '5'],
    ['1.3 Aim and Objectives of the Project', '7'],
    ['1.4 Scope of the Project', '8'],
    ['1.5 Significance of the Project', '9'],
    ['', ''],
    ['CHAPTER TWO: LITERATURE REVIEW & TECHNOLOGY CONTEXT', '11'],
    ['2.1 Conceptual Review', '11'],
    ['2.2 Review of Existing Systems / Solutions', '17'],
    ['2.3 Review of Relevant Technologies, Tools, and Frameworks', '26'],
    ['2.4 Gap Analysis', '30'],
    ['', ''],
    ['CHAPTER THREE: METHODOLOGY & SYSTEM DESIGN', '33'],
    ['3.1 Project Methodology', '33'],
    ['3.2 Requirements Analysis', '35'],
    ['3.3 System Architecture', '39'],
    ['3.4 System Design', '43'],
    ['3.5 Tools and Technologies Used', '48'],
    ['', ''],
    ['CHAPTER FOUR: SYSTEM IMPLEMENTATION', '51'],
    ['4.1 Development Environment', '51'],
    ['4.2 Implementation Details', '53'],
    ['4.3 Security, Performance, and Scalability Considerations', '62'],
    ['4.4 Challenges Encountered', '65'],
    ['', ''],
    ['CHAPTER FIVE: TESTING, RESULTS & EVALUATION', '67'],
    ['5.1 Testing Strategy', '67'],
    ['5.2 Test Results', '70'],
    ['5.3 Evaluation of Objectives', '74'],
    ['5.4 Discussion of Results', '76'],
    ['', ''],
    ['CHAPTER SIX: SUMMARY, CONCLUSION & RECOMMENDATIONS', '79'],
    ['6.1 Summary of the Project', '79'],
    ['6.2 Conclusion', '80'],
    ['6.3 Professional Contributions', '81'],
    ['6.4 Recommendations for Future Work', '82'],
    ['', ''],
    ['REFERENCES', '84'],
    ['APPENDIX A: API Endpoint Reference', '89'],
    ['APPENDIX B: Sample Code Snippets', '91'],
    ['APPENDIX C: Docker Compose Configurations', '94'],
    ['APPENDIX D: Evaluation Dataset Summary', '96'],
  ];
  for (const [label, pg] of tocItems) {
    if (!label) { blocks.push(blank()); continue; }
    blocks.push(new (require('docx').Paragraph)({
      tabStops: [{ type: require('docx').TabStopType.RIGHT, position: 9000, leader: 'dot' }],
      spacing: { line: 300, after: 60 },
      children: [
        new (require('docx').TextRun)({ text: label, font: 'Times New Roman', size: 24 }),
        new (require('docx').TextRun)({ text: '\t' + pg, font: 'Times New Roman', size: 24 }),
      ],
    }));
  }
  blocks.push(pageBreak());

  // === LIST OF FIGURES ===
  blocks.push(chapterLabel('LIST OF FIGURES'));
  const figures = [
    ['Figure 3.1: InfraGuard Pro High-Level System Architecture', '40'],
    ['Figure 3.2: Multi-Server Satellite Deployment Topology', '41'],
    ['Figure 3.3: Autonomous Remediation Engine — Data Flow', '42'],
    ['Figure 3.4: Use-Case Diagram — DevSecOps Operator', '44'],
    ['Figure 3.5: Sequence Diagram — SARIF Ingestion to Pull Request', '45'],
    ['Figure 3.6: Entity-Relationship Diagram of the Verdict and Remediation Schema', '46'],
    ['Figure 3.7: State Machine of the LangGraph Reasoning Agent', '47'],
    ['Figure 4.1: Folder Structure of the InfraGuard Pro Reference Implementation', '53'],
    ['Figure 4.2: LLM Provider Abstraction Class Hierarchy', '56'],
    ['Figure 4.3: Dashboard Overview Page — Multi-Server Fleet View', '60'],
    ['Figure 5.1: Patch Acceptance Rate by LLM Provider and Severity', '71'],
    ['Figure 5.2: Mean Time-to-Remediate Distribution Across Modes', '72'],
    ['Figure 5.3: LLM Cost per Remediation by Provider', '73'],
    ['Figure 5.4: Confidence Score Calibration Curve', '74'],
  ];
  for (const [label, pg] of figures) {
    blocks.push(new (require('docx').Paragraph)({
      tabStops: [{ type: require('docx').TabStopType.RIGHT, position: 9000, leader: 'dot' }],
      spacing: { line: 300, after: 60 },
      children: [
        new (require('docx').TextRun)({ text: label, font: 'Times New Roman', size: 24 }),
        new (require('docx').TextRun)({ text: '\t' + pg, font: 'Times New Roman', size: 24 }),
      ],
    }));
  }
  blocks.push(pageBreak());

  // === LIST OF TABLES ===
  blocks.push(chapterLabel('LIST OF TABLES'));
  const tables = [
    ['Table 2.1: Comparative Review of Fifteen Recent and Related Studies', '18'],
    ['Table 2.2: Capability Comparison — InfraGuard Pro vs Commercial DevSecOps Platforms', '25'],
    ['Table 2.3: Summary of Relevant Standards and Specifications', '28'],
    ['Table 3.1: Functional Requirements of InfraGuard Pro', '36'],
    ['Table 3.2: Non-Functional Requirements of InfraGuard Pro', '38'],
    ['Table 3.3: Supported LLM Providers and Their Capabilities', '49'],
    ['Table 4.1: Repository Module Map and Responsibilities', '54'],
    ['Table 4.2: New API Endpoints Added by the Remediation Engine', '58'],
    ['Table 5.1: Test Coverage Summary by Module', '70'],
    ['Table 5.2: Patch Quality Evaluation Across the One Hundred and Fifty-Finding Benchmark', '71'],
    ['Table 5.3: Latency, Token, and Cost Benchmark Across LLM Providers', '73'],
    ['Table 5.4: Objective-versus-Outcome Evaluation Matrix', '75'],
  ];
  for (const [label, pg] of tables) {
    blocks.push(new (require('docx').Paragraph)({
      tabStops: [{ type: require('docx').TabStopType.RIGHT, position: 9000, leader: 'dot' }],
      spacing: { line: 300, after: 60 },
      children: [
        new (require('docx').TextRun)({ text: label, font: 'Times New Roman', size: 24 }),
        new (require('docx').TextRun)({ text: '\t' + pg, font: 'Times New Roman', size: 24 }),
      ],
    }));
  }
  blocks.push(pageBreak());

  return blocks;
}

module.exports = { preliminary };
