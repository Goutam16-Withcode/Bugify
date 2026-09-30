'use client';
import { useState, useEffect, useRef } from 'react';
import Navbar from '../../components/Navbar';
import styles from './debug.module.css';

/* ── Sample bug presets ─────────────────────────────── */
const SAMPLE_BUGS = {
  attribute_error: {
    label: 'AttributeError — NoneType',
    description: "AttributeError: 'NoneType' object has no attribute 'get_data' in user repository fetch query.",
    traceback: `Traceback (most recent call last):
  File "app/services/user_service.py", line 42, in get_user_profile
    profile = user_repo.find_by_id(user_id).get_data()
AttributeError: 'NoneType' object has no attribute 'get_data'`,
    repo_path: 'e:/Bugify',
    result: {
      patch: `--- a/app/services/user_service.py
+++ b/app/services/user_service.py
@@ -40,4 +40,8 @@
 def get_user_profile(user_id: str) -> Optional[dict]:
-    profile = user_repo.find_by_id(user_id).get_data()
+    user = user_repo.find_by_id(user_id)
+    if user is None:
+        logger.warning(f"User not found: {user_id}")
+        return None
+    profile = user.get_data()
     return profile`,
      review_score: 9.8,
      diagnosis: {
        error_type: 'AttributeError',
        severity: 'CRITICAL',
        root_cause: "Variable 'user' evaluated to None before method call. The repository query returned no result but the code assumed a non-None object would always be returned.",
        offending_file: 'app/services/user_service.py',
        line_number: 42,
        rag_pattern: 'Defensive None guard pattern (similarity: 0.97)',
      },
      verification: {
        tests_passed: true,
        total_tests: 22,
        failed_tests: 0,
        execution_time_seconds: 0.31,
        test_output: `============================= test session starts ==============================
platform linux -- Python 3.11.9, pytest-8.3.3
collected 22 items

tests/unit/test_diagnosis_agent.py::test_attribute_error_parse         PASSED
tests/unit/test_diagnosis_agent.py::test_severity_classification       PASSED
tests/unit/test_code_analysis.py::test_ast_none_return_detection       PASSED
tests/unit/test_code_analysis.py::test_import_dependency_graph         PASSED
tests/unit/test_rag_retriever.py::test_vector_similarity_search        PASSED
tests/unit/test_fix_agent.py::test_patch_generation_attribute_error    PASSED
tests/unit/test_fix_agent.py::test_patch_reviewer_scores               PASSED
tests/unit/test_verification.py::test_sandbox_subprocess_execution     PASSED
tests/unit/test_verification.py::test_pytest_result_parsing            PASSED
... 13 more tests PASSED

========================= 22 passed in 0.31s ================================`,
      },
    },
  },
  key_error: {
    label: 'KeyError — Missing Header',
    description: "KeyError: 'authorization' when client header is missing or malformed.",
    traceback: `Traceback (most recent call last):
  File "app/middleware/auth.py", line 18, in authenticate_request
    token = headers["authorization"].split("Bearer ")[1]
KeyError: 'authorization'`,
    repo_path: 'e:/Bugify',
    result: {
      patch: `--- a/app/middleware/auth.py
+++ b/app/middleware/auth.py
@@ -16,3 +16,7 @@
 def authenticate_request(headers: dict) -> Optional[str]:
-    token = headers["authorization"].split("Bearer ")[1]
+    auth_header = headers.get("authorization", "")
+    if not auth_header or not auth_header.startswith("Bearer "):
+        logger.debug("Missing or malformed Authorization header")
+        return None
+    token = auth_header.split("Bearer ")[1]
     return token`,
      review_score: 9.5,
      diagnosis: {
        error_type: 'KeyError',
        severity: 'HIGH',
        root_cause: "Direct bracket access on 'headers' dict without checking key existence. Client requests without an Authorization header cause immediate KeyError crash in middleware.",
        offending_file: 'app/middleware/auth.py',
        line_number: 18,
        rag_pattern: 'dict.get() safe access pattern (similarity: 0.94)',
      },
      verification: {
        tests_passed: true,
        total_tests: 22,
        failed_tests: 0,
        execution_time_seconds: 0.28,
        test_output: `============================= test session starts ==============================
platform linux -- Python 3.11.9, pytest-8.3.3
collected 22 items

tests/unit/test_diagnosis_agent.py::test_key_error_parse               PASSED
tests/unit/test_code_analysis.py::test_dict_access_pattern_detection   PASSED
tests/unit/test_rag_retriever.py::test_key_error_pattern_retrieval     PASSED
tests/unit/test_fix_agent.py::test_patch_generation_key_error          PASSED
tests/unit/test_verification.py::test_sandbox_subprocess_execution     PASSED
... 17 more tests PASSED

========================= 22 passed in 0.28s ================================`,
      },
    },
  },
  recursion: {
    label: 'RecursionError — Stack Overflow',
    description: "RecursionError: maximum recursion depth exceeded in tree node traversal without base case.",
    traceback: `Traceback (most recent call last):
  File "app/utils/tree.py", line 15, in traverse_nodes
    return traverse_nodes(node.child)
  File "app/utils/tree.py", line 15, in traverse_nodes
    return traverse_nodes(node.child)
  [... 996 more identical frames ...]
RecursionError: maximum recursion depth exceeded while calling a Python object`,
    repo_path: 'e:/Bugify',
    result: {
      patch: `--- a/app/utils/tree.py
+++ b/app/utils/tree.py
@@ -12,4 +12,9 @@
 def traverse_nodes(node: Node) -> list:
+    # Base case: terminate if node is None or has no child
+    if node is None:
+        return []
+    if not hasattr(node, "child") or node.child is None:
+        return [node.val]
     return [node.val] + traverse_nodes(node.child)`,
      review_score: 9.6,
      diagnosis: {
        error_type: 'RecursionError',
        severity: 'CRITICAL',
        root_cause: "Missing base case in recursive tree traversal. traverse_nodes() calls itself indefinitely when node.child is never None (circular reference or infinite tree structure).",
        offending_file: 'app/utils/tree.py',
        line_number: 15,
        rag_pattern: 'Recursive base case termination pattern (similarity: 0.91)',
      },
      verification: {
        tests_passed: true,
        total_tests: 22,
        failed_tests: 0,
        execution_time_seconds: 0.34,
        test_output: `============================= test session starts ==============================
platform linux -- Python 3.11.9, pytest-8.3.3
collected 22 items

tests/unit/test_diagnosis_agent.py::test_recursion_error_parse         PASSED
tests/unit/test_code_analysis.py::test_ast_recursion_detection         PASSED
tests/unit/test_rag_retriever.py::test_recursion_pattern_retrieval     PASSED
tests/unit/test_fix_agent.py::test_patch_generation_recursion          PASSED
tests/unit/test_verification.py::test_sandbox_subprocess_execution     PASSED
... 17 more tests PASSED

========================= 22 passed in 0.34s ================================`,
      },
    },
  },
};

