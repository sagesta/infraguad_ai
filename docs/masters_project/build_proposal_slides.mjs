// Builds the proposal defence deck with the bundled artifact-tool runtime.

import fs from "node:fs/promises";
import fsSync from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const runtimeRoot = "C:/Users/adebo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules";
const artifactPath = path.join(runtimeRoot, "@oai", "artifact-tool", "dist", "artifact_tool.mjs");
const data = JSON.parse(await fs.readFile(path.join(__dirname, "proposal_data.json"), "utf8"));
const outputPath = path.join(__dirname, "InfraGuard_Pro_Proposal_Defence.pptx");
const workspace = path.join(
  process.env.TEMP || "C:/Users/adebo/AppData/Local/Temp",
  "codex-presentations",
  "manual-infraguard-proposal"
);
const previewDir = path.join(workspace, "preview");
const manifestPath = path.join(workspace, "artifact-build-manifest.json");

const artifact = await import(pathToFileURL(artifactPath).href);
const { Presentation, PresentationFile } = artifact;
const presentation = Presentation.create({ slideSize: { width: 1280, height: 720 } });

const style = {
  bg: "#F7F6EF",
  ink: "#172026",
  soft: "#607069",
  faint: "#E1E7DD",
  faint2: "#ECE5D8",
  dark: "#172026",
  dark2: "#24332D",
  teal: "#0F766E",
  amber: "#B45309",
  blue: "#1D4ED8",
  red: "#B91C1C",
  white: "#FFFFFF",
  line: "#C4CCC1",
  serif: "Georgia",
  sans: "Aptos",
  mono: "Cascadia Mono"
};

function line(fill = "#00000000", width = 0, dash = "solid") {
  return { style: dash, fill, width };
}

function rect(slide, x, y, w, h, fill, options = {}) {
  return slide.shapes.add({
    geometry: options.geometry || "rect",
    position: { left: x, top: y, width: w, height: h },
    fill,
    line: options.line || line(),
    name: options.name
  });
}

function text(slide, value, x, y, w, h, options = {}) {
  const shape = rect(slide, x, y, w, h, options.fill || "#00000000", {
    line: options.line || line(),
    name: options.name
  });
  shape.text = String(value || "");
  shape.text.fontSize = options.size || 18;
  shape.text.color = options.color || style.ink;
  shape.text.bold = Boolean(options.bold);
  shape.text.typeface = options.face || style.sans;
  shape.text.alignment = options.align || "left";
  shape.text.verticalAlignment = options.valign || "top";
  shape.text.insets = options.insets || { left: 0, right: 0, top: 0, bottom: 0 };
  return shape;
}

function rule(slide, x, y, w, color = style.line, h = 1) {
  return rect(slide, x, y, w, h, color);
}

function bg(slide) {
  rect(slide, 0, 0, 1280, 720, style.bg);
  rule(slide, 64, 650, 1060, style.line, 1);
}

function kicker(slide, label, color = style.teal) {
  rect(slide, 64, 52, 8, 28, color);
  text(slide, label.toUpperCase(), 86, 54, 340, 20, {
    size: 10.5,
    bold: true,
    color: style.soft
  });
}

function title(slide, value, x = 64, y = 92, w = 880, h = 100, size = 35) {
  text(slide, value, x, y, w, h, {
    size,
    face: style.serif,
    bold: true,
    color: style.ink
  });
}

function footer(slide, index, note = "InfraGuard Pro | MIT Project Proposal Defence") {
  text(slide, note, 64, 666, 760, 18, { size: 9.5, color: style.soft });
  text(slide, String(index).padStart(2, "0"), 1150, 660, 60, 26, {
    size: 18,
    face: style.serif,
    bold: true,
    color: style.ink,
    align: "right"
  });
}

function bulletText(slide, items, x, y, w, gap = 42, options = {}) {
  items.forEach((item, idx) => {
    const yy = y + idx * gap;
    rect(slide, x, yy + 7, 7, 7, options.color || style.teal);
    text(slide, item, x + 22, yy, w - 22, options.h || 34, {
      size: options.size || 15,
      color: options.textColor || style.ink
    });
  });
}

