const { p, pCenter, chapterLabel, h2, h3, h4, bullet, num, blank, pageBreak, buildTable } = require('../helpers');
const { Paragraph, TextRun, AlignmentType } = require('docx');

function code(text) {
  // Render code in a monospaced font, preserved as-is (line breaks split into separate paragraphs).
  const lines = text.replace(/[\u2013\u2014]/g, '-').split('\n');
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
  b.push(chapterLabel('APPENDIX A: API ENDPOINT REFERENCE'));
  b.push(blank());
  b.push(p('Appendix A lists the HTTP endpoints exposed by the InfraGuard AI API. A dagger marks routes that require a valid session cookie. Only the health check and login routes are public.'));
  b.push(blank());

  b.push(h2('A.1  Authentication and Health'));
  b.push(p('GET /login: Serve the login page. POST /login: Submit credentials; sets a signed session cookie on success; rate-limited to five attempts per minute.'));
  b.push(p('GET /logout †: Clear the session cookie.'));
  b.push(p('GET /health: Liveness probe; returns 200 when the API is reachable.'));

  b.push(h2('A.2  Status, History, and Configuration'));
  b.push(p('GET /status †: The latest verdict with staleness (age, stale) and memory (fingerprint, acknowledged, suppressed) fields.'));
  b.push(p('GET /alerts †: The twenty most recent verdicts with their per-row memory fields.'));
  b.push(p('GET /api/config †: Which integrations are configured, as booleans only (Loki, Prometheus, HTTP probes, local runbooks, CrowdSec, ntfy notifications, Docker monitoring).'));
  b.push(p('GET /api/agent/mode †: The active reasoning mode (langchain or gemini_direct) and the model.'));

  b.push(h2('A.3  Verdict Memory'));
  b.push(p('POST /api/verdicts/ack †: Acknowledge a verdict condition as a known non-issue, keyed on its fingerprint; rejected with HTTP 409 for high/critical severity.'));
  b.push(p('POST /api/verdicts/unack †: Remove an acknowledgement so the condition re-opens.'));
  b.push(p('GET /api/acks †: List the active acknowledgements.'));

  b.push(h2('A.4  Threats'));
  b.push(p('GET /api/threats †: Scan recent Loki logs for HTTP/SSH brute-force and port-scan patterns; returns detected threats and source IPs.'));
  b.push(p('POST /api/threats/apply †: Build and apply a CrowdSec ban for a detected threat; runs in dry-run mode when CrowdSec is not configured.'));

  b.push(h2('A.5  Runbooks (RAG)'));
  b.push(p('POST /api/runbooks/query †: Answer a question over the indexed runbooks; returns an answer and source citations.'));
  b.push(p('POST /api/runbooks/index †: Re-index Markdown runbooks from the configured local directory into ChromaDB.'));

  // ============ APPENDIX B ============
  b.push(chapterLabel('APPENDIX B: SAMPLE CODE SNIPPETS'));
  b.push(blank());
  b.push(p('The excerpts below show the fingerprint, severity safeguard, known-condition prompt block, threat detector, and LangGraph workflow. The project repository contains the complete source.'));
  b.push(blank());

  b.push(h2('B.1  Verdict Fingerprint and Signature Derivation'));
  b.push(p('From agent/memory.py, the condition-and-ruleset fingerprint used by the acknowledgement feature:'));
  b.push(blank());
  b.push(...code(`import hashlib, re

PROMPT_VERSION = "1"           # bump to invalidate all prior acknowledgements
DEFAULT_MODEL = "gemini-3.6-flash"
OK_SIGNATURE = "none:healthy:all"

def compute_fingerprint(signature, model=DEFAULT_MODEL,
                        prompt_version=PROMPT_VERSION):
    """Stable content-plus-ruleset fingerprint for a verdict condition."""
    sig = (signature or "").strip().lower() or OK_SIGNATURE
    basis = f"{sig}\\x1f{prompt_version}\\x1f{model}"
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()

def derive_signature_fallback(severity, root_cause="", summary=""):
    """Deterministic signature when the model does not supply one;
    volatile tokens (IPs, numbers, hashes) are stripped so the same
    condition normalises to the same string across heartbeats."""
    sev = (severity or "warning").strip().lower()
    if sev == "ok":
        return OK_SIGNATURE
    basis = _normalize(root_cause) or _normalize(summary)
    slug = _NONWORD.sub("-", basis).strip("-")[:48] or "unspecified"
    return f"{sev}:{slug}"`));
  b.push(blank());

  b.push(h2('B.2  Severity Safeguard'));
  b.push(p('From api/store.py, the rule that prevents a high or critical verdict from being suppressed:'));
  b.push(blank());
  b.push(...code(`def is_suppressed(severity, acknowledged):
    """An acknowledged condition is hidden only when low-risk;
    high/critical always surface, acknowledged or not."""
    return acknowledged and str(severity or "").lower() in {"ok", "warning"}`));
  b.push(blank());

  b.push(h2('B.3  Known-Conditions Memory Block'));
  b.push(p('From agent/llm/prompts.py, active acknowledgements included in the next prompt as contextual information:'));
  b.push(blank());
  b.push(...code(`def _known_conditions_block(known_conditions):
    if not known_conditions:
        return ""
    lines = []
    for kc in known_conditions:
        sig = str(kc.get("signature") or "").strip()
        if not sig:
            continue
        note = str(kc.get("note") or "").strip()
        lines.append(f"- {sig}" + (f"; operator note: {note}" if note else ""))
    if not lines:
        return ""
    return (
        "OPERATOR-ACKNOWLEDGED KNOWN CONDITIONS (already triaged and "
        "accepted as non-issues; do NOT re-flag or escalate these unless "
        "the underlying condition has materially changed). If a current "
        "observation matches one of these and has not materially changed, "
        "return severity \\"ok\\" and reuse its signature:\\n"
        + "\\n".join(lines) + "\\n\\n"
    )`));
  b.push(blank());

  b.push(h2('B.4  Deterministic Threat Detection'));
  b.push(p('From agent/tools/threat_response.py, the deterministic per-source-IP threshold detector:'));
  b.push(blank());
  b.push(...code(`def analyze_threats(loki_logs):
    ip_401_count, ip_ssh_fail = {}, {}
    for entry in loki_logs:
        line = str(entry.get("line", ""))
        low = line.lower()
        if " 401 " in line or " 403 " in line or "unauthorized" in low:
            for ip in _extract_ips(line):
                ip_401_count[ip] = ip_401_count.get(ip, 0) + 1
        if "failed password" in low or "authentication failure" in low:
            for ip in _extract_ips(line):
                ip_ssh_fail[ip] = ip_ssh_fail.get(ip, 0) + 1
    threats = []
    for ip, n in ip_401_count.items():
        if n >= _BRUTE_FORCE_THRESHOLD:
            threats.append({"threat_type": "http_brute_force",
                            "source_ip": ip, "count": n})
    # ... ssh and port-scan thresholds elided ...
    return {"threats_found": bool(threats), "threats": threats}`));
  b.push(blank());

  b.push(h2('B.5  LangGraph Reasoning Loop'));
  b.push(p('From agent/orchestrator.py, the four-node state machine:'));
  b.push(blank());
  b.push(...code(`def build_graph():
    graph = StateGraph(GraphState)
    graph.add_node("collect_data", _collect_data)
    graph.add_node("analyze", _analyze)
    graph.add_node("decide_action", _decide_action)
    graph.add_node("notify", _notify)
    graph.add_edge(START, "collect_data")
    graph.add_edge("collect_data", "analyze")
    graph.add_edge("analyze", "decide_action")
    graph.add_conditional_edges("decide_action", _route_notify,
                                {"notify": "notify", "skip": END})
    graph.add_edge("notify", END)
    return graph.compile()`));
  b.push(blank());

  // ============ APPENDIX C ============
  b.push(chapterLabel('APPENDIX C: DOCKER COMPOSE CONFIGURATION'));
  b.push(blank());
  b.push(p('The docker-compose.yml extract below defines the single-host deployment. The agent and API share the SQLite volume. The API also mounts the local Markdown runbooks, ChromaDB data, and local embedding cache. The optional Ollama service provides on-host inference, while cloud providers use API keys supplied through the environment file. No Google Cloud service-account credential is mounted.'));
  b.push(blank());
  b.push(...code(`services:
  api:
    build:
      context: .
      dockerfile: api/Dockerfile
    image: \${REGISTRY:-infraguard}/api:latest
    env_file:
      - .env
    ports: ["8080:8080"]
    environment:
      - PYTHONPATH=/app
      - DB_PATH=/data/verdicts.db
      - RUNBOOKS_DIR=/app/runbooks
    volumes:
      - ./runbooks:/app/runbooks:ro
      - sqlite_data:/data
      - chroma_data:/app/chroma_db
      - embedding_cache:/root/.cache
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  agent:
    build:
      context: .
      dockerfile: agent/Dockerfile
    image: \${REGISTRY:-infraguard}/agent:latest
    env_file:
      - .env
    environment:
      - PYTHONPATH=/app
      - DB_PATH=/data/verdicts.db
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - sqlite_data:/data
    restart: unless-stopped
    depends_on:
      - api

  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

volumes:
  sqlite_data: {}
  chroma_data: {}
  embedding_cache: {}
  ollama_data: {}`));
  b.push(blank());

  // ============ APPENDIX D ============
  b.push(chapterLabel('APPENDIX D: PROPOSED USABILITY EVALUATION INSTRUMENT'));
  b.push(blank());
  b.push(p('Appendix D contains the task script and System Usability Scale questionnaire prepared for a later practitioner study. The instrument was not administered for Chapter Five. The later study must obtain any ethics approval and participant consent required by University policy.'));
  b.push(blank());

  b.push(h2('D.1  Task Script'));
  b.push(p('In a future session, each participant would receive a brief orientation and complete the following tasks while the facilitator records success, time, errors, and requests for help.'));
  b.push(num('Log in to the dashboard and state the current overall severity.'));
  b.push(num('Open the root-cause and recommended-action sections of a non-OK verdict and paraphrase them.'));
  b.push(num('State which integrations are configured by reading the status chips.'));
  b.push(num('Ask the runbook assistant a question and confirm a cited answer is returned.'));
  b.push(num('Locate a detected threat and trigger the block-IP action (dry-run).'));
  b.push(num('Mark a recurring warning as known, and confirm on the next refresh that it is suppressed.'));
  b.push(num('Explain what the stale-agent banner indicates.'));

  b.push(h2('D.2  System Usability Scale Questionnaire'));
  b.push(p('Participants rate each statement on a five-point scale from 1 (strongly disagree) to 5 (strongly agree). The standard SUS scoring is applied: for odd-numbered items subtract 1 from the response; for even-numbered items subtract the response from 5; sum the ten contributions and multiply by 2.5 to yield a score out of 100 (Brooke, 1996).'));
  b.push(num('I think that I would like to use this dashboard frequently.'));
  b.push(num('I found the dashboard unnecessarily complex.'));
  b.push(num('I thought the dashboard was easy to use.'));
  b.push(num('I think that I would need the support of a technical person to be able to use this dashboard.'));
  b.push(num('I found the various functions in this dashboard were well integrated.'));
  b.push(num('I thought there was too much inconsistency in this dashboard.'));
  b.push(num('I would imagine that most people would learn to use this dashboard very quickly.'));
  b.push(num('I found the dashboard very cumbersome to use.'));
  b.push(num('I felt very confident using the dashboard.'));
  b.push(num('I needed to learn a lot of things before I could get going with this dashboard.'));
  b.push(blank());
  b.push(p('A short structured interview may follow the questionnaire and cover effectiveness, efficiency, learnability, and trust. When the study is conducted, the report should include participant characteristics, task results, SUS calculations, qualitative themes, and any interface changes.'));

  return b;
}

module.exports = { appendices };
