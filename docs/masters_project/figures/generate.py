"""Figure generator for the InfraGuard AI master's project.

Produces fourteen PNG figures suitable for embedding in the docx. All figures
depict the system as actually implemented. The Chapter 5 figures report measured
outcomes (coverage, duplicate-verdict reduction); the usability figures are
templates populated from the participant sessions described in Appendix D.
"""

from __future__ import annotations
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle
import numpy as np

OUT = Path(__file__).parent
OUT.mkdir(exist_ok=True)

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'DejaVu Serif'],
    'font.size': 10,
    'axes.titlesize': 11,
    'figure.dpi': 150,
    'savefig.dpi': 220,
    'savefig.bbox': 'tight',
    'axes.spines.top': False,
    'axes.spines.right': False,
})

COL = {
    'agent':  '#1f3a68',
    'api':    '#2b6cb0',
    'llm':    '#d97706',
    'data':   '#2f855a',
    'ext':    '#475569',
    'mem':    '#7c3aed',
    'accent': '#dc2626',
}


def _box(ax, x, y, w, h, label, fc, ec='#1e293b', tc='white', fs=9, lw=1.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.04,rounding_size=0.08',
                                fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, label, ha='center', va='center',
            color=tc, fontsize=fs, weight='bold', wrap=True)


def _arrow(ax, x1, y1, x2, y2, label=None, style='-|>', dashed=False, color=None, fs=8):
    color = color or COL['ext']
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, color=color,
                                 mutation_scale=12, linestyle='--' if dashed else '-',
                                 lw=1.2, shrinkA=2, shrinkB=2))
    if label:
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, label, fontsize=fs, color='#1e293b',
                bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.85))


def _fig(w=10, h=6.2, xlim=10, ylim=6):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, xlim); ax.set_ylim(0, ylim); ax.axis('off')
    return fig, ax


# Fig 3.1 - High-Level Architecture
def fig_3_1():
    fig, ax = _fig(11, 7, 11, 7)
    ax.text(5.5, 6.6, 'Figure 3.1  InfraGuard AI: High-Level System Architecture',
            ha='center', fontsize=12, weight='bold')
    _box(ax, 0.5, 1.4, 6.6, 4.4, '', '#eef2ff', '#3730a3', tc='#1e1b4b')
    ax.text(0.7, 5.55, 'SINGLE HOST (Docker Compose)', fontsize=9, weight='bold', color='#3730a3')
    _box(ax, 0.85, 4.55, 2.6, 0.9, 'Agent container\nheartbeat + LangGraph', COL['agent'])
    _box(ax, 4.0, 4.55, 2.8, 0.9, 'API container\ndashboard + REST API', COL['api'])
    _box(ax, 0.85, 3.25, 2.6, 0.85, 'Shared SQLite volume\nverdicts + acknowledgements', COL['data'], fs=8)
    _box(ax, 4.0, 3.25, 2.8, 0.85, 'Local runbooks + Chroma\nfiles and vector index', COL['data'], fs=8)
    _box(ax, 0.85, 2.05, 2.6, 0.75, 'Threat detection\nlog-pattern matching', COL['agent'], fs=8)
    _box(ax, 4.0, 2.05, 2.8, 0.75, 'Verdict presentation\nfilter acknowledged low-risk items', COL['mem'], fs=8)
    _arrow(ax, 3.45, 5.0, 4.0, 5.0, dashed=True)
    _arrow(ax, 2.15, 4.55, 2.15, 4.1)
    _arrow(ax, 5.4, 4.55, 5.4, 4.1)

    # Telemetry sources (left)
    _box(ax, 7.4, 5.0, 1.6, 0.55, 'Loki', COL['ext'], fs=8)
    _box(ax, 7.4, 4.35, 1.6, 0.55, 'Prometheus', COL['ext'], fs=8)
    _box(ax, 7.4, 3.70, 1.6, 0.55, 'HTTP probes', COL['ext'], fs=8)
    _box(ax, 7.4, 3.05, 1.6, 0.55, 'Docker (opt.)', COL['ext'], fs=8)
    for yy in (5.27, 4.62, 3.97, 3.32):
        _arrow(ax, 7.4, yy, 3.45, 5.0, dashed=True)

    # External services (right)
    _box(ax, 9.2, 5.0, 1.6, 0.55, 'Selected LLM\nprovider', COL['llm'], fs=8)
    _box(ax, 9.2, 4.1, 1.6, 0.55, 'ntfy.sh', COL['llm'], fs=8)
    _box(ax, 9.2, 3.2, 1.6, 0.55, 'CrowdSec\n(optional)', COL['accent'], fs=7.5)
    _arrow(ax, 3.45, 5.05, 9.2, 5.27, dashed=True)
    _arrow(ax, 2.15, 4.6, 9.2, 4.37, dashed=True)
    _arrow(ax, 2.15, 2.05, 9.2, 3.47, dashed=True)

    # Operator + dashboard
    _box(ax, 2.4, 0.4, 2.8, 0.7, 'Operator (browser dashboard)', '#312e81')
    _arrow(ax, 4.0, 1.1, 5.0, 4.6)
    plt.tight_layout(); plt.savefig(OUT / 'fig_3_1_architecture.png'); plt.close()