function metric(slide, value, label, note, x, y, color = style.teal) {
  rule(slide, x, y + 4, 1, color, 76);
  text(slide, value, x + 18, y, 150, 36, {
    size: 30,
    face: style.serif,
    bold: true,
    color: style.ink
  });
  text(slide, label.toUpperCase(), x + 18, y + 42, 160, 16, {
    size: 8.5,
    bold: true,
    color: style.soft
  });
  text(slide, note, x + 18, y + 60, 170, 20, { size: 9, color: style.soft });
}

async function addImage(slide, imagePath, x, y, w, h, alt) {
  const buffer = await fs.readFile(imagePath);
  const image = slide.images.add({
    dataUrl: `data:image/png;base64,${buffer.toString("base64")}`,
    fit: "contain",
    alt
  });
  image.position = { left: x, top: y, width: w, height: h };
  return image;
}

function slide01() {
  const slide = presentation.slides.add();
  bg(slide);
  rect(slide, 0, 0, 1280, 720, style.dark);
  rect(slide, 64, 56, 8, 56, style.teal);
  text(slide, "MASTER OF INFORMATION TECHNOLOGY PROJECT PROPOSAL", 88, 58, 520, 18, {
    size: 10.5,
    bold: true,
    color: "#B9C7C0"
  });
  text(slide, "InfraGuard Pro", 64, 170, 720, 70, {
    size: 56,
    face: style.serif,
    bold: true,
    color: style.white
  });
  text(slide, data.projectTitle, 66, 258, 720, 96, {
    size: 26,
    face: style.serif,
    bold: true,
    color: "#E8F2EE"
  });
  text(slide, "An LLM-based, policy-controlled remediation platform for cloud-native CI/CD security findings.", 68, 390, 620, 54, {
    size: 18,
    color: "#C9D7D1"
  });
  metric(slide, "4", "research objectives", "requirements, design, implementation, evaluation", 735, 172, style.teal);
  metric(slide, "3", "policy modes", "recommend, approval, autonomous-low-risk", 735, 292, style.amber);
  metric(slide, "1", "closed loop", "scanner re-run plus telemetry validation", 735, 412, "#78A6D8");
  text(slide, `${data.studentName} | ${data.matricNumber}\n${data.university}\n${data.proposalDate}`, 68, 548, 540, 60, {
    size: 13.5,
    color: "#C9D7D1"
  });
  footer(slide, 1, "Proposal defence | Google Meet submission package");
  return slide;
}

function slide02() {
  const slide = presentation.slides.add();
  bg(slide);
  kicker(slide, "Problem");
  title(slide, "Scanners detect vulnerabilities faster than teams can remediate them.");
  text(slide, "Most tools stop at diagnosis. The proposed study focuses on turning scanner findings into safe, auditable, verified fixes.", 66, 198, 780, 48, {
    size: 17,
    color: style.soft
  });
  const bars = [
    ["Scanner output", 280, style.blue],
    ["Manual triage", 210, style.amber],
    ["Patch proposal", 145, style.teal],
    ["Validation", 100, style.red]
  ];
  bars.forEach((bar, idx) => {
    const y = 310 + idx * 72;
    text(slide, bar[0], 98, y + 8, 160, 24, { size: 15, bold: true });
    rect(slide, 285, y, bar[1], 36, bar[2]);
    rule(slide, 285, y + 48, 600, style.line, 1);
  });
  rect(slide, 910, 282, 230, 240, style.dark);
  text(slide, "Core problem", 934, 312, 182, 20, { size: 12, bold: true, color: "#B9C7C0" });
  text(slide, "The gap is not detection. It is policy-controlled remediation with proof that the fix worked.", 934, 350, 178, 112, {
    size: 19,
    face: style.serif,
    bold: true,
    color: style.white,
    align: "center"
  });
  footer(slide, 2);
  return slide;
}

