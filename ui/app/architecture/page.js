'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import Navbar from '../../components/Navbar';
import styles from './architecture.module.css';

/* ── SVG Icons ──────────────────────────────────────── */
function IconDiagnosis() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
      <path d="M12 2L2 7l10 5 10-5-10-5z" stroke="#fbbf24" strokeWidth="1.8" strokeLinejoin="round"/>
      <path d="M2 17l10 5 10-5" stroke="#fbbf24" strokeWidth="1.8" strokeLinejoin="round"/>
      <path d="M2 12l10 5 10-5" stroke="#fbbf24" strokeWidth="1.8" strokeLinejoin="round"/>
    </svg>
  );
}

function IconAST() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="4" r="2.5" stroke="#fbbf24" strokeWidth="1.8"/>
      <circle cx="5" cy="18" r="2.5" stroke="#fbbf24" strokeWidth="1.8"/>
      <circle cx="19" cy="18" r="2.5" stroke="#fbbf24" strokeWidth="1.8"/>
      <path d="M12 6.5V10M12 10L5 15.5M12 10L19 15.5" stroke="#fbbf24" strokeWidth="1.6" strokeDasharray="3 2"/>
    </svg>
  );
}

function IconRAG() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
      <rect x="3" y="3" width="8" height="8" rx="2" stroke="#fbbf24" strokeWidth="1.8"/>
      <rect x="13" y="3" width="8" height="8" rx="2" stroke="#fbbf24" strokeWidth="1.8"/>
      <rect x="3" y="13" width="8" height="8" rx="2" stroke="#fbbf24" strokeWidth="1.8"/>
      <path d="M17 13v2M17 15h-4v3h4v2" stroke="#fbbf24" strokeWidth="1.8" strokeLinecap="round"/>
    </svg>
  );
}

function IconPatch() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
      <path d="M12 20h9" stroke="#fbbf24" strokeWidth="1.8" strokeLinecap="round"/>
      <path d="M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z" stroke="#fbbf24" strokeWidth="1.8" strokeLinejoin="round"/>
    </svg>
  );
}

function IconVerify() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
      <path d="M22 11.08V12a10 10 0 11-5.93-9.14" stroke="#fbbf24" strokeWidth="1.8" strokeLinecap="round"/>
      <polyline points="22 4 12 14.01 9 11.01" stroke="#22c55e" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

function IconComplete() {
  return (
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="10" stroke="#fbbf24" strokeWidth="1.8"/>
      <path d="M8 12l3 3 5-6" stroke="#fbbf24" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

function IconRouter() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
      <polyline points="17 1 21 5 17 9" stroke="#fbbf24" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M3 11V9a4 4 0 014-4h14" stroke="#fbbf24" strokeWidth="1.8" strokeLinecap="round"/>
      <polyline points="7 23 3 19 7 15" stroke="#fbbf24" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
      <path d="M21 13v2a4 4 0 01-4 4H3" stroke="#fbbf24" strokeWidth="1.8" strokeLinecap="round"/>
    </svg>
  );
}

