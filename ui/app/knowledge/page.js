'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import Navbar from '../../components/Navbar';
import styles from './knowledge.module.css';

/* ── SVG Icons ──────────────────────────────────────── */
function IconSearch() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
      <circle cx="11" cy="11" r="8" stroke="currentColor" strokeWidth="2"/>
      <path d="M21 21l-4.35-4.35" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
    </svg>
  );
}

function IconVector() {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
      <circle cx="5" cy="5" r="2" stroke="#fbbf24" strokeWidth="1.8"/>
      <circle cx="19" cy="5" r="2" stroke="#fbbf24" strokeWidth="1.8"/>
      <circle cx="5" cy="19" r="2" stroke="#fbbf24" strokeWidth="1.8"/>
      <circle cx="19" cy="19" r="2" stroke="#fbbf24" strokeWidth="1.8"/>
      <circle cx="12" cy="12" r="2.5" stroke="#fbbf24" strokeWidth="1.8" fill="rgba(245,158,11,0.15)"/>
      <line x1="7" y1="6" x2="10.5" y2="10.5" stroke="#fbbf24" strokeWidth="1.2" strokeDasharray="2 2"/>
      <line x1="17" y1="6" x2="13.5" y2="10.5" stroke="#fbbf24" strokeWidth="1.2" strokeDasharray="2 2"/>
      <line x1="7" y1="18" x2="10.5" y2="13.5" stroke="#fbbf24" strokeWidth="1.2" strokeDasharray="2 2"/>
      <line x1="17" y1="18" x2="13.5" y2="13.5" stroke="#fbbf24" strokeWidth="1.2" strokeDasharray="2 2"/>
    </svg>
  );
}

function IconDB() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
      <ellipse cx="12" cy="6" rx="9" ry="3" stroke="currentColor" strokeWidth="1.8"/>
      <path d="M3 6v6c0 1.66 4.03 3 9 3s9-1.34 9-3V6" stroke="currentColor" strokeWidth="1.8"/>
      <path d="M3 12v6c0 1.66 4.03 3 9 3s9-1.34 9-3v-6" stroke="currentColor" strokeWidth="1.8"/>
    </svg>
  );
}

function IconDoc() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
      <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8L14 2z" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round"/>
      <polyline points="14 2 14 8 20 8" stroke="currentColor" strokeWidth="1.8" strokeLinejoin="round"/>
      <line x1="8" y1="13" x2="16" y2="13" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
      <line x1="8" y1="17" x2="13" y2="17" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
    </svg>
  );
}

const COLLECTIONS = [
  {
    id: 'bug_knowledge',
    label: 'Bug Knowledge',
    color: '#f59e0b',
    count: 247,
    dim: 384,
    desc: 'Resolved bug fix patterns with context, root cause, and defensive code guards.',
  },
  {
    id: 'error_patterns',
    label: 'Error Patterns',
    color: '#ef4444',
    count: 183,
    dim: 384,
    desc: 'Common Python exception hierarchies, anti-patterns, and known failure modes.',
  },
  {
    id: 'documentation',
    label: 'Documentation',
    color: '#3b82f6',
    count: 94,
    dim: 384,
    desc: 'Python stdlib docs, PEP references, and best-practice coding guides.',
  },
];

