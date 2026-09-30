'use client';
import { useState } from 'react';
import Link from 'next/link';
import Navbar from '../../components/Navbar';
import styles from './agents.module.css';

const AGENTS_DATA = [
  {
    num: '01',
    stage: 'STAGE 1 / ROOT CAUSE',
    name: 'Diagnosis Agent',
    role: 'Traceback Parsing & Bug Classification',
    desc: 'The front-line agent in the LangGraph workflow. It parses multi-frame Python tracebacks, isolates the originating file and line number, classifies error severity, and structures the diagnostic payload.',
    metrics: [
      { label: 'Parse Accuracy', value: '99.4%' },
      { label: 'Avg Latency', value: '< 1.8s' },
      { label: 'Classification', value: 'Deterministic' },
    ],
    subcomponents: [
      {
        name: 'ErrorParser',
        desc: 'Extracts exception class (e.g. AttributeError, KeyError), filename, line number, and stack call hierarchy from arbitrary raw tracebacks.'
      },
      {
        name: 'BugClassifier',
        desc: 'Categorizes bugs into structural, semantic, runtime, or concurrency faults and assigns a priority level from LOW to CRITICAL.'
      },
      {
        name: 'LogAnalyzer',
        desc: 'Scans accompanying execution logs for warning indicators, HTTP status codes, and database connection timeouts prior to failure.'
      }
    ],
    prompt: `You are the Diagnosis Agent in Bugify.
Given a raw Python stack trace and user problem description:
1. Parse the exception name and offending file/line.
2. Formulate a concise root-cause diagnosis.
3. Output strictly structured JSON conforming to BugReport schema.`,
    stateIO: {
      reads: ['traceback', 'problem_description', 'repo_path'],
      writes: ['diagnosis', 'current_stage'],
    },
    tags: ['Traceback Engine', 'Regex Extractor', 'Severity Matrix', 'BugReport Schema']
  },
  {
    num: '02',
    stage: 'STAGE 2 / REPO EXPLORATION',
    name: 'Code Analysis Agent',
    role: 'AST Syntax Traversal & Dependency Graphing',
    desc: 'Performs deep static inspection on the target repository. Uses Python AST traversal to map classes, functions, variable scopes, and module import trees surrounding the identified failure site.',
    metrics: [
      { label: 'AST Traversal', value: '100% Tree-sitter' },
      { label: 'Graph Depth', value: 'Recursive' },
      { label: 'Cycle Detection', value: 'Tarjan Algorithm' },
    ],
    subcomponents: [
      {
        name: 'ASTAnalyzer',
        desc: 'Walks the Python Abstract Syntax Tree to identify function definitions, cyclomatic complexity, unhandled None returns, and syntax errors.'
      },
      {
        name: 'DependencyAnalyzer',
        desc: 'Constructs an import dependency graph across repository files to ensure proposed modifications do not cause circular imports or cascade failures.'
      },
      {
        name: 'RepositoryExplorer',
        desc: 'Traverses git directory trees, identifies configuration files, and indexes source code for contextual retrieval.'
      }
    ],
    prompt: `You are the Code Analysis Agent.
Analyze the target Python module's AST:
1. Identify all functions and class scopes surrounding the error line.
2. Check caller references and import dependencies.
3. Return CodeAnalysisResult with AST nodes and dependency paths.`,
    stateIO: {
      reads: ['diagnosis', 'repo_path'],
      writes: ['code_analysis', 'current_stage'],
    },
    tags: ['ast module', 'Call Graphs', 'Static Analysis', 'Import Resolver']
  },
  {
    num: '03',
    stage: 'STAGE 3 / KNOWLEDGE RETRIEVAL',
    name: 'Research Agent',
    role: 'Dense Vector Knowledge Retrieval & Hypothesis Formulation',
    desc: 'Interfaces with Qdrant vector database to perform semantic similarity searches over past resolved issues, error patterns, and official library documentation. Employs Groq LLaMA 3.3 to formulate actionable fix hypotheses.',
    metrics: [
      { label: 'Vector Index', value: 'Qdrant 384-d' },
      { label: 'Similarity Cutoff', value: '0.82 Cosine' },
      { label: 'Fallback', value: 'In-Memory Matrix' },
    ],
    subcomponents: [
      {
        name: 'Retriever',
        desc: 'Queries collections in Qdrant using dense embeddings with automated fallback to an in-memory cosine similarity store.'
      },
      {
        name: 'EmbeddingService',
        desc: 'Transforms bug descriptions and code snippets into 384-dimensional vector embeddings using sentence-transformers or miniLM.'
      },
      {
        name: 'KnowledgeIngestionPipeline',
        desc: 'Chunks, indexes, and stores error patterns and seed bug documentation into persistent vector collections.'
      }
    ],
    prompt: `You are the Research Agent.
Given the diagnosis and code context:
1. Review the retrieved semantic knowledge chunks from Qdrant.
2. Formulate 1-2 verified hypotheses explaining the bug.
3. Recommend specific defensive coding strategies.`,
    stateIO: {
      reads: ['diagnosis', 'code_analysis'],
      writes: ['research', 'current_stage'],
    },
    tags: ['Qdrant DB', 'Sentence Transformers', 'Groq LLaMA 3.3', 'RAG Pipeline']
  },
  {
    num: '04',
    stage: 'STAGE 4 / PATCH SYNTHESIS',
    name: 'Fix Agent',
    role: 'Patch Synthesis, Review Scoring & Automated Refactoring',
    desc: 'Synthesizes clean unified diff patches tailored to resolve the diagnosed issue. Employs a multi-turn LLM reviewer loop: if a patch is scored below threshold, the agent revises the diff or rejects it prior to application.',
    metrics: [
      { label: 'Review Threshold', value: 'Score >= 8.0/10' },
      { label: 'Max Retries', value: '3 Iterations' },
      { label: 'Diff Standard', value: 'Unified Git Diff' },
    ],
    subcomponents: [
      {
        name: 'PatchGenerator',
        desc: 'Generates standard unified diff patches adhering to git format without extraneous refactoring or unintended side-effects.'
      },
      {
        name: 'PatchReviewer',
        desc: 'An independent LLM critic that scores candidate patches on correctness, minimal scope, and safety. Returns APPROVE, REVISE, or REJECT.'
      },
      {
        name: 'RefactoringAgent',
        desc: 'Optional optimization agent that refactors approved patches for PEP 8 compliance, type annotations, and performance efficiency.'
      }
    ],
    prompt: `You are the Fix Agent.
Synthesize a minimal unified diff patch to fix the diagnosed error:
1. Never introduce extraneous refactoring or scope creep.
2. Preserve existing docstrings, style, and comments.
3. Output strictly valid unified diff format (--- a/..., +++ b/...).`,
    stateIO: {
      reads: ['diagnosis', 'code_analysis', 'research', 'iteration_count'],
      writes: ['patch', 'current_stage'],
    },
    tags: ['Unified Diffs', 'Self-Correction Loop', 'Patch Reviewer', 'Git Apply']
  },
  {
    num: '05',
    stage: 'STAGE 5 / VERIFICATION & TESTS',
    name: 'Verification Agent',
    role: 'Isolated Sandbox Execution & Pytest Regression Suite',
    desc: 'The final quality gate before a patch is delivered. Validates syntax correctness and executes test suites inside isolated Docker containers or sandboxed subprocess environments with strict memory and CPU quotas.',
    metrics: [
      { label: 'Isolation', value: 'Docker Container' },
      { label: 'Timeout Guard', value: '60s Hard Limit' },
      { label: 'Memory Ceiling', value: '512 MB Cap' },
    ],
    subcomponents: [
      {
        name: 'SyntaxValidator',
        desc: 'Compiles the patched Python files with ast.parse() to guarantee zero syntax or indentation errors before test execution.'
      },
      {
        name: 'SandboxExecutor',
        desc: 'Executes tests within an ephemeral Docker container with read-only volume mounts and disabled network access.'
      },
      {
        name: 'TestRunner',
        desc: 'Invokes pytest against the unit test suite and parses stdout/stderr to calculate pass rates, execution durations, and regression statuses.'
      }
    ],
    prompt: `You are the Verification Agent.
Examine the pytest execution stdout, stderr, and exit code:
1. Check if all unit tests passed with 0 failures.
2. Verify no new regressions were introduced.
3. Output TestSuiteResult to complete or loopback state.`,
    stateIO: {
      reads: ['patch', 'repo_path'],
      writes: ['verification', 'is_success', 'current_stage'],
    },
    tags: ['Docker Sandbox', 'Pytest Runner', 'Resource Quotas', 'Syntax Compiler']
  }
];

