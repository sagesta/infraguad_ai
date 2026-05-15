"""Figure generator for the InfraGuard Pro master's project.

Produces fourteen PNG figures at 300 DPI suitable for embedding in the docx.
Charts in Chapter 5 carry an explicit "ILLUSTRATIVE — proposed evaluation protocol"
label since the project report has been reframed to present these as a planned
evaluation rather than measured results.
"""

from __future__ import annotations
import os
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Polygon
from matplotlib.lines import Line2D
import numpy as np

OUT = Path(__file__).parent
OUT.mkdir(exist_ok=True)

# ---- Visual style ----
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 10,
    'axes.titlesize': 11,
    'axes.labelsize': 10,
    'figure.dpi': 150,
    'savefig.dpi': 220,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

COLOURS = {
    'plane':   '#1f3a68',   # central control plane
    'sat':     '#2b6cb0',   # satellite
    'llm':     '#d97706',   # LLM provider
    'git':     '#7c3aed',   # git provider
    'data':    '#2f855a',   # data store
    'arrow':   '#475569',
    'note':    '#94a3b8',
    'accent':  '#dc2626',
    'bg':      '#f8fafc',
}

ILLUSTRATIVE_NOTE = (
    'Illustrative — figures depict expected outcomes from the proposed evaluation '
    'protocol; values are projections, not measurements.'
)


def _box(ax, x, y, w, h, label, fc, ec='#1e293b', tc='white', fs=9, lw=1.0):
    """Draw a rounded rectangle with a centred label."""
    patch = FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.04,rounding_size=0.08',
                           fc=fc, ec=ec, lw=lw)
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, label, ha='center', va='center',
            color=tc, fontsize=fs, weight='bold', wrap=True)


def _arrow(ax, x1, y1, x2, y2, label=None, style='-|>', dashed=False, color=None, fs=8):
    color = color or COLOURS['arrow']
    ls = '--' if dashed else '-'
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle=style, color=color, mutation_scale=12,
                            linestyle=ls, lw=1.2, shrinkA=2, shrinkB=2)
    ax.add_patch(arrow)
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, label,
                fontsize=fs, color='#1e293b',
                bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.8))


def _new_fig(w=10, h=6.2):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


# =====================================================================
# Figure 3.1 — High-Level System Architecture
# =====================================================================
def fig_3_1():
    fig, ax = _new_fig(11, 7)
    ax.set_xlim(0, 11); ax.set_ylim(0, 7)
    ax.text(5.5, 6.65, 'Figure 3.1  InfraGuard Pro — High-Level System Architecture',
            ha='center', fontsize=12, weight='bold')

    # Outer control-plane box
    _box(ax, 0.5, 1.2, 8.2, 4.6, '', '#eef2ff', '#3730a3', tc='#1e1b4b')
    ax.text(0.7, 5.55, 'CENTRAL CONTROL PLANE', fontsize=9, weight='bold', color='#3730a3')

    # Internal components
    _box(ax, 0.85, 4.55, 1.85, 0.7, 'FastAPI Service', COLOURS['plane'])
    _box(ax, 2.85, 4.55, 1.85, 0.7, 'Reasoning Agent\n(LangGraph)', COLOURS['plane'])
    _box(ax, 4.85, 4.55, 1.85, 0.7, 'Remediation\nEngine', COLOURS['accent'])
    _box(ax, 6.85, 4.55, 1.75, 0.7, 'Policy Engine', COLOURS['plane'])

    _box(ax, 0.85, 3.55, 1.85, 0.7, 'LLM Provider\nAbstraction', COLOURS['llm'])
    _box(ax, 2.85, 3.55, 1.85, 0.7, 'RAG Service\n(ChromaDB)', COLOURS['data'])
    _box(ax, 4.85, 3.55, 1.85, 0.7, 'Git Provider\nAdapter', COLOURS['git'])
    _box(ax, 6.85, 3.55, 1.75, 0.7, 'Closed-Loop\nValidator', COLOURS['accent'])

    _box(ax, 0.85, 2.55, 1.85, 0.7, 'Audit Service\n(hash-chained)', '#0f766e')
    _box(ax, 2.85, 2.55, 1.85, 0.7, 'Notification\nDispatcher', '#0f766e')
    _box(ax, 4.85, 2.55, 1.85, 0.7, 'Traceway +\nClickHouse', COLOURS['data'])
    _box(ax, 6.85, 2.55, 1.75, 0.7, 'PostgreSQL', COLOURS['data'])

    _box(ax, 2.4, 1.45, 4.3, 0.7, 'Dashboard (SvelteKit 5, dark-mode)', '#312e81')

    # External LLM providers (right)
    _box(ax, 9.0, 5.0, 1.8, 0.55, 'Vertex AI', COLOURS['llm'], fs=8)
    _box(ax, 9.0, 4.35, 1.8, 0.55, 'OpenAI', COLOURS['llm'], fs=8)
    _box(ax, 9.0, 3.70, 1.8, 0.55, 'Anthropic', COLOURS['llm'], fs=8)
    _box(ax, 9.0, 3.05, 1.8, 0.55, 'Moonshot Kimi', COLOURS['llm'], fs=8)
    _box(ax, 9.0, 2.40, 1.8, 0.55, 'Ollama (local)', COLOURS['llm'], fs=8)
    _box(ax, 9.0, 1.75, 1.8, 0.55, 'LM Studio', COLOURS['llm'], fs=8)
    _arrow(ax, 2.7, 3.85, 9.0, 4.0, dashed=True)

    # Git providers (left, beside satellite layer)
    _box(ax, 0.05, 0.20, 1.7, 0.5, 'GitHub', COLOURS['git'], fs=8)
    _box(ax, 1.85, 0.20, 1.7, 0.5, 'GitLab', COLOURS['git'], fs=8)
    _arrow(ax, 5.75, 3.55, 1.7, 0.7, dashed=True)

    # Satellites at bottom
    _box(ax, 4.6, 0.20, 2.0, 0.5, 'Satellite Fleet (HTTPS)', COLOURS['sat'], fs=8)
    _box(ax, 7.0, 0.20, 1.6, 0.5, 'Scanners (SARIF)', '#475569', fs=8)
    _arrow(ax, 1.0, 2.55, 5.6, 0.7, dashed=True)
    _arrow(ax, 7.0, 0.45, 4.0, 4.55, dashed=True)

    plt.tight_layout()
    plt.savefig(OUT / 'fig_3_1_architecture.png')
    plt.close()


