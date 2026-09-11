// Builds an editable proposal DOCX from proposal_data.json.
// The existing full master's project document is not overwritten.

process.env.NODE_PATH = 'C:/Users/adebo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
require('module').Module._initPaths();

const fs = require('fs');
const path = require('path');
const {
  Document,
  Packer,
  Header,
  Footer,
  Paragraph,
  TextRun,
  AlignmentType,
  PageNumber,
} = require('docx');

const {
  p,
  pCenter,
  pBold,
  chapterLabel,
  h2,
  h3,
  bullet,
  num,
  blank,
  pageBreak,
  buildTable,
  image,
  numbering,
  styles,
  sectionProps,
  FONT,
} = require('./helpers');

const data = JSON.parse(fs.readFileSync(path.join(__dirname, 'proposal_data.json'), 'utf8'));

function buildHeader() {
  return new Header({
    children: [
      new Paragraph({
        alignment: AlignmentType.RIGHT,
        children: [
          new TextRun({
            text: 'InfraGuard Pro - MIT Project Proposal',
            font: FONT,
            size: 18,
            italics: true,
            color: '666666',
          }),
        ],
      }),
    ],
  });
}

function buildFooter() {
  return new Footer({
    children: [
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [
          new TextRun({ text: 'Page ', font: FONT, size: 20 }),
          new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 20 }),
          new TextRun({ text: ' of ', font: FONT, size: 20 }),
          new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT, size: 20 }),
        ],
      }),
    ],
  });
}

function coverPage() {
  const b = [];
  b.push(new Paragraph({ spacing: { before: 940 }, children: [] }));
  b.push(pCenter('MASTER OF INFORMATION TECHNOLOGY (MIT) PROFESSIONAL MASTER\'S PROJECT PROPOSAL', { after: 360 }));
  b.push(blank());
  b.push(pCenter(data.projectTitle.toUpperCase(), { after: 360 }));
  b.push(pCenter(`(${data.projectSubtitle})`, { after: 620 }));
  b.push(pCenter('BY:', { after: 180 }));
  b.push(pCenter(data.studentName.toUpperCase(), { after: 80 }));
  b.push(pCenter(`(${data.matricNumber})`, { after: 520 }));
  b.push(blank());
  b.push(pCenter(data.department.toUpperCase(), { after: 90 }));
  b.push(pCenter(data.school.toUpperCase(), { after: 90 }));
  b.push(pCenter(data.university.toUpperCase(), { after: 520 }));
  b.push(pCenter(`SUPERVISOR: ${data.supervisor}`, { after: 300 }));
  b.push(pCenter(data.proposalDate.toUpperCase()));
  b.push(pageBreak());
  return b;
}

function addParagraphs(blocks, paragraphs = []) {
  for (const paragraph of paragraphs) {
    blocks.push(p(paragraph));
  }
}

function addChapterOne(blocks) {
  blocks.push(chapterLabel('CHAPTER ONE'));
  blocks.push(pCenter('INTRODUCTION'));
  blocks.push(blank());

  for (const section of data.chapterOne) {
    blocks.push(h2(section.heading));
    addParagraphs(blocks, section.paragraphs);

    if (section.aim) {
      blocks.push(pBold('Aim'));
      blocks.push(p(section.aim));
    }

    if (section.objectives) {
      blocks.push(pBold('Specific Objectives'));
      const rows = [
        ['Objective Area', 'Objective Statement', 'Expected Evidence'],
        ...section.objectives.map((objective) => [
          objective.area,
          objective.statement,
          objective.evidence,
        ]),
      ];
      blocks.push(buildTable([1700, 4300, 3026], rows));
      blocks.push(blank());
    }

    if (section.questions) {
      const rows = [
        ['No.', 'Research Question'],
        ...section.questions.map((question, index) => [String(index + 1), question]),
      ];
      blocks.push(buildTable([700, 8326], rows));
      blocks.push(blank());
    }

    if (section.withinScope) {
      blocks.push(h3('Within Scope'));
      section.withinScope.forEach((item) => blocks.push(bullet(item)));
      blocks.push(h3('Out of Scope'));
      section.outOfScope.forEach((item) => blocks.push(bullet(item)));
    }

    if (section.items) {
      section.items.forEach((item) => blocks.push(bullet(item)));
    }

    if (section.terms) {
      blocks.push(buildTable([2200, 6826], [['Term', 'Definition'], ...section.terms]));
      blocks.push(blank());
    }
  }
}

