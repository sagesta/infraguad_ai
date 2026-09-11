#!/usr/bin/env python3
"""Generate a historical Beautiful.ai prompt from an earlier project report.

This generator predates the final defence manuscript and presentation. It is
retained for history, excluded from the defence package, and blocked by default
so it cannot silently recreate obsolete study or coverage claims.
"""

from __future__ import annotations

import argparse
import os
import re
import textwrap
import zipfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
NS = {"w": W_NS, "a": A_NS}


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def natural_number(path: str) -> int:
    match = re.search(r"(\d+)(?=\.xml$)", path)
    return int(match.group(1)) if match else 0


def truncate(value: str, limit: int = 520) -> str:
    value = clean(value)
    if len(value) <= limit:
        return value
    shortened = value[: limit + 1].rsplit(" ", 1)[0]
    return shortened.rstrip(" ,;:") + "..."


def sentences(value: str, count: int = 1) -> str:
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", clean(value))
    return " ".join(parts[:count])


def bullet_block(
    items: Iterable[str], *, limit: int = 6, indent: int = 0, max_chars: int = 360
) -> str:
    chosen = [truncate(item, max_chars) for item in items if clean(item)][:limit]
    prefix = " " * indent
    return "\n".join(f"{prefix}- {item}" for item in chosen)


@dataclass
class Section:
    heading: str
    paragraphs: list[str] = field(default_factory=list)
    bullets: list[str] = field(default_factory=list)
    tables: list[list[list[str]]] = field(default_factory=list)

    @property
    def text(self) -> str:
        return " ".join(self.paragraphs)


@dataclass
class Report:
    path: Path
    title: str
    abstract: str
    sections: list[Section]

    def section(self, pattern: str) -> Section:
        regex = re.compile(pattern, re.IGNORECASE)
        for section in self.sections:
            if regex.search(section.heading):
                return section
        return Section(heading=pattern)


def paragraph_text(node: ET.Element) -> str:
    return clean("".join(part.text or "" for part in node.findall(".//w:t", NS)))


def paragraph_style(node: ET.Element) -> str:
    style = node.find("./w:pPr/w:pStyle", NS)
    if style is None:
        return ""
    return style.attrib.get(f"{{{W_NS}}}val", "")


def table_rows(node: ET.Element) -> list[list[str]]:
    rows: list[list[str]] = []
    for row in node.findall("./w:tr", NS):
        cells = []
        for cell in row.findall("./w:tc", NS):
            cells.append(clean(" ".join(paragraph_text(p) for p in cell.findall(".//w:p", NS))))
        if any(cells):
            rows.append(cells)
    return rows


def extract_report(path: Path) -> Report:
    with zipfile.ZipFile(path) as package:
        root = ET.fromstring(package.read("word/document.xml"))

    body = root.find(".//w:body", NS)
    if body is None:
        raise ValueError(f"No Word document body found in {path}")

    title = ""
    abstract = ""
    abstract_pending = False
    current = Section("Front matter")
    sections = [current]

    for node in body:
        local_name = node.tag.rsplit("}", 1)[-1]
        if local_name == "p":
            text = paragraph_text(node)
            if not text:
                continue
            style = paragraph_style(node)

            if not title and "INFRAGUARD" in text.upper() and len(text) > 25:
                title = text

            if text.upper() == "ABSTRACT":
                abstract_pending = True
                continue
            if abstract_pending and not abstract:
                abstract = text
                abstract_pending = False

            if style.lower().startswith("heading"):
                current = Section(text)
                sections.append(current)
            elif style == "ListParagraph":
                current.bullets.append(text)
            else:
                current.paragraphs.append(text)
        elif local_name == "tbl":
            rows = table_rows(node)
            if rows:
                current.tables.append(rows)

    return Report(
        path=path,
        title=title or "InfraGuard AI",
        abstract=abstract,
        sections=sections,
    )


def newest_report(directory: Path) -> Path:
    candidates = [
        path
        for path in directory.glob("*.docx")
        if not path.name.startswith("~$")
        and "InfraGuard" in path.name
        and "Use_Case" not in path.name
    ]
    if not candidates:
        raise FileNotFoundError(f"No InfraGuard project DOCX found in {directory}")
    return max(candidates, key=lambda path: path.stat().st_mtime)


