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
    desc: 'The front-line agent in the LangGraph workflow. Parses multi-frame Python stack traces, isolates the originating file and line number, classifies error severity, and structures the diagnostic payload.',
    metrics: [
      { label: 'Parse Accuracy', value: '99.4%' },
      { label: 'Avg Latency', value: '< 1.2s' },
      { label: 'Classification', value: 'Deterministic' },
    ],
    subcomponents: [
      {
        name: 'ErrorParser',
        desc: 'Extracts exception class (e.g. AttributeError, KeyError), filename, line number, and stack frame call hierarchy from arbitrary raw tracebacks.'
      },
      {
        name: 'BugClassifier',
        desc: 'Categorizes bugs into runtime, semantic, logic, or concurrency faults and assigns a priority level from LOW to CRITICAL.'
      },
      {
        name: 'LogAnalyzer',
        desc: 'Scans accompanying execution logs for warning indicators, HTTP status codes, and database timeouts prior to failure.'
      }
    ],
    prompt: `You are Bugify's Bug Classification Agent.
Determine bug_type, category, severity, and confidence based strictly on provided error evidence.`,
    stateIO: {
      reads: ['traceback', 'problem', 'logs'],
      writes: ['bug_type', 'error_type', 'error_file', 'error_line', 'code_line'],
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
      { label: 'AST Traversal', value: 'Python ast Engine' },
      { label: 'Graph Depth', value: 'Bounded Recursive' },
      { label: 'Cycle Detection', value: 'Import Grapher' },
    ],
    subcomponents: [
      {
        name: 'ASTAnalyzer',
        desc: 'Walks the Python Abstract Syntax Tree to identify function definitions, cyclomatic complexity, unhandled None returns, and syntax errors.'
      },
      {
        name: 'DependencyAnalyzer',
        desc: 'Constructs an import dependency graph across repository files to ensure proposed modifications do not cause circular imports.'
      },
      {
        name: 'RepositoryExplorer',
        desc: 'Traverses git directory trees, identifies configuration files, and indexes source code for contextual retrieval.'
      }
    ],
    prompt: `You are the Code Analysis Agent.
Inspect AST nodes and import hierarchy surrounding the offending line. Return structured functions, classes, and scopes.`,
    stateIO: {
      reads: ['repository_path', 'relevant_files', 'error_file'],
      writes: ['ast_analysis', 'repository_info', 'dependency_info'],
    },
    tags: ['ast module', 'Call Graphs', 'Static Analysis', 'Import Resolver']
  },
  {
    num: '03',
    stage: 'STAGE 3 / KNOWLEDGE RETRIEVAL',
    name: 'Research Agent (RAG)',
    role: 'Dense Vector Knowledge Retrieval & Hypothesis Formulation',
    desc: 'Interfaces with Qdrant vector database and Tavily live documentation search to perform semantic similarity searches over past resolved issues, error patterns, and official library documentation.',
    metrics: [
      { label: 'Vector Index', value: 'Qdrant 384-d' },
      { label: 'Similarity Cutoff', value: '0.82 Cosine' },
      { label: 'Live Docs', value: 'Tavily API' },
    ],
    subcomponents: [
      {
        name: 'DocumentationRetriever',
        desc: 'Queries collections in Qdrant using dense embeddings with automated fallback to in-memory cosine similarity and official docs.'
      },
      {
        name: 'IssueRetriever',
        desc: 'Finds past resolved bug reports and GitHub discussions sharing identical exception patterns.'
      },
      {
        name: 'KnowledgeSynthesizer',
        desc: 'Synthesizes retrieved documentation snippets into actionable root-cause hypotheses.'
      }
    ],
    prompt: `You are the Knowledge Synthesizer Agent.
Given retrieved documentation and similar issues, formulate 1-3 ranked hypotheses explaining the root cause.`,
    stateIO: {
      reads: ['problem', 'error_message', 'bug_type'],
      writes: ['hypotheses', 'retrieved_context', 'root_cause'],
    },
    tags: ['Dense Embeddings', 'Qdrant Store', 'Tavily Docs', 'Hypothesis Engine']
  },
  {
    num: '04',
    stage: 'STAGE 4 / PATCH SYNTHESIS',
    name: 'Fix Synthesis Agent',
    role: 'Adversarial Patch Generation & Localized Refactoring',
    desc: 'Generates minimal, surgical code patches formatted as unified diffs. Operates in an adversarial loop with an independent Patch Reviewer to reject incomplete or speculative code changes.',
    metrics: [
      { label: 'Diff Precision', value: '1-5 Lines Minimal' },
      { label: 'Review Gate', value: 'Adversarial Reviewer' },
      { label: 'Format', value: 'Standard Unified Diff' },
    ],
    subcomponents: [
      {
        name: 'PatchGenerator',
        desc: 'Constructs the minimal code change that resolves the root cause while preserving existing contracts.'
      },
      {
        name: 'PatchReviewer',
        desc: 'Independent adversarial gate that critiques the patch for regression hazards, broad exception suppressing, or missing imports.'
      },
      {
        name: 'RefactoringAgent',
        desc: 'Performs small, localized structural cleanup only when strictly required for maintainability.'
      }
    ],
    prompt: `You are the Patch Generation Agent in Bugify.
Generate ONLY the minimal unified diff or NO_PATCH. Do not suppress errors or alter unrelated interfaces.`,
    stateIO: {
      reads: ['root_cause', 'code_context', 'relevant_files', 'retrieved_context'],
      writes: ['proposed_patches', 'patch_summary', 'patch_review'],
    },
    tags: ['Unified Diff', 'Adversarial Gate', 'AST Hotfix', 'Minimal Mutations']
  },
  {
    num: '05',
    stage: 'STAGE 5 / SECURITY & VULNERABILITY',
    name: 'Security Audit Agent',
    role: 'OWASP Top 10 & CWE Exploit Scanner',
    desc: 'Acts as an adversarial security scanner for both the root cause defect and the proposed fix. Ensures fixes do not introduce OWASP Top 10 vulnerabilities like SQLi, Command Injection, or Insecure Deserialization.',
    metrics: [
      { label: 'OWASP Rules', value: 'CWE-78, 89, 95, 502' },
      { label: 'Safety Metric', value: '0-100 Radial Score' },
      { label: 'Scan Engine', value: 'Static CWE + Semantic' },
    ],
    subcomponents: [
      {
        name: 'InjectionScanner',
        desc: 'Detects OS command injection (shell=True, os.system), SQL query concatenation, and dynamic eval/exec.'
      },
      {
        name: 'DeserializationGuard',
        desc: 'Audits pickle.loads, yaml.load without SafeLoader, and untrusted object hydration.'
      },
      {
        name: 'SecretLeakFilter',
        desc: 'Ensures no API keys, credentials, or confidential headers are exposed in debug patches.'
      }
    ],
    prompt: `You are Bugify's Security Audit Agent.
Analyze the proposed patch for OWASP Top 10 vulnerabilities (CWE-78, CWE-89, CWE-95, CWE-502). Return safety score and risk level.`,
    stateIO: {
      reads: ['problem', 'proposed_patches', 'root_cause'],
      writes: ['security_audit'],
    },
    tags: ['OWASP Top 10', 'CWE Classifier', 'Shell Injection', 'Deserialization']
  },
  {
    num: '06',
    stage: 'STAGE 6 / PERFORMANCE & BIG-O',
    name: 'Performance Profiler Agent',
    role: 'Asymptotic Complexity & Hotspot Analysis',
    desc: 'Performs Big-O time and space complexity shifts on the proposed patch. Detects quadratic nested loops in hot paths, memory leak vectors, unindexed lookups, and unclosed I/O handlers.',
    metrics: [
      { label: 'Complexity Metric', value: 'Big-O Asymptotic' },
      { label: 'Latency Budget', value: '< 0.05ms Overhead' },
      { label: 'Hotspot Detection', value: 'Loop Nesting AST' },
    ],
    subcomponents: [
      {
        name: 'AsymptoticAnalyzer',
        desc: 'Compares algorithmic time complexity Before vs After (e.g. O(N^2) to O(N)).'
      },
      {
        name: 'MemoryFootprintProfiler',
        desc: 'Monitors heap allocations and ensures unbounded list comprehensions are replaced by iterators.'
      },
      {
        name: 'LatencyEstimator',
        desc: 'Calculates expected runtime latency delta on critical request pathways.'
      }
    ],
    prompt: `You are the Performance Profiler Agent.
Evaluate Big-O time and space complexity changes. Flag any quadratic iteration or memory leak risks.`,
    stateIO: {
      reads: ['problem', 'proposed_patches', 'root_cause'],
      writes: ['complexity_analysis'],
    },
    tags: ['Big-O Notation', 'Asymptotic Shifts', 'Hotspot Guard', 'Memory Profiler']
  },
  {
    num: '07',
    stage: 'STAGE 7 / SELF-HEALING REGRESSION',
    name: 'Test Generator Agent',
    role: 'Automated Pytest Suite Synthesis',
    desc: 'Synthesizes an automated, standalone pytest unit test suite specifically crafted to reproduce the defect and assert that the generated patch permanently resolves the failure condition.',
    metrics: [
      { label: 'Framework', value: 'Pytest 8.x' },
      { label: 'Coverage', value: 'Reproduction + Edge Cases' },
      { label: 'Mock Engine', value: 'unittest.mock' },
    ],
    subcomponents: [
      {
        name: 'ReproductionSynthesizer',
        desc: 'Generates a unit test that mirrors the exact input conditions that triggered the traceback.'
      },
      {
        name: 'BoundaryTester',
        desc: 'Tests edge cases such as None values, empty dictionaries, negative numbers, and malformed strings.'
      },
      {
        name: 'FixtureGenerator',
        desc: 'Constructs mock repositories, monkeypatches, and synthetic database cursors for zero-dependency execution.'
      }
    ],
    prompt: `You are the Self-Healing Test Generator Agent.
Synthesize an executable pytest suite with reproduction and boundary assertion tests.`,
    stateIO: {
      reads: ['problem', 'traceback', 'proposed_patches', 'error_file'],
      writes: ['regression_test'],
    },
    tags: ['Pytest Engine', 'Self-Healing', 'Boundary Checks', 'Regression Suite']
  },
  {
    num: '08',
    stage: 'STAGE 8 / ISOLATED SANDBOX',
    name: 'Verification Sandbox Agent',
    role: 'Sandbox Execution & Regression Testing',
    desc: 'The final gate in the autonomous loop. Validates patch syntax and in-memory application, then runs unit tests inside a sterile subprocess or Docker container before greenlighting deployment.',
    metrics: [
      { label: 'Isolation Mode', value: 'Subprocess / Docker' },
      { label: 'Network Access', value: 'Zero-Egress Sterile' },
      { label: 'Syntax Gate', value: 'Python compile() AST' },
    ],
    subcomponents: [
      {
        name: 'RuntimeValidator',
        desc: 'Applies patch in-memory to verify syntactic correctness with Python compile() without modifying disk.'
      },
      {
        name: 'TestExecutor',
        desc: 'Executes pytest against the patched code inside an isolated environment.'
      },
      {
        name: 'RegressionTester',
        desc: 'Compares test suite results against baseline to ensure zero regression failures.'
      }
    ],
    prompt: `You are the Verification Agent.
Verify patch application in memory, check syntax compile errors, and record test execution verdict.`,
    stateIO: {
      reads: ['proposed_patches', 'repository_path', 'relevant_files'],
      writes: ['tests_passed', 'test_output', 'verified_patch', 'syntax_error'],
    },
    tags: ['Docker Isolation', 'Pytest Runner', 'Zero-Egress', 'Zero Regressions']
  },
];