function addChapterTwo(blocks) {
  blocks.push(chapterLabel('CHAPTER TWO'));
  blocks.push(pCenter('PRELIMINARY LITERATURE REVIEW AND TECHNOLOGY CONTEXT'));
  blocks.push(blank());

  for (const section of data.chapterTwo) {
    blocks.push(h2(section.heading));
    addParagraphs(blocks, section.paragraphs);
    if (section.gaps) {
      section.gaps.forEach((gap) => blocks.push(bullet(gap)));
    }
  }
}

function addChapterThree(blocks) {
  blocks.push(chapterLabel('CHAPTER THREE'));
  blocks.push(pCenter('PROPOSED METHODOLOGY AND SYSTEM DESIGN'));
  blocks.push(blank());

  for (const section of data.chapterThree) {
    blocks.push(h2(section.heading));
    addParagraphs(blocks, section.paragraphs);
  }

  blocks.push(h2('3.7 Methodology Alignment Matrix'));
  blocks.push(buildTable([2100, 4300, 2626], data.methodologyMatrix));
  blocks.push(blank());

  blocks.push(h2(data.solutionOverview.heading));
  addParagraphs(blocks, data.solutionOverview.paragraphs);
  blocks.push(h3('Key System Components'));
  data.solutionOverview.components.forEach((component) => blocks.push(bullet(component)));
  blocks.push(blank());
  blocks.push(image('figures/fig_3_1_architecture.png', {
    w: 7.2,
    h: 4.5,
    title: 'InfraGuard Pro architecture',
    desc: 'High-level architecture of the proposed InfraGuard Pro system',
  }));
  blocks.push(pCenter('Figure 3.1: Proposed High-Level Architecture of InfraGuard Pro.'));

  blocks.push(h2('3.8 Tools and Technologies to be Used'));
  blocks.push(buildTable([2000, 7026], data.tools));
  blocks.push(blank());
}

function addOtherProposalSections(blocks) {
  blocks.push(chapterLabel('FEASIBILITY CONSIDERATIONS'));
  for (const item of data.feasibility) {
    blocks.push(h2(item.heading));
    blocks.push(p(item.text));
  }

  blocks.push(chapterLabel('PROJECT PLAN AND TIMELINE'));
  blocks.push(p('The proposed project plan is summarised below. The schedule will be refined after proposal approval and supervisor feedback.'));
  blocks.push(buildTable([1600, 3600, 3826], data.timeline));
  blocks.push(blank());

  blocks.push(chapterLabel('EXPECTED DELIVERABLES'));
  data.expectedDeliverables.forEach((deliverable) => blocks.push(bullet(deliverable)));

  blocks.push(chapterLabel('REFERENCES'));
  data.references.forEach((reference, index) => blocks.push(num(reference, 0)));
}

async function main() {
  const children = [
    ...coverPage(),
  ];
  addChapterOne(children);
  addChapterTwo(children);
  addChapterThree(children);
  addOtherProposalSections(children);

  const doc = new Document({
    creator: 'InfraGuard Pro MIT Project',
    title: `${data.projectTitle} - Project Proposal`,
    description: 'MIT professional master project proposal for Miva Open University',
    styles,
    numbering,
    sections: [
      {
        properties: sectionProps,
        headers: { default: buildHeader() },
        footers: { default: buildFooter() },
        children,
      },
    ],
  });

  const buffer = await Packer.toBuffer(doc);
  const out = path.join(__dirname, 'InfraGuard_Pro_Project_Proposal.docx');
  fs.writeFileSync(out, buffer);
  console.log(`Wrote ${out} (${buffer.length} bytes).`);
}

main().catch((error) => {
  console.error('Build failed:', error);
  process.exit(1);
});
