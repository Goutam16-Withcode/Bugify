import './globals.css';

export const metadata = {
  title: 'Bugify — Autonomous AI Debugging System',
  description:
    'Bugify is an autonomous multi-agent AI debugging system that diagnoses bugs, generates patches, and verifies fixes using LangGraph, LLMs, and RAG.',
  keywords: 'AI debugging, LangGraph, autonomous agents, bug fix, code analysis, Groq, Qdrant',
  openGraph: {
    title: 'Bugify — Autonomous AI Debugging System',
    description: 'Multi-agent AI that autonomously diagnoses and fixes bugs in your codebase.',
    type: 'website',
  },
};

export const viewport = {
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,400;1,600&family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  );
}
