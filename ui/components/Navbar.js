'use client';
import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import styles from './Navbar.module.css';

const NAV_LINKS = [
  { label: 'Overview',      href: '/' },
  { label: 'Debug Console', href: '/debug' },
  { label: 'Agents',        href: '/agents' },
  { label: 'Architecture',  href: '/architecture' },
  { label: 'Knowledge Base', href: '/knowledge' },
  { label: 'Sandbox',       href: '/sandbox' },
];

export default function Navbar() {
  const path = usePathname();
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <header className={`${styles.header} ${scrolled ? styles.scrolled : ''}`} role="banner">
      <div className={`container ${styles.inner}`}>
        {/* Brand */}
        <Link href="/" className={styles.logo} id="nav-logo" aria-label="Bugify Home">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" className={styles.logoSvg}>
            <polygon
              points="12,2 22,8.5 22,15.5 12,22 2,15.5 2,8.5"
              stroke="#f59e0b"
              strokeWidth="1.8"
              fill="rgba(245,158,11,0.08)"
            />
            <circle cx="12" cy="12" r="3" fill="#f59e0b" />
            <line x1="12" y1="5" x2="12" y2="9" stroke="#f59e0b" strokeWidth="1.5" strokeLinecap="round"/>
            <line x1="18" y1="8.5" x2="14.6" y2="10.5" stroke="#f59e0b" strokeWidth="1.5" strokeLinecap="round"/>
            <line x1="18" y1="15.5" x2="14.6" y2="13.5" stroke="#f59e0b" strokeWidth="1.5" strokeLinecap="round"/>
          </svg>
          <span className={styles.logoText}>
            Bugify<span className={styles.logoDot}>.</span>
          </span>
        </Link>

        {/* Desktop Nav */}
        <nav className={styles.nav} aria-label="Primary navigation">
          {NAV_LINKS.map((l) => {
            const isActive = path === l.href;
            return (
              <Link
                key={l.href}
                href={l.href}
                id={`nav-${l.label.toLowerCase().replace(/\s+/g, '-')}`}
                className={`${styles.navLink} ${isActive ? styles.active : ''}`}
              >
                {l.label}
                {isActive && <span className={styles.activeBar} />}
              </Link>
            );
          })}
        </nav>

        {/* Right actions */}
        <div className={styles.actions}>
          <div className={styles.statusPill}>
            <span className="dot-pulse" style={{ width: 6, height: 6 }} />
            <span className={styles.statusText}>Live</span>
          </div>
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            id="nav-api-docs"
            className={styles.loginLink}
          >
            API Docs
          </a>
          <Link
            href="/debug"
            id="nav-cta"
            className="btn-primary"
            style={{ padding: '8px 20px', fontSize: '0.8rem' }}
          >
            Launch →
          </Link>
        </div>

        {/* Mobile hamburger */}
        <button
          className={styles.hamburger}
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-label="Toggle navigation"
        >
          <span className={`${styles.hamLine} ${mobileOpen ? styles.hamLineOpen1 : ''}`} />
          <span className={`${styles.hamLine} ${mobileOpen ? styles.hamLineOpen2 : ''}`} />
          <span className={`${styles.hamLine} ${mobileOpen ? styles.hamLineOpen3 : ''}`} />
        </button>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className={styles.mobileMenu}>
          {NAV_LINKS.map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className={`${styles.mobileLink} ${path === l.href ? styles.mobileLinkActive : ''}`}
              onClick={() => setMobileOpen(false)}
            >
              {l.label}
            </Link>
          ))}
          <Link href="/debug" className="btn-primary" style={{ marginTop: 8, justifyContent: 'center' }}>
            Launch Bugify →
          </Link>
        </div>
      )}
    </header>
  );
}