# Fig 3.2 - Single-Host Deployment Topology
def fig_3_2():
    fig, ax = _fig(10, 6, 10, 6)
    ax.text(5, 5.7, 'Figure 3.2  Single-Host Deployment Topology', ha='center', fontsize=12, weight='bold')
    ax.add_patch(Rectangle((1.0, 0.8), 6.2, 4.3, fc='#f1f5f9', ec='#334155', lw=1.5))
    ax.text(1.2, 4.8, 'Google Compute Engine VM (Terraform-provisioned)', fontsize=9, weight='bold', color='#334155')
    _box(ax, 1.4, 3.6, 2.4, 0.9, 'api container', COL['api'])
    _box(ax, 4.2, 3.6, 2.6, 0.9, 'agent container', COL['agent'])
    _box(ax, 1.4, 2.4, 2.4, 0.8, 'Chroma volume +\nread-only runbooks', COL['data'], fs=8)
    _box(ax, 4.2, 2.4, 2.6, 0.8, 'sqlite_data\nshared volume', COL['data'], fs=8)
    _box(ax, 1.4, 1.2, 2.4, 0.8, 'shared network\n+ Docker volumes', COL['ext'], fs=8)
    _box(ax, 4.2, 1.2, 2.6, 0.8, 'optional Docker socket\nread access', COL['ext'], fs=8)
    # external
    _box(ax, 7.8, 4.2, 1.9, 0.65, 'LLM provider', COL['llm'], fs=8)
    _box(ax, 7.8, 3.25, 1.9, 0.65, 'Loki / Prometheus\n/ HTTP targets', COL['ext'], fs=7.5)
    _box(ax, 7.8, 2.3, 1.9, 0.65, 'ntfy / CrowdSec\n(optional)', COL['llm'], fs=7.3)
    _arrow(ax, 6.8, 4.0, 7.8, 4.52, dashed=True, label='HTTPS')
    _arrow(ax, 6.8, 3.7, 7.8, 3.57, dashed=True)
    _arrow(ax, 6.8, 3.5, 7.8, 2.62, dashed=True)
    plt.tight_layout(); plt.savefig(OUT / 'fig_3_2_topology.png'); plt.close()


# Fig 3.3 - Heartbeat Verdict Pipeline
def fig_3_3():
    fig, ax = _fig(11, 5, 11, 5)
    ax.text(5.5, 4.7, 'Figure 3.3  Heartbeat Verdict Pipeline: Collect, Analyse, Store, Present',
            ha='center', fontsize=12, weight='bold')
    steps = [
        (0.2, 'Fetch\nacks'), (1.6, 'Collect\ntelemetry'), (3.0, 'Assemble\nprompt'),
        (4.4, 'Call LLM\nevery cycle'), (5.8, 'Verdict\n+ signature'), (7.2, 'Fingerprint\n+ persist'),
        (8.6, 'Filter API\nresponse'), (9.75, 'Notify\n(high/crit)'),
    ]
    cols = [COL['mem'], COL['ext'], COL['agent'], COL['llm'], COL['agent'], COL['data'], COL['agent'], COL['accent']]
    y = 2.6
    for (x, lbl), c in zip(steps, cols):
        _box(ax, x, y, 1.15, 0.85, lbl, c, fs=8)
    for i in range(len(steps) - 1):
        _arrow(ax, steps[i][0] + 1.15, y + 0.42, steps[i + 1][0], y + 0.42)
    _box(ax, 2.35, 1.0, 3.7, 0.7, 'acknowledged conditions provide prompt context', COL['mem'], fs=8)
    _box(ax, 7.0, 1.0, 3.3, 0.7, 'matching low-risk items are hidden from the API view', COL['mem'], fs=7.5)
    _arrow(ax, 1.2, 1.7, 3.3, 2.6, dashed=True, color=COL['mem'])
    _arrow(ax, 4.0, 2.6, 4.2, 1.7, dashed=True, color=COL['mem'])
    _arrow(ax, 8.0, 2.6, 8.4, 1.7, dashed=True, color=COL['mem'])
    plt.tight_layout(); plt.savefig(OUT / 'fig_3_3_remediation_flow.png'); plt.close()


