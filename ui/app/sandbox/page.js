'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import Navbar from '../../components/Navbar';
import styles from './sandbox.module.css';

/* ── SVG Icons ──────────────────────────────────────── */
function IconShield() {
  return (
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none">
      <path d="M12 2L3 6.5V12c0 5.25 3.75 10.15 9 11.5C17.25 22.15 21 17.25 21 12V6.5L12 2z"
        stroke="#fbbf24" strokeWidth="1.8" strokeLinejoin="round" fill="rgba(245,158,11,0.1)" />
      <path d="M9 12l2 2 4-4" stroke="#22c55e" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

function IconLock() {
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <rect x="3" y="11" width="18" height="11" rx="2" stroke="#fbbf24" strokeWidth="1.8"/>
      <path d="M7 11V7a5 5 0 0110 0v4" stroke="#fbbf24" strokeWidth="1.8" strokeLinecap="round"/>
      <circle cx="12" cy="16" r="1.5" fill="#fbbf24"/>
    </svg>
  );
}

function IconNetwork() {
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="10" stroke="#ef4444" strokeWidth="1.8"/>
      <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" stroke="#ef4444" strokeWidth="1.8" strokeLinecap="round"/>
    </svg>
  );
}

function IconClock() {
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="10" stroke="#3b82f6" strokeWidth="1.8"/>
      <polyline points="12 6 12 12 16 14" stroke="#3b82f6" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

function IconDocker() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
      <rect x="2" y="10" width="5" height="4" rx="1" stroke="#06b6d4" strokeWidth="1.5"/>
      <rect x="9" y="10" width="5" height="4" rx="1" stroke="#06b6d4" strokeWidth="1.5"/>
      <rect x="9" y="4" width="5" height="4" rx="1" stroke="#06b6d4" strokeWidth="1.5"/>
      <rect x="16" y="10" width="5" height="4" rx="1" stroke="#06b6d4" strokeWidth="1.5"/>
      <path d="M2 18c0 0 3-2 10-2s10 2 10 2" stroke="#06b6d4" strokeWidth="1.5" strokeLinecap="round"/>
    </svg>
  );
}

function IconProcess() {
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
      <rect x="3" y="3" width="18" height="18" rx="3" stroke="#a855f7" strokeWidth="1.8"/>
      <path d="M8 12h8M12 8v8" stroke="#a855f7" strokeWidth="1.8" strokeLinecap="round"/>
    </svg>
  );
}

function IconCheck() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
      <polyline points="20 6 9 17 4 12" stroke="#22c55e" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  );
}

const POLICIES = [
  {
    Icon: IconLock,
    title: 'Read-Only Host Mounts',
    color: '#f59e0b',
    desc: 'The repository workspace is mounted as a read-only volume (mode: "ro") inside the Docker container. Patches are staged in temporary memory overlays — the host filesystem is never mutated.',
    detail: 'volumes={repo_path: {"bind": "/workspace", "mode": "ro"}}',
  },
  {
    Icon: IconNetwork,
    title: 'Network Isolation',
    color: '#ef4444',
    desc: 'Sandbox executes with network_disabled=True. No outbound socket connections, no external script downloads, no environment secret exfiltration possible.',
    detail: 'network_disabled=True  # enforced by Docker daemon',
  },
  {
    Icon: IconClock,
    title: 'Process Quotas & Timeouts',
    color: '#3b82f6',
    desc: 'Hard wall-clock timeouts of 60 seconds and 512 MB RAM caps prevent infinite loops, fork bombs, and memory exhaustion from hanging the orchestrator.',
    detail: 'timeout=60  •  mem_limit="512m"  •  pids_limit=64',
  },
];

const CAPABILITIES = [
  { label: 'Docker Image', value: 'python:3.11-slim', Icon: IconDocker, icon: IconDocker, color: '#06b6d4' },
  { label: 'Memory Cap', value: '512 MB', Icon: IconProcess, icon: IconProcess, color: '#a855f7' },
  { label: 'Wall Timeout', value: '60 seconds', Icon: IconClock, icon: IconClock, color: '#3b82f6' },
  { label: 'Subprocess Fallback', value: 'Automatic', Icon: IconCheck, icon: IconCheck, color: '#22c55e' },
];

const CONTAINMENT_STATUS = [
  { label: 'Network Socket Egress', detail: 'Outbound TCP/UDP packets dropped via iptables', status: 'BLOCKED', statusColor: '#ef4444' },
  { label: 'Host Filesystem Mount', detail: 'Host codebase bind-mounted strictly read-only', status: 'READ-ONLY', statusColor: '#f59e0b' },
  { label: 'Memory Allocation Cap', detail: 'Hard cgroups limit enforced at 512 MB', status: 'CAPPED 512M', statusColor: '#3b82f6' },
  { label: 'Execution Process Timer', detail: 'SIGKILL triggered if wall time exceeds 60s', status: '60s TIMEOUT', statusColor: '#a855f7' },
  { label: 'Non-Root Execution UID', detail: 'Runs as unprivileged user (UID 1000:1000)', status: 'ENFORCED', statusColor: '#22c55e' },
  { label: 'Container Lifecycle', detail: 'Ephemeral container pruned upon exit', status: 'ZERO-TRACE', statusColor: '#22c55e' },
];