# =====================================================================
# Figure 3.2 — Multi-Server Satellite Topology
# =====================================================================
def fig_3_2():
    fig, ax = _new_fig(10, 6.5)
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.text(5, 5.7, 'Figure 3.2  Multi-Server Satellite Deployment Topology',
            ha='center', fontsize=12, weight='bold')

    # Central hub
    _box(ax, 4.0, 2.5, 2.0, 0.9, 'Central Control Plane\n(Lagos / GCP region)', COLOURS['plane'])

    # 5 satellites in a star
    sats = [
        (1.2, 4.4, 'prod-eu-1\n(Frankfurt)'),
        (1.2, 1.0, 'prod-us-1\n(Iowa)'),
        (8.0, 4.4, 'staging-eu-1\n(Frankfurt)'),
        (8.0, 1.0, 'dev-local\n(Lagos office)'),
        (4.5, 0.2, 'prod-af-1\n(Lagos)'),
    ]
    for x, y, label in sats:
        _box(ax, x, y, 2.0, 0.8, label, COLOURS['sat'])
        _arrow(ax, 5.0, 2.95, x + 1.0, y + 0.4, dashed=True)

    # Inset
    inset_x, inset_y = 6.5, 2.4
    ax.add_patch(Rectangle((inset_x, inset_y), 3.3, 0.85, fc='#fef3c7', ec='#92400e', lw=1))
    ax.text(inset_x + 0.1, inset_y + 0.65, 'Satellite contents:', fontsize=8, weight='bold', color='#92400e')
    ax.text(inset_x + 0.1, inset_y + 0.45, '• Agent + SQLite buffer', fontsize=7, color='#92400e')
    ax.text(inset_x + 0.1, inset_y + 0.28, '• Prometheus + Promtail', fontsize=7, color='#92400e')
    ax.text(inset_x + 0.1, inset_y + 0.11, '• CrowdSec + workload containers', fontsize=7, color='#92400e')

    # legend
    ax.text(0.2, 2.3, 'Dashed line = HTTPS heartbeat\n(60s; OTLP push + REST poll)',
            fontsize=8, color='#475569', bbox=dict(boxstyle='round', fc='white', ec='#cbd5e1'))

    plt.tight_layout()
    plt.savefig(OUT / 'fig_3_2_topology.png')
    plt.close()