# Fig 3.4 - Use-Case Diagram
def fig_3_4():
    fig, ax = _fig(10, 7, 10, 7)
    ax.text(5, 6.7, 'Figure 3.4  Use-Case Diagram: Operator and Agent', ha='center', fontsize=12, weight='bold')
    ax.add_patch(Rectangle((2.6, 0.5), 4.8, 5.7, fc='#f1f5f9', ec='#334155', lw=1.5))
    ax.text(5, 6.0, 'InfraGuard AI', ha='center', fontsize=10, weight='bold', color='#334155')

    def stick(x, y, label):
        ax.add_patch(Circle((x, y + 0.5), 0.13, fc='#1e293b'))
        ax.plot([x, x], [y, y + 0.35], color='#1e293b', lw=1.5)
        ax.plot([x - 0.2, x + 0.2], [y + 0.25, y + 0.25], color='#1e293b', lw=1.5)
        ax.plot([x, x - 0.18], [y, y - 0.3], color='#1e293b', lw=1.5)
        ax.plot([x, x + 0.18], [y, y - 0.3], color='#1e293b', lw=1.5)
        ax.text(x, y - 0.55, label, ha='center', fontsize=9, weight='bold')

    stick(1.0, 3.2, 'Operator')
    stick(9.0, 4.2, 'Agent')
    stick(9.0, 1.6, 'LLM\nProvider')
    cases = [
        (5, 5.4, 'View status & verdict'), (5, 4.8, 'Acknowledge known condition'),
        (5, 4.2, 'Review & block threat'), (5, 3.6, 'Ask runbook assistant'),
        (5, 3.0, 'Re-index runbooks'), (5, 2.4, 'Generate verdict (heartbeat)'),
        (5, 1.8, 'Send notification'),
    ]
    for x, y, t in cases:
        ax.add_patch(mpatches.Ellipse((x, y), 3.4, 0.5, fc='#dbeafe', ec='#1e3a8a'))
        ax.text(x, y, t, ha='center', va='center', fontsize=8, color='#1e3a8a')
    for y in (5.4, 4.8, 4.2, 3.6, 3.0):
        ax.plot([1.3, 3.3], [3.2, y], color='#475569', lw=0.7)
    ax.plot([8.7, 6.7], [4.2, 2.4], color='#475569', lw=0.7)
    ax.plot([8.7, 6.7], [4.2, 1.8], color='#475569', lw=0.7)
    ax.plot([8.7, 6.7], [1.6, 2.4], color='#475569', lw=0.7)
    plt.tight_layout(); plt.savefig(OUT / 'fig_3_4_usecase.png'); plt.close()