def extract_sample_slides(path: Path | None) -> list[str]:
    if not path or not path.exists():
        return []
    with zipfile.ZipFile(path) as package:
        names = sorted(
            (
                name
                for name in package.namelist()
                if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
            ),
            key=natural_number,
        )
        slides = []
        for name in names:
            root = ET.fromstring(package.read(name))
            parts = [clean(node.text or "") for node in root.findall(".//a:t", NS)]
            text = " | ".join(part for part in parts if part)
            slides.append(truncate(text, 340))
        return slides


def find_figures(directory: Path) -> list[Path]:
    figures_dir = directory / "figures"
    preferred = [
        "fig_3_1_architecture.png",
        "fig_3_3_remediation_flow.png",
        "fig_3_7_state_machine.png",
        "fig_4_3_dashboard.png",
        "fig_4_4_runbook_retrieval.png",
        "fig_5_1_acceptance.png",
        "fig_5_2_mttr.png",
        "fig_5_4_calibration.png",
    ]
    return [figures_dir / name for name in preferred if (figures_dir / name).exists()]


def source_material(report: Report) -> dict[str, object]:
    problem = report.section(r"^1\.2\b")
    aim = report.section(r"^1\.3\.1\b")
    objectives = report.section(r"^1\.3\.2\b")
    in_scope = report.section(r"^1\.4\.1\b")
    out_scope = report.section(r"^1\.4\.2\b")
    gaps_parent = report.section(r"^2\.4\b")
    gap_sections = [section for section in report.sections if re.match(r"2\.4\.\d+", section.heading)]
    methodology = report.section(r"^3\.1\.1\b")
    architecture = report.section(r"^3\.3\b")
    components = report.section(r"^3\.3\.2\b")
    workflow = report.section(r"^4\.2\.2\b")
    modes = report.section(r"^4\.2\.3\b")
    prompt_validation = report.section(r"^4\.2\.4\b")
    memory = report.section(r"^4\.2\.5\b")
    rag = report.section(r"^4\.2\.7\b")
    dashboard = report.section(r"^4\.2\.11\b")
    tests = report.section(r"^5\.2\b")
    acknowledgement = report.section(r"^5\.3\b")
    pilot = report.section(r"^5\.4\.1\b")
    usability = report.section(r"^5\.4\.2\b")
    supported = report.section(r"^5\.6\.1\b")
    limitations = report.section(r"^5\.6\.2\b")
    conclusion = report.section(r"^6\.2\b")
    contributions = [section for section in report.sections if re.match(r"6\.3\.\d+", section.heading)]
    recommendations = [section for section in report.sections if re.match(r"6\.4\.\d+", section.heading)]
    all_references = report.section(r"^REFERENCES$").paragraphs
    reference_leads = (
        "Ahmed,",
        "Beyer,",
        "Central Bank of Nigeria",
        "Federal Republic of Nigeria",
        "Hevner,",
        "Lewis,",
        "National Institute of Standards and Technology",
        "Yao,",
    )
    selected_references = [
        reference
        for lead in reference_leads
        for reference in all_references
        if reference.startswith(lead)
    ]

    return {
        "problem": problem.bullets,
        "problem_question": sentences(problem.text, 2),
        "aim": sentences(aim.text, 2),
        "objectives": objectives.bullets,
        "in_scope": in_scope.bullets,
        "out_scope": out_scope.bullets,
        "gaps_intro": gaps_parent.text,
        "gaps": [f"{s.heading}: {sentences(s.text, 1)}" for s in gap_sections],
        "methodology": methodology.bullets,
        "architecture": sentences(architecture.text, 3),
        "components": components.bullets,
        "workflow": sentences(workflow.text, 4),
        "modes": sentences(modes.text, 4),
        "prompt_validation": sentences(prompt_validation.text, 4),
        "memory": sentences(memory.text, 5),
        "rag": sentences(rag.text, 4),
        "dashboard": sentences(dashboard.text, 4),
        "tests": sentences(tests.text, 5),
        "acknowledgement": sentences(acknowledgement.text, 6),
        "pilot": sentences(pilot.text, 7),
        "usability": sentences(usability.text, 3),
        "supported": sentences(supported.text, 4),
        "limitations": sentences(limitations.text, 6),
        "conclusion": sentences(conclusion.text, 6),
        "contributions": [f"{s.heading}: {sentences(s.text, 2)}" for s in contributions],
        "recommendations": [
            f"{s.heading}: {' '.join(s.bullets[:3]) or sentences(s.text, 3)}" for s in recommendations
        ],
        "references": selected_references,
    }