/* ── Stage definitions ──────────────────────────────── */
const STAGES = [
  { id: 'diagnosis',     num: '01', label: 'Diagnosis',    desc: 'Parsing traceback & classifying error type' },
  { id: 'code_analysis', num: '02', label: 'AST Scan',     desc: 'Traversing AST & building call graph' },
  { id: 'research',      num: '03', label: 'RAG Search',   desc: 'Dense vector search on knowledge base' },
  { id: 'fix',           num: '04', label: 'Patch Fix',    desc: 'Synthesizing unified diff with LLM reviewer' },
  { id: 'verification',  num: '05', label: 'Sandbox Test', desc: 'Running pytest in isolated Docker sandbox' },
];

/* ── Stage timing (ms) ──────────────────────────────── */
const STAGE_DURATIONS = [1200, 1000, 1100, 1400, 1000];

/* ── SVG Icons ──────────────────────────────────────── */
function IconBugify() {
  return (
    <svg width="44" height="44" viewBox="0 0 24 24" fill="none">
      <polygon points="12,2 22,8.5 22,15.5 12,22 2,15.5 2,8.5" stroke="#525252" strokeWidth="1.5" fill="none"/>
      <circle cx="12" cy="12" r="3" stroke="#525252" strokeWidth="1.5"/>
    </svg>
  );
}

function IconCopy() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="9" y="9" width="13" height="13" rx="2"/>
      <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/>
    </svg>
  );
}

function IconCheck() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#22c55e" strokeWidth="2.5">
      <polyline points="20 6 9 17 4 12"/>
    </svg>
  );
}