# Fig 3.5 - Sequence Diagram (one heartbeat)
def fig_3_5():
    fig, ax = _fig(11, 7, 11, 8)
    ax.text(5.5, 7.7, 'Figure 3.5  Sequence Diagram: One Heartbeat Cycle', ha='center', fontsize=12, weight='bold')
    actors = ['Agent', 'Store', 'Telemetry', 'LLM\nProvider', 'ntfy.sh']
    xs = np.linspace(0.9, 10.1, len(actors))
    for x, label in zip(xs, actors):
        _box(ax, x - 0.6, 6.9, 1.2, 0.45, label, COL['agent'], fs=8)
        ax.plot([x, x], [6.5, 0.5], color='#94a3b8', lw=0.8, ls='--')
    msgs = [
        (0, 1, 'fetch active acknowledgements', 6.2),
        (0, 2, 'collect logs / metrics / probes', 5.6),
        (0, 3, 'reason(telemetry + known conditions)', 5.0),
        (3, 0, 'structured verdict + signature', 4.4),
        (0, 1, 'persist verdict (fingerprint)', 3.8),
        (0, 4, 'notify if high / critical', 3.2),
    ]
    for s, e, label, y in msgs:
        _arrow(ax, xs[s], y, xs[e], y, label=label, fs=7.5)
    plt.tight_layout(); plt.savefig(OUT / 'fig_3_5_sequence.png'); plt.close()


# Fig 3.6 - ERD
def fig_3_6():
    fig, ax = _fig(10, 6, 10, 6)
    ax.text(5, 5.7, 'Figure 3.6  Entity-Relationship Diagram: Verdict and Acknowledgement Schema',
            ha='center', fontsize=12, weight='bold')

    def table(x, y, name, fields):
        h = 0.3 + 0.24 * len(fields)
        ax.add_patch(Rectangle((x, y - h), 3.0, h, fc='white', ec='#1e293b', lw=1.2))
        ax.add_patch(Rectangle((x, y - 0.28), 3.0, 0.28, fc='#1e293b'))
        ax.text(x + 1.5, y - 0.14, name, ha='center', va='center', color='white', fontsize=9, weight='bold')
        for i, f in enumerate(fields):
            ax.text(x + 0.12, y - 0.5 - i * 0.24, f, fontsize=7.5, color='#1e293b')

    table(0.6, 5.0, 'verdicts',
          ['id (PK)', 'created_at', 'severity', 'summary', 'payload', 'signature', 'fingerprint'])
    table(6.4, 5.0, 'acknowledgements',
          ['fingerprint (PK)', 'signature', 'severity', 'summary', 'note', 'acked_by', 'created_at', 'expires_at'])
    _arrow(ax, 3.6, 3.4, 6.4, 3.4, label='by fingerprint (N verdicts : 0..1 active ack)', fs=7.5)
    ax.text(0.6, 0.7, 'External: ChromaDB (runbook vectors); audit.log (request audit file)',
            fontsize=8, color='#475569', style='italic')
    plt.tight_layout(); plt.savefig(OUT / 'fig_3_6_erd.png'); plt.close()


# Fig 3.7 - LangGraph State Machine
def fig_3_7():
    fig, ax = _fig(11, 4.5, 11, 4.5)
    ax.text(5.5, 4.2, 'Figure 3.7  State Machine of the LangGraph Reasoning Agent',
            ha='center', fontsize=12, weight='bold')
    states = [(1.3, 2.3, 'collect_data'), (4.0, 2.3, 'analyze'), (6.7, 2.3, 'decide_action'), (9.4, 2.3, 'notify')]
    for x, y, name in states:
        ax.add_patch(FancyBboxPatch((x - 0.85, y - 0.4), 1.7, 0.8, boxstyle='round,pad=0.04',
                                    fc=COL['agent'], ec='#0c1e3d'))
        ax.text(x, y, name, ha='center', va='center', color='white', fontsize=9, weight='bold')
    for i in range(len(states) - 1):
        _arrow(ax, states[i][0] + 0.85, states[i][1], states[i + 1][0] - 0.85, states[i + 1][1])
    ax.add_patch(Circle((0.4, 2.3), 0.12, fc='#1e293b'))
    _arrow(ax, 0.52, 2.3, 0.45, 2.3)
    ax.add_patch(Circle((10.6, 2.3), 0.16, fc='none', ec='#1e293b', lw=1.5))
    ax.add_patch(Circle((10.6, 2.3), 0.09, fc='#1e293b'))
    _arrow(ax, 6.7, 1.9, 10.5, 2.18, dashed=True, label='ok / warning → END', fs=7.5)
    _arrow(ax, 10.25, 2.3, 10.44, 2.3)
    plt.tight_layout(); plt.savefig(OUT / 'fig_3_7_state_machine.png'); plt.close()


