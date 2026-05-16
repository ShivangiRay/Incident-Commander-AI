import React from "react";
import { createRoot } from "react-dom/client";
import { Activity, GitBranch, ShieldAlert } from "lucide-react";
import "./styles.css";

function App() {
  return (
    <main className="console">
      <header>
        <div>
          <p>Incident Commander AI</p>
          <h1>Active Incident: Checkout latency regression</h1>
        </div>
        <button>sre@example.com</button>
      </header>
      <section className="summary">
        <article><span>Severity</span><strong>SEV1</strong></article>
        <article><span>Top hypothesis</span><strong>payments deploy</strong></article>
        <article><span>Approval gates</span><strong>2</strong></article>
        <article><span>Similar incidents</span><strong>1</strong></article>
      </section>
      <section className="layout">
        <article>
          <h2><Activity size={18} /> Signal Timeline</h2>
          <ol><li>09:02 payments deployed</li><li>09:07 checkout p95 latency spike</li><li>09:08 SLO burn alert</li><li>09:09 payment auth timeout trace</li></ol>
        </article>
        <article>
          <h2><GitBranch size={18} /> Evidence Graph</h2>
          <div className="graph">deploy:payments -> metric:checkout -> hypothesis:payments regression -> action:rollback</div>
        </article>
        <article>
          <h2><ShieldAlert size={18} /> Policy Decisions</h2>
          <p><b>Rollback payments</b> requires human review. No destructive action can auto-execute.</p>
        </article>
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);

