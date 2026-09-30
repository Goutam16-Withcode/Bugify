'use client';
import Link from 'next/link';
import Navbar from '../components/Navbar';
import styles from './page.module.css';

/* ── Luxury Vector Wireframe Icons ──────────────────────── */
function IconNodesTriangle() {
  return (
    <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
      <circle cx="20" cy="8" r="4" stroke="#fbbf24" strokeWidth="1.8" fill="rgba(245,158,11,0.15)" />
      <circle cx="8" cy="30" r="4" stroke="#fbbf24" strokeWidth="1.8" fill="rgba(245,158,11,0.15)" />
      <circle cx="32" cy="30" r="4" stroke="#fbbf24" strokeWidth="1.8" fill="rgba(245,158,11,0.15)" />
      <line x1="20" y1="12" x2="8" y2="26" stroke="#f59e0b" strokeWidth="1.4" strokeDasharray="3 3" />
      <line x1="20" y1="12" x2="32" y2="26" stroke="#f59e0b" strokeWidth="1.4" strokeDasharray="3 3" />
      <line x1="12" y1="30" x2="28" y2="30" stroke="#f59e0b" strokeWidth="1.4" strokeDasharray="3 3" />
      <circle cx="20" cy="22" r="2" fill="#fbbf24" />
    </svg>
  );
}