def generate_prompt(report: Report, sample_slides: list[str], figures: list[Path]) -> str:
    material = source_material(report)
    generated = datetime.now().astimezone().strftime("%d %B %Y, %H:%M %Z")
    source_time = datetime.fromtimestamp(report.path.stat().st_mtime).astimezone().strftime(
        "%d %B %Y, %H:%M %Z"
    )
    sample_note = (
        f"The supplied Sample_MIT.pptx contains {len(sample_slides)} slides and uses a formal "
        "MIT proposal-defence rhythm with alternating deep-navy and white slides, red section "
        "titles, restrained gold accents, a thin top rule, and the MIT mark in the upper-right."
        if sample_slides
        else "No sample PPTX was supplied to the generator; use the MIT-inspired direction below."
    )

    assets = "\n".join(f"- {path.name}" for path in figures)
    prompt = f"""
CREATE A 16:9 ACADEMIC FINAL-PROJECT DEFENCE PRESENTATION

Project title
{report.title}

Source-of-truth rule
Use only the factual content below, which was extracted from the most recent report:
{report.path.name} (last modified {source_time}). Do not revive older "InfraGuard Pro" claims.
The implemented artefact is an LLM-assisted observability and incident-triage reference system.
Autonomous code remediation, SARIF-to-pull-request automation, and multi-host operation are future
work, not delivered features. Do not invent evaluation results, users, cost savings, accuracy,
production-readiness claims, or citations.

Audience and purpose
The audience is a Master of Information Technology project-defence panel. The presentation must
demonstrate a clearly bounded problem, an implemented software artefact, evidence of verification,
intellectual honesty about limits, and a defensible contribution to professional IT practice.
By the end, the panel should understand that InfraGuard AI is a tested, inspectable single-host
reference implementation that connects telemetry, LLM reasoning, runbook retrieval, operator
controls, persistence, and a dashboard; the available evidence supports implementation feasibility,
not proven diagnostic accuracy or production effectiveness.

Visual direction
{sample_note}
- Treat Sample_MIT.pptx as a visual reference, not a content source.
- Preserve the formal academic character while improving hierarchy, spacing, and visual storytelling.
- Palette: deep navy #0B3553, warm white #F7F5F0, coral red #E43D30, muted gold #C8A36A,
  charcoal #17212B, and a limited green #159447 for passed/completed evidence.
- Alternate light and dark slides deliberately. Keep the MIT logo/header treatment only if the
  authentic asset is available from the sample; never fabricate a university logo.
- Use one strong composition per slide, not a dashboard of cards. Keep body copy concise.
- Use large takeaway titles, restrained transitions, consistent page numbers, and APA-style short
  citations in a small footer where a scholarly claim is used.
- Prefer the project's authentic diagrams and screenshots over stock imagery. Do not generate fake
  product screens, fake telemetry, or fake charts.

Slide-by-slide content

1. Title slide - "InfraGuard AI"
   Subtitle: "An LLM-Driven Observability and Incident-Triage Agent for Self-Hosted Cloud-Native Infrastructure"
   Add: Final Project Defence; Master of Information Technology; student name, matriculation number,
   supervisor, and date as editable placeholders. Keep this slide minimal and premium.

2. The operational problem - "Telemetry exists, but first-pass interpretation remains manual"
   Frame the project around small operations teams comparing distributed signals before deciding
   whether a service is healthy, degraded, or failing.
{bullet_block(material['problem'], limit=5, indent=3)}
   Closing line: {truncate(str(material['problem_question']), 360)}

3. Aim and objectives - "Five objectives connect telemetry collection to verified behaviour"
   Aim: {truncate(str(material['aim']), 520)}
{bullet_block(material['objectives'], limit=5, indent=3)}
   Show the objectives as a clean numbered progression, not five dense text boxes.

4. Literature and gap - "The opportunity lies between monitoring, AIOps, and operator control"
   Establish the conceptual foundation: observability, SRE/toil reduction, AIOps, LLM agents, RAG,
   incident memory, and human oversight. Then show the seven design gaps:
{bullet_block(material['gaps'], limit=7, indent=3)}
   Keep claims cautious: constraints and validation reduce risk but do not prove model correctness.

5. Scope and boundaries - "The project assists triage; it does not autonomously remediate"
   Within scope:
{bullet_block(material['in_scope'], limit=7, indent=5)}
   Explicitly outside scope/future work:
{bullet_block(material['out_scope'], limit=7, indent=5)}
   Make the distinction between diagnosis/recommendation and enforcement unmistakable.

6. Methodology - "Iterative design science kept the problem, artefact, and evidence aligned"
{bullet_block(material['methodology'], limit=6, indent=3)}
   Use a six-stage horizontal process with feedback loops. State that tests and review sometimes
   caused earlier decisions to be revisited.

7. Architecture - "A two-process, single-host design keeps collection and review inspectable"
   Core architecture: {truncate(str(material['architecture']), 650)}
   Key components:
{bullet_block(material['components'], limit=8, indent=3)}
   Use the authentic high-level architecture image. Emphasise that the agent and FastAPI service
   share SQLite, while adapters isolate Loki, Prometheus, HTTP probes, Docker, and LLM providers.

8. Reasoning workflow - "Each heartbeat follows a bounded collect-analyse-decide-notify cycle"
   Workflow: {truncate(str(material['workflow']), 720)}
   Provider modes: {truncate(str(material['modes']), 620)}
   Show the authentic state-machine or heartbeat-flow diagram. Label Gemini Developer API,
   Anthropic, OpenAI-compatible endpoints, and Ollama as configurable provider options.

9. Grounding and operator control - "Runbooks add local context; enforcement stays human-approved"
   Runbook RAG: {truncate(str(material['rag']), 700)}
   Explain deterministic HTTP/SSH brute-force and port-scan detection, optional CrowdSec integration,
   and operator approval before an IP ban. Use the runbook-retrieval figure and, if space permits,
   a small authentic dashboard crop.

10. Safety and memory design - "Structured outputs and fingerprinted acknowledgements constrain recurring risk"
   Output validation: {truncate(str(material['prompt_validation']), 650)}
   Verdict memory: {truncate(str(material['memory']), 760)}
   Explain the fingerprint as condition signature + prompt version + model. State clearly that high
   and critical verdicts cannot be hidden and that acknowledgement reduces dashboard repetition,
   not model calls, storage, or inference cost.

11. Implemented interface - "The dashboard turns verdicts into reviewable operational records"
   {truncate(str(material['dashboard']), 760)}
   Use the authentic dashboard screenshot full-width or in a strong two-column composition.
   Call out session authentication, rate limiting, security headers, request auditing, output escaping,
   staleness status, recent checks, threat review, runbook queries, and acknowledgement controls.

12. Automated verification - "82 tests passed; coverage is strong in core control paths but uneven overall"
   Exact evidence: {truncate(str(material['tests']), 900)}
   Highlight only verified figures: 82 passing tests, 17 warnings, 27.01 seconds, 1,476 executable
   statements, 508 missed statements, and 66% overall line coverage. Show the authentic module-
   coverage chart. Visually distinguish high-coverage modules from low-coverage paths that need work.

13. Acknowledgement evaluation - "Reviewed low-risk warnings fall out of the default view without stopping analysis"
   {truncate(str(material['acknowledgement']), 900)}
   Use the authentic 30-cycle comparison chart. Make the narrow conclusion explicit: after the
   operator acknowledges the repeated warning after cycle 3, the next 27 matching warnings remain
   recorded but are hidden from the default view; high/critical findings remain visible.

14. Limited live verification - "The deployed RAG path worked end to end, but the pilot was not an accuracy study"
   Pilot evidence: {truncate(str(material['pilot']), 1000)}
   Usability status: {truncate(str(material['usability']), 420)}
   Present a balanced evidence panel: completed automated tests, coverage, memory demonstration,
   and a three-question live runbook pilot using 20 indexed Markdown runbooks and DeepSeek V4 Flash;
   mark live-model quality benchmarking and the practitioner study as not completed.

15. Contributions, limitations, and next work - "The contribution is a reproducible reference implementation with explicit limits"
   Contributions:
{bullet_block(material['contributions'], limit=3, indent=3)}
   Main limitations: {truncate(str(material['limitations']), 900)}
   Priority next work:
{bullet_block(material['recommendations'], limit=3, indent=3)}
   Avoid marketing language. Make "tested reference implementation" the strongest defensible claim.

16. Conclusion and questions - "InfraGuard AI makes first-pass triage more structured, inspectable, and reviewable"
   Synthesis: {truncate(str(material['conclusion']), 850)}
   Close with three short takeaways: bounded multi-source collection; provider-flexible structured
   reasoning with local runbook grounding; and operator-controlled memory/threat response.
   End with "Questions" rather than a generic thank-you slide. Add a small selected-references footer
   or a backup references slide if the platform permits an appendix.

Approved references for in-slide short citations and an optional appendix
{bullet_block(material['references'], limit=8, indent=0, max_chars=520)}
Use only references from this list unless another source is copied exactly from the report. Do not
invent bibliographic details. Suggested short citations include Ahmed et al. (2023), Beyer et al.
(2016), Hevner et al. (2004), Lewis et al. (2020), NIST (2024), and Yao et al. (2023).

Asset-use plan
Upload the following authentic project assets before generation and map them to the indicated slides:
{assets or '- No project figures were found; omit image placeholders rather than inventing evidence.'}

Copy and evidence rules
- Use no more than 3-5 short bullets on most slides; convert detail into presenter notes.
- Keep each slide focused on one claim and use a takeaway title rather than a topic label.
- Do not change "InfraGuard AI" to "InfraGuard Pro".
- Do not call the system autonomous remediation software.
- Do not imply that acknowledgements reduce inference calls or cost.
- Do not imply that three live questions establish RAG accuracy.
- Do not report a System Usability Scale score; the practitioner study was not completed.
- Do not describe the demonstration deployment as production-secure. Production hardening still
  requires HTTPS-only exposure, restricted telemetry/admin ports, secure cookies, managed secrets,
  a stricter CSP, and protected external audit storage.
- Preserve numerical precision exactly where metrics are shown.
- Include a final appendix/reference slide only if it does not dilute the 16-slide narrative.
"""

    header = (
        f"# Beautiful.ai generation prompt\n\n"
        f"Generated: {generated}\n"
        f"Source report: {report.path}\n\n"
    )
    return header + textwrap.dedent(prompt).strip() + "\n"