# =====================================================================
# Figure 3.3 — Remediation Engine Data Flow
# =====================================================================
def fig_3_3():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 11); ax.set_ylim(0, 6.4)
    ax.set_aspect('auto')
    ax.axis('off')
    ax.text(5.5, 6.1, 'Figure 3.3  Autonomous Remediation Engine — End-to-End Data Flow',
            ha='center', fontsize=12, weight='bold')

    steps = [
        (0.3, 'CI/CD\nPipeline', '#475569'),
        (1.6, 'SARIF\nIngest', COLOURS['plane']),
        (2.9, 'Normalise\n→ findings', COLOURS['plane']),
        (4.2, 'RAG\nRetrieve', COLOURS['data']),
        (5.5, 'LLM\nReason', COLOURS['llm']),
        (6.8, 'Policy\nClassify', COLOURS['plane']),
        (8.1, 'Git PR\nOpen', COLOURS['git']),
        (9.4, 'Merge +\nRe-scan', COLOURS['accent']),
        (10.7, 'Validate\nOutcome', COLOURS['accent']),
    ]
    y_box = 3.4
    for x, label, fc in steps:
        _box(ax, x - 0.55, y_box, 1.05, 0.85, label, fc, fs=7.5)
    for i in range(len(steps) - 1):
        _arrow(ax, steps[i][0] + 0.5, y_box + 0.42, steps[i + 1][0] - 0.55, y_box + 0.42)

    # Feedback loop
    _box(ax, 4.6, 1.4, 2.6, 0.7, 'Outcome → RAG corpus (historical fix index)', '#0f766e', fs=8)
    _arrow(ax, 10.5, 3.4, 7.2, 2.1, dashed=True, color=COLOURS['accent'])
    _arrow(ax, 4.6, 1.75, 4.2, 3.4, dashed=True, color=COLOURS['accent'])

    # Audit log strip
    ax.add_patch(Rectangle((0.1, 0.3), 10.7, 0.55, fc='#fef9c3', ec='#854d0e'))
    ax.text(5.45, 0.575, 'Audit log entry per step (SHA-256 hash chained, tamper-evident)',
            ha='center', fontsize=8, weight='bold', color='#854d0e')

    plt.tight_layout()
    plt.savefig(OUT / 'fig_3_3_remediation_flow.png')
    plt.close()


# =====================================================================
# Figure 3.4 — Use-Case Diagram
# =====================================================================
def fig_3_4():
    fig, ax = _new_fig(10, 7)
    ax.set_xlim(0, 10); ax.set_ylim(0, 7)
    ax.text(5, 6.7, 'Figure 3.4  Use-Case Diagram — DevSecOps Operator', ha='center', fontsize=12, weight='bold')

    # System boundary
    ax.add_patch(Rectangle((2.5, 0.6), 5, 5.6, fc='#f1f5f9', ec='#334155', lw=1.5))
    ax.text(5, 6.05, 'InfraGuard Pro', ha='center', fontsize=10, weight='bold', color='#334155')

    # Actors (stick figures)
    def stick(ax, x, y, label):
        ax.add_patch(Circle((x, y + 0.5), 0.13, fc='#1e293b'))
        ax.plot([x, x], [y, y + 0.35], color='#1e293b', lw=1.5)
        ax.plot([x - 0.2, x + 0.2], [y + 0.25, y + 0.25], color='#1e293b', lw=1.5)
        ax.plot([x, x - 0.18], [y, y - 0.3], color='#1e293b', lw=1.5)
        ax.plot([x, x + 0.18], [y, y - 0.3], color='#1e293b', lw=1.5)
        ax.text(x, y - 0.55, label, ha='center', fontsize=9, weight='bold')

    stick(ax, 0.9, 4.5, 'Operator')
    stick(ax, 0.9, 2.0, 'Developer')
    stick(ax, 9.1, 4.5, 'CI/CD\nPipeline')
    stick(ax, 9.1, 2.0, 'LLM\nProvider')

    # Use cases (ellipses)
    use_cases = [
        (5, 5.4, 'Ingest SARIF'),
        (5, 4.7, 'Review verdicts feed'),
        (5, 4.0, 'Approve / reject patch'),
        (5, 3.3, 'Switch LLM provider'),
        (5, 2.6, 'Inspect validation outcome'),
        (5, 1.9, 'Roll back failed patch'),
        (5, 1.2, 'Search runbooks'),
    ]
    for x, y, t in use_cases:
        ell = mpatches.Ellipse((x, y), 3.2, 0.5, fc='#dbeafe', ec='#1e3a8a')
        ax.add_patch(ell)
        ax.text(x, y, t, ha='center', va='center', fontsize=8, color='#1e3a8a')

    # actor → use case lines
    for y in [4.7, 4.0, 3.3, 2.6, 1.9, 1.2]:
        ax.plot([1.25, 3.4], [4.5, y], color='#475569', lw=0.7)
    ax.plot([1.25, 3.4], [2.0, 1.9], color='#475569', lw=0.7)  # developer
    ax.plot([8.75, 6.6], [4.5, 5.4], color='#475569', lw=0.7)  # pipeline → ingest
    ax.plot([8.75, 6.6], [2.0, 2.6], color='#475569', lw=0.7)  # LLM → inspect (proxy)

    plt.tight_layout()
    plt.savefig(OUT / 'fig_3_4_usecase.png')
    plt.close()