const PIPELINE = [
  {
    step: '01',
    id: 'diagnosis',
    name: 'Diagnosis Node',
    role: 'Root Cause Analysis',
    desc: 'Parses traceback frames, classifies exception type, extracts file & line, assigns severity priority.',
    Icon: IconDiagnosis,
    color: '#f59e0b',
    reads: ['traceback', 'problem_description'],
    writes: ['diagnosis', 'current_stage'],
    metric: '< 1.8s avg',
  },
  {
    step: '02',
    id: 'code_analysis',
    name: 'Code Analysis Node',
    role: 'AST Traversal & Graph',
    desc: 'Walks Python AST tree, maps call graph, detects None-return paths, resolves import chains.',
    Icon: IconAST,
    color: '#3b82f6',
    reads: ['diagnosis', 'repo_path'],
    writes: ['code_analysis', 'current_stage'],
    metric: '100% AST coverage',
  },
  {
    step: '03',
    id: 'research',
    name: 'Research Node',
    role: 'RAG Vector Retrieval',
    desc: 'Executes 384-dim dense vector search against Qdrant collections. Retrieves similar bug patterns.',
    Icon: IconRAG,
    color: '#a855f7',
    reads: ['diagnosis', 'code_analysis'],
    writes: ['research', 'current_stage'],
    metric: '0.94 similarity',
  },
  {
    step: '04',
    id: 'fix',
    name: 'Fix Node',
    role: 'Patch Generation',
    desc: 'Synthesizes unified diff patch from LLM reasoning over diagnosis + code context + RAG results.',
    Icon: IconPatch,
    color: '#ea580c',
    reads: ['diagnosis', 'code_analysis', 'research'],
    writes: ['patch', 'current_stage'],
    metric: '9.8/10 review score',
  },
  {
    step: '05',
    id: 'verification',
    name: 'Verification Node',
    role: 'Isolated Pytest Sandbox',
    desc: 'Executes patch inside Docker container or subprocess sandbox. Runs full test suite with 22/22 coverage.',
    Icon: IconVerify,
    color: '#22c55e',
    reads: ['patch', 'repo_path'],
    writes: ['verification', 'is_success'],
    metric: '22/22 tests pass',
  },
  {
    step: '06',
    id: 'complete',
    name: 'Complete Node',
    role: 'Delivery & Report',
    desc: 'Assembles final debugging report, patch diff, test results, and delivers structured JSON response.',
    Icon: IconComplete,
    color: '#fbbf24',
    reads: ['verification', 'patch'],
    writes: ['final_report'],
    metric: 'Deterministic',
  },
];

const STACK_ITEMS = [
  { label: 'Orchestration', value: 'LangGraph', sub: 'State machine + conditional edges', color: '#f59e0b' },
  { label: 'LLM Engine', value: 'Groq LLaMA 3.3', sub: 'Ultra-low latency inference', color: '#a855f7' },
  { label: 'Vector Store', value: 'Qdrant', sub: '384-dim dense embeddings', color: '#3b82f6' },
  { label: 'API Layer', value: 'FastAPI', sub: 'Async Python ASGI server', color: '#22c55e' },
  { label: 'Sandbox', value: 'Docker', sub: 'python:3.11-slim isolated', color: '#ea580c' },
  { label: 'Schema', value: 'Pydantic v2', sub: 'TypedDict strict validation', color: '#06b6d4' },
];

