const { p, pCenter, chapterLabel, h2, h3, h4, bullet, num, blank, pageBreak, buildTable } = require('../helpers');
const { Paragraph, TextRun, AlignmentType } = require('docx');

function code(text) {
  // Render code in a monospaced font, preserved as-is (line breaks split into separate paragraphs).
  const lines = text.split('\n');
  return lines.map(line =>
    new Paragraph({
      children: [new TextRun({ text: line || ' ', font: 'Consolas', size: 20 })],
      alignment: AlignmentType.LEFT,
      spacing: { line: 240, after: 0 },
    })
  );
}

function appendices() {
  const b = [];

  // ============ APPENDIX A ============
  b.push(chapterLabel('APPENDIX A'));
  b.push(pCenter('API ENDPOINT REFERENCE'));
  b.push(blank());
  b.push(p('The following enumerates the principal HTTP endpoints exposed by the InfraGuard Pro control-plane API. Endpoints requiring authentication are marked with † (session cookie) or ‡ (satellite bearer token). Public endpoints have no marker.'));
  b.push(blank());

  b.push(h2('A.1  Authentication and Session'));
  b.push(p('POST /login — Submit username and password; sets a signed session cookie on success.'));
  b.push(p('GET /logout † — Clear the session cookie.'));
  b.push(p('GET /health — Liveness probe; returns 200 if the API and database are reachable.'));

  b.push(h2('A.2  Verdicts and Alerts'));
  b.push(p('GET /status † — Latest verdict summary.'));
  b.push(p('GET /alerts † — Recent 20 verdicts.'));
  b.push(p('GET /api/verdicts † — Paged verdict listing with severity, server, provider, and time-range filters.'));
  b.push(p('GET /api/verdicts/{id} † — Verdict detail including evidence chain, raw LLM output, audit references.'));

  b.push(h2('A.3  SARIF Ingestion'));
  b.push(p('POST /api/sarif/ingest † — Accept a SARIF 2.1.0 document (multipart/form-data or application/json).'));

  b.push(h2('A.4  Remediation'));
  b.push(p('GET /api/remediations † — List remediations with optional status, severity, provider filters.'));
  b.push(p('GET /api/remediations/{id} † — Detail view including diff, evidence, audit chain, validation outcome.'));
  b.push(p('POST /api/remediations/{id}/approve † — Approve and dispatch a human-approval-required remediation.'));
  b.push(p('POST /api/remediations/{id}/reject † — Reject with reason recorded.'));
  b.push(p('POST /api/remediations/{id}/rollback † — Open a reverting pull request.'));

  b.push(h2('A.5  Agent and LLM Configuration'));
  b.push(p('GET /api/agent/mode † — Current reasoning mode and active provider.'));
  b.push(p('GET /api/agent/llm-config † — Active provider and model identifiers.'));
  b.push(p('POST /api/agent/llm-config † — Hot-swap provider and model.'));
  b.push(p('POST /api/agent/diagnose-now † — Trigger an out-of-cycle diagnosis cycle.'));

  b.push(h2('A.6  Satellites and Containers'));
  b.push(p('POST /api/satellites/register — First-boot satellite registration (no auth — issues a token).'));
  b.push(p('POST /api/satellites/{id}/heartbeat ‡ — Periodic heartbeat from a satellite.'));
  b.push(p('GET /api/satellites † — List of registered satellites.'));
  b.push(p('GET /api/satellites/{id} † — Satellite detail with container inventory.'));
  b.push(p('GET /api/satellites/{id}/actions ‡ — Satellite polls for approved remote actions.'));
  b.push(p('POST /api/containers/{id}/restart † — Remote container restart.'));
  b.push(p('POST /api/containers/{id}/stop † — Remote container stop.'));
  b.push(p('GET /api/containers/{id}/logs † — WebSocket-upgraded log stream.'));
  b.push(p('POST /api/containers/{id}/diagnose † — On-demand diagnosis for a specific container.'));

  b.push(h2('A.7  RAG and Runbooks'));
  b.push(p('GET /api/runbooks/list † — Indexed runbook inventory.'));
  b.push(p('POST /api/runbooks/upload † — Upload a runbook (Markdown, text, or PDF).'));
  b.push(p('POST /api/runbooks/index † — Trigger full re-index.'));
  b.push(p('POST /api/runbooks/query † — RAG semantic search; returns answer and citations.'));
  b.push(p('GET /api/incidents/similar † — Top-k historical incidents similar to supplied context.'));

  b.push(h2('A.8  Traceway Bridge'));
  b.push(p('GET /api/traceway/exceptions † — Proxied exception feed.'));
  b.push(p('GET /api/traceway/traces/{trace_id} † — Specific trace by ID.'));
  b.push(p('POST /api/traceway/correlate † — On-demand AI correlation between an exception and surrounding telemetry.'));

  b.push(h2('A.9  Threats and CrowdSec'));
  b.push(p('GET /api/threats † — Detected threat patterns and source IPs from latest verdict.'));
  b.push(p('POST /api/threats/apply † — Apply a CrowdSec ban to a single satellite.'));
  b.push(p('POST /api/threats/apply-global † — Apply a CrowdSec ban to all satellites.'));

  b.push(h2('A.10  Audit'));
  b.push(p('GET /api/audit † (admin) — Paged audit-log access with actor, action, and entity filters.'));

  // ============ APPENDIX B ============
  b.push(chapterLabel('APPENDIX B'));
  b.push(pCenter('SAMPLE CODE SNIPPETS'));
  b.push(blank());
  b.push(p('The following code snippets illustrate the principal architectural patterns introduced by the project. They are excerpts from the reference implementation; complete source is available in the public repository.'));
  b.push(blank());

  b.push(h2('B.1  LLM Provider Abstract Base'));
  b.push(p('From agent/llm/provider.py:'));
  b.push(blank());
  b.push(...code(`from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

@dataclass
class AgentContext:
    telemetry: dict[str, Any]
    rag_documents: list[dict]
    finding: dict | None = None
    patch_hint: str | None = None

@dataclass
class Verdict:
    severity: str
    summary: str
    root_cause: str
    recommended_action: str
    confidence: float
    evidence: list[dict]
    provider: str
    model: str
    raw_text: str
    patch: str | None = None

class LLMProvider(ABC):
    name: str
    model: str

    @abstractmethod
    async def reason(self, context: AgentContext) -> Verdict: ...

    @abstractmethod
    async def health_check(self) -> bool: ...`));
  b.push(blank());

  b.push(h2('B.2  OpenAI Provider Implementation'));
  b.push(p('From agent/llm/openai.py (excerpt):'));
  b.push(blank());
  b.push(...code(`from openai import AsyncOpenAI
from .provider import LLMProvider, AgentContext, Verdict
from .prompts import build_system_prompt, build_user_prompt
from .parser import parse_structured_verdict

class OpenAIProvider(LLMProvider):
    name = "openai"

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def reason(self, context: AgentContext) -> Verdict:
        response = await self.client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            temperature=0.2,
            messages=[
                {"role": "system", "content": build_system_prompt()},
                {"role": "user", "content": build_user_prompt(context)},
            ],
        )
        return parse_structured_verdict(
            raw=response.choices[0].message.content,
            provider=self.name,
            model=self.model,
        )

    async def health_check(self) -> bool:
        try:
            await self.client.models.retrieve(self.model)
            return True
        except Exception:
            return False`));
  b.push(blank());

  b.push(h2('B.3  Policy Engine Rule Evaluation'));
  b.push(p('From agent/remediation/policy.py (excerpt):'));
  b.push(blank());
  b.push(...code(`from dataclasses import dataclass
from fnmatch import fnmatch

@dataclass
class PolicyDecision:
    mode: str            # "autonomous" | "approval" | "recommend"
    rule_id: str
    rationale: str

class PolicyEngine:
    def __init__(self, config: dict):
        self.autonomous_globs = config.get("autonomous_globs", [])
        self.autonomous_min_confidence = config.get("autonomous_min_confidence", 0.8)
        self.autonomous_max_cvss = config.get("autonomous_max_cvss", 6.9)
        self.approval_min_confidence = config.get("approval_min_confidence", 0.6)
        self.max_files_for_autonomous = config.get("max_files_for_autonomous", 1)

    def classify(self, finding, patch) -> PolicyDecision:
        if patch.confidence < self.approval_min_confidence:
            return PolicyDecision("recommend", "POL-001",
                "confidence below approval threshold")
        if finding.cvss and finding.cvss >= 9.0:
            return PolicyDecision("approval", "POL-002",
                "CVSS critical findings always require human approval")
        if len(patch.files_touched) > self.max_files_for_autonomous:
            return PolicyDecision("approval", "POL-003",
                f"patch spans {len(patch.files_touched)} files")
        if (patch.confidence >= self.autonomous_min_confidence
            and finding.cvss <= self.autonomous_max_cvss
            and all(any(fnmatch(f, g) for g in self.autonomous_globs)
                    for f in patch.files_touched)):
            return PolicyDecision("autonomous", "POL-100",
                "all autonomous criteria satisfied")
        return PolicyDecision("approval", "POL-200",
            "default to human approval")`));
  b.push(blank());

  b.push(h2('B.4  Audit-Log Hash Chain'));
  b.push(p('From api/store/audit.py (excerpt):'));
  b.push(blank());
  b.push(...code(`import hashlib
import json

class AuditService:
    def __init__(self, db, salt: str):
        self.db = db
        self.salt = salt

    @staticmethod
    def _canonical_json(obj) -> str:
        return json.dumps(obj, sort_keys=True, separators=(",", ":"))

    async def append(self, *, actor, action, entity_type, entity_id, details):
        prev = await self.db.fetch_last_audit_hash()
        prev_hash = prev or self.salt
        payload = (
            prev_hash
            + str(int(time.time() * 1000))
            + actor
            + action
            + entity_type
            + str(entity_id)
            + self._canonical_json(details)
        )
        h = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        await self.db.insert_audit(
            actor=actor, action=action, entity_type=entity_type,
            entity_id=entity_id, details=details,
            prev_hash=prev_hash, hash=h,
        )
        return h`));
  b.push(blank());

  b.push(h2('B.5  SARIF Adapter Excerpt'));
  b.push(p('From agent/remediation/sarif.py (excerpt):'));
  b.push(blank());
  b.push(...code(`from typing import Iterator
import json

class SarifAdapter:
    def __init__(self, nvd_client):
        self.nvd = nvd_client

    async def normalise(self, raw: dict) -> Iterator[dict]:
        for run in raw.get("runs", []):
            tool = run["tool"]["driver"]["name"]
            for result in run.get("results", []):
                location = result["locations"][0]["physicalLocation"]
                rule_id = result.get("ruleId") or ""
                cwe = self._extract_cwe(result)
                cve = self._extract_cve(result)
                cvss = await self.nvd.cvss_for(cve) if cve else None
                yield {
                    "source_scanner": tool,
                    "rule_id": rule_id,
                    "cwe": cwe,
                    "cve": cve,
                    "cvss": cvss,
                    "severity": self._derive_severity(result, cvss),
                    "file_path": location["artifactLocation"]["uri"],
                    "line_start": location.get("region", {}).get("startLine", 0),
                    "line_end": location.get("region", {}).get("endLine", 0),
                    "message": result["message"]["text"],
                    "sarif_raw": result,
                }`));
  b.push(blank());

  // ============ APPENDIX C ============
  b.push(chapterLabel('APPENDIX C'));
  b.push(pCenter('DOCKER COMPOSE CONFIGURATIONS'));
  b.push(blank());
  b.push(p('Two Docker Compose configurations are provided: the central control plane composition and the satellite composition. Both have been simplified for inclusion here by omitting volume and network declarations; the complete versions are in the repository at docker-compose.yml and docker-compose.satellite.yml.'));
  b.push(blank());

  b.push(h2('C.1  Central Control Plane (docker-compose.yml)'));
  b.push(blank());
  b.push(...code(`services:
  infraguard-api:
    image: ghcr.io/sagesta/infraguard-pro-api:latest
    environment:
      - DATABASE_URL=postgresql+asyncpg://infra:secret@postgres:5432/infraguard
      - SECRET_KEY=\${SECRET_KEY}
      - INFRAGUARD_USERNAME=admin
      - INFRAGUARD_PASSWORD=\${ADMIN_PASSWORD}
      - LLM_PROVIDER=\${LLM_PROVIDER:-vertex_ai}
      - LLM_MODEL=\${LLM_MODEL:-gemini-2.5-flash}
      - LOKI_URL=http://loki:3100
      - PROMETHEUS_URL=http://prometheus:9090
      - TRACEWAY_URL=http://traceway:4318
      - CHROMA_PATH=/data/chroma
    depends_on: [postgres, chromadb, loki, prometheus, traceway]
    ports: ["8000:8000"]

  infraguard-agent:
    image: ghcr.io/sagesta/infraguard-pro-agent:latest
    environment:
      - DATABASE_URL=postgresql+asyncpg://infra:secret@postgres:5432/infraguard
      - LLM_PROVIDER=\${LLM_PROVIDER:-vertex_ai}
      - REMEDIATION_WORKER_COUNT=4
    depends_on: [infraguard-api]

  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=infra
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=infraguard

  chromadb:
    image: chromadb/chroma:0.5.0
    volumes: ["chroma-data:/chroma/chroma"]

  prometheus:
    image: prom/prometheus:v2.55.0
    volumes: ["./prometheus.yml:/etc/prometheus/prometheus.yml:ro"]

  loki:
    image: grafana/loki:3.2.0

  traceway:
    image: traceway/traceway:latest
    depends_on: [clickhouse]

  clickhouse:
    image: clickhouse/clickhouse-server:24.10

  crowdsec:
    image: crowdsecurity/crowdsec:v1.6
    volumes: ["/var/run/docker.sock:/var/run/docker.sock:ro"]`));
  b.push(blank());

  b.push(h2('C.2  Satellite Agent (docker-compose.satellite.yml)'));
  b.push(blank());
  b.push(...code(`services:
  infraguard-satellite:
    image: ghcr.io/sagesta/infraguard-pro-satellite:latest
    environment:
      - CENTRAL_API_URL=https://infraguard.example.com
      - SERVER_ID=\${SERVER_ID}
      - SERVER_LABEL=\${SERVER_LABEL}
      - SERVER_ENV=\${SERVER_ENV}
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - satellite-state:/data

  prometheus:
    image: prom/prometheus:v2.55.0
    volumes: ["./prometheus-satellite.yml:/etc/prometheus/prometheus.yml:ro"]

  promtail:
    image: grafana/promtail:3.2.0
    volumes:
      - /var/log:/var/log:ro
      - ./promtail-config.yml:/etc/promtail/config.yml:ro
    command: -config.file=/etc/promtail/config.yml

  crowdsec:
    image: crowdsecurity/crowdsec:v1.6
    volumes: ["/var/log:/var/log:ro"]

volumes:
  satellite-state:`));
  b.push(blank());

  // ============ APPENDIX D ============
  b.push(chapterLabel('APPENDIX D'));
  b.push(pCenter('EVALUATION DATASET SUMMARY'));
  b.push(blank());
  b.push(p('The 150-finding evaluation benchmark, referenced throughout Chapter Five, is summarised below by scanner class, CVSS severity band, and source provenance.'));
  b.push(blank());

  b.push(h2('D.1  Distribution by Scanner Class'));
  b.push(blank());
  const dColW = [3000, 2000, 2000, 2026];
  const dHead = ['Scanner Class', 'Real-World', 'Synthetic', 'Total'];
  const dRows = [
    dHead,
    ['SCA — Vulnerable Dependencies', '30', '15', '45'],
    ['SAST — Insecure Source Patterns', '18', '12', '30'],
    ['Container — Vulnerable Base Images', '14', '11', '25'],
    ['IaC — Misconfigured Cloud Resources', '20', '10', '30'],
    ['Secret — Hardcoded Credentials', '8', '12', '20'],
    ['TOTAL', '90', '60', '150'],
  ];
  b.push(buildTable(dColW, dRows));
  b.push(blank());

  b.push(h2('D.2  Distribution by CVSS Severity Band'));
  b.push(blank());
  const sColW = [3000, 3026, 3000];
  const sHead = ['CVSS Band', 'Count', 'Approx. Share'];
  const sRows = [
    sHead,
    ['Critical (9.0–10.0)', '40', '26.7%'],
    ['High (7.0–8.9)', '50', '33.3%'],
    ['Medium (4.0–6.9)', '40', '26.7%'],
    ['Low (0.1–3.9)', '20', '13.3%'],
    ['TOTAL', '150', '100.0%'],
  ];
  b.push(buildTable(sColW, sRows));
  b.push(blank());

  b.push(h2('D.3  Representative CWE Coverage'));
  b.push(p('The benchmark exercises a deliberately broad CWE surface. The following weaknesses are each represented by at least three findings: CWE-79 (Cross-Site Scripting), CWE-89 (SQL Injection), CWE-200 (Information Exposure), CWE-22 (Path Traversal), CWE-78 (OS Command Injection), CWE-269 (Improper Privilege Management), CWE-798 (Hard-coded Credentials), CWE-1104 (Vulnerable Third-Party Component), CWE-94 (Improper Code Generation), CWE-352 (Cross-Site Request Forgery), CWE-732 (Incorrect Permission Assignment), CWE-863 (Incorrect Authorisation), CWE-918 (Server-Side Request Forgery), and CWE-1004 (Sensitive Cookie Without HttpOnly Flag).'));
  b.push(blank());

  b.push(h2('D.4  Source Provenance'));
  b.push(p('Real-world findings were harvested from public security advisories and scanner outputs against the following open-source projects: requests (PyPI), urllib3 (PyPI), Pillow (PyPI), Flask-related packages, FastAPI-related packages, lxml, paramiko, cryptography, axios (npm), express (npm), node-fetch (npm), lodash (npm), nginx official Docker images, postgres official Docker images, redis official Docker images, ubuntu base images, and the public Terraform modules in the hashicorp/terraform-aws-modules organisation. Synthetic findings were authored to exercise specific edge cases not adequately represented in the real-world corpus and are reproduced in the repository at tests/fixtures/synthetic/ for independent re-evaluation.'));

  return b;
}

module.exports = { appendices };