# =====================================================================
# Figure 3.5 — Sequence Diagram (SARIF → PR)
# =====================================================================
def fig_3_5():
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 11); ax.set_ylim(0, 8)
    ax.axis('off')
    ax.text(5.5, 7.7, 'Figure 3.5  Sequence Diagram — SARIF Ingestion to Merged Pull Request',
            ha='center', fontsize=12, weight='bold')

    actors = ['CI/CD\nPipeline', 'SARIF\nAdapter', 'Remediation\nEngine', 'RAG\nService',
              'LLM\nProvider', 'Policy\nEngine', 'Git\nProvider', 'Validator']
    xs = np.linspace(0.7, 10.3, len(actors))
    y_top, y_bot = 7.0, 0.5

    for x, label in zip(xs, actors):
        _box(ax, x - 0.55, 6.85, 1.1, 0.45, label, COLOURS['plane'], fs=7.5)
        ax.plot([x, x], [y_top - 0.4, y_bot], color='#94a3b8', lw=0.8, ls='--')

    msgs = [
        (0, 1, 'POST SARIF',     6.45),
        (1, 2, 'normalised findings', 5.95),
        (2, 3, 'query(top-k)',   5.45),
        (3, 2, 'docs + history', 4.95),
        (2, 4, 'reason(ctx)',    4.45),
        (4, 2, 'patch + conf',   3.95),
        (2, 5, 'classify',       3.45),
        (5, 2, 'mode',           2.95),
        (2, 6, 'open PR (autonomous)', 2.45),
        (6, 2, 'pr_url',         1.95),
        (6, 7, 'on-merge webhook', 1.45),
        (7, 6, 'rescan + observe → outcome', 0.95),
    ]
    for s, e, label, y in msgs:
        x1, x2 = xs[s], xs[e]
        _arrow(ax, x1, y, x2, y, label=label, fs=7.5)

    plt.tight_layout()
    plt.savefig(OUT / 'fig_3_5_sequence.png')
    plt.close()


# =====================================================================
# Figure 3.6 — Entity-Relationship Diagram
# =====================================================================
def fig_3_6():
    fig, ax = _new_fig(11, 7)
    ax.set_xlim(0, 11); ax.set_ylim(0, 7)
    ax.text(5.5, 6.7, 'Figure 3.6  Entity-Relationship Diagram — Verdict & Remediation Schema',
            ha='center', fontsize=12, weight='bold')

    entities = [
        (0.4, 4.6, 1.9, 'satellites', ['id (PK)', 'label', 'environment', 'region', 'status', 'last_heartbeat']),
        (3.0, 4.6, 1.9, 'containers',  ['id (PK)', 'satellite_id (FK)', 'name', 'image', 'cpu_pct', 'restart_count']),
        (5.6, 5.0, 1.9, 'findings',    ['id (PK)', 'source_scanner', 'rule_id', 'cwe', 'cve', 'cvss', 'severity']),
        (8.2, 5.0, 2.4, 'remediations',['id (PK)', 'finding_id (FK)', 'llm_provider', 'llm_model',
                                         'patch_diff', 'confidence', 'policy_mode', 'pr_url']),
        (8.2, 1.8, 2.4, 'validations', ['id (PK)', 'remediation_id (FK)', 'rescan_status',
                                         'runtime_regression', 'outcome']),
        (5.6, 1.8, 1.9, 'verdicts',    ['id (PK)', 'satellite_id (FK)', 'severity', 'summary', 'payload']),
        (3.0, 1.8, 1.9, 'audit_log',   ['id (PK)', 'actor', 'action', 'entity_type', 'prev_hash', 'hash']),
        (0.4, 1.8, 1.9, 'users',       ['id (PK)', 'username', 'role', 'last_login']),
    ]
    coords = {}
    for x, y, w, name, fields in entities:
        h = 0.3 + 0.22 * len(fields) + 0.1
        ax.add_patch(Rectangle((x, y - h), w, h, fc='white', ec='#1e293b', lw=1.2))
        ax.add_patch(Rectangle((x, y - 0.25), w, 0.25, fc='#1e293b'))
        ax.text(x + w/2, y - 0.125, name, ha='center', va='center', color='white', fontsize=8, weight='bold')
        for i, f in enumerate(fields):
            ax.text(x + 0.1, y - 0.42 - i*0.22, f, fontsize=7, color='#1e293b')
        coords[name] = (x + w/2, y - h/2, x, y - h, x + w, y)

    def connect(a, b, label=''):
        ax, ay = coords[a][0], coords[a][1]
        bx, by = coords[b][0], coords[b][1]
        ax_p, ay_p = ax, ay
        bx_p, by_p = bx, by
        _arrow(plt.gca(), ax_p, ay_p, bx_p, by_p, label=label, style='-|>', color='#475569', fs=7)

    connect('satellites', 'containers', '1..*')
    connect('satellites', 'verdicts',   '1..*')
    connect('findings', 'remediations', '1..1')
    connect('remediations', 'validations', '1..1')
    connect('users', 'audit_log', '1..*')

    plt.tight_layout()
    plt.savefig(OUT / 'fig_3_6_erd.png')
    plt.close()