const SEED_DATA = [
  {
    collection: 'bug_knowledge',
    title: "AttributeError: 'NoneType' has no attribute",
    content: "Occurs when a variable expected to hold an object is None. Check all code paths that assign the variable. Ensure database queries handle missing rows using .first() with a None guard. Add defensive None checks or Optional typing with early returns.",
    tags: ['AttributeError', 'NoneType', 'Defensive Guard'],
    similarity: 0.97,
  },
  {
    collection: 'bug_knowledge',
    title: 'KeyError in dictionary access',
    content: "KeyError occurs when accessing a dict with a key that does not exist. Prefer dict.get(key, default) for safe access. Use 'if key in dict:' checks before direct bracket access. defaultdict and dict.setdefault are robust alternatives.",
    tags: ['KeyError', 'dict.get', 'Safe Access'],
    similarity: 0.94,
  },
  {
    collection: 'error_patterns',
    title: 'ImportError: cannot import name (Circular Import)',
    content: 'Indicates a circular dependency, a renamed module symbol, or a missing package. Check for circular imports by reviewing import cycles. Move imports inside function scope if required, or restructure modules into a shared base layer.',
    tags: ['ImportError', 'Circular Dependency', 'Module Scope'],
    similarity: 0.91,
  },
  {
    collection: 'error_patterns',
    title: 'RecursionError: maximum recursion depth exceeded',
    content: 'Infinite or deeply nested recursive calls exceed Python default stack limit (1000). Add a base case terminating condition. Prefer converting to iterative loops with while or an explicit stack queue structure.',
    tags: ['RecursionError', 'Base Case', 'Stack Overflow'],
    similarity: 0.88,
  },
  {
    collection: 'documentation',
    title: 'Python Standard Exception Hierarchy',
    content: 'BaseException → Exception → (ValueError, TypeError, AttributeError, KeyError, IndexError, RuntimeError, OSError). Catching Exception is generally safe. Never catch BaseException silently — it masks SystemExit and KeyboardInterrupt.',
    tags: ['Exception Hierarchy', 'BaseException', 'Error Handling'],
    similarity: 0.85,
  },
  {
    collection: 'bug_knowledge',
    title: 'TypeError: unsupported operand types',
    content: 'Occurs when an operation is applied to incompatible types (e.g., str + int). Use isinstance() checks before operations. Enable strict type annotations with mypy. Consider type coercion at API boundaries.',
    tags: ['TypeError', 'Type Coercion', 'isinstance'],
    similarity: 0.82,
  },
];

const COLLECTION_COLORS = {
  bug_knowledge: '#f59e0b',
  error_patterns: '#ef4444',
  documentation: '#3b82f6',
};