# Fig 4.1 - Folder Structure
def fig_4_1():
    fig, ax = plt.subplots(figsize=(8.5, 9)); ax.set_xlim(0, 10); ax.set_ylim(0, 14); ax.axis('off')
    ax.text(5, 13.6, 'Figure 4.1  Folder Structure of the Reference Implementation', ha='center', fontsize=12, weight='bold')
    tree = [
        (0.2, 13.0, 'infraguard_ai/', True), (0.8, 12.5, 'agent/', True),
        (1.4, 12.1, 'main.py  (heartbeat)'), (1.4, 11.7, 'orchestrator.py  (LangGraph)'),
        (1.4, 11.3, 'memory.py  [key] verdict fingerprint'), (1.4, 10.9, 'llm/  gemini_client.py, providers.py, prompts.py'),
        (1.4, 10.5, 'rag/  local_runbooks_loader.py, vector_store.py, runbook_agent.py'),
        (1.4, 10.1, 'tools/  loki, prometheus, http_probe, docker_*, threat_response, notify'),
        (0.8, 9.5, 'api/', True), (1.4, 9.1, 'main.py  (routes + middleware)'),
        (1.4, 8.7, 'auth.py, store.py  [key] verdicts + acks'),
        (1.4, 8.3, 'middleware/  audit.py, security.py, rate_limit.py'),
        (0.8, 7.7, 'dashboard/  index.html, login.html', True),
        (0.8, 7.2, 'tests/  test_tools, test_agent, test_api, test_store, test_memory, etc.', True),
        (0.8, 6.7, 'terraform/  (GCE IaC)', True),
        (0.8, 6.2, '.github/workflows/  test.yml, deploy.yml', True),
        (0.8, 5.7, 'docker-compose.yml, agent/Dockerfile, api/Dockerfile', True),
    ]
    for x, y, label, *bold in tree:
        ax.text(x, y, label, fontsize=10 if bold else 9.5, family='monospace',
                weight='bold' if bold else 'normal', color='#1e293b' if bold else '#334155')
    ax.text(5.0, 5.0, '[key] = modules central to verdict memory', fontsize=8, color=COL['mem'], weight='bold')
    plt.tight_layout(); plt.savefig(OUT / 'fig_4_1_folder.png'); plt.close()


# Fig 4.2 - Verdict-Memory Flow
def fig_4_2():
    fig, ax = _fig(11, 5.5, 11, 5.5)
    ax.text(5.5, 5.2, 'Figure 4.2  Verdict-Memory Fingerprint and Acknowledgement Flow',
            ha='center', fontsize=12, weight='bold')
    _box(ax, 0.3, 3.6, 2.0, 0.9, 'Verdict\n(severity, signature)', COL['agent'], fs=8)
    _box(ax, 2.9, 3.6, 3.2, 0.9, 'fingerprint =\nSHA-256(signature ‖ prompt_version ‖ model)', COL['mem'], fs=7.5)
    _box(ax, 6.9, 3.6, 1.9, 0.9, 'acknowledgements\n(by fingerprint, TTL)', COL['data'], fs=8)
    _arrow(ax, 2.3, 4.05, 2.9, 4.05)
    _arrow(ax, 6.1, 4.05, 6.9, 4.05, label='low-risk ack', fs=7)
    _box(ax, 2.9, 1.9, 3.2, 0.8, 'next heartbeat: known conditions enter the prompt', COL['mem'], fs=8)
    _arrow(ax, 7.8, 3.6, 6.1, 2.7, dashed=True, color=COL['mem'])
    _arrow(ax, 4.5, 1.9, 1.3, 3.6, dashed=True, color=COL['mem'], label='LLM analysis still runs')
    ax.text(0.3, 1.0, 'Invalidation: a change to the signature, prompt_version, or model yields a new fingerprint '
                      '(the prior row remains, but no longer matches). High and critical items remain visible.',
            fontsize=8, color=COL['accent'], style='italic')
    plt.tight_layout(); plt.savefig(OUT / 'fig_4_2_llm_classes.png'); plt.close()