# =====================================================================
# Figure 3.7 — LangGraph State Machine
# =====================================================================
def fig_3_7():
    fig, ax = _new_fig(11, 5.5)
    ax.set_xlim(0, 11); ax.set_ylim(0, 5)
    ax.text(5.5, 4.7, 'Figure 3.7  State Machine of the LangGraph Reasoning Agent',
            ha='center', fontsize=12, weight='bold')

    states = [
        (0.6, 2.5, 'Collect'),
        (2.2, 2.5, 'Retrieve'),
        (3.8, 2.5, 'Analyse'),
        (5.4, 2.5, 'Classify'),
        (7.0, 2.5, 'Remediate'),
        (8.6, 2.5, 'Validate'),
        (10.2, 2.5, 'Notify'),
    ]
    for x, y, name in states:
        c = Circle((x, y), 0.55, fc=COLOURS['plane'], ec='#0c1e3d')
        ax.add_patch(c)
        ax.text(x, y, name, ha='center', va='center', color='white', fontsize=9, weight='bold')

    for i in range(len(states) - 1):
        _arrow(ax, states[i][0] + 0.55, states[i][1], states[i+1][0] - 0.55, states[i+1][1])

    # Failure path
    _arrow(ax, 3.8, 1.95, 10.2, 1.95, dashed=True, color=COLOURS['accent'],
           label='on irrecoverable error → Notify')

    # Reflection loop on validate failure
    _arrow(ax, 8.6, 3.05, 3.8, 3.05, dashed=True, color='#0f766e',
           label='validation fail → Reflexion-style retry (≤ 3)')

    plt.tight_layout()
    plt.savefig(OUT / 'fig_3_7_state_machine.png')
    plt.close()


# =====================================================================
# Figure 4.1 — Folder Structure
# =====================================================================
def fig_4_1():
    fig, ax = plt.subplots(figsize=(8.5, 9))
    ax.set_xlim(0, 10); ax.set_ylim(0, 14)
    ax.axis('off')
    ax.text(5, 13.6, 'Figure 4.1  Folder Structure of the Reference Implementation',
            ha='center', fontsize=12, weight='bold')

    tree = [
        (0.2, 13.0, 'infraguard_pro/', True),
        (0.8, 12.5, 'agent/', True),
        (1.4, 12.0, 'main.py'),
        (1.4, 11.6, 'orchestrator.py  (LangGraph)'),
        (1.4, 11.2, 'llm/  (provider abstraction)'),
        (2.0, 10.8, 'provider.py'),
        (2.0, 10.4, 'vertex.py / openai.py / anthropic.py'),
        (2.0, 10.0, 'kimi.py / ollama.py / lmstudio.py'),
        (1.4, 9.6, 'rag/  (multi-source RAG)'),
        (2.0, 9.2, 'vector_store.py'),
        (2.0, 8.8, 'notion_loader.py / markdown_loader.py'),
        (2.0, 8.4, 'verdict_indexer.py'),
        (1.4, 8.0, 'remediation/  ★ new'),
        (2.0, 7.6, 'engine.py'),
        (2.0, 7.2, 'sarif.py'),
        (2.0, 6.8, 'policy.py'),
        (2.0, 6.4, 'git_provider.py'),
        (2.0, 6.0, 'patch_builder.py'),
        (2.0, 5.6, 'validator.py  (closed-loop)'),
        (1.4, 5.2, 'tools/  (Prometheus, Loki, Docker, …)'),
        (0.8, 4.8, 'api/'),
        (1.4, 4.4, 'main.py  +  routes/  +  middleware/'),
        (1.4, 4.0, 'store/  (PostgreSQL via SQLAlchemy 2)'),
        (0.8, 3.6, 'satellite/  ★ new'),
        (1.4, 3.2, 'main.py / heartbeat.py / action_executor.py'),
        (1.4, 2.8, 'Dockerfile  (Python 3.11-slim, ~110 MB)'),
        (0.8, 2.4, 'dashboard/  (SvelteKit 5 + Tailwind 4)'),
        (0.8, 2.0, 'tests/  (~400 tests, pytest + respx + hypothesis)'),
        (0.8, 1.6, 'terraform/  (GCP IaC)'),
        (0.8, 1.2, '.github/workflows/  (ci.yml + deploy.yml)'),
        (0.8, 0.8, 'docker-compose.yml / docker-compose.satellite.yml'),
    ]
    for entry in tree:
        if len(entry) == 4:
            x, y, label, bold = entry
            ax.text(x, y, label, fontsize=10, weight='bold', family='monospace', color='#1e293b')
        else:
            x, y, label = entry
            ax.text(x, y, label, fontsize=9.5, family='monospace', color='#334155')

    ax.text(5.5, 0.2, '★ = new modules introduced by this project',
            fontsize=8, color=COLOURS['accent'], weight='bold')

    plt.tight_layout()
    plt.savefig(OUT / 'fig_4_1_folder.png')
    plt.close()


