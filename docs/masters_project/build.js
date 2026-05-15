// Master build script for the InfraGuard Pro master's project docx.
// Assembles preliminary pages + six chapters + references + appendices.
// Outputs InfraGuard_Pro_Masters_Project.docx in the same folder.

const fs = require('fs');
const path = require('path');
const { Document, Packer, Header, Footer, Paragraph, TextRun, AlignmentType, PageNumber } = require('docx');

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
        new TextRun({ text: 'Page ', font: FONT, size: 20 }),
        new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 20 }),
        new TextRun({ text: ' of ', font: FONT, size: 20 }),
        new TextRun({ children: [PageNumber.TOTAL_PAGES], font: FONT, size: 20 }),
      ],
    })],
  });
}

function buildHeader() {
  return new Header({
    children: [new Paragraph({
      alignment: AlignmentType.RIGHT,
      children: [new TextRun({
        text: 'InfraGuard Pro — MIT Master’s Project',
        font: FONT, size: 18, italics: true, color: '666666',
      })],
    })],
  });
}

function assembleChildren() {
  const blocks = [];
  blocks.push(...preliminary());
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
  const children = assembleChildren();

  const doc = new Document({
    creator: 'InfraGuard Pro MIT Project',
    title: 'Design and Development of an LLM-Based Autonomous Security Remediation System for Cloud-Native CI/CD Pipelines',
    description: 'Professional Master of Information Technology Project — Miva Open University Abuja, Nigeria',
    styles,
    numbering,
    sections: [{
      properties: sectionProps,
      headers: { default: buildHeader() },
      footers: { default: buildFooter() },
      children,
    }],
  });

  const buffer = await Packer.toBuffer(doc);
  const out = path.join(__dirname, 'InfraGuard_Pro_Masters_Project.docx');
  fs.writeFileSync(out, buffer);
  console.log(`Wrote ${out} (${buffer.length} bytes, ${children.length} top-level blocks).`);
}

main().catch(err => {
  console.error('Build failed:', err);
  process.exit(1);
});