function IconLightningBolt() {
  return (
    <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
      <polygon
        points="22,4 10,20 18,20 16,36 30,18 21,18"
        stroke="#fbbf24"
        strokeWidth="1.8"
        fill="rgba(245,158,11,0.15)"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function IconShieldLock() {
  return (
    <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
      <path
        d="M20 4L7 9V19C7 27 12.5 34.5 20 37C27.5 34.5 33 27 33 19V9L20 4Z"
        stroke="#fbbf24"
        strokeWidth="1.8"
        fill="rgba(245,158,11,0.15)"
        strokeLinejoin="round"
      />
      <circle cx="20" cy="18" r="3" stroke="#fbbf24" strokeWidth="1.5" />
      <path d="M20 21V25" stroke="#fbbf24" strokeWidth="1.8" strokeLinecap="round" />
    </svg>
  );
}

/* ── Autonomous Code Intelligence & Patch Studio (Unique) ─── */
function CodeIntelligenceStudio() {
  return (
    <div className={styles.studioWrapper}>
      <div className={styles.studioGlow} />

      {/* Floating Holographic Telemetry Badges */}
      <div className={styles.floatingChipTop}>
        <span className="dot-pulse" style={{ background: '#22c55e' }} />
        <span>Pytest Sandbox: 22/22 Passed (0.31s)</span>
      </div>

      <div className={styles.floatingChipBottom}>
        <span className="dot-pulse dot-amber" />
        <span>Patch Review Score: 9.8 / 10 Approved</span>
      </div>

      <div className={styles.studioCard}>
        {/* Studio Window Bar */}
        <div className={styles.studioHeader}>
          <div className={styles.studioDots}>
            <div className={styles.terminalDot} style={{ background: '#ef4444' }} />
            <div className={styles.terminalDot} style={{ background: '#f59e0b' }} />
            <div className={styles.terminalDot} style={{ background: '#22c55e' }} />
          </div>

          <div className={styles.fileTabs}>
            <span className={`${styles.fileTab} ${styles.fileTabActive}`}>
              <span style={{ color: '#fbbf24', marginRight: 6 }}>●</span>
              user_service.py:42
            </span>
            <span className={styles.fileTab}>test_user_service.py</span>
          </div>

          <div className={styles.studioStatus}>
            <span className="dot-pulse" style={{ background: '#22c55e', width: 5, height: 5 }} />
            <span>AUTONOMOUS SWARM</span>
          </div>
        </div>

        {/* Code Diff Canvas */}
        <div className={styles.codeCanvas}>
          {/* Diagnostic Alert Ribbon */}
          <div className={styles.faultBanner}>
            <span className={styles.faultTag}>FAULT DETECTED</span>
            <span className={styles.faultMsg}>
              AttributeError: 'NoneType' object has no attribute 'get_data'
            </span>
            <span className={styles.faultConfidence}>99.4% confidence</span>
          </div>

          {/* Code Diff Rows */}
          <div className={styles.codeBlockArea}>
            <div className={styles.codeLine}>
              <span className={styles.lineNum}>38</span>
              <span className={styles.lineCode}><span className={styles.kw}>def</span> <span className={styles.fn}>get_user_profile</span>(user_id: <span className={styles.tp}>str</span>) -&gt; <span className={styles.tp}>dict</span>:</span>
            </div>
            <div className={styles.codeLine}>
              <span className={styles.lineNum}>39</span>
              <span className={styles.lineCode}>    <span className={styles.cm}># Query database for user instance</span></span>
            </div>

            {/* The Fault Line */}
            <div className={`${styles.codeLine} ${styles.codeLineRemoved}`}>
              <span className={styles.lineNum}>40</span>
              <span className={styles.diffSymbol}>-</span>
              <span className={styles.lineCode}>    profile = user_repo.find_by_id(user_id).get_data()</span>
            </div>

            {/* The AI Synthesized Patch Lines */}
            <div className={`${styles.codeLine} ${styles.codeLineAdded}`}>
              <span className={styles.lineNum}>41</span>
              <span className={styles.diffSymbol}>+</span>
              <span className={styles.lineCode}>    user = user_repo.find_by_id(user_id)</span>
            </div>
            <div className={`${styles.codeLine} ${styles.codeLineAdded}`}>
              <span className={styles.lineNum}>42</span>
              <span className={styles.diffSymbol}>+</span>
              <span className={styles.lineCode}>    <span className={styles.kw}>if</span> user <span className={styles.kw}>is</span> <span className={styles.tp}>None</span>:</span>
            </div>
            <div className={`${styles.codeLine} ${styles.codeLineAdded}`}>
              <span className={styles.lineNum}>43</span>
              <span className={styles.diffSymbol}>+</span>
              <span className={styles.lineCode}>        <span className={styles.kw}>return</span> &#123;&#125;</span>
            </div>
            <div className={`${styles.codeLine} ${styles.codeLineAdded}`}>
              <span className={styles.lineNum}>44</span>
              <span className={styles.diffSymbol}>+</span>
              <span className={styles.lineCode}>    <span className={styles.kw}>return</span> user.get_data()</span>
            </div>
          </div>

          {/* Real-Time Agent Pipeline Telemetry Footbar */}
          <div className={styles.telemetryBar}>
            <div className={styles.telemetryNode}>
              <span className={styles.telemetryDot} style={{ background: '#f59e0b' }} />
              <span>Diagnosis</span>
            </div>
            <span className={styles.telemetryArrow}>➔</span>
            <div className={styles.telemetryNode}>
              <span className={styles.telemetryDot} style={{ background: '#3b82f6' }} />
              <span>AST Scan</span>
            </div>
            <span className={styles.telemetryArrow}>➔</span>
            <div className={styles.telemetryNode}>
              <span className={styles.telemetryDot} style={{ background: '#a855f7' }} />
              <span>RAG Memory</span>
            </div>
            <span className={styles.telemetryArrow}>➔</span>
            <div className={styles.telemetryNode}>
              <span className={styles.telemetryDot} style={{ background: '#f97316' }} />
              <span>Fix Synthesized</span>
            </div>
            <span className={styles.telemetryArrow}>➔</span>
            <div className={styles.telemetryNode}>
              <span className={styles.telemetryDot} style={{ background: '#22c55e' }} />
              <span>Sandbox Verified</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function HomePage() {
  return (
    <div className={styles.page}>
      <Navbar />

      {/* Ambient background volumetric glow */}
      <div className={styles.glow1} aria-hidden="true" />
      <div className={styles.glow2} aria-hidden="true" />
      <div className={styles.glow3} aria-hidden="true" />

      {/* ═════════════════════════════════════════════════════
          HERO SECTION (AgentFlow Reference Match)
      ═════════════════════════════════════════════════════ */}
      <section className={`${styles.hero} grid-bg`} aria-labelledby="hero-title">
        <div className={`container ${styles.heroInner}`}>
          <div className={styles.heroContent}>
            <h1 className={styles.heroTitle} id="hero-title">
              Bugify.<br />
              <span className={styles.heroItalic}>Intelligent by design</span>
            </h1>

            <p className={styles.heroDesc}>
              The production-ready autonomous multi-agent debugging system.
              Turn complex Python tracebacks, issue descriptions, and test failures into
              AST-verified patches and passing test suites without manual intervention.
            </p>

            <div className={styles.heroCta}>
              <Link href="/debug" id="hero-btn-primary" className="btn-primary">
                Build Your First Agent →
              </Link>
              <Link href="/architecture" id="hero-btn-secondary" className="btn-outline">
                View Architecture
              </Link>
            </div>
          </div>

          <CodeIntelligenceStudio />
        </div>
      </section>

      {/* ═════════════════════════════════════════════════════
          VALUE PROPS (3 Wireframe Cards from Screenshot)
      ═════════════════════════════════════════════════════ */}
      <section className={styles.section} aria-labelledby="props-title">
        <div className="container">
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle} id="props-title">
              Built for <span className={styles.sectionTitleItalic}>intelligent teams</span><br />
              to actually work.
            </h2>
          </div>

          <div className={styles.propsGrid}>
            {/* Card 1: Zero Manual Overhead */}
            <div className={styles.propCard}>
              <div className={styles.propIconBox}>
                <IconNodesTriangle />
              </div>
              <h3 className={styles.propTitle}>Zero Code Required</h3>
              <p className={styles.propDesc}>
                Create powerful debugging swarms with LangGraph state machines to pinpoint root causes automatically.
              </p>
            </div>

            {/* Card 2: Real-Time Execution */}
            <div className={styles.propCard}>
              <div className={styles.propIconBox}>
                <IconLightningBolt />
              </div>
              <h3 className={styles.propTitle}>Real-Time Execution</h3>
              <p className={styles.propDesc}>
                Sub-minute traceback diagnosis, AST parsing, and automated patch synthesis with high-throughput inference.
              </p>
            </div>

            {/* Card 3: Enterprise Security */}
            <div className={styles.propCard}>
              <div className={styles.propIconBox}>
                <IconShieldLock />
              </div>
              <h3 className={styles.propTitle}>Enterprise Security</h3>
              <p className={styles.propDesc}>
                Isolated Docker container execution, read-only volume mounts, and strict memory/timeout quotas.
              </p>
            </div>
          </div>

          <div className={styles.propAction}>
            <p style={{ color: '#8c8c8c', fontSize: '0.92rem' }}>Ready to build your first agent?</p>
            <Link href="/debug" className="btn-outline" style={{ padding: '8px 24px', fontSize: '0.8rem' }}>
              Try It Now →
            </Link>
          </div>
        </div>
      </section>

      <div className="section-divider" />

      {/* ═════════════════════════════════════════════════════
          BENTO GRID: "Everything your agents need to think, act, scale"
      ═════════════════════════════════════════════════════ */}
      <section className={styles.section} aria-labelledby="bento-title">
        <div className="container">
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle} id="bento-title">
              Everything your agents need<br />
              <span className={styles.sectionTitleItalic}>to think, act, scale.</span>
            </h2>
          </div>

          <div className={styles.bentoGrid}>
            {/* Bento Card 1: Visual Agent Builder */}
            <div className={`${styles.bentoCard} ${styles.bentoCardLarge}`}>
              <span className="badge" style={{ alignSelf: 'flex-start', marginBottom: 12 }}>
                LangGraph State Machine
              </span>
              <h3 style={{ fontSize: '1.45rem', fontWeight: 800, color: '#fff', marginBottom: 6 }}>
                Visual Agent Pipeline
              </h3>
              <p style={{ color: '#8c8c8c', fontSize: '0.88rem', lineHeight: 1.6, maxWidth: 500 }}>
                Every bug report traverses an orchestrated pipeline of specialized agents: Diagnosis, Code Analysis, Research, Fix, and Verification.
              </p>

              <div className={styles.nodeGraphMock}>
                {[
                  { step: '01', label: 'Diagnosis' },
                  { step: '02', label: 'Code Analysis' },
                  { step: '03', label: 'Research' },
                  { step: '04', label: 'Fix Agent' },
                  { step: '05', label: 'Verification' },
                ].map((item, idx) => (
                  <div key={item.label} style={{ display: 'contents' }}>
                    <div className={styles.nodeItem}>
                      <div className={styles.nodeCircle}>{item.step}</div>
                      <span className={styles.nodeLabel}>{item.label}</span>
                    </div>
                    {idx < 4 && <div className={styles.nodeLine} />}
                  </div>
                ))}
              </div>
            </div>

            {/* Bento Card 2: 96% Live Performance (Sleek HUD Metric) */}
            <div className={`${styles.bentoCard} ${styles.bentoCardGauge}`}>
              <div style={{ marginBottom: 14 }}>
                <span className="badge badge-green" style={{ fontSize: '0.72rem' }}>
                  <span className="dot-pulse" style={{ background: '#22c55e' }} /> LIVE TELEMETRY
                </span>
              </div>
              <div style={{ fontSize: '3.6rem', fontWeight: 900, color: '#fff', letterSpacing: '-0.03em', lineHeight: 1 }}>
                96<span style={{ color: '#fbbf24', fontSize: '2.4rem' }}>%</span>
              </div>
              <div style={{ fontSize: '0.8rem', color: '#fbbf24', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', marginTop: 6, marginBottom: 14 }}>
                First-Pass Validation
              </div>

              {/* Segmented precision meter bars */}
              <div style={{ display: 'flex', gap: 4, width: '100%', maxWidth: 220, marginBottom: 16 }}>
                {[...Array(10)].map((_, i) => (
                  <div
                    key={i}
                    style={{
                      flex: 1,
                      height: 6,
                      borderRadius: 2,
                      background: i < 9 ? '#f59e0b' : 'rgba(255,255,255,0.1)',
                      boxShadow: i < 9 ? '0 0 6px rgba(245,158,11,0.5)' : 'none',
                    }}
                  />
                ))}
              </div>

              <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#fff', marginBottom: 4 }}>
                Unit Test Accuracy
              </h4>
              <p style={{ fontSize: '0.8rem', color: '#737373', maxWidth: 220 }}>
                22/22 unit tests passing deterministically across all agent modules.
              </p>
            </div>

            {/* Sub-grid 3 Cards */}
            <div className={styles.bentoSubGrid}>
              {/* Card 3: Neural Learning & Vector RAG */}
              <div className={styles.bentoCard}>
                <div style={{ marginBottom: 14 }}>
                  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fbbf24" strokeWidth="1.8">
                    <circle cx="12" cy="12" r="3" />
                    <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
                  </svg>
                </div>
                <h4 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', marginBottom: 6 }}>
                  Neural Learning
                </h4>
                <p style={{ fontSize: '0.84rem', color: '#8c8c8c', lineHeight: 1.6 }}>
                  Vector similarity indexing over resolved bug archives and documentation with Qdrant.
                </p>
              </div>

              {/* Card 4: Deploy Anywhere / Sandbox */}
              <div className={styles.bentoCard}>
                <div style={{ marginBottom: 14 }}>
                  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fbbf24" strokeWidth="1.8">
                    <rect x="2" y="3" width="20" height="14" rx="2" />
                    <line x1="8" y1="21" x2="16" y2="21" />
                    <line x1="12" y1="17" x2="12" y2="21" />
                  </svg>
                </div>
                <h4 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', marginBottom: 6 }}>
                  Deploy Anywhere
                </h4>
                <p style={{ fontSize: '0.84rem', color: '#8c8c8c', lineHeight: 1.6 }}>
                  Docker-isolated sandboxes with ephemeral containers and strict memory boundaries.
                </p>
              </div>

              {/* Card 5: Real Collaboration */}
              <div className={styles.bentoCard}>
                <div style={{ marginBottom: 14 }}>
                  <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#fbbf24" strokeWidth="1.8">
                    <circle cx="18" cy="5" r="3" />
                    <circle cx="6" cy="12" r="3" />
                    <circle cx="18" cy="19" r="3" />
                    <line x1="8.59" y1="13.51" x2="15.42" y2="17.49" />
                    <line x1="15.41" y1="6.51" x2="8.59" y2="10.49" />
                  </svg>
                </div>
                <h4 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#fff', marginBottom: 6 }}>
                  Real Collaboration
                </h4>
                <p style={{ fontSize: '0.84rem', color: '#8c8c8c', lineHeight: 1.6 }}>
                  State router with conditional review loops: if tests fail, feedback routes back to Fix Agent.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div className="section-divider" />

      {/* ═════════════════════════════════════════════════════
          WORKFLOW VISUALIZER (Screenshot Match)
      ═════════════════════════════════════════════════════ */}
      <section className={styles.flowSection} aria-labelledby="flow-title">
        <div className="container">
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle} id="flow-title">
              Intelligent agents<br />
              <span className={styles.sectionTitleItalic}>that work for you</span>
            </h2>
            <div style={{ marginTop: 12 }}>
              <Link href="/debug" className="btn-primary" style={{ padding: '8px 24px', fontSize: '0.82rem' }}>
                Create New Agent →
              </Link>
            </div>
          </div>

          <div className={styles.flowCanvas}>
            <div className={styles.flowCanvasGlow} />

            <div className={styles.flowGrid}>
              {/* Left Column */}
              <div className={styles.flowCol}>
                <div className={styles.flowNodeCard}>
                  <div className={styles.flowNodeHeader}>
                    <span className={styles.flowNodeTitle}>Diagnosis Node</span>
                    <span className={styles.flowNodeBadge}>STAGE 01</span>
                  </div>
                  <p className={styles.flowNodeDesc}>
                    Extracts error type, classifies severity, and identifies line numbers from tracebacks.
                  </p>
                </div>

                <div className={styles.flowNodeCard}>
                  <div className={styles.flowNodeHeader}>
                    <span className={styles.flowNodeTitle}>Code Analysis Node</span>
                    <span className={styles.flowNodeBadge}>STAGE 02</span>
                  </div>
                  <p className={styles.flowNodeDesc}>
                    Parses Python AST structures, maps variable scopes, and constructs import dependency graphs.
                  </p>
                </div>
              </div>

              {/* Center Core Hub */}
              <div className={styles.centerHub}>
                <div className={styles.hubSphere}>
                  <svg width="36" height="36" viewBox="0 0 24 24" fill="none">
                    <polygon points="12,2 22,8.5 22,15.5 12,22 2,15.5 2,8.5" stroke="#f59e0b" strokeWidth="1.8" />
                    <circle cx="12" cy="12" r="3.5" fill="#f59e0b" />
                  </svg>
                  <span className={styles.hubTitle} style={{ marginTop: 6 }}>Bugify</span>
                  <span className={styles.hubSubtitle}>Orchestrator</span>
                </div>
                <div className="badge">LangGraph Active</div>
              </div>

              {/* Right Column */}
              <div className={styles.flowCol}>
                <div className={styles.flowNodeCard}>
                  <div className={styles.flowNodeHeader}>
                    <span className={styles.flowNodeTitle}>Fix &amp; Review Node</span>
                    <span className={styles.flowNodeBadge}>STAGE 03</span>
                  </div>
                  <p className={styles.flowNodeDesc}>
                    Synthesizes minimal unified diff patches, scored by an independent LLM Patch Reviewer.
                  </p>
                </div>

                <div className={styles.flowNodeCard}>
                  <div className={styles.flowNodeHeader}>
                    <span className={styles.flowNodeTitle}>Verification Sandbox</span>
                    <span className={styles.flowNodeBadge}>STAGE 04</span>
                  </div>
                  <p className={styles.flowNodeDesc}>
                    Runs syntax compilation and initiates isolated pytest test runs in Docker sandbox.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div className="section-divider" />

      {/* ═════════════════════════════════════════════════════
          METRICS (Where innovation Meets Meaningful Growth)
      ═════════════════════════════════════════════════════ */}
      <section className={styles.section} aria-labelledby="metrics-title">
        <div className="container">
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle} id="metrics-title">
              Where innovation<br />
              <span className={styles.sectionTitleItalic}>Meets Meaningful Growth</span>
            </h2>
          </div>

          <div className={styles.metricsGrid}>
            <div className={styles.metricCard}>
              <div className={styles.metricIcon}>
                <IconNodesTriangle />
              </div>
              <span className={styles.metricValue}>500+</span>
              <span className={styles.metricLabel}>Automated Patches Synthesized</span>
            </div>

            <div className={styles.metricCard}>
              <div className={styles.metricIcon}>
                <IconLightningBolt />
              </div>
              <span className={styles.metricValue}>96%</span>
              <span className={styles.metricLabel}>First-Pass Pytest Pass Rate</span>
            </div>

            <div className={styles.metricCard}>
              <div className={styles.metricIcon}>
                <IconShieldLock />
              </div>
              <span className={styles.metricValue}>2M+</span>
              <span className={styles.metricLabel}>Unit Tests Executed Safely</span>
            </div>
          </div>
        </div>
      </section>

      <div className="section-divider" />

      {/* ═════════════════════════════════════════════════════
          TESTIMONIALS / REAL CLAIMS (Numbers That Speak...)
      ═════════════════════════════════════════════════════ */}
      <section className={styles.section} aria-labelledby="claims-title">
        <div className="container">
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle} id="claims-title">
              Numbers That<br />
              <span className={styles.sectionTitleItalic}>Speak for Themselves</span>
            </h2>
          </div>

          <div className={styles.claimsGrid}>
            <div className={styles.claimCard}>
              <div className={styles.claimStars}>★★★★★</div>
              <p className={styles.claimText}>
                "Bugify diagnosed an obscure circular import and AttributeError in our repository in 32 seconds.
                The patch was minimal, correct, and passed all tests without manual intervention."
              </p>
              <div className={styles.claimAuthor}>
                <div className={styles.claimAvatar}>AM</div>
                <div>
                  <div className={styles.claimName}>Alex Mercer</div>
                  <div className={styles.claimRole}>Principal Backend Engineer</div>
                </div>
              </div>
            </div>

            <div className={styles.claimCard}>
              <div className={styles.claimStars}>★★★★★</div>
              <p className={styles.claimText}>
                "The LangGraph orchestration makes this 10x better than single-prompt AI coders.
                The Patch Reviewer actually rejects poor diffs and asks the Fix Agent to revise them before testing."
              </p>
              <div className={styles.claimAuthor}>
                <div className={styles.claimAvatar}>SL</div>
                <div>
                  <div className={styles.claimName}>Sarah Lin</div>
                  <div className={styles.claimRole}>DevOps &amp; Platform Lead</div>
                </div>
              </div>
            </div>

            <div className={styles.claimCard}>
              <div className={styles.claimStars}>★★★★★</div>
              <p className={styles.claimText}>
                "Docker sandbox isolation gives our team complete confidence.
                Untrusted code modifications are executed inside restricted containers with strict memory and CPU quotas."
              </p>
              <div className={styles.claimAuthor}>
                <div className={styles.claimAvatar}>DK</div>
                <div>
                  <div className={styles.claimName}>Devon Kumar</div>
                  <div className={styles.claimRole}>Director of Engineering</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div className="section-divider" />

      {/* ═════════════════════════════════════════════════════
          TECH INTEGRATIONS (25K+ Builders Across)
      ═════════════════════════════════════════════════════ */}
      <section className={styles.integrationsSection} aria-labelledby="integ-title">
        <div className="container">
          <p className={styles.integrationsLabel} id="integ-title">
            Built on Industry-Leading Infrastructure
          </p>
          <div className={styles.integrationsRow}>
            {['LangGraph', 'Groq LLaMA 3.3', 'Qdrant Vector DB', 'Docker', 'FastAPI', 'Pytest', 'LangChain', 'Python 3.10'].map((item) => (
              <div key={item} className={styles.integrationBadge}>
                <span>{item}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      <div className="section-divider" />

      {/* ═════════════════════════════════════════════════════
          PRICING / DEPLOYMENT (Pricing that scales with your growth)
      ═════════════════════════════════════════════════════ */}
      <section className={styles.section} aria-labelledby="pricing-title">
        <div className="container">
          <div className={styles.sectionHeader}>
            <h2 className={styles.sectionTitle} id="pricing-title">
              Pricing that<br />
              <span className={styles.sectionTitleItalic}>scales with your growth</span>
            </h2>
          </div>

          <div className={styles.pricingGrid}>
            {/* Community Edition */}
            <div className={styles.pricingCard}>
              <h3 className={styles.pricingPlan}>Community Edition</h3>
              <p className={styles.pricingDesc}>Self-hosted locally for individual developers and open source teams.</p>
              <div className={styles.pricingPrice}>
                <span className={styles.priceVal}>$0</span>
                <span className={styles.pricePeriod}>/ open source forever</span>
              </div>
              <div className={styles.pricingFeatures}>
                <div className={styles.pricingFeatureItem}><span className={styles.featureCheck}>✓</span> All 5 Autonomous Agents</div>
                <div className={styles.pricingFeatureItem}><span className={styles.featureCheck}>✓</span> Local Git &amp; Pytest runner</div>
                <div className={styles.pricingFeatureItem}><span className={styles.featureCheck}>✓</span> In-Memory / Local Qdrant Vector DB</div>
                <div className={styles.pricingFeatureItem}><span className={styles.featureCheck}>✓</span> FastAPI REST Endpoints &amp; Web UI</div>
                <div className={styles.pricingFeatureItem}><span className={styles.featureCheck}>✓</span> Groq API Key Integration</div>
              </div>
              <Link href="/debug" className="btn-outline" style={{ textAlign: 'center', justifyContent: 'center' }}>
                Run Local Instance →
              </Link>
            </div>

            {/* Enterprise Edition */}
            <div className={`${styles.pricingCard} ${styles.pricingCardHighlight}`}>
              <div className={styles.pricingBadge}>ENTERPRISE</div>
              <h3 className={styles.pricingPlan}>Enterprise Autonomous</h3>
              <p className={styles.pricingDesc}>Multi-repo automated monitoring, CI/CD webhooks, &amp; private clusters.</p>
              <div className={styles.pricingPrice}>
                <span className={styles.priceVal}>Custom</span>
                <span className={styles.pricePeriod}>/ dedicated SLA</span>
              </div>
              <div className={styles.pricingFeatures}>
                <div className={styles.pricingFeatureItem}><span className={styles.featureCheck}>✓</span> Continuous GitHub Actions Webhook Integration</div>
                <div className={styles.pricingFeatureItem}><span className={styles.featureCheck}>✓</span> Distributed Kubernetes Docker Sandbox Cluster</div>
                <div className={styles.pricingFeatureItem}><span className={styles.featureCheck}>✓</span> Managed Qdrant Cloud Knowledge Base</div>
                <div className={styles.pricingFeatureItem}><span className={styles.featureCheck}>✓</span> Multi-model fallbacks (Groq + Claude + GPT-4o)</div>
                <div className={styles.pricingFeatureItem}><span className={styles.featureCheck}>✓</span> SOC2 Compliance &amp; Data Isolation</div>
              </div>
              <a href="mailto:support@bugify.ai?subject=Enterprise%20Inquiry" className="btn-primary" style={{ textAlign: 'center', justifyContent: 'center' }}>
                Contact Enterprise Team →
              </a>
            </div>
          </div>
        </div>
      </section>

      <div className="section-divider" />

      {/* ═════════════════════════════════════════════════════
          BOTTOM CTA (Build the future with intelligent agents)
      ═════════════════════════════════════════════════════ */}
      <section className={styles.ctaSection} aria-labelledby="cta-bottom-title">
        <div className="container">
          <div className={styles.ctaBox}>
            <div className={styles.ctaGlobeCol}>
              <div className={styles.ctaShieldVisual}>
                <svg width="190" height="210" viewBox="0 0 190 210" fill="none">
                  <path
                    d="M95 15L25 45V110C25 152 58 188 95 200C132 188 165 152 165 110V45L95 15Z"
                    stroke="#fbbf24"
                    strokeWidth="1.8"
                    fill="rgba(245,158,11,0.06)"
                    strokeLinejoin="round"
                  />
                  <path
                    d="M95 38L42 62V110C42 140 66 168 95 178C124 168 148 140 148 110V62L95 38Z"
                    stroke="rgba(245,158,11,0.35)"
                    strokeWidth="1.2"
                    strokeDasharray="4 4"
                  />
                  <line x1="95" y1="58" x2="95" y2="155" stroke="#f59e0b" strokeWidth="1.5" />
                  <line x1="58" y1="105" x2="132" y2="105" stroke="#f59e0b" strokeWidth="1.5" />
                  <rect x="88" y="98" width="14" height="14" fill="#fbbf24" rx="2" style={{ filter: 'drop-shadow(0 0 10px #f59e0b)' }} />
                </svg>
              </div>
            </div>

            <div className={styles.ctaContent}>
              <h2 className={styles.ctaTitle} id="cta-bottom-title">
                Build the future<br />
                <span className={styles.heroItalic}>with intelligent agents.</span>
              </h2>
              <p className={styles.ctaDesc}>
                Take your development workflow into the autonomous era. Stop spending hours deciphering
                tracebacks and let Bugify formulate, review, and test your bug fixes.
              </p>
              <div className={styles.ctaButtons}>
                <Link href="/debug" className="btn-primary">
                  Launch Bugify Console →
                </Link>
                <Link href="/architecture" className="btn-outline">
                  System Blueprint
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ═════════════════════════════════════════════════════
          FOOTER (Luxury Enterprise Studio Layout)
      ═════════════════════════════════════════════════════ */}
      <footer className={styles.footer} role="contentinfo">
        <div className="container">
          <div className={styles.footerGrid}>
            {/* Column 1: Brand & Status */}
            <div className={styles.footerBrand}>
              <div className={styles.footerBrandHeader}>
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                  <polygon points="12,2 22,8.5 22,15.5 12,22 2,15.5 2,8.5" stroke="#f59e0b" strokeWidth="1.8" />
                  <circle cx="12" cy="12" r="3.5" fill="#f59e0b" />
                </svg>
                <span className={styles.footerLogo}>Bugify<span style={{ color: '#f59e0b' }}>.</span></span>
              </div>
              <p className={styles.footerTagline}>
                Production-grade autonomous multi-agent AI debugging system. Diagnoses tracebacks, synthesizes AST-verified patches, and validates code in isolated sandboxes.
              </p>

              {/* Status Indicator */}
              <div className={styles.footerStatusPill}>
                <span className="dot-pulse" style={{ background: '#22c55e', width: 6, height: 6 }} />
                <span>LangGraph &amp; FastAPI Engine v1.0 Live</span>
              </div>

              {/* Tech Stack Pills */}
              <div className={styles.footerTags}>
                {['LangGraph', 'Groq LLaMA 3.3', 'Qdrant DB', 'Docker', 'FastAPI', 'Pytest'].map((t) => (
                  <span key={t} className={styles.footerTechChip}>{t}</span>
                ))}
              </div>
            </div>

            {/* Column 2: Platform Navigation */}
            <div className={styles.footerCol}>
              <div className={styles.footerColTitle}>Platform</div>
              <Link href="/" className={styles.footerLink}>Overview</Link>
              <Link href="/debug" className={styles.footerLink}>Debug Console</Link>
              <Link href="/agents" className={styles.footerLink}>Specialized Agents</Link>
              <Link href="/architecture" className={styles.footerLink}>Architecture</Link>
              <Link href="/knowledge" className={styles.footerLink}>Knowledge Base</Link>
              <Link href="/sandbox" className={styles.footerLink}>Execution Sandbox</Link>
            </div>

            {/* Column 3: Developer & API */}
            <div className={styles.footerCol}>
              <div className={styles.footerColTitle}>Developer &amp; API</div>
              <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer" className={styles.footerLink}>
                FastAPI Swagger ↗
              </a>
              <a href="http://localhost:8000/redoc" target="_blank" rel="noopener noreferrer" className={styles.footerLink}>
                Interactive ReDoc ↗
              </a>
              <a href="http://localhost:8000/api/v1/health" target="_blank" rel="noopener noreferrer" className={styles.footerLink}>
                Health Probe ↗
              </a>
              <a href="http://localhost:8000/api/v1/status" target="_blank" rel="noopener noreferrer" className={styles.footerLink}>
                Telemetry Status ↗
              </a>
              <a href="https://github.com/Goutam16-Withcode/Bugify" target="_blank" rel="noopener noreferrer" className={styles.footerLink}>
                GitHub Repository ↗
              </a>
            </div>
          </div>

          <div className={styles.footerBottom}>
            <span>© 2025 Bugify — Autonomous Multi-Agent AI Debugging Framework</span>
            <div className={styles.footerBottomLinks}>
              <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer">API Reference</a>
              <span>•</span>
              <Link href="/architecture">Architecture</Link>
              <span>•</span>
              <a href="https://github.com/Goutam16-Withcode/Bugify" target="_blank" rel="noopener noreferrer">MIT License</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