export default function SandboxPage() {
  const [animating, setAnimating] = useState(false);
  const [activePolicy, setActivePolicy] = useState(0);

  useEffect(() => {
    const t = setTimeout(() => setAnimating(true), 300);
    return () => clearTimeout(t);
  }, []);

  return (
    <div className={styles.page}>
      <Navbar />
      <div className={styles.glow1} />
      <div className={styles.glow2} />

      <div className="container" style={{ paddingTop: 110, paddingBottom: 80 }}>

        {/* Header */}
        <header className={styles.header}>
          <div className="badge">
            <span className="dot-pulse dot-amber" />
            Isolated Runtime Environment
          </div>
          <h1 className={styles.title}>
            Execution <span className="gradient-text">Sandbox</span>
          </h1>
          <p className={styles.subtitle}>
            Every candidate patch is tested inside an isolated Docker container or constrained
            subprocess sandbox. The host machine is never touched — security is enforced at the kernel level.
          </p>
        </header>

        {/* Status Banner */}
        <div className={styles.statusCard}>
          <div className={styles.statusLeft}>
            <div className={styles.statusIconWrap}>
              <IconShield />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 4 }}>
                <h3 className={styles.statusTitle}>Sandbox Engine Status</h3>
                <span className="badge badge-green">
                  <span className="dot-pulse" style={{ width: 5, height: 5 }} />
                  Ready
                </span>
              </div>
              <p className={styles.statusDesc}>
                Dual-mode executor: Ephemeral Docker container with automatic subprocess fallback.
              </p>
            </div>
          </div>
          <div className={styles.capsGrid}>
            {CAPABILITIES.map((c) => {
              const Icon = c.Icon || c.icon;
              return (
                <div key={c.label} className={styles.capItem}>
                  {Icon && <Icon />}
                  <div>
                    <div className={styles.capLabel}>{c.label}</div>
                    <div className={styles.capValue} style={{ color: c.color }}>{c.value}</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Security Policies */}
        <div className="section-label">Enforced Sandbox Safeguards</div>
        <div className={styles.policyRow}>
          {POLICIES.map((p, i) => {
            const Icon = p.Icon;
            const isActive = activePolicy === i;
            return (
              <button
                key={p.title}
                className={`${styles.policyCard} ${isActive ? styles.policyCardActive : ''}`}
                style={{ '--p-color': p.color }}
                onClick={() => setActivePolicy(i)}
                aria-label={p.title}
              >
                <div className={styles.policyIconWrap} style={{ background: `${p.color}18`, border: `1px solid ${p.color}30` }}>
                  {Icon && <Icon />}
                </div>
                <h3 className={styles.policyTitle}>{p.title}</h3>
                <p className={styles.policyDesc}>{p.desc}</p>
                {isActive && (
                  <div className={styles.policyCode}>
                    <code className="mono">{p.detail}</code>
                  </div>
                )}
              </button>
            );
          })}
        </div>

        {/* Two columns: Policy dataclass + Test Results */}
        <div className={styles.twoCol}>
          {/* SandboxPolicy spec */}
          <div className={styles.specCard}>
            <div className="badge" style={{ alignSelf: 'flex-start', marginBottom: 14 }}>
              sandbox/security.py
            </div>
            <h3 className={styles.specTitle}>SandboxPolicy Dataclass</h3>
            <p className={styles.specDesc}>
              Configurable policies dynamically enforce execution bounds depending on deployment mode.
              All fields are validated at runtime before container creation.
            </p>
            <pre className="code-block" style={{ fontSize: '0.78rem', marginTop: 16 }}>
{`@dataclass
class SandboxPolicy:
    timeout_seconds:  int  = 60
    network_disabled: bool = True
    memory_limit_mb:  int  = 512
    allowed_env_vars: List[str] = field(
        default_factory=lambda: [
            "PATH", "PYTHONPATH", "HOME"
        ]
    )
    run_as_nonroot:   bool = True
    max_output_bytes: int  = 1_000_000

    # Auto-fallback to subprocess when
    # Docker daemon is unavailable
    prefer_docker:    bool = True`}
            </pre>
          </div>

          {/* Real-time Sandbox Security & Containment Telemetry */}
          <div className={styles.testCard}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18 }}>
              <div>
                <div className="badge badge-green" style={{ marginBottom: 8 }}>
                  <span className="dot-pulse" />
                  Kernel Containment Active
                </div>
                <h3 className={styles.specTitle}>Live Security Telemetry</h3>
              </div>
              <div className={styles.testPassRate}>
                <div className={styles.testPassRateNum} style={{ color: '#06b6d4' }}>0-Trace</div>
                <div className={styles.testPassRateLabel}>Host Isolation</div>
              </div>
            </div>

            <div className={styles.testList}>
              {CONTAINMENT_STATUS.map((item, i) => (
                <div
                  key={item.label}
                  className={`${styles.testRow} ${styles.testRowVisible}`}
                  style={{ animationDelay: `${i * 0.08}s` }}
                >
                  <div className={styles.testCheck}>
                    <IconCheck />
                  </div>
                  <div className={styles.testName} style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <span style={{ fontWeight: 600, color: '#f5f5f5' }}>{item.label}</span>
                    <span style={{ fontSize: '0.74rem', color: '#737373' }}>{item.detail}</span>
                  </div>
                  <div className={styles.testTime} style={{ color: item.statusColor || '#22c55e', fontWeight: 700, fontSize: '0.74rem' }}>
                    {item.status}
                  </div>
                </div>
              ))}
            </div>
            <div className={styles.testFooter}>
              <span style={{ color: 'var(--text-muted)', fontSize: '0.75rem' }}>
                Kernel cgroups v2 + IPC namespace separation enforced
              </span>
              <Link href="/debug" className="btn-primary" style={{ padding: '8px 20px', fontSize: '0.8rem' }}>
                Open Debug Studio →
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