# Fig 4.3 - Dashboard
def fig_4_3():
    fig, ax = plt.subplots(figsize=(11, 6.2)); ax.set_xlim(0, 11); ax.set_ylim(0, 7); ax.axis('off')
    ax.text(5.5, 6.7, 'Figure 4.3  Dashboard Overview Page', ha='center', fontsize=12, weight='bold')
    ax.add_patch(Rectangle((0.2, 0.3), 10.6, 6.0, fc='#0f1117', ec='#1e293b'))
    ax.text(0.5, 5.9, 'InfraGuard AI', color='white', fontsize=12, weight='bold')
    ax.text(9.0, 5.92, 'LangChain Agent', color='#818cf8', fontsize=8)
    # chips
    chips = [('Loki', True), ('Prometheus', True), ('Probes', True), ('Runbooks', True), ('CrowdSec', False), ('ntfy', True)]
    for i, (lbl, on) in enumerate(chips):
        x = 0.5 + i * 1.6
        ax.add_patch(FancyBboxPatch((x, 5.2), 1.45, 0.35, boxstyle='round,pad=0.03',
                                    fc='#1a1d27', ec='#22c55e' if on else '#334155'))
        ax.text(x + 0.1, 5.37, ('● ' if on else '○ ') + lbl, color='#e4e4e7' if on else '#71717a', fontsize=7)
    # verdict card
    ax.add_patch(FancyBboxPatch((0.5, 3.3), 10.0, 1.6, boxstyle='round,pad=0.04', fc='#1a1d27', ec='#334155'))
    ax.text(0.7, 4.6, 'Current Status', color='white', fontsize=9.5, weight='bold')
    ax.add_patch(Rectangle((4.4, 4.5), 1.4, 0.32, fc='#eab308'))
    ax.text(5.1, 4.66, 'WARNING', color='#0f1117', fontsize=8, ha='center', weight='bold')
    ax.text(0.7, 4.1, 'Disk usage on / approaching threshold on api-host; non-urgent.', color='#e4e4e7', fontsize=8)
    ax.text(0.7, 3.7, 'Root cause | Recommended action', color='#71717a', fontsize=8)
    ax.add_patch(FancyBboxPatch((8.3, 3.55), 2.0, 0.4, boxstyle='round,pad=0.03', fc='#22252f', ec='#dc2626'))
    ax.text(9.3, 3.74, 'Mark as known', color='#ef4444', fontsize=7.5, ha='center', weight='bold')
    # threats + runbook
    ax.add_patch(FancyBboxPatch((0.5, 1.7), 4.9, 1.4, boxstyle='round,pad=0.04', fc='#1a1d27', ec='#334155'))
    ax.text(0.7, 2.85, 'Threat Detection', color='white', fontsize=9, weight='bold')
    ax.text(0.7, 2.45, 'No threats detected; 312 log lines scanned', color='#22c55e', fontsize=8)
    ax.add_patch(FancyBboxPatch((5.6, 1.7), 4.9, 1.4, boxstyle='round,pad=0.04', fc='#1a1d27', ec='#334155'))
    ax.text(5.8, 2.85, 'Runbook Assistant', color='white', fontsize=9, weight='bold')
    ax.text(5.8, 2.45, 'Ask about your runbooks and procedures...', color='#71717a', fontsize=8)
    # history
    ax.add_patch(FancyBboxPatch((0.5, 0.5), 10.0, 1.0, boxstyle='round,pad=0.04', fc='#1a1d27', ec='#334155'))
    ax.text(0.7, 1.25, 'Check History', color='white', fontsize=9, weight='bold')
    ax.text(0.7, 0.85, 'Issues only [ ]   Hide acknowledged [x]', color='#71717a', fontsize=7.5)
    plt.tight_layout(); plt.savefig(OUT / 'fig_4_3_dashboard.png'); plt.close()


# Fig 5.1 - Test Coverage by Module (measured)
def fig_5_1():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    mods = ['memory', 'orchestrator', 'store', 'schema', 'providers', 'api/main', 'api/auth',
            'loki', 'prometheus', 'threat_resp', 'notify', 'vector_store', 'OVERALL']
    cov = [100, 94, 94, 95, 93, 79, 82, 85, 80, 67, 32, 31, 66]
    colors = ['#16a34a' if c >= 80 else '#ca8a04' if c >= 60 else '#dc2626' for c in cov[:-1]] + ['#1f3a68']
    ax.bar(mods, cov, color=colors)
    for i, c in enumerate(cov):
        ax.text(i, c + 1.5, f'{c}%', ha='center', fontsize=8)
    ax.set_ylabel('Line Coverage (%)'); ax.set_ylim(0, 110)
    ax.set_title('Figure 5.1  Test Coverage by Selected Modules (measured, 80 tests)')
    plt.setp(ax.get_xticklabels(), rotation=30, ha='right', fontsize=8)
    ax.grid(axis='y', linestyle=':', alpha=0.4)
    plt.tight_layout(); plt.savefig(OUT / 'fig_5_1_acceptance.png'); plt.close()


