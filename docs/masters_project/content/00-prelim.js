const { p, pCenter, chapterLabel, pageBreak, blank } = require('../helpers');
const { Paragraph, TableOfContents, StyleLevel } = require('docx');

function preliminary() {
  const blocks = [];

  // Cover page. The student name is taken from the existing project defence
  // material. The remaining identity fields are left as writing lines because
  // no verified values are present in the repository.
  blocks.push(new Paragraph({ spacing: { before: 1200 }, children: [] }));
  blocks.push(pCenter('INFRAGUARD AI: AN LLM-DRIVEN OBSERVABILITY AND INCIDENT-TRIAGE AGENT FOR SELF-HOSTED CLOUD-NATIVE INFRASTRUCTURE', { after: 720 }));
  blocks.push(blank());
  blocks.push(pCenter('BY', { after: 240 }));
  blocks.push(pCenter('ADEBODUN SAMUEL TOMOLA', { after: 120 }));
  blocks.push(pCenter('MATRICULATION NUMBER: ____________________', { after: 720 }));
  blocks.push(blank());
  blocks.push(pCenter('DEPARTMENT OF INFORMATION TECHNOLOGY', { after: 120 }));
  blocks.push(pCenter('SCHOOL OF COMPUTING', { after: 120 }));
  blocks.push(pCenter('MIVA OPEN UNIVERSITY, ABUJA', { after: 120 }));
  blocks.push(pCenter('NIGERIA', { after: 720 }));
  blocks.push(blank());
  blocks.push(pCenter('A PROFESSIONAL MASTER\'S PROJECT SUBMITTED TO THE DEPARTMENT OF INFORMATION TECHNOLOGY, SCHOOL OF COMPUTING, MIVA OPEN UNIVERSITY, ABUJA, NIGERIA.', { after: 480 }));
  blocks.push(pCenter('IN PARTIAL FULFILMENT OF THE REQUIREMENTS FOR THE AWARD OF THE PROFESSIONAL MASTER OF INFORMATION TECHNOLOGY DEGREE', { after: 720 }));
  blocks.push(blank());
  blocks.push(pCenter('AUGUST 2026'));
  blocks.push(pageBreak());

  blocks.push(chapterLabel('CERTIFICATION'));
  blocks.push(p('I certify that this project is my original work, except where the work of others is acknowledged through citations and references. The project has not been submitted to this University or another institution for the award of a degree.', { after: 600 }));
  blocks.push(blank());
  blocks.push(p('Student: Adebodun Samuel Tomola'));
  blocks.push(p('Matriculation Number: ____________________'));
  blocks.push(p('Signature: ____________________    Date: ____________________'));
  blocks.push(pageBreak());

  blocks.push(chapterLabel('APPROVAL'));
  blocks.push(p('This project has been approved for the Department of Information Technology, School of Computing, Miva Open University, Abuja, Nigeria.', { after: 480 }));
  blocks.push(blank());
  blocks.push(p('Supervisor: ______________________________'));
  blocks.push(p('Signature: ____________________    Date: ____________________', { after: 360 }));
  blocks.push(blank());
  blocks.push(p('Head of Department or Programme Coordinator: ______________________________'));
  blocks.push(p('Signature: ____________________    Date: ____________________', { after: 360 }));
  blocks.push(blank());
  blocks.push(p('Dean, School of Computing: ______________________________'));
  blocks.push(p('Signature: ____________________    Date: ____________________', { after: 360 }));
  blocks.push(blank());
  blocks.push(p('External Examiner: ______________________________'));
  blocks.push(p('Signature: ____________________    Date: ____________________'));
  blocks.push(pageBreak());

  blocks.push(chapterLabel('DEDICATION'));
  blocks.push(blank());
  blocks.push(pCenter('This project is dedicated to my family and to the engineers who maintain critical digital services with limited operational resources.'));
  blocks.push(pageBreak());

  blocks.push(chapterLabel('ACKNOWLEDGEMENT'));
  blocks.push(p('I thank Almighty God for the strength and opportunity to complete this programme and project.'));
  blocks.push(p('I am grateful to my project supervisor and the staff of the Department of Information Technology for their guidance and criticism throughout the work. Their feedback helped narrow the project to a testable implementation.'));
  blocks.push(p('I also thank colleagues and practitioners who discussed the operational problems that motivated the system, particularly alert fatigue, slow incident triage, and the cost of maintaining several monitoring tools.'));
  blocks.push(p('I acknowledge the maintainers of the open-source software used in the implementation, including FastAPI, LangChain, LangGraph, ChromaDB, Prometheus, Grafana Loki, and CrowdSec.'));
  blocks.push(p('Finally, I thank my family and friends for their patience, encouragement, and support during the programme.'));
  blocks.push(pageBreak());

  blocks.push(chapterLabel('ABSTRACT'));
  blocks.push(p('Cloud-native systems produce logs, metrics, and service events faster than small operations teams can interpret them. Monitoring tools can detect abnormal signals, but an engineer must still correlate the available evidence, identify a likely cause, and decide what to do. This project develops InfraGuard AI, a self-hosted observability and incident-triage system intended to support that first review.'));
  blocks.push(p('The implementation uses a scheduled agent to collect data from Grafana Loki, Prometheus, HTTP probes, and optional Docker sources. A LangGraph workflow sends the collected context to a configured large language model and parses the response into a structured verdict containing severity, summary, root cause, recommended action, and a condition signature. The API and dashboard provide authenticated access to current and historical verdicts, deterministic threat-pattern detection, operator-approved CrowdSec actions, and retrieval over locally indexed Markdown runbooks. The application supports the Gemini Developer API, Anthropic, OpenAI, and local Ollama through a common interface. Only the telemetry included in a prompt is sent to the selected provider.'));
  blocks.push(p('InfraGuard AI identifies recurring conditions by hashing the condition signature, prompt version, and model with SHA-256. When an active acknowledgement matches the hash, the API and dashboard suppress an ok or warning verdict; high and critical verdicts remain visible. The agent still calls the model on every heartbeat, so acknowledgement changes what the operator sees but does not reduce model use. In the verification run, all 80 tests passed and overall line coverage was 66 percent. Coverage for the memory and orchestration modules was 100 percent and 94 percent respectively. Because the tests mock external services, the results establish code behaviour but not live-model diagnostic accuracy or practitioner usability. These two questions require separate studies.'));
  blocks.push(p('Keywords: AIOps, observability, large language models, retrieval-augmented generation, site reliability engineering, incident triage, operator acknowledgement, threat detection, LangGraph.'));
  blocks.push(pageBreak());

  blocks.push(chapterLabel('TABLE OF CONTENTS'));
  blocks.push(new TableOfContents('Contents', {
    headingStyleRange: '1-3',
    hyperlink: true,
  }));
  blocks.push(pageBreak());

  blocks.push(chapterLabel('LIST OF FIGURES'));
  blocks.push(new TableOfContents('Figures', {
    stylesWithLevels: [new StyleLevel('Figure Caption', 1)],
    hyperlink: true,
  }));
  blocks.push(pageBreak());

  blocks.push(chapterLabel('LIST OF TABLES'));
  blocks.push(new TableOfContents('Tables', {
    stylesWithLevels: [new StyleLevel('Table Caption', 1)],
    hyperlink: true,
  }));

  return blocks;
}

module.exports = { preliminary };