export default function AgentsPage() {
  const [activeTabs, setActiveTabs] = useState({});

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
            Specialized Autonomous Swarm Architecture
          </div>
          <h1 className={styles.title}>
            The 8 Autonomous Agents.<br />
            <span className={styles.titleItalic}>Engineered for absolute precision</span>
          </h1>
          <p className={styles.subtitle}>
            Bugify is not a simple single-prompt chatbot. It is a synchronized network of eight specialized AI agents,
            each engineered with deterministic AST parsers, OWASP security scanners, Big-O profilers, self-healing test generators, and isolated sandboxes.
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

                  <div style={{ marginTop: 14 }}>
                    <Link href="/debug" className="btn btn-primary" style={{ padding: '8px 22px', fontSize: '0.8rem', display: 'inline-flex', alignItems: 'center', gap: 6 }}>
                      <span>Launch Agent {agent.num} in Console</span>
                      <span>→</span>
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
                      Sub-Components
                    </button>
                    <button
                      type="button"
                      className={`${styles.tabBtn} ${currentTab === 'prompt' ? styles.tabBtnActive : ''}`}
                      onClick={() => handleTabChange(agent.num, 'prompt')}
                    >
                      System Directive
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
                      <pre className="code-block" style={{ fontSize: '0.76rem', color: '#fbbf24', maxHeight: 220, overflowY: 'auto' }}>
                        {agent.prompt}
                      </pre>
                    </div>
                  )}

                  {currentTab === 'state' && (
                    <div className={styles.tabContent} style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                      <div className="card" style={{ padding: '12px 16px' }}>
                        <div style={{ fontSize: '0.7rem', color: '#737373', textTransform: 'uppercase', marginBottom: 6, fontWeight: 700 }}>
                          Reads from BugifyState:
                        </div>
                        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                          {agent.stateIO.reads.map((r) => (
                            <span key={r} className="tag mono" style={{ color: '#38bdf8' }}>{r}</span>
                          ))}
                        </div>
                      </div>

                      <div className="card" style={{ padding: '12px 16px' }}>
                        <div style={{ fontSize: '0.7rem', color: '#737373', textTransform: 'uppercase', marginBottom: 6, fontWeight: 700 }}>
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