# =====================================================================
# Figure 4.2 — LLM Provider Class Hierarchy
# =====================================================================
def fig_4_2():
    fig, ax = _new_fig(11, 6)
    ax.set_xlim(0, 11); ax.set_ylim(0, 5.5)
    ax.text(5.5, 5.25, 'Figure 4.2  LLM Provider Abstraction — Class Hierarchy', ha='center', fontsize=12, weight='bold')

    # Abstract base
    _box(ax, 4.0, 3.8, 3.0, 0.95, '«abstract»\nLLMProvider\n+ reason(ctx) → Verdict\n+ health_check() → bool',
         '#1e293b', tc='white', fs=8.5)

    # Concrete providers
    providers = [
        (0.2, 1.5, 'VertexAIProvider\ngemini-2.5-flash', COLOURS['llm']),
        (2.0, 1.5, 'OpenAIProvider\ngpt-4o', COLOURS['llm']),
        (3.8, 1.5, 'AnthropicProvider\nclaude-3.5-sonnet', COLOURS['llm']),
        (5.6, 1.5, 'KimiProvider\nkimi-k2', COLOURS['llm']),
        (7.4, 1.5, 'OllamaProvider\nllama3.1/deepseek-r1', COLOURS['llm']),
        (9.2, 1.5, 'LMStudioProvider\nOAI-compat local', COLOURS['llm']),
    ]
    for x, y, label, fc in providers:
        _box(ax, x, y, 1.65, 1.05, label, fc, fs=7.5)
        _arrow(ax, x + 0.825, 2.55, 5.5, 3.8, style='-|>', color='#1e293b')

    # Registry + monitor
    _box(ax, 0.5, 0.1, 2.5, 0.7, 'ProviderRegistry\nget_active / set_active', '#0f766e', fs=8)
    _box(ax, 7.5, 0.1, 3.0, 0.7, 'ProviderHealthMonitor\nperiodic liveness + fallback', '#0f766e', fs=8)
    _arrow(ax, 3.0, 0.45, 7.5, 0.45, dashed=True)

    plt.tight_layout()
    plt.savefig(OUT / 'fig_4_2_llm_classes.png')
    plt.close()


# =====================================================================
# Figure 4.3 — Dashboard Overview mock
# =====================================================================
def fig_4_3():
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 11); ax.set_ylim(0, 7)
    ax.axis('off')
    ax.text(5.5, 6.7, 'Figure 4.3  Dashboard Overview Page — Multi-Server Fleet View (mock)',
            ha='center', fontsize=12, weight='bold')

    # Window chrome
    ax.add_patch(Rectangle((0.1, 0.2), 10.8, 6.1, fc='#0b1220', ec='#1e293b'))
    # Sidebar
    ax.add_patch(Rectangle((0.1, 0.2), 1.3, 6.1, fc='#020617'))
    for i, label in enumerate(['Overview', 'Servers', 'Verdicts', 'Remediation',
                                'Runbooks', 'Threats', 'AI Config', 'Audit']):
        ax.text(0.25, 5.6 - i * 0.55, label, color='#cbd5e1', fontsize=9,
                weight='bold' if i == 0 else 'normal')

    # Top bar
    ax.text(1.7, 6.0, 'InfraGuard Pro',  color='white', fontsize=11, weight='bold')
    ax.text(1.7, 5.7, 'Fleet: 5 servers · 38 containers · 2 active critical · LLM: Claude 3.5 Sonnet',
            color='#94a3b8', fontsize=8)

    # Severity cards
    cards = [('OK', '34', '#16a34a'), ('Warning', '6', '#ca8a04'),
             ('High', '4', '#ea580c'), ('Critical', '2', '#dc2626')]
    for i, (label, n, c) in enumerate(cards):
        x = 1.7 + i * 2.2
        ax.add_patch(FancyBboxPatch((x, 4.4), 2.0, 0.95, boxstyle='round,pad=0.04', fc='#0f172a', ec=c))
        ax.text(x + 0.15, 5.2, label, color=c, fontsize=9, weight='bold')
        ax.text(x + 0.15, 4.55, n, color='white', fontsize=18, weight='bold')

    # Server cards
    servers = [('prod-af-1', 'Lagos', '12 ctrs', '#16a34a'),
               ('prod-eu-1', 'Frankfurt', '10 ctrs', '#dc2626'),
               ('prod-us-1', 'Iowa', '8 ctrs', '#ca8a04'),
               ('staging-eu-1', 'Frankfurt', '5 ctrs', '#16a34a'),
               ('dev-local', 'Lagos office', '3 ctrs', '#16a34a')]
    for i, (name, region, ctrs, c) in enumerate(servers):
        x = 1.7 + (i % 5) * 1.85
        ax.add_patch(FancyBboxPatch((x, 2.95), 1.7, 1.1, boxstyle='round,pad=0.04', fc='#0f172a', ec='#334155'))
        ax.add_patch(Circle((x + 0.15, 3.9), 0.07, fc=c))
        ax.text(x + 0.3, 3.86, name, color='white', fontsize=8, weight='bold')
        ax.text(x + 0.15, 3.55, region, color='#94a3b8', fontsize=7)
        ax.text(x + 0.15, 3.30, ctrs, color='#cbd5e1', fontsize=7)
        ax.text(x + 0.15, 3.05, 'CPU 41% · RAM 62%', color='#94a3b8', fontsize=6)

    # Latest verdicts feed
    ax.add_patch(FancyBboxPatch((1.7, 0.45), 9.0, 2.3, boxstyle='round,pad=0.04', fc='#0f172a', ec='#334155'))
    ax.text(1.85, 2.55, 'Recent Verdicts', color='white', fontsize=9.5, weight='bold')
    feed = [('CRITICAL', 'prod-eu-1', 'urllib3 1.26.7 → CVE-2024-37891 — autonomous PR #341 merged', '#dc2626'),
            ('HIGH',     'prod-us-1', 'nginx:1.22 base image vulnerable — approval queued', '#ea580c'),
            ('WARN',     'prod-af-1', 'p95 latency rising on api-gw; correlated with Traceway trace 8a3f…', '#ca8a04'),
            ('OK',       'staging-eu-1', 'overnight rescan clean across 5 services', '#16a34a')]
    for i, (sev, srv, msg, c) in enumerate(feed):
        y = 2.2 - i * 0.42
        ax.add_patch(Rectangle((1.85, y - 0.05), 0.65, 0.3, fc=c))
        ax.text(2.175, y + 0.10, sev, color='white', fontsize=7, ha='center', weight='bold')
        ax.text(2.6, y + 0.10, srv, color='#cbd5e1', fontsize=8)
        ax.text(3.7, y + 0.10, msg, color='#94a3b8', fontsize=8)

    plt.tight_layout()
    plt.savefig(OUT / 'fig_4_3_dashboard.png')
    plt.close()