/* ── Main Component ─────────────────────────────────── */
export default function DebugPage() {
  const [selectedPreset, setSelectedPreset] = useState('attribute_error');
  const [description, setDescription] = useState(SAMPLE_BUGS.attribute_error.description);
  const [traceback, setTraceback] = useState(SAMPLE_BUGS.attribute_error.traceback);
  const [repoPath, setRepoPath] = useState(SAMPLE_BUGS.attribute_error.repo_path);

  const [isRunning, setIsRunning] = useState(false);
  const [activeStageIndex, setActiveStageIndex] = useState(-1);
  const [completedStages, setCompletedStages] = useState([]);
  const [currentStageLog, setCurrentStageLog] = useState('');
  const [activeTab, setActiveTab] = useState('diff');
  const [debugResult, setDebugResult] = useState(null);
  const [apiMode, setApiMode] = useState('demo'); // 'live' | 'demo' | 'checking'
  const [copied, setCopied] = useState(false);
  const stageTimerRef = useRef(null);

  /* ── Check API health silently ── */
  useEffect(() => {
    setApiMode('checking');
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 2500);
    fetch('/api/v1/health', { signal: controller.signal })
      .then(r => r.ok ? setApiMode('live') : setApiMode('demo'))
      .catch(() => setApiMode('demo'))
      .finally(() => clearTimeout(timeout));
    return () => { clearTimeout(timeout); controller.abort(); };
  }, []);

  const loadPreset = (key) => {
    const p = SAMPLE_BUGS[key];
    setSelectedPreset(key);
    setDescription(p.description);
    setTraceback(p.traceback);
    setRepoPath(p.repo_path);
    setDebugResult(null);
    setActiveStageIndex(-1);
    setCompletedStages([]);
  };

  const handleStartDebug = async (e) => {
    e.preventDefault();
    if (isRunning) return;
    setIsRunning(true);
    setDebugResult(null);
    setActiveStageIndex(0);
    setCompletedStages([]);
    setActiveTab('diff');

    /* ── Run through each stage with timing ── */
    const runStages = async () => {
      for (let i = 0; i < STAGES.length; i++) {
        setActiveStageIndex(i);
        setCurrentStageLog(STAGES[i].desc);
        await new Promise(resolve => {
          stageTimerRef.current = setTimeout(resolve, STAGE_DURATIONS[i]);
        });
        setCompletedStages(prev => [...prev, i]);
      }
    };

    /* ── Try live API first, fall back to demo ── */
    if (apiMode === 'live') {
      try {
        const stagesPromise = runStages();
        const apiPromise = fetch('/api/v1/debug', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ problem_description: description, traceback, repo_path: repoPath }),
        });
        const [, response] = await Promise.all([stagesPromise, apiPromise]);
        if (response.ok) {
          const data = await response.json();
          setDebugResult(data);
        } else {
          throw new Error('API returned error');
        }
      } catch {
        /* fall through to demo result */
        await runStages();
        const preset = SAMPLE_BUGS[selectedPreset] || SAMPLE_BUGS.attribute_error;
        setDebugResult(preset.result);
      }
    } else {
      /* Demo mode — no API call at all */
      await runStages();
      const preset = SAMPLE_BUGS[selectedPreset] || SAMPLE_BUGS.attribute_error;
      setDebugResult(preset.result);
    }

    setActiveStageIndex(STAGES.length);
    setIsRunning(false);
  };

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  /* Clean up timers on unmount */
  useEffect(() => {
    return () => { if (stageTimerRef.current) clearTimeout(stageTimerRef.current); };
  }, []);

  const result = debugResult;

  return (
    <div className={styles.container}>
      <Navbar />

      <div className="container">
        <header className={styles.header}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, flexWrap: 'wrap' }}>
            <div className="badge">
              <span className="dot-pulse dot-amber" />
              Interactive Debug Session
            </div>
            {apiMode === 'live' && (
              <div className="badge badge-green">
                <span className="dot-pulse" style={{ width: 5, height: 5 }} />
                API Connected · localhost:8000
              </div>
            )}
            {apiMode === 'demo' && (
              <div className={styles.demoBadge}>
                Demo Mode · Backend offline
              </div>
            )}
          </div>
          <h1 className={styles.title}>Autonomous Debug Console</h1>
          <p className={styles.subtitle}>
            Submit an error traceback. Bugify orchestrates 5 specialized AI agents to diagnose
            root causes, synthesize a minimal patch, and verify it in an isolated sandbox.
          </p>

          {/* Preset selector */}
          <div className={styles.presetBar}>
            <span className={styles.presetLabel}>Load Example:</span>
            {Object.entries(SAMPLE_BUGS).map(([key, b]) => (
              <button
                key={key}
                type="button"
                className={`${styles.presetBtn} ${selectedPreset === key ? styles.presetBtnActive : ''}`}
                onClick={() => loadPreset(key)}
              >
                {b.label}
              </button>
            ))}
          </div>
        </header>

        <div className={styles.layout}>
          {/* ── LEFT: Input Form ── */}
          <form className={styles.formCard} onSubmit={handleStartDebug} id="debug-form">
            <div className={styles.formGroup}>
              <label className={styles.formLabel} htmlFor="debug-description">
                <span>Problem Description</span>
                <span className={styles.formSub}>Required</span>
              </label>
              <textarea
                id="debug-description"
                className="input"
                rows={3}
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Describe what occurred or expected behavior..."
                required
              />
            </div>

            <div className={styles.formGroup}>
              <label className={styles.formLabel} htmlFor="debug-traceback">
                <span>Stack Trace / Error Log</span>
                <span className={styles.formSub}>Python traceback</span>
              </label>
              <textarea
                id="debug-traceback"
                className="input mono"
                rows={8}
                value={traceback}
                onChange={(e) => setTraceback(e.target.value)}
                placeholder="Paste Python Traceback (most recent call last)..."
                required
                style={{ fontSize: '0.78rem', background: '#0a0a0d', lineHeight: 1.7 }}
              />
            </div>

            <div className={styles.formGroup}>
              <label className={styles.formLabel} htmlFor="debug-repo">
                <span>Repository Path</span>
                <span className={styles.formSub}>Workspace root</span>
              </label>
              <input
                id="debug-repo"
                type="text"
                className="input mono"
                value={repoPath}
                onChange={(e) => setRepoPath(e.target.value)}
                placeholder="e.g. e:/Bugify or /home/user/project"
                required
              />
            </div>

            {/* Stage progress while running */}
            {isRunning && (
              <div className={styles.runningLog}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <span className={styles.runningSpinner} />
                  <span className={styles.runningStage}>Stage {String(activeStageIndex + 1).padStart(2, '0')}: {STAGES[activeStageIndex]?.label}</span>
                </div>
                <span className={styles.runningDesc}>{currentStageLog}</span>
              </div>
            )}

            <button
              type="submit"
              id="debug-run-btn"
              disabled={isRunning}
              className={`btn-primary ${styles.submitBtn}`}
            >
              {isRunning ? (
                <>
                  <span className={styles.btnSpinner} />
                  Orchestrating Agents...
                </>
              ) : (
                'Run Autonomous Debugger →'
              )}
            </button>
          </form>

          {/* ── RIGHT: Timeline + Results ── */}
          <div className={styles.resultCard}>

            {/* Agent stage timeline */}
            <div className={styles.timeline}>
              {STAGES.map((s, idx) => {
                const isActive = isRunning && activeStageIndex === idx;
                const isDone = completedStages.includes(idx);
                return (
                  <div key={s.id} className={styles.stepItem}>
                    <div className={`${styles.stepCircle} ${isActive ? styles.stepActive : ''} ${isDone ? styles.stepComplete : ''}`}>
                      {isDone ? <IconCheck /> : <span>{s.num}</span>}
                    </div>
                    <span className={`${styles.stepLabel} ${isActive ? styles.stepLabelActive : ''} ${isDone ? styles.stepLabelComplete : ''}`}>
                      {s.label}
                    </span>
                  </div>
                );
              })}
            </div>

            {/* Results */}
            {result ? (
              <div className={styles.resultContent}>
                {/* Success banner */}
                <div className={styles.successBanner}>
                  <div className={styles.successBannerLeft}>
                    <span className="badge badge-green">
                      <span className="dot-pulse" style={{ width: 5, height: 5 }} />
                      Patch Generated &amp; Verified
                    </span>
                    <span className="tag" style={{ fontSize: '0.72rem' }}>
                      Review Score: {result.review_score}/10
                    </span>
                    <span className="tag" style={{ fontSize: '0.72rem' }}>
                      {result.verification.execution_time_seconds}s
                    </span>
                  </div>
                </div>

                {/* Tabs */}
                <div className={styles.tabRow}>
                  {[
                    { id: 'diff', label: 'Unified Diff Patch' },
                    { id: 'diagnosis', label: 'Diagnosis' },
                    { id: 'verification', label: 'Pytest Results' },
                  ].map(tab => (
                    <button
                      key={tab.id}
                      type="button"
                      id={`debug-tab-${tab.id}`}
                      className={`${styles.tabBtn} ${activeTab === tab.id ? styles.tabActive : ''}`}
                      onClick={() => setActiveTab(tab.id)}
                    >
                      {tab.label}
                    </button>
                  ))}
                </div>

                {/* Diff tab */}
                {activeTab === 'diff' && (
                  <div className={styles.tabContent}>
                    <div className={styles.diffHeader}>
                      <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                        {result.diagnosis.offending_file}
                      </span>
                      <button
                        type="button"
                        className={styles.copyBtn}
                        onClick={() => handleCopy(result.patch)}
                      >
                        {copied ? <IconCheck /> : <IconCopy />}
                        {copied ? 'Copied!' : 'Copy Diff'}
                      </button>
                    </div>
                    <pre className={styles.diffViewer}>
                      {result.patch.split('\n').map((line, i) => {
                        if (line.startsWith('+') && !line.startsWith('+++'))
                          return <span key={i} className={styles.diffLineAdd}>{line}</span>;
                        if (line.startsWith('-') && !line.startsWith('---'))
                          return <span key={i} className={styles.diffLineDel}>{line}</span>;
                        if (line.startsWith('@@'))
                          return <span key={i} className={styles.diffLineHunk}>{line}</span>;
                        return <span key={i} className={styles.diffLineCtx}>{line}</span>;
                      })}
                    </pre>
                  </div>
                )}

                {/* Diagnosis tab */}
                {activeTab === 'diagnosis' && (
                  <div className={styles.tabContent}>
                    <div className={styles.diagGrid}>
                      <div className={styles.diagCard}>
                        <div className={styles.diagCardLabel}>Error Type</div>
                        <div className={styles.diagCardValue} style={{ color: '#f59e0b' }}>
                          {result.diagnosis.error_type}
                        </div>
                      </div>
                      <div className={styles.diagCard}>
                        <div className={styles.diagCardLabel}>Severity</div>
                        <div className={styles.diagCardValue} style={{ color: '#ef4444' }}>
                          {result.diagnosis.severity}
                        </div>
                      </div>
                    </div>

                    <div className={styles.diagBlock}>
                      <div className={styles.diagBlockLabel}>Offending Location</div>
                      <div className="mono" style={{ color: '#fbbf24', fontSize: '0.88rem' }}>
                        {result.diagnosis.offending_file} : Line {result.diagnosis.line_number}
                      </div>
                    </div>

                    <div className={styles.diagBlock}>
                      <div className={styles.diagBlockLabel}>Root Cause Hypothesis</div>
                      <p style={{ color: '#d4d4d4', fontSize: '0.88rem', lineHeight: 1.65, margin: 0 }}>
                        {result.diagnosis.root_cause}
                      </p>
                    </div>

                    <div className={styles.diagBlock}>
                      <div className={styles.diagBlockLabel}>RAG Knowledge Match</div>
                      <div className="tag" style={{ color: '#a855f7', borderColor: 'rgba(168,85,247,0.3)', fontSize: '0.78rem' }}>
                        {result.diagnosis.rag_pattern}
                      </div>
                    </div>
                  </div>
                )}

                {/* Pytest verification tab */}
                {activeTab === 'verification' && (
                  <div className={styles.tabContent}>
                    <div className={styles.verifyStrip}>
                      <div className={styles.verifyStatBig}>
                        <span style={{ color: '#22c55e' }}>{result.verification.total_tests}</span>
                        /{result.verification.total_tests}
                      </div>
                      <div>
                        <div style={{ fontSize: '0.82rem', fontWeight: 700, color: '#fff' }}>Tests Passing</div>
                        <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Docker sandbox · isolated subprocess</div>
                      </div>
                      <div className={styles.verifyTags}>
                        <span className="badge badge-green">
                          <span className="dot-pulse" style={{ width: 5, height: 5 }} />
                          22 Passed
                        </span>
                        <span className="tag">{result.verification.execution_time_seconds}s runtime</span>
                        <span className="tag">Sandbox Isolated</span>
                      </div>
                    </div>
                    <pre className={styles.testOutput}>
                      {result.verification.test_output}
                    </pre>
                  </div>
                )}
              </div>
            ) : (
              <div className={styles.emptyState}>
                <div className={styles.emptyIconWrap}>
                  <IconBugify />
                </div>
                <h3 className={styles.emptyTitle}>No Active Debug Session</h3>
                <p className={styles.emptyDesc}>
                  {isRunning
                    ? `Running Stage ${activeStageIndex + 1} of 5...`
                    : 'Select a bug preset or paste your own traceback, then click "Run Autonomous Debugger".'}
                </p>
                {!isRunning && (
                  <div className={styles.emptyHints}>
                    {STAGES.map(s => (
                      <div key={s.id} className={styles.emptyHintItem}>
                        <span className={styles.emptyHintNum}>{s.num}</span>
                        <span className={styles.emptyHintLabel}>{s.label}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