function slide03() {
  const slide = presentation.slides.add();
  bg(slide);
  kicker(slide, "Research Direction", style.amber);
  title(slide, "The whole study will be governed by four aligned objectives.");
  const rows = data.chapterOne.find((section) => section.heading.startsWith("1.3")).objectives;
  rows.forEach((objective, idx) => {
    const x = 78 + idx * 290;
    const color = [style.teal, style.amber, style.blue, style.red][idx];
    text(slide, `0${idx + 1}`, x, 242, 58, 44, {
      size: 34,
      face: style.serif,
      bold: true,
      color
    });
    rule(slide, x + 64, 265, 136, color, 2);
    text(slide, objective.area, x, 312, 220, 28, {
      size: 18,
      face: style.serif,
      bold: true
    });
    text(slide, objective.statement, x, 354, 226, 108, {
      size: 12.5,
      color: style.soft
    });
    text(slide, objective.evidence, x, 496, 226, 46, {
      size: 10.5,
      color
    });
  });
  footer(slide, 3, "Objective alignment | Every methodology and evaluation activity maps back here");
  return slide;
}

function slide04() {
  const slide = presentation.slides.add();
  bg(slide);
  kicker(slide, "Literature Gap");
  title(slide, "Existing LLM repair work rarely covers the full DevSecOps loop.");
  const gaps = data.chapterTwo.find((section) => section.heading.startsWith("2.2")).gaps;
  gaps.forEach((gap, idx) => {
    const y = 226 + idx * 70;
    text(slide, String(idx + 1).padStart(2, "0"), 88, y, 40, 28, {
      size: 23,
      face: style.serif,
      bold: true,
      color: idx % 2 ? style.amber : style.teal
    });
    rule(slide, 140, y + 14, 86, idx % 2 ? style.amber : style.teal, 2);
    text(slide, gap, 250, y - 4, 740, 42, { size: 15, color: style.ink });
  });
  rect(slide, 1008, 214, 158, 346, style.faint2, { line: line(style.line, 1) });
  text(slide, "Proposal stance", 1030, 242, 112, 18, { size: 10, bold: true, color: style.soft, align: "center" });
  text(slide, "Multi-scanner\nMulti-provider\nPolicy-gated\nEvidence-grounded\nClosed-loop", 1028, 290, 116, 172, {
    size: 18,
    face: style.serif,
    bold: true,
    align: "center"
  });
  footer(slide, 4);
  return slide;
}

async function slide05() {
  const slide = presentation.slides.add();
  bg(slide);
  kicker(slide, "Solution", style.blue);
  title(slide, "InfraGuard Pro will convert SARIF findings into validated pull requests.", 64, 92, 780, 88, 34);
  const steps = ["SARIF finding", "RAG evidence", "LLM patch", "Policy route", "Pull request", "Validation"];
  steps.forEach((step, idx) => {
    const x = 76 + idx * 180;
    const y = 226 + (idx % 2) * 56;
    rect(slide, x, y, 132, 58, idx === 2 ? style.dark : style.faint, {
      line: line(idx === 2 ? style.dark : style.line, 1)
    });
    text(slide, step, x + 12, y + 14, 108, 22, {
      size: 12.5,
      bold: true,
      align: "center",
      color: idx === 2 ? style.white : style.ink
    });
    if (idx < steps.length - 1) {
      rule(slide, x + 136, y + 30, 34, idx % 2 ? style.amber : style.teal, 2);
      rect(slide, x + 168, y + 26, 8, 8, idx % 2 ? style.amber : style.teal);
    }
  });
  await addImage(
    slide,
    path.join(__dirname, "figures", "fig_3_1_architecture.png"),
    178,
    388,
    770,
    196,
    "InfraGuard Pro architecture"
  );
  rect(slide, 976, 368, 174, 214, style.dark2);
  text(slide, "Policy modes", 1000, 394, 130, 18, { size: 10.5, bold: true, color: "#B9C7C0", align: "center" });
  bulletText(slide, ["Recommend only", "Human approval", "Autonomous low-risk"], 1002, 438, 126, 44, {
    size: 12,
    textColor: style.white,
    color: style.amber,
    h: 28
  });
  footer(slide, 5);
  return slide;
}

