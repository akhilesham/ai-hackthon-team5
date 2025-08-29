import React from "react";

// LLM Code Snippet Generator – Reference Architecture Diagram
// Notes:
// - This is a pure React + SVG diagram. No external libs required.
// - Tailwind classes are used for layout and typography.
// - Boxes are grouped in lanes to show trust boundaries and flow.
// - You can export as PNG/PDF via your browser's print or screenshot tools.

const Box = ({ x, y, w, h, title, lines = [], tone = "default" }) => {
  const tones = {
    default: "fill-white stroke-gray-300",
    accent: "fill-indigo-50 stroke-indigo-300",
    danger: "fill-rose-50 stroke-rose-300",
    success: "fill-emerald-50 stroke-emerald-300",
    muted: "fill-gray-50 stroke-gray-200",
    dark: "fill-slate-50 stroke-slate-300",
  };
  return (
    <g transform={`translate(${x}, ${y})`}>
      <rect
        width={w}
        height={h}
        rx={14}
        className={`${tones[tone]} stroke-2 shadow`}
      />
      <text x={14} y={24} className="fill-slate-800 text-[12px] font-semibold">
        {title}
      </text>
      {lines.map((t, i) => (
        <text key={i} x={14} y={44 + i * 18} className="fill-slate-700 text-[11px]">
          • {t}
        </text>
      ))}
    </g>
  );
};

const Lane = ({ x, y, w, h, title }) => (
  <g transform={`translate(${x}, ${y})`}>
    <rect width={w} height={h} rx={18} className="fill-white stroke-slate-200 stroke-2" />
    <text x={12} y={22} className="fill-slate-500 text-[12px] font-semibold uppercase tracking-wide">
      {title}
    </text>
  </g>
);

const Arrow = ({ from, to, label }) => {
  // from = {x, y}; to = {x, y}
  const id = `arrow-${Math.random().toString(36).slice(2, 7)}`;
  return (
    <g>
      <defs>
        <marker id={`${id}-head`} markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
          <polygon points="0 0, 10 3.5, 0 7" className="fill-slate-500" />
        </marker>
      </defs>
      <line
        x1={from.x}
        y1={from.y}
        x2={to.x}
        y2={to.y}
        className="stroke-slate-400"
        strokeWidth={2}
        markerEnd={`url(#${id}-head)`}
      />
      {label && (
        <text x={(from.x + to.x) / 2 + 6} y={(from.y + to.y) / 2 - 6} className="fill-slate-600 text-[11px]">
          {label}
        </text>
      )}
    </g>
  );
};