# =====================================================================
# Chapter 5 charts (ILLUSTRATIVE)
# =====================================================================
def _add_illustrative_banner(ax):
    ax.figure.text(0.5, 0.005, ILLUSTRATIVE_NOTE, ha='center', fontsize=7,
                   style='italic', color='#64748b')


def fig_5_1():
    """Projected patch acceptance rate by LLM provider and severity."""
    fig, ax = plt.subplots(figsize=(10, 5.5))
    providers = ['Vertex AI\nGemini 2.5 Flash', 'OpenAI\nGPT-4o', 'Anthropic\nClaude 3.5 Sonnet',
                 'Moonshot\nKimi-K2', 'Ollama\nLlama 3.1 8B', 'Ensemble\n(best-of-3)']
    # Projected values
    crit   = [62, 70, 73, 55, 38, 82]
    high   = [76, 84, 86, 70, 55, 92]
    med    = [85, 90, 92, 80, 71, 96]
    low    = [92, 95, 96, 88, 80, 98]
    x = np.arange(len(providers))
    w = 0.2
    ax.bar(x - 1.5*w, crit, w, label='Critical', color='#dc2626')
    ax.bar(x - 0.5*w, high, w, label='High',     color='#ea580c')
    ax.bar(x + 0.5*w, med,  w, label='Medium',   color='#ca8a04')
    ax.bar(x + 1.5*w, low,  w, label='Low',      color='#16a34a')
    ax.set_xticks(x); ax.set_xticklabels(providers, fontsize=8)
    ax.set_ylabel('Projected Patch Acceptance Rate (%)')
    ax.set_ylim(0, 110)
    ax.set_title('Figure 5.1  Projected Patch Acceptance Rate by LLM Provider and Severity')
    ax.legend(loc='upper left', ncol=4, frameon=False, fontsize=8)
    ax.grid(axis='y', linestyle=':', alpha=0.4)
    _add_illustrative_banner(ax)
    plt.tight_layout()
    plt.savefig(OUT / 'fig_5_1_acceptance.png')
    plt.close()