export default function ArchitecturePage() {
  const [activeNode, setActiveNode] = useState(null);
  const [flowActive, setFlowActive] = useState(false);
  const [flowStep, setFlowStep] = useState(-1);

  useEffect(() => {
    const t = setTimeout(() => setFlowActive(true), 600);
    return () => clearTimeout(t);
  }, []);

  useEffect(() => {
    if (!flowActive) return;
    let i = 0;
    const interval = setInterval(() => {
      setFlowStep(i % PIPELINE.length);
      i++;
    }, 900);
    return () => clearInterval(interval);
  }, [flowActive]);

  const selected = activeNode !== null ? PIPELINE[activeNode] : null;

  return (
    <div className={styles.page}>
      <Navbar />

      {/* Ambient glow */}
      <div className={styles.glow1} />
      <div className={styles.glow2} />

      <div className="container" style={{ paddingTop: 110, paddingBottom: 80 }}>

        {/* Header */}
        <header className={styles.header}>
          <div className="badge" style={{ animationDelay: '0s' }}>
            <span className="dot-pulse dot-amber" />
            LangGraph State Machine Engine
          </div>
          <h1 className={styles.title}>
            System <span className="gradient-text">Architecture</span>
          </h1>
          <p className={styles.subtitle}>
            A deterministic, state-machine driven agentic workflow. Each node is a specialized AI agent
            that reads from a shared <code>BugifyState</code>, executes, and writes results — enabling
            conditional retry branching and full traceability.
          </p>
        </header>

        {/* ── Interactive Pipeline Flow ── */}
        <div className={styles.pipelineCard}>
          <div className={styles.pipelineHeader}>
            <div>
              <div className="badge" style={{ marginBottom: 8 }}>
                <span className="dot-pulse" />
                Live Node Execution Flow
              </div>
              <h2 className={styles.pipelineTitle}>LangGraph Compiled State Graph</h2>
            </div>
            <div className={styles.pipelineMeta}>
              <span className="tag mono">6 nodes</span>
              <span className="tag mono">1 conditional router</span>
              <span className="tag mono">3 max retries</span>
            </div>
          </div>

          {/* Flow nodes */}
          <div className={styles.flowGrid}>
            {PIPELINE.map((node, i) => {
              const Icon = node.Icon;
              const isActive = flowStep === i;
              const isDone = flowStep > i;
              const isSelected = activeNode === i;
              return (
                <div key={node.id} style={{ display: 'contents' }}>
                  <button
                    className={`${styles.flowNode} ${isActive ? styles.flowNodeActive : ''} ${isDone ? styles.flowNodeDone : ''} ${isSelected ? styles.flowNodeSelected : ''}`}
                    onClick={() => setActiveNode(activeNode === i ? null : i)}
                    style={{ '--node-color': node.color }}
                    aria-label={`View ${node.name} details`}
                  >
                    <div className={styles.flowNodeStep} style={{ color: node.color }}>
                      {isDone ? '✓' : node.step}
                    </div>
                    <div className={styles.flowNodeIcon} style={{ color: node.color }}>
                      <Icon />
                    </div>
                    <div className={styles.flowNodeName}>{node.name}</div>
                    <div className={styles.flowNodeRole}>{node.role}</div>
                    {isActive && <div className={styles.flowNodePing} style={{ background: node.color }} />}
                  </button>

                  {i < PIPELINE.length - 1 && (
                    <div className={styles.flowConnector}>
                      <svg width="40" height="20" viewBox="0 0 40 20">
                        <line
                          x1="0" y1="10" x2="40" y2="10"
                          stroke={isDone ? '#22c55e' : 'rgba(255,255,255,0.1)'}
                          strokeWidth="1.5"
                          strokeDasharray="4 4"
                          style={{ transition: 'stroke 0.4s ease' }}
                        />
                        <polygon
                          points="32,6 40,10 32,14"
                          fill={isDone ? '#22c55e' : 'rgba(255,255,255,0.15)'}
                          style={{ transition: 'fill 0.4s ease' }}
                        />
                      </svg>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Retry loop indicator */}
          <div className={styles.retryLoop}>
            <div className={styles.retryLoopLine} />
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <IconRouter />
              <span className={styles.retryLoopLabel}>
                Conditional Router: if <code>tests_fail</code> &amp;&amp; <code>retries &lt; 3</code> → loops back to Fix Node
              </span>
            </div>
          </div>

          {/* Node detail panel */}
          {selected && (
            <div className={styles.nodeDetail} style={{ '--node-color': selected.color }}>
              <div className={styles.nodeDetailHeader}>
                <div>
                  <span className="badge" style={{ background: `${selected.color}18`, borderColor: `${selected.color}40`, color: selected.color }}>
                    Stage {selected.step}
                  </span>
                  <h3 className={styles.nodeDetailTitle}>{selected.name}</h3>
                  <p className={styles.nodeDetailRole}>{selected.role}</p>
                </div>
                <div className={styles.nodeDetailMetric}>
                  <div className={styles.nodeDetailMetricValue}>{selected.metric}</div>
                  <div className={styles.nodeDetailMetricLabel}>Performance</div>
                </div>
              </div>
              <p className={styles.nodeDetailDesc}>{selected.desc}</p>
              <div className={styles.nodeDetailIO}>
                <div className={styles.nodeIOGroup}>
                  <div className={styles.nodeIOLabel} style={{ color: '#ef4444' }}>Reads from State</div>
                  {selected.reads.map(r => <span key={r} className="tag mono" style={{ borderColor: 'rgba(239,68,68,0.3)', color: '#fca5a5' }}>{r}</span>)}
                </div>
                <div className={styles.nodeIOArrow}>→</div>
                <div className={styles.nodeIOGroup}>
                  <div className={styles.nodeIOLabel} style={{ color: '#22c55e' }}>Writes to State</div>
                  {selected.writes.map(w => <span key={w} className="tag mono" style={{ borderColor: 'rgba(34,197,94,0.3)', color: '#86efac' }}>{w}</span>)}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* ── Two Column: State Schema + Router ── */}
        <div className={styles.twoCol}>
          <div className={styles.infoCard}>
            <div className="badge" style={{ alignSelf: 'flex-start', marginBottom: 12 }}>Pydantic State Schema</div>
            <h3 className={styles.infoTitle}>TypedDict BugifyState</h3>
            <p className={styles.infoDesc}>
              Strictly typed state schema defined in <code>orchestrator/state.py</code>.
              Every agent reads from and writes to the same immutable state, guaranteeing
              100% context preservation across all 6 nodes.
            </p>
            <pre className="code-block" style={{ fontSize: '0.76rem', marginTop: 16 }}>
{`class BugifyState(TypedDict, total=False):
    # ── Inputs ──────────────────────────
    problem_description: str
    traceback:           str
    repo_path:           str

    # ── Agent Outputs ───────────────────
    diagnosis:     Optional[BugReport]
    code_analysis: Optional[CodeAnalysisResult]
    research:      Optional[ResearchResult]
    patch:         Optional[PatchResult]
    verification:  Optional[TestSuiteResult]

    # ── Control Flow ────────────────────
    current_stage:   str
    iteration_count: int     # max = 3
    error:           Optional[str]
    is_success:      bool`}
            </pre>
          </div>

          <div className={styles.infoCard}>
            <div className="badge" style={{ alignSelf: 'flex-start', marginBottom: 12 }}>Dynamic Router</div>
            <h3 className={styles.infoTitle}>Conditional Edge Router</h3>
            <p className={styles.infoDesc}>
              The router in <code>orchestrator/router.py</code> inspects verification results
              and patch review scores — routing autonomously without human intervention.
            </p>
            <pre className="code-block" style={{ fontSize: '0.76rem', marginTop: 16 }}>
{`def route_after_verification(
    state: BugifyState
) -> str:
    verif = state.get("verification")
    n = state.get("iteration_count", 0)

    # Success: all tests passed
    if verif and verif.tests_passed:
        return "complete"

    # Retry loop: re-enter fix node
    if n < MAX_RETRIES:  # MAX_RETRIES = 3
        return "fix"

    # Exhausted: graceful degradation
    return "complete"  # returns best-effort`}
            </pre>

            <div className={styles.endpointRow}>
              <div className={styles.nodeIOLabel} style={{ color: '#737373', marginBottom: 8 }}>REST API Endpoints</div>
              <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                <span className="tag mono" style={{ color: '#f59e0b', borderColor: 'rgba(245,158,11,0.3)' }}>POST /api/v1/debug</span>
                <span className="tag mono">GET /api/v1/health</span>
                <span className="tag mono">GET /api/v1/status</span>
              </div>
            </div>
          </div>
        </div>

        {/* ── Tech Stack Grid ── */}
        <div className={styles.stackSection}>
          <div className="section-label">Production Technology Stack</div>
          <div className={styles.stackGrid}>
            {STACK_ITEMS.map((s) => (
              <div key={s.label} className={styles.stackCard}>
                <div className={styles.stackDot} style={{ background: s.color, boxShadow: `0 0 12px ${s.color}` }} />
                <div>
                  <div className={styles.stackLabel}>{s.label}</div>
                  <div className={styles.stackValue} style={{ color: s.color }}>{s.value}</div>
                  <div className={styles.stackSub}>{s.sub}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div style={{ textAlign: 'center', marginTop: 60 }}>
          <Link href="/debug" className="btn-primary" style={{ padding: '13px 36px' }}>
            Run the Workflow in Debug Console →
          </Link>
        </div>
      </div>
    </div>
  );
}