def main() -> int:
    if os.environ.get("INFRAGUARD_ALLOW_HISTORICAL_PROMPT") != "1":
        raise SystemExit(
            "Historical prompt generation is disabled. Use "
            "InfraGuard_AI_Masters_Project_DEFENCE_PRESENTATION.pptx. "
            "Set INFRAGUARD_ALLOW_HISTORICAL_PROMPT=1 only to reproduce the archived prompt."
        )
    script_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Generate a paste-ready Beautiful.ai final-defence prompt from the latest report."
    )
    parser.add_argument(
        "--docs-dir",
        type=Path,
        default=script_dir,
        help="Directory containing InfraGuard project DOCX files (default: script directory).",
    )
    parser.add_argument(
        "--sample",
        type=Path,
        help="Optional Sample_MIT.pptx path used to confirm the reference slide structure.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=script_dir / "beautiful_ai_prompt.txt",
        help="Output prompt path (default: beautiful_ai_prompt.txt beside this script).",
    )
    args = parser.parse_args()

    docs_dir = args.docs_dir.resolve()
    report_path = newest_report(docs_dir)
    report = extract_report(report_path)
    sample_slides = extract_sample_slides(args.sample.resolve() if args.sample else None)
    figures = find_figures(docs_dir)
    prompt = generate_prompt(report, sample_slides, figures)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(prompt, encoding="utf-8")

    print(f"Source report: {report_path}")
    print(f"Sample slides inspected: {len(sample_slides)}")
    print(f"Project figures listed: {len(figures)}")
    print(f"Beautiful.ai prompt: {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