export default function AgentsPage() {
  const [activeTabs, setActiveTabs] = useState({
    '01': 'submodules',
    '02': 'submodules',
    '03': 'submodules',
    '04': 'submodules',
    '05': 'submodules',
  });

  const handleTabChange = (num, tab) => {
    setActiveTabs((prev) => ({ ...prev, [num]: tab }));
  };

  return (
    <div className={styles.container}>
      <Navbar />

      <div className={styles.ambientGlow} aria-hidden="true" />

      <div className="container">
        <header className={styles.header}>
          <div className="badge">
            <span className="dot-pulse dot-amber" />
            Specialized Autonomous Swarm
          </div>
          <h1 className={styles.title}>
            The 5 Autonomous Agents.<br />
            <span className={styles.titleItalic}>Engineered for precision</span>
          </h1>
          <p className={styles.subtitle}>
            Bugify is not a single prompt. It is a synchronized network of five specialized agents,
            each engineered with deterministic tools, AST parsers, isolated sandboxes, and verification loops.
          </p>
        </header>

        <div className={styles.agentsList}>
          {AGENTS_DATA.map((agent) => {
            const currentTab = activeTabs[agent.num] || 'submodules';
            return (
              <div key={agent.num} className={styles.agentCard}>
                {/* Left Side: Agent Identity & Specs */}
                <div className={styles.agentLeft}>
                  <div className={styles.agentNumberBadge}>
                    <span className={styles.numberBox}>{agent.num}</span>
                    <span className={styles.stageText}>{agent.stage}</span>
                  </div>

                  <div>
                    <div className={styles.agentRole}>{agent.role}</div>
                    <h2 className={styles.agentName}>{agent.name}</h2>
                  </div>

                  <p className={styles.agentDesc}>{agent.desc}</p>

                  {/* Telemetry metrics bar */}
                  <div className={styles.agentMetricsBar}>
                    {agent.metrics.map((m) => (
                      <div key={m.label} className={styles.metricCol}>
                        <span className={styles.metricValue}>{m.value}</span>
                        <span className={styles.metricLabel}>{m.label}</span>
                      </div>
                    ))}
                  </div>

                  <div className={styles.specRow}>
                    {agent.tags.map((t) => (
                      <span key={t} className="tag">{t}</span>
                    ))}
                  </div>

                  <div style={{ marginTop: 10 }}>
                    <Link href="/debug" className="btn-primary" style={{ padding: '8px 22px', fontSize: '0.8rem' }}>
                      Test Agent {agent.num} in Console →
                    </Link>
                  </div>
                </div>

                {/* Right Side: Interactive Inspector Drawer */}
                <div className={styles.agentRight}>
                  <div className={styles.tabBar}>
                    <button
                      type="button"
                      className={`${styles.tabBtn} ${currentTab === 'submodules' ? styles.tabBtnActive : ''}`}
                      onClick={() => handleTabChange(agent.num, 'submodules')}
                    >
                      Sub-Modules
                    </button>
                    <button
                      type="button"
                      className={`${styles.tabBtn} ${currentTab === 'prompt' ? styles.tabBtnActive : ''}`}
                      onClick={() => handleTabChange(agent.num, 'prompt')}
                    >
                      Prompt Directive
                    </button>
                    <button
                      type="button"
                      className={`${styles.tabBtn} ${currentTab === 'state' ? styles.tabBtnActive : ''}`}
                      onClick={() => handleTabChange(agent.num, 'state')}
                    >
                      State I/O
                    </button>
                  </div>

                  {currentTab === 'submodules' && (
                    <div className={styles.tabContent}>
                      {agent.subcomponents.map((sub) => (
                        <div key={sub.name} className={styles.subcomponentItem}>
                          <div className={styles.subcomponentBullet} />
                          <div>
                            <div className={styles.subcomponentName}>{sub.name}</div>
                            <div className={styles.subcomponentDetail}>{sub.desc}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}

                  {currentTab === 'prompt' && (
                    <div className={styles.tabContent}>
                      <pre className="code-block" style={{ fontSize: '0.76rem', color: '#fbbf24', maxHeight: 220 }}>
                        {agent.prompt}
                      </pre>
                    </div>
                  )}

                  {currentTab === 'state' && (
                    <div className={styles.tabContent} style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                      <div className="card" style={{ padding: '12px 16px' }}>
                        <div style={{ fontSize: '0.7rem', color: '#737373', textTransform: 'uppercase', marginBottom: 4 }}>
                          Reads from BugifyState:
                        </div>
                        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                          {agent.stateIO.reads.map((r) => (
                            <span key={r} className="tag mono" style={{ color: '#38bdf8' }}>{r}</span>
                          ))}
                        </div>
                      </div>

                      <div className="card" style={{ padding: '12px 16px' }}>
                        <div style={{ fontSize: '0.7rem', color: '#737373', textTransform: 'uppercase', marginBottom: 4 }}>
                          Writes to BugifyState:
                        </div>
                        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                          {agent.stateIO.writes.map((w) => (
                            <span key={w} className="tag mono" style={{ color: '#4ade80' }}>{w}</span>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