def fig_5_2():
    """Projected MTTR distribution across remediation modes."""
    fig, ax = plt.subplots(figsize=(10, 5))
    rng = np.random.default_rng(42)
    auto    = rng.lognormal(mean=1.4, sigma=0.35, size=200)   # ~ 4 min median
    appr    = rng.lognormal(mean=3.3, sigma=0.30, size=200)   # ~ 27 min median
    manual  = rng.lognormal(mean=6.6, sigma=0.55, size=200)   # ~ 14 h median (in minutes)
    data = [auto, appr, manual / 60.0]  # convert manual to hours scale via /60 then in min units? keep mins
    # Plot in minutes for first two and hours for manual? Simpler: log-scale x in minutes
    fig, ax = plt.subplots(figsize=(10, 5))
    bp = ax.boxplot([auto, appr, manual], labels=['Autonomous mode', 'Human-approval', 'Manual baseline'],
                    patch_artist=True, widths=0.55, showfliers=False)
    for patch, c in zip(bp['boxes'], ['#16a34a', '#ca8a04', '#dc2626']):
        patch.set_facecolor(c); patch.set_alpha(0.7)
    ax.set_yscale('log')
    ax.set_ylabel('End-to-end MTTR (minutes, log scale)')
    ax.set_title('Figure 5.2  Projected Mean Time-to-Remediate Distribution Across Modes')
    ax.grid(axis='y', which='both', linestyle=':', alpha=0.4)
    _add_illustrative_banner(ax)
    plt.tight_layout()
    plt.savefig(OUT / 'fig_5_2_mttr.png')
    plt.close()


def fig_5_3():
    """Projected LLM cost per remediation by provider."""
    fig, ax = plt.subplots(figsize=(10, 5))
    providers = ['Vertex AI\nGemini 2.5 Flash', 'OpenAI\nGPT-4o', 'Anthropic\nClaude 3.5 Sonnet',
                 'Moonshot\nKimi-K2', 'Ollama\n(self-hosted)', 'LM Studio\n(self-hosted)']
    costs = [0.0006, 0.0084, 0.0173, 0.0019, 0.0000, 0.0000]
    colors = ['#1f3a68', '#10a37f', '#d97706', '#7c3aed', '#475569', '#475569']
    bars = ax.bar(providers, costs, color=colors)
    for bar, c in zip(bars, costs):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.0003,
                f'${c:.4f}' if c else 'self-hosted', ha='center', fontsize=8)
    ax.set_ylabel('Projected USD Cost per Remediation')
    ax.set_ylim(0, max(costs) * 1.4)
    ax.set_title('Figure 5.3  Projected LLM Cost per Remediation by Provider')
    plt.setp(ax.get_xticklabels(), fontsize=8)
    ax.grid(axis='y', linestyle=':', alpha=0.4)
    _add_illustrative_banner(ax)
    plt.tight_layout()
    plt.savefig(OUT / 'fig_5_3_cost.png')
    plt.close()


def fig_5_4():
    """Projected confidence calibration curve."""
    fig, ax = plt.subplots(figsize=(8.5, 6))
    bins = np.linspace(0.1, 1.0, 10)
    # Diagonal reference
    ax.plot([0, 1], [0, 1], color='#94a3b8', linestyle='--', label='Perfect calibration')
    series = {
        'OpenAI GPT-4o':        [0.18, 0.30, 0.41, 0.52, 0.61, 0.70, 0.79, 0.86, 0.92, 0.96],
        'Anthropic Claude 3.5': [0.20, 0.32, 0.44, 0.55, 0.65, 0.74, 0.82, 0.88, 0.93, 0.97],
        'Vertex AI Gemini 2.5': [0.12, 0.22, 0.34, 0.47, 0.59, 0.69, 0.78, 0.85, 0.91, 0.95],
        'Moonshot Kimi-K2':     [0.30, 0.34, 0.41, 0.50, 0.58, 0.66, 0.72, 0.78, 0.82, 0.85],
        'Ollama Llama 3.1 8B':  [0.42, 0.43, 0.46, 0.50, 0.54, 0.57, 0.61, 0.64, 0.67, 0.70],
    }
    colors = ['#10a37f', '#d97706', '#1f3a68', '#7c3aed', '#475569']
    for (lbl, y), c in zip(series.items(), colors):
        ax.plot(bins, y, marker='o', label=lbl, color=c, lw=1.3)
    ax.set_xlabel('Reported Confidence')
    ax.set_ylabel('Empirical Correctness Rate')
    ax.set_title('Figure 5.4  Projected Confidence-Calibration Curve')
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.grid(linestyle=':', alpha=0.4)
    ax.legend(fontsize=8, loc='lower right', frameon=False)
    _add_illustrative_banner(ax)
    plt.tight_layout()
    plt.savefig(OUT / 'fig_5_4_calibration.png')
    plt.close()


def main():
    fig_3_1(); print('OK fig_3_1')
    fig_3_2(); print('OK fig_3_2')
    fig_3_3(); print('OK fig_3_3')
    fig_3_4(); print('OK fig_3_4')
    fig_3_5(); print('OK fig_3_5')
    fig_3_6(); print('OK fig_3_6')
    fig_3_7(); print('OK fig_3_7')
    fig_4_1(); print('OK fig_4_1')
    fig_4_2(); print('OK fig_4_2')
    fig_4_3(); print('OK fig_4_3')
    fig_5_1(); print('OK fig_5_1')
    fig_5_2(); print('OK fig_5_2')
    fig_5_3(); print('OK fig_5_3')
    fig_5_4(); print('OK fig_5_4')


if __name__ == '__main__':
    main()
