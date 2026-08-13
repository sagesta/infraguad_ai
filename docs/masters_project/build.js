// Master build script for the InfraGuard AI master's project docx.
// Assembles preliminary pages + six chapters + references + appendices.
// Outputs InfraGuard_AI_Masters_Project.docx in the same folder.

const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Footer, Paragraph, TextRun, AlignmentType, PageNumber,
  NumberFormat, SectionType,
} = require('docx');

const { numbering, styles, sectionProps, FONT, SIZE_BODY } = require('./helpers');
const { preliminary } = require('./content/00-prelim');
const { chapter1 } = require('./content/01-intro');
const { chapter2 } = require('./content/02-litreview');
const { chapter3 } = require('./content/03-methodology');
const { chapter4 } = require('./content/04-implementation');
const { chapter5 } = require('./content/05-testing');
const { chapter6 } = require('./content/06-conclusion');
const { references } = require('./content/07-references');
const { appendices } = require('./content/08-appendices');

function buildFooter() {
  return new Footer({
    children: [new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [
        new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 20 }),
      ],
    })],
  });
}

function buildEmptyFooter() {
  return new Footer({ children: [new Paragraph({ children: [] })] });
}

function assembleBody() {
  const blocks = [];
  blocks.push(...chapter1());
  blocks.push(...chapter2());
  blocks.push(...chapter3());
  blocks.push(...chapter4());
  blocks.push(...chapter5());
  blocks.push(...chapter6());
  blocks.push(...references());
  blocks.push(...appendices());
  return blocks;
}

async function main() {
  const preliminaryChildren = preliminary();
  const bodyChildren = assembleBody();

  const preliminaryProps = {
    ...sectionProps,
    titlePage: true,
    page: {
      ...sectionProps.page,
      pageNumbers: { start: 1, formatType: NumberFormat.LOWER_ROMAN },
    },
  };
  const bodyProps = {
    ...sectionProps,
    type: SectionType.NEXT_PAGE,
    page: {
      ...sectionProps.page,
      pageNumbers: { start: 1, formatType: NumberFormat.DECIMAL },
    },
  };

  const doc = new Document({
    creator: 'InfraGuard AI MIT Project',
    title: 'InfraGuard AI: An LLM-Driven Observability and Incident-Triage Agent for Self-Hosted Cloud-Native Infrastructure',
    description: 'Professional Master of Information Technology Project, Miva Open University Abuja, Nigeria',
    styles,
    numbering,
    settings: { updateFields: true },
    sections: [
      {
        properties: preliminaryProps,
        footers: { default: buildFooter(), first: buildEmptyFooter() },
        children: preliminaryChildren,
      },
      {
        properties: bodyProps,
        footers: { default: buildFooter() },
        children: bodyChildren,
      },
    ],
  });

  const buffer = await Packer.toBuffer(doc);
  const out = process.argv[2]
    ? path.resolve(process.argv[2])
    : path.join(__dirname, 'InfraGuard_AI_Masters_Project.docx');
  fs.writeFileSync(out, buffer);
  console.log(`Wrote ${out} (${buffer.length} bytes, ${preliminaryChildren.length + bodyChildren.length} top-level blocks).`);
}

main().catch(err => {
  console.error('Build failed:', err);
  process.exit(1);
});