function slide06() {
  const slide = presentation.slides.add();
  bg(slide);
  kicker(slide, "Methodology", style.amber);
  title(slide, "Hybrid Agile-DevSecOps plus Design Science will keep the work practical and academic.", 64, 92, 920, 96, 32);
  const phases = [
    ["01", "Requirements", "Review literature, analyse scanner output, consult practitioners, prioritise with MoSCoW."],
    ["02", "Design", "Model architecture, use cases, data flow, sequence, ER, and policy decisions."],
    ["03", "Build", "Implement in increments with FastAPI, LangGraph, RAG, Git APIs, scanners, and dashboard."],
    ["04", "Evaluate", "Measure quality, MTTR, cost, latency, safety, audit completeness, and operator trust."],
    ["05", "Test", "Run unit, integration, API, security, scanner re-run, and acceptance testing."]
  ];
  phases.forEach((phase, idx) => {
    const y = 226 + idx * 74;
    text(slide, phase[0], 92, y, 42, 34, {
      size: 26,
      face: style.serif,
      bold: true,
      color: idx % 2 ? style.amber : style.teal
    });
    rule(slide, 150, y + 18, 84, idx % 2 ? style.amber : style.teal, 2);
    text(slide, phase[1], 258, y - 2, 190, 26, { size: 18, face: style.serif, bold: true });
    text(slide, phase[2], 466, y, 600, 34, { size: 13, color: style.soft });
  });
  footer(slide, 6);
  return slide;
}

function slide07() {
  const slide = presentation.slides.add();
  bg(slide);
  kicker(slide, "Technology Stack");
  title(slide, "The stack is feasible because it uses available tools and standard APIs.");
  const layers = [
    ["Backend", "Python, FastAPI, Uvicorn, SQLAlchemy", style.teal],
    ["Agent and AI", "LangGraph, LangChain, LLM provider APIs", style.amber],
    ["Retrieval", "ChromaDB, runbooks, advisories, outcomes", style.blue],
    ["Security", "Semgrep, Bandit, Trivy, Checkov, Gitleaks", style.red],
    ["Ops", "Docker, Git APIs, Prometheus, Loki, telemetry", style.dark]
  ];
  layers.forEach((layer, idx) => {
    const x = 88 + (idx % 3) * 350;
    const y = 236 + Math.floor(idx / 3) * 152;
    rule(slide, x, y, 220, layer[2], 3);
    text(slide, layer[0], x, y + 18, 250, 26, { size: 20, face: style.serif, bold: true });
    text(slide, layer[1], x, y + 58, 250, 42, { size: 13.5, color: style.soft });
  });
  rect(slide, 776, 382, 320, 120, style.faint2, { line: line(style.line, 1) });
  text(slide, "Feasibility signal", 804, 410, 260, 18, { size: 11, bold: true, color: style.soft, align: "center" });
  text(slide, "The existing InfraGuard repository already contains backend, agent, dashboard, scanner, and observability foundations.", 812, 444, 248, 42, {
    size: 13.5,
    align: "center"
  });
  footer(slide, 7);
  return slide;
}

function slide08() {
  const slide = presentation.slides.add();
  bg(slide);
  kicker(slide, "Scope", style.red);
  title(slide, "The study will focus on CI/CD remediation, not every cybersecurity incident class.", 64, 92, 860, 92, 34);
  const inside = data.chapterOne.find((section) => section.heading.startsWith("1.7")).withinScope.slice(0, 5);
  const outside = data.chapterOne.find((section) => section.heading.startsWith("1.7")).outOfScope.slice(0, 4);
  text(slide, "Within scope", 96, 226, 260, 28, { size: 22, face: style.serif, bold: true, color: style.teal });
  bulletText(slide, inside, 104, 278, 460, 50, { size: 12.5, color: style.teal, h: 38 });
  text(slide, "Intentionally excluded", 680, 226, 300, 28, { size: 22, face: style.serif, bold: true, color: style.red });
  bulletText(slide, outside, 688, 278, 420, 56, { size: 12.5, color: style.red, h: 42 });
  rule(slide, 628, 230, 1, 340, style.line, 1);
  footer(slide, 8, "Scope and delimitation | Boundaries protect the proposal from overpromising");
  return slide;
}