export default function KnowledgePage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(SEED_DATA);
  const [isSearching, setIsSearching] = useState(false);
  const [activeCollection, setActiveCollection] = useState('all');

  const handleSearch = (e) => {
    e.preventDefault();
    if (!query.trim() && activeCollection === 'all') {
      setResults(SEED_DATA);
      return;
    }
    setIsSearching(true);
    setTimeout(() => {
      const q = query.toLowerCase();
      let filtered = SEED_DATA;

      if (activeCollection !== 'all') {
        filtered = filtered.filter(item => item.collection === activeCollection);
      }
      if (q) {
        filtered = filtered.filter(
          (item) =>
            item.title.toLowerCase().includes(q) ||
            item.content.toLowerCase().includes(q) ||
            item.collection.toLowerCase().includes(q) ||
            item.tags.some((t) => t.toLowerCase().includes(q))
        );
      }
      setResults(filtered.length ? filtered : SEED_DATA);
      setIsSearching(false);
    }, 600);
  };

  const handleFilter = (col) => {
    setActiveCollection(col);
    const filtered = col === 'all' ? SEED_DATA : SEED_DATA.filter(item => item.collection === col);
    setResults(filtered);
  };

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
            Semantic Memory Vector Store
          </div>
          <h1 className={styles.title}>
            RAG <span className="gradient-text">Knowledge Base</span>
          </h1>
          <p className={styles.subtitle}>
            Bugify indexes resolved bug fixes, common error patterns, and language documentation
            into Qdrant collections using 384-dimensional dense semantic embeddings with in-memory fallback.
          </p>
        </header>

        {/* Stats strip */}
        <div className={styles.statsStrip}>
          {COLLECTIONS.map(col => (
            <div key={col.id} className={styles.statItem}>
              <div className={styles.statNum} style={{ color: col.color }}>{col.count}</div>
              <div className={styles.statLabel}>{col.label}</div>
              <div className={styles.statSub}>{col.dim}-dim embeddings</div>
            </div>
          ))}
          <div className={styles.statItem}>
            <div className={styles.statNum} style={{ color: '#22c55e' }}>0.94</div>
            <div className={styles.statLabel}>Avg Similarity</div>
            <div className={styles.statSub}>dense retrieval</div>
          </div>
        </div>

        {/* Collections overview */}
        <div className="section-label">Vector Collections</div>
        <div className={styles.collectionsRow}>
          {COLLECTIONS.map(col => (
            <button
              key={col.id}
              className={`${styles.collectionChip} ${activeCollection === col.id ? styles.collectionChipActive : ''}`}
              style={{ '--c-color': col.color }}
              onClick={() => handleFilter(col.id)}
            >
              <span className={styles.collectionDot} style={{ background: col.color, boxShadow: `0 0 8px ${col.color}` }} />
              <div className={styles.collectionChipText}>
                <span className={styles.collectionChipLabel}>{col.label}</span>
                <span className={styles.collectionChipCount}>{col.count} chunks</span>
              </div>
            </button>
          ))}
          <button
            className={`${styles.collectionChip} ${activeCollection === 'all' ? styles.collectionChipActive : ''}`}
            style={{ '--c-color': '#a855f7' }}
            onClick={() => handleFilter('all')}
          >
            <IconDB />
            <div className={styles.collectionChipText}>
              <span className={styles.collectionChipLabel}>All Collections</span>
              <span className={styles.collectionChipCount}>{SEED_DATA.length} visible</span>
            </div>
          </button>
        </div>

        {/* Search */}
        <div className={styles.searchSection}>
          <div className="badge" style={{ marginBottom: 8 }}>
            <IconVector />
            Interactive Semantic Retrieval
          </div>
          <h2 className={styles.searchTitle}>Query The Knowledge Base</h2>
          <p className={styles.searchDesc}>
            Simulates dense vector search across Bugify's Qdrant embeddings. Type any error or symptom.
          </p>
          <form onSubmit={handleSearch} className={styles.searchBar}>
            <div className={styles.searchIcon}><IconSearch /></div>
            <input
              type="text"
              className={`input ${styles.searchInput}`}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. NoneType attribute, circular import, recursion limit..."
              style={{ background: '#09090b', paddingLeft: '44px' }}
              id="knowledge-search"
            />
            <button
              type="submit"
              className="btn-primary"
              style={{ padding: '0 24px', whiteSpace: 'nowrap' }}
              disabled={isSearching}
            >
              {isSearching ? (
                <>
                  <span style={{ width: 14, height: 14, border: '2px solid rgba(0,0,0,0.3)', borderTopColor: '#000', borderRadius: '50%', animation: 'spin 0.6s linear infinite', display: 'inline-block' }} />
                  Searching...
                </>
              ) : (
                <>Search Vectors →</>
              )}
            </button>
          </form>
        </div>

        {/* Results Grid */}
        <div className="section-label">
          Vector Retrieval Results
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 400, textTransform: 'none', letterSpacing: 0, marginLeft: 8 }}>
            {results.length} chunks
          </span>
        </div>
        <div className={styles.resultsGrid}>
          {results.map((item, idx) => {
            const color = COLLECTION_COLORS[item.collection] || '#f59e0b';
            return (
              <div
                key={idx}
                className={styles.resultCard}
                style={{ animationDelay: `${idx * 0.06}s` }}
              >
                {/* Header */}
                <div className={styles.resultCardTop}>
                  <span
                    className="badge"
                    style={{ background: `${color}15`, borderColor: `${color}35`, color }}
                  >
                    <IconDoc />
                    {item.collection}
                  </span>
                  <div className={styles.similarityBar}>
                    <div className={styles.similarityLabel}>Similarity</div>
                    <div className={styles.similarityValue} style={{ color: '#22c55e' }}>
                      {item.similarity.toFixed(2)}
                    </div>
                    <div className="progress-bar" style={{ width: 60 }}>
                      <div
                        className="progress-fill"
                        style={{ '--target-width': `${item.similarity * 100}%`, width: `${item.similarity * 100}%` }}
                      />
                    </div>
                  </div>
                </div>

                {/* Similarity accent line */}
                <div style={{ height: 2, background: `linear-gradient(90deg, ${color}, transparent)`, margin: '12px 0', borderRadius: 1, opacity: 0.5 }} />

                <h3 className={styles.resultTitle}>{item.title}</h3>
                <p className={styles.resultContent}>{item.content}</p>

                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginTop: 12 }}>
                  {item.tags.map((t) => (
                    <span key={t} className="tag" style={{ fontSize: '0.7rem', borderColor: `${color}25`, color }}>{t}</span>
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        {/* Footer CTA */}
        <div style={{ textAlign: 'center', marginTop: 60 }}>
          <p style={{ color: 'var(--text-muted)', marginBottom: 20, fontSize: '0.9rem' }}>
            Ingest your own documentation with <code style={{ color: '#fbbf24', background: 'rgba(245,158,11,0.1)', padding: '2px 6px', borderRadius: 4 }}>python scripts/ingest_knowledge.py</code>
          </p>
          <Link href="/debug" className="btn-primary">
            Debug Using Knowledge Base →
          </Link>
        </div>

      </div>
    </div>
  );
}
