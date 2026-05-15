// Shared formatting helpers for the master's project docx generator.
// Formatting baseline: Times New Roman 12pt, line spacing 1.25, justified, A4, 1 inch margins.

const fs = require('fs');
const path = require('path');
const {
  Paragraph, TextRun, AlignmentType, HeadingLevel, PageBreak,
  Table, TableRow, TableCell, BorderStyle, WidthType, ShadingType,
  LevelFormat, TabStopType, TabStopPosition,
  ImageRun,
} = require('docx');

const FONT = 'Times New Roman';
const SIZE_BODY = 24;          // 12pt
const SIZE_H1 = 32;            // 16pt
const SIZE_H2 = 28;            // 14pt
const SIZE_H3 = 26;            // 13pt
const LINE_125 = 300;          // 1.25 line spacing (240 = 1.0)
const CONTENT_W = 9026;        // A4 (11906) minus 1in margins

const border = { style: BorderStyle.SINGLE, size: 4, color: '808080' };
const borders = { top: border, bottom: border, left: border, right: border };

// --- Paragraph helpers ---
function p(text, opts = {}) {
  const runs = Array.isArray(text)
    ? text.map(t => (typeof t === 'string' ? new TextRun({ text: t, font: FONT, size: SIZE_BODY }) : t))
    : [new TextRun({ text, font: FONT, size: SIZE_BODY })];
  return new Paragraph({
    children: runs,
    alignment: opts.align || AlignmentType.JUSTIFIED,
    spacing: { line: LINE_125, before: opts.before ?? 0, after: opts.after ?? 120 },
    indent: opts.indent,
    pageBreakBefore: !!opts.pageBreakBefore,
  });
}

function pCenter(text, opts = {}) {
  return p(text, { ...opts, align: AlignmentType.CENTER });
}

function pBold(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: SIZE_BODY, bold: true })],
    alignment: opts.align || AlignmentType.JUSTIFIED,
    spacing: { line: LINE_125, after: opts.after ?? 120 },
    pageBreakBefore: !!opts.pageBreakBefore,
  });
}

function chapterTitle(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: SIZE_H1, bold: true })],
    alignment: AlignmentType.CENTER,
    spacing: { line: LINE_125, before: 240, after: 360 },
    pageBreakBefore: true,
  });
}

function chapterLabel(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: SIZE_H1, bold: true })],
    alignment: AlignmentType.CENTER,
    spacing: { line: LINE_125, before: 480, after: 120 },
    pageBreakBefore: true,
  });
}

function h2(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: SIZE_H2, bold: true })],
    alignment: AlignmentType.LEFT,
    spacing: { line: LINE_125, before: 240, after: 120 },
  });
}

function h3(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: SIZE_H3, bold: true })],
    alignment: AlignmentType.LEFT,
    spacing: { line: LINE_125, before: 200, after: 100 },
  });
}

function h4(text) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: SIZE_BODY, bold: true, italics: true })],
    alignment: AlignmentType.LEFT,
    spacing: { line: LINE_125, before: 120, after: 60 },
  });
}

function bullet(text, level = 0) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: SIZE_BODY })],
    numbering: { reference: 'bullets', level },
    spacing: { line: LINE_125, after: 80 },
    alignment: AlignmentType.JUSTIFIED,
  });
}

function num(text, level = 0) {
  return new Paragraph({
    children: [new TextRun({ text, font: FONT, size: SIZE_BODY })],
    numbering: { reference: 'numbers', level },
    spacing: { line: LINE_125, after: 80 },
    alignment: AlignmentType.JUSTIFIED,
  });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

function blank() {
  return new Paragraph({
    children: [new TextRun({ text: '', font: FONT, size: SIZE_BODY })],
    spacing: { line: LINE_125, after: 120 },
  });
}

// Embed an image (path is relative to docs/masters_project/). Width/height in inches.
function image(relPath, opts = {}) {
  const absPath = path.resolve(__dirname, relPath);
  const buffer = fs.readFileSync(absPath);
  const widthIn = opts.w || 6.0;
  const heightIn = opts.h || 4.0;
  return new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 160, after: 80 },
    children: [new ImageRun({
      type: 'png',
      data: buffer,
      transformation: { width: Math.round(widthIn * 96), height: Math.round(heightIn * 96) },
      altText: {
        title: opts.title || relPath,
        description: opts.desc || relPath,
        name: opts.name || relPath,
      },
    })],
  });
}

// --- Table helpers ---
function tableCell(text, opts = {}) {
  const runs = (Array.isArray(text) ? text : [text]).map(t =>
    new TextRun({
      text: typeof t === 'string' ? t : t.text,
      font: FONT,
      size: opts.size || 22,
      bold: !!opts.bold,
    }));
  return new TableCell({
    borders,
    width: { size: opts.width, type: WidthType.DXA },
    shading: opts.shade ? { fill: opts.shade, type: ShadingType.CLEAR, color: 'auto' } : undefined,
    margins: { top: 80, bottom: 80, left: 100, right: 100 },
    children: [new Paragraph({
      children: runs,
      spacing: { line: 260 },
      alignment: opts.align || AlignmentType.LEFT,
    })],
  });
}

function buildTable(columnWidths, rows, headerShade = 'D9E2F3') {
  const totalWidth = columnWidths.reduce((a, b) => a + b, 0);
  return new Table({
    width: { size: totalWidth, type: WidthType.DXA },
    columnWidths,
    rows: rows.map((row, ri) =>
      new TableRow({
        tableHeader: ri === 0,
        children: row.map((cellText, ci) =>
          tableCell(cellText, {
            width: columnWidths[ci],
            bold: ri === 0,
            shade: ri === 0 ? headerShade : undefined,
            size: 20,
          })),
      })),
  });
}

// --- Numbering / bullet definitions for the Document constructor ---
const numbering = {
  config: [
    {
      reference: 'bullets',
      levels: [
        { level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
        { level: 1, format: LevelFormat.BULLET, text: '◦', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 1440, hanging: 360 } } } },
      ],
    },
    {
      reference: 'numbers',
      levels: [
        { level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
      ],
    },
  ],
};

const styles = {
  default: { document: { run: { font: FONT, size: SIZE_BODY } } },
  paragraphStyles: [
    { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { size: SIZE_H1, bold: true, font: FONT },
      paragraph: { spacing: { before: 240, after: 240, line: LINE_125 }, outlineLevel: 0 } },
    { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { size: SIZE_H2, bold: true, font: FONT },
      paragraph: { spacing: { before: 200, after: 120, line: LINE_125 }, outlineLevel: 1 } },
    { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
      run: { size: SIZE_H3, bold: true, font: FONT },
      paragraph: { spacing: { before: 180, after: 100, line: LINE_125 }, outlineLevel: 2 } },
  ],
};

const sectionProps = {
  page: {
    size: { width: 11906, height: 16838 }, // A4
    margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
  },
};

module.exports = {
  p, pCenter, pBold, chapterTitle, chapterLabel, h2, h3, h4,
  bullet, num, pageBreak, blank, buildTable, tableCell, image,
  numbering, styles, sectionProps, FONT, SIZE_BODY, CONTENT_W,
};