export default function Diagram() {
  // Canvas size
  const W = 1400;
  const H = 980;

  // Lane geometry
  const lanePad = 20;
  const laneW = W - lanePad * 2;

  return (
    <div className="w-full min-h-screen bg-slate-50 p-6">
      <div className="max-w-[1500px] mx-auto">
        <h1 className="text-3xl font-semibold text-slate-900 mb-2">LLM-Based Code Snippet Generator – Reference Architecture</h1>
        <p className="text-slate-600 mb-6">Secure, observable, and responsible-by-default design. The diagram highlights data flow, trust boundaries, safety gates, and retrieval/tooling components.</p>

        <div className="rounded-2xl bg-white shadow p-3 overflow-auto">
          <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`}>
            {/* Lanes / Boundaries */}
            <Lane x={lanePad} y={10} w={laneW} h={210} title="Client Layer (Untrusted / External)" />
            <Lane x={lanePad} y={230} w={laneW} h={260} title="API & Orchestration (Trusted)" />
            <Lane x={lanePad} y={510} w={laneW} h={220} title="Context, Retrieval & Tooling (Trusted)" />
            <Lane x={lanePad} y={750} w={laneW} h={210} title="Models & Providers (Partially Trusted)" />

            {/* Client Layer */}
            <Box
              x={40}
              y={40}
              w={340}
              h={160}
              title="User Clients"
              tone="muted"
              lines={[
                "Web UI (Playground)",
                "IDE Extension (VS Code/JetBrains)",
                "CLI / CI Integration",
                "Partner API Consumers",
              ]}
            />

            <Box
              x={410}
              y={40}
              w={340}
              h={160}
              title="AuthN/Z & Front Door"
              tone="accent"
              lines={[
                "OIDC/SAML, OAuth2, API Keys",
                "Rate Limits & Quotas",
                "Tenant Isolation, Usage Plans",
                "WAF / Bot Detection",
              ]}
            />

            <Box
              x={780}
              y={40}
              w={560}
              h={160}
              title="Observability Edge"
              tone="dark"
              lines={[
                "Request Logging (PII scrubbing)",
                "Trace/Span Correlation (OpenTelemetry)",
                "Prompt/Response Vault (Redacted)",
                "User Feedback Capture (👍/👎)",
              ]}
            />

            {/* API & Orchestration */}
            <Box
              x={40}
              y={260}
              w={360}
              h={210}
              title="Orchestrator / Router"
              lines={[
                "Request validation & schema checks",
                "Policy guardrails (Responsible AI)",
                "Model selection & cost routing",
                "Streaming & tool-calls management",
              ]}
            />

            <Box
              x={430}
              y={260}
              w={360}
              h={210}
              title="Prompt & Context Builder"
              tone="muted"
              lines={[
                "Templates (task, style, constraints)",
                "System policies (security, licenses)",
                "Few-shot exemplars / chain-of-thought hints",
                "Determinism controls (temp/top-p)",
              ]}
            />

            <Box
              x={820}
              y={260}
              w={260}
              h={210}
              title="Safety Gates"
              tone="danger"
              lines={[
                "PII redaction & secret scanning",
                "Toxicity / unsafe action filters",
                "Code security lints (SAST pre-gen)",
                "License policy checks",
              ]}
            />

            <Box
              x={1100}
              y={260}
              w={240}
              h={210}
              title="Async Workers"
              tone="muted"
              lines={[
                "Queue for long jobs (tests/docs)",
                "Retries / dead-letter",
                "Batch scoring & evals",
                "Backpressure controls",
              ]}
            />

            {/* Context, Retrieval & Tooling */}
            <Box
              x={40}
              y={540}
              w={360}
              h={190}
              title="Retrieval Layer"
              tone="accent"
              lines={[
                "Embedding service (text + code)",
                "Vector DB (namespaces per tenant)",
                "RAG over codebase & docs",
                "Hybrid search (BM25 + vector)",
              ]}
            />

            <Box
              x={430}
              y={540}
              w={360}
              h={190}
              title="Internal Knowledge & Artifacts"
              lines={[
                "Code patterns & secure templates",
                "Org SDKs, API specs (OpenAPI)",
                "Playbooks & style guides",
                "Golden snippets & test fixtures",
              ]}
            />

            <Box
              x={820}
              y={540}
              w={260}
              h={190}
              title="Tools (Function Calling)"
              tone="success"
              lines={[
                "Package indexer / dependency advisor",
                "Static analyzer (SAST) pre/post",
                "Unit test & docstring generators",
                "Exploit/taint checks (sandbox)",
              ]}
            />

            <Box
              x={1100}
              y={540}
              w={240}
              h={190}
              title="Storage & Feedback"
              lines={[
                "Prompt/response store (hashed)",
                "User feedback & issue reports",
                "Telemetry, costs, tokens",
                "Eval datasets & scores",
              ]}
            />

            {/* Models & Providers */}
            <Box
              x={40}
              y={780}
              w={520}
              h={160}
              title="LLM Gateway / Model Mesh"
              tone="dark"
              lines={[
                "Provider abstraction (OpenAI, Anthropic, etc.)",
                "Policy-compliant model catalog",
                "Token/cost accounting & quotas",
                "A/B and canary routing",
              ]}
            />

            <Box
              x={580}
              y={780}
              w={360}
              h={160}
              title="Hosted Models"
              lines={[
                "General LLMs (code-specialized)",
                "Open-source models (self-hosted)",
                "Guardrail models (moderation)",
                "Embedding models",
              ]}
            />

            <Box
              x={960}
              y={780}
              w={380}
              h={160}
              title="Security & Compliance"
              tone="danger"
              lines={[
                "Secrets boundary / no-train zones",
                "Data residency & tenancy controls",
                "DLP & egress policies",
                "Audit logs / model attestations",
              ]}
            />

            {/* Flow Arrows */}
            <Arrow from={{ x: 380, y: 120 }} to={{ x: 410, y: 120 }} label="TLS" />
            <Arrow from={{ x: 750, y: 120 }} to={{ x: 780, y: 120 }} label="OTel" />

            <Arrow from={{ x: 210, y: 200 }} to={{ x: 210, y: 260 }} label="API" />
            <Arrow from={{ x: 590, y: 200 }} to={{ x: 590, y: 260 }} />
            <Arrow from={{ x: 1020, y: 200 }} to={{ x: 1020, y: 260 }} />

            <Arrow from={{ x: 220, y: 365 }} to={{ x: 430, y: 365 }} label="validated request" />
            <Arrow from={{ x: 610, y: 365 }} to={{ x: 820, y: 365 }} label="redact & lint" />
            <Arrow from={{ x: 950, y: 365 }} to={{ x: 1100, y: 365 }} label="async tasks" />

            <Arrow from={{ x: 610, y: 470 }} to={{ x: 610, y: 540 }} label="build context" />
            <Arrow from={{ x: 220, y: 470 }} to={{ x: 220, y: 540 }} label="RAG" />
            <Arrow from={{ x: 950, y: 470 }} to={{ x: 950, y: 540 }} label="tools" />

            <Arrow from={{ x: 610, y: 635 }} to={{ x: 300, y: 635 }} label="retrieve" />
            <Arrow from={{ x: 610, y: 635 }} to={{ x: 1010, y: 635 }} label="invoke tools" />
            <Arrow from={{ x: 1010, y: 635 }} to={{ x: 1220, y: 635 }} label="log & eval" />

            <Arrow from={{ x: 610, y: 730 }} to={{ x: 610, y: 780 }} label="prompt+context" />
            <Arrow from={{ x: 300, y: 860 }} to={{ x: 580, y: 860 }} label="route" />
            <Arrow from={{ x: 760, y: 860 }} to={{ x: 960, y: 860 }} label="moderate" />

            <Arrow from={{ x: 760, y: 780 }} to={{ x: 760, y: 720 }} label="completion" />
            <Arrow from={{ x: 590, y: 720 }} to={{ x: 590, y: 470 }} label="stream back" />
            <Arrow from={{ x: 210, y: 470 }} to={{ x: 210, y: 200 }} label="response" />

            {/* Legend */}
            <g transform={`translate(${40}, ${940})`}>
              <rect width={540} height={28} rx={10} className="fill-white stroke-slate-200" />
              <circle cx={22} cy={14} r={6} className="fill-slate-400" />
              <text x={36} y={18} className="fill-slate-600 text-[11px]">Solid arrows: primary request/response path</text>
              <rect x={280} y={6} width={16} height={16} rx={3} className="fill-rose-50 stroke-rose-300" />
              <text x={304} y={18} className="fill-slate-600 text-[11px]">Red boxes: safety/compliance gates</text>
            </g>
          </svg>
        </div>

        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 rounded-2xl bg-white shadow">
            <h2 className="text-xl font-semibold text-slate-900 mb-2">Core Flow</h2>
            <ol className="list-decimal list-inside text-slate-700 space-y-1 text-sm">
              <li>Client sends a request (task + constraints) → AuthN/Z & rate limit.</li>
              <li>Orchestrator validates schema and applies Responsible AI guardrails.</li>
              <li>Prompt/Context Builder composes system prompt + user prompt + retrieved context.</li>
              <li>Safety Gates redact secrets/PII and pre-lint code instructions.</li>
              <li>Retrieval layer fetches org-specific code/docs (RAG). Tools may be invoked.</li>
              <li>Model Mesh routes to an appropriate model (code-specialized) with moderation.</li>
              <li>Stream completion back; post-generation linters/tests may run via Async Workers.</li>
              <li>Observability logs (redacted), feedback capture, and eval scoring for continuous improvement.</li>
            </ol>
          </div>

          <div className="p-4 rounded-2xl bg-white shadow">
            <h2 className="text-xl font-semibold text-slate-900 mb-2">Security & Responsible AI Notes</h2>
            <ul className="list-disc list-inside text-slate-700 space-y-1 text-sm">
              <li>Strict tenant isolation across vector DB namespaces and prompt vaults.</li>
              <li>PII/secret scanning on both prompts and completions; never store raw secrets.</li>
              <li>License policy checks for third-party code suggestions; prefer vetted templates.</li>
              <li>Model catalog with attestations, data use policies, and region pinning.</li>
              <li>Offline evals for security, quality, bias; golden datasets and regression gates.</li>
              <li>Human-in-the-loop approvals for high-risk actions (e.g., code that manipulates prod infra).</li>
            </ul>
          </div>
        </div>

        <div className="mt-6 p-4 rounded-2xl bg-white shadow">
          <h2 className="text-xl font-semibold text-slate-900 mb-2">Deploy Options (Cloud-native)</h2>
          <ul className="list-disc list-inside text-slate-700 space-y-1 text-sm">
            <li><span className="font-medium">API Layer:</span> Managed gateway (e.g., Kong/Apigee) + serverless functions or containers.</li>
            <li><span className="font-medium">Vector DB:</span> Managed (Pinecone/Vertex/Opensearch) or self-hosted (PGVector/Weaviate).</li>
            <li><span className="font-medium">Model Mesh:</span> Vendor SDKs with a routing facade; include fallback and timeouts.</li>
            <li><span className="font-medium">Observability:</span> OpenTelemetry + your APM (Datadog, New Relic, Grafana).</li>
            <li><span className="font-medium">Queues:</span> SQS/PubSub/Kafka for async post-gen tasks (tests, SAST, docs).</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