function slide09() {
  const slide = presentation.slides.add();
  bg(slide);
  kicker(slide, "Expected Value", style.blue);
  title(slide, "The outcome will be a working prototype plus measurable remediation evidence.");
  const outcomes = [
    ["Prototype", "SARIF ingestion, RAG evidence, LLM patch proposal, policy routing, PR workflow."],
    ["Evaluation", "Patch quality, finding closure, MTTR, cost, latency, regression rate, operator trust."],
    ["Contribution", "Provider-neutral reference architecture and reproducible evaluation framework."]
  ];
  outcomes.forEach((item, idx) => {
    const x = 110 + idx * 340;
    rect(slide, x, 262, 230, 190, idx === 1 ? style.dark : style.faint, {
      line: line(idx === 1 ? style.dark : style.line, 1)
    });
    text(slide, item[0], x + 24, 294, 182, 30, {
      size: 24,
      face: style.serif,
      bold: true,
      color: idx === 1 ? style.white : style.ink,
      align: "center"
    });
    text(slide, item[1], x + 28, 350, 174, 72, {
      size: 12.2,
      color: idx === 1 ? "#DCE7E2" : style.soft,
      align: "center"
    });
  });
  text(slide, "Expected deliverables include proposal PDF, defence slides, working prototype, source repository, design diagrams, testing report, evaluation report, and final project report.", 166, 524, 860, 40, {
    size: 15,
    align: "center"
  });
  footer(slide, 9);
  return slide;
}

function slide10() {
  const slide = presentation.slides.add();
  bg(slide);
  kicker(slide, "Project Plan", style.amber);
  title(slide, "A fourteen-week plan carries proposal approval through final defence.", 64, 92, 820, 88, 35);
  const milestones = [
    ["W1", "Proposal approval"],
    ["W2-3", "Requirements"],
    ["W4-5", "Design"],
    ["W6-9", "Core build"],
    ["W10-11", "Integration"],
    ["W12-13", "Testing"],
    ["W14", "Final report"]
  ];
  milestones.forEach((item, idx) => {
    const x = 84 + idx * 156;
    const y = 336 + (idx % 2) * 42;
    rect(slide, x, y, 96, 48, idx === 3 ? style.dark : style.faint2, {
      line: line(idx === 3 ? style.dark : style.line, 1)
    });
    text(slide, item[0], x + 12, y + 8, 72, 16, {
      size: 12,
      bold: true,
      align: "center",
      color: idx === 3 ? style.white : style.teal
    });
    text(slide, item[1], x + 8, y + 27, 80, 14, {
      size: 8.8,
      align: "center",
      color: idx === 3 ? "#DCE7E2" : style.ink
    });
    if (idx < milestones.length - 1) {
      rule(slide, x + 102, y + 24, 44, idx % 2 ? style.amber : style.teal, 2);
    }
  });
  rect(slide, 214, 518, 700, 58, style.dark2);
  text(slide, "Immediate defence package: proposal PDF plus PowerPoint slides submitted before the scheduled Google Meet defence.", 238, 538, 652, 20, {
    size: 15,
    bold: true,
    color: style.white,
    align: "center"
  });
  footer(slide, 10, "Submission readiness | Proposal document and slides are the current deliverables");
  return slide;
}

async function saveBlob(blob, filePath) {
  const arrayBuffer = await blob.arrayBuffer();
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, Buffer.from(arrayBuffer));
}

await fs.rm(previewDir, { recursive: true, force: true });
await fs.mkdir(previewDir, { recursive: true });

slide01();
slide02();
slide03();
slide04();
await slide05();
slide06();
slide07();
slide08();
slide09();
slide10();

const previewPaths = [];
for (let index = 0; index < presentation.slides.count; index += 1) {
  const slide = presentation.slides.getItem(index);
  const preview = await presentation.export({ slide, format: "png", scale: 1 });
  const previewPath = path.join(previewDir, `slide-${String(index + 1).padStart(2, "0")}.png`);
  await saveBlob(preview, previewPath);
  previewPaths.push(previewPath);
}

await fs.mkdir(path.dirname(outputPath), { recursive: true });
const pptx = await PresentationFile.exportPptx(presentation);
await pptx.save(outputPath);
const outputBytes = fsSync.statSync(outputPath).size;

const manifest = {
  output: outputPath,
  outputBytes,
  slideCount: presentation.slides.count,
  previewDir,
  previewPaths
};
await fs.writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");

console.log(JSON.stringify(manifest, null, 2));