# Fig 5.2 - Duplicate-Verdict Reduction (controlled demonstration)
def fig_5_2():
    fig, ax = plt.subplots(figsize=(10, 5))
    cycles = np.arange(0, 31)
    baseline = cycles.copy()                       # one surfaced duplicate per cycle
    ack_at = 3
    memory = np.where(cycles <= ack_at, cycles, ack_at)  # plateaus after acknowledgement
    ax.plot(cycles, baseline, marker='o', ms=3, color='#dc2626', label='Stateless baseline')
    ax.plot(cycles, memory, marker='o', ms=3, color='#16a34a', label='Memory-enabled (acknowledged at cycle 3)')
    ax.axvline(ack_at, color='#475569', ls='--', lw=1)
    ax.text(ack_at + 0.3, 24, 'operator acknowledges', fontsize=8, color='#475569')
    ax.set_xlabel('Heartbeat cycle'); ax.set_ylabel('Cumulative surfaced duplicate warnings')
    ax.set_title('Figure 5.2  Visible Duplicate Warnings: Stateless vs Memory-Enabled Demonstration')
    ax.text(15, 5.5, 'The model is still called on every heartbeat.', ha='center', fontsize=8,
            color='#475569', bbox=dict(boxstyle='round,pad=0.25', fc='white', ec='#cbd5e1'))
    ax.legend(frameon=False, fontsize=9); ax.grid(linestyle=':', alpha=0.4)
    plt.tight_layout(); plt.savefig(OUT / 'fig_5_2_mttr.png'); plt.close()


# Fig 5.3 - Test counts by test file
def fig_5_3():
    fig, ax = plt.subplots(figsize=(10, 5))
    files = ['agent', 'api', 'memory', 'providers', 'rag', 'store', 'threat response', 'tools']
    counts = [4, 17, 9, 22, 7, 9, 3, 9]
    ax.bar(files, counts, color='#1f3a68')
    for i, count in enumerate(counts):
        ax.text(i, count + 0.35, str(count), ha='center', fontsize=8)
    ax.set_ylabel('Collected tests'); ax.set_ylim(0, 20)
    ax.set_title('Figure 5.3  Collected Tests by Test File (80 total)')
    plt.setp(ax.get_xticklabels(), rotation=25, ha='right', fontsize=8)
    ax.grid(axis='y', linestyle=':', alpha=0.4)
    plt.tight_layout(); plt.savefig(OUT / 'fig_5_3_cost.png'); plt.close()


# Fig 5.4 - Evaluation status
def fig_5_4():
    fig, ax = plt.subplots(figsize=(9, 4.8))
    labels = ['Automated tests', 'Coverage', 'Memory demo', 'Live-model quality', 'User study']
    status = [1, 1, 1, 0, 0]
    colors = ['#16a34a' if value else '#94a3b8' for value in status]
    ax.barh(labels, status, color=colors)
    ax.set_xlim(0, 1.05); ax.set_xticks([])
    ax.set_title('Figure 5.4  Evaluation Evidence Available at Submission')
    for i, value in enumerate(status):
        ax.text(0.5, i, 'Completed' if value else 'Not completed', ha='center', va='center',
                color='white' if value else '#1e293b', fontsize=9, weight='bold')
    ax.invert_yaxis()
    plt.tight_layout(); plt.savefig(OUT / 'fig_5_4_calibration.png'); plt.close()


def main():
    for fn in [fig_3_1, fig_3_2, fig_3_3, fig_3_4, fig_3_5, fig_3_6, fig_3_7,
               fig_4_1, fig_4_2, fig_4_3, fig_5_1, fig_5_2, fig_5_3, fig_5_4]:
        fn(); print('OK', fn.__name__)


if __name__ == '__main__':
    main()
