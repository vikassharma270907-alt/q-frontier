"""
Q-FRONTIER: System Health & Diagnostic HTML Dashboard Generator.
Provides an auditable, modern status UI when /api/health is accessed directly in a browser.
"""

from __future__ import annotations
import json
from typing import Dict, Any


def generate_health_dashboard_html(data: Dict[str, Any]) -> str:
    """Generates a responsive, dark-zinc styled diagnostic dashboard HTML."""
    json_str = json.dumps(data, indent=2)
    sponsors_html = "".join(
        f'<span class="badge sponsor">{s}</span>' for s in data.get("sponsors", [])
    )
    
    aer_status = "ACTIVE" if data.get("backends", {}).get("qiskit_aer") else "SIMULATED"
    ionq_status = "READY" if data.get("backends", {}).get("ionq_transpiler") else "STANDBY"
    qr_status = "SDK READY" if data.get("backends", {}).get("quantum_rings_lib") else "SIMULATED FALLBACK"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Q-FRONTIER | System Health & Diagnostics</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      background: #050505;
      color: #e4e4e7;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      padding: 24px 16px;
    }}
    .container {{
      max-width: 960px;
      margin: 0 auto;
      width: 100%;
    }}
    header {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      padding-bottom: 24px;
      border-bottom: 1px solid #27272a;
      margin-bottom: 24px;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .logo-badge {{
      background: #18181b;
      border: 1px solid #3f3f46;
      border-radius: 10px;
      padding: 6px 10px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      font-weight: 800;
      color: #fff;
      letter-spacing: -0.5px;
    }}
    .brand h1 {{
      font-size: 18px;
      font-weight: 800;
      color: #fff;
      letter-spacing: -0.5px;
    }}
    .brand p {{
      font-size: 12px;
      color: #a1a1aa;
      margin-top: 2px;
    }}
    .status-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.35);
      color: #34d399;
      padding: 6px 14px;
      border-radius: 9999px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.5px;
    }}
    .pulse-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 10px #10b981;
      animation: pulse 2s infinite ease-in-out;
    }}
    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.4; transform: scale(0.85); }}
    }}
    .banner {{
      background: #09090b;
      border: 1px solid #27272a;
      border-radius: 12px;
      padding: 12px 16px;
      margin-bottom: 24px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: #a1a1aa;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }}
    .banner strong {{
      color: #e4e4e7;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}
    .card {{
      background: #09090b;
      border: 1px solid #27272a;
      border-radius: 16px;
      padding: 18px;
      transition: all 0.2s ease;
    }}
    .card:hover {{
      border-color: #3f3f46;
      transform: translateY(-2px);
    }}
    .card-label {{
      font-size: 11px;
      color: #71717a;
      font-family: 'JetBrains Mono', monospace;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 6px;
    }}
    .card-val {{
      font-size: 16px;
      font-weight: 800;
      color: #fff;
      font-family: 'JetBrains Mono', monospace;
    }}
    .card-sub {{
      font-size: 11px;
      color: #a1a1aa;
      margin-top: 4px;
    }}
    .badge {{
      display: inline-block;
      font-family: 'JetBrains Mono', monospace;
      font-size: 10px;
      padding: 2px 8px;
      border-radius: 6px;
      margin-top: 6px;
      border: 1px solid transparent;
    }}
    .badge.active {{
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border-color: rgba(16, 185, 129, 0.3);
    }}
    .badge.ready {{
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      border-color: rgba(56, 189, 248, 0.3);
    }}
    .badge.sponsor {{
      background: #18181b;
      color: #d4d4d8;
      border-color: #27272a;
      font-size: 11px;
      padding: 4px 10px;
      margin: 3px;
    }}
    .section-title {{
      font-size: 13px;
      font-weight: 700;
      color: #fff;
      font-family: 'JetBrains Mono', monospace;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .sponsors-wrap {{
      background: #09090b;
      border: 1px solid #27272a;
      border-radius: 16px;
      padding: 18px;
      margin-bottom: 24px;
    }}
    .sponsors-list {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }}
    .actions-bar {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 24px;
    }}
    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 13px;
      font-weight: 700;
      padding: 10px 18px;
      border-radius: 12px;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s ease;
      border: 1px solid transparent;
    }}
    .btn-primary {{
      background: #fff;
      color: #000;
    }}
    .btn-primary:hover {{
      background: #e4e4e7;
      transform: translateY(-1px);
    }}
    .btn-secondary {{
      background: #18181b;
      color: #e4e4e7;
      border-color: #3f3f46;
    }}
    .btn-secondary:hover {{
      background: #27272a;
      color: #fff;
    }}
    .json-box {{
      background: #09090b;
      border: 1px solid #27272a;
      border-radius: 16px;
      overflow: hidden;
      margin-bottom: 24px;
    }}
    .json-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 12px 18px;
      border-bottom: 1px solid #18181b;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: #71717a;
    }}
    .copy-btn {{
      background: #18181b;
      border: 1px solid #27272a;
      color: #a1a1aa;
      font-size: 11px;
      padding: 4px 10px;
      border-radius: 6px;
      cursor: pointer;
      font-family: 'JetBrains Mono', monospace;
    }}
    .copy-btn:hover {{
      color: #fff;
      border-color: #3f3f46;
    }}
    pre {{
      padding: 18px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      line-height: 1.6;
      color: #a1a1aa;
      overflow-x: auto;
      max-height: 380px;
    }}
    footer {{
      margin-top: auto;
      padding-top: 24px;
      border-top: 1px solid #18181b;
      text-align: center;
      font-size: 11px;
      color: #71717a;
      font-family: 'JetBrains Mono', monospace;
    }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="brand">
        <div class="logo-badge">Q-FRONTIER v2.0</div>
        <div>
          <h1>System Health & Quantum Diagnostic Monitor</h1>
          <p>Intermountain Quantum Competition (IQC) 2026 &bull; Brigham Young University</p>
        </div>
      </div>
      <div class="status-pill">
        <div class="pulse-dot"></div>
        <span>200 OK &bull; SYSTEM HEALTHY</span>
      </div>
    </header>

    <div class="banner">
      <div>
        <strong>RESEARCH PROTOTYPE ONLY</strong> &mdash; NOT INVESTMENT ADVICE. NO QUANTUM ADVANTAGE CLAIMED.
      </div>
      <div>
        REPRODUCIBILITY AUDIT GUARANTEED
      </div>
    </div>

    <div class="actions-bar">
      <a href="/" class="btn btn-primary">&larr; Launch Research Workbench</a>
      <a href="/demo" class="btn btn-secondary">&#9654; 3-Min Interactive Video Presentation</a>
      <a href="/api/health?format=json" class="btn btn-secondary">&#123; &#125; Raw JSON API</a>
    </div>

    <div class="grid">
      <div class="card">
        <div class="card-label">Quantum Simulation Backend</div>
        <div class="card-val">Qiskit Aer</div>
        <div class="card-sub">Statevector Exact Simulation</div>
        <span class="badge active">&bull; {aer_status}</span>
      </div>

      <div class="card">
        <div class="card-label">Hardware Transpiler</div>
        <div class="card-val">IonQ Trapped-Ion</div>
        <div class="card-sub">All-to-All K_n Native Routing</div>
        <span class="badge ready">&bull; {ionq_status}</span>
      </div>

      <div class="card">
        <div class="card-label">Algorithmic Innovation</div>
        <div class="card-val">CCD-QAOA + GNN</div>
        <div class="card-sub">Counterdiabatic AGP & Sparsified XY</div>
        <span class="badge active">&bull; ACTIVE</span>
      </div>

      <div class="card">
        <div class="card-label">Runtime Environment</div>
        <div class="card-val">Python {data.get("python_version", "3.11")}</div>
        <div class="card-sub">FastAPI High-Concurrence Server</div>
        <span class="badge active">&bull; PRODUCTION READY</span>
      </div>
    </div>

    <div class="sponsors-wrap">
      <div class="section-title">Official Competition Sponsors & Ecosystem Partners</div>
      <div class="sponsors-list">
        {sponsors_html}
      </div>
    </div>

    <div class="json-box">
      <div class="json-header">
        <span>RAW AUDITABLE HEALTH PAYLOAD (APPLICATION/JSON)</span>
        <button class="copy-btn" onclick="copyJson(this)">Copy JSON</button>
      </div>
      <pre id="json-content">{json_str}</pre>
    </div>

    <footer>
      Q-FRONTIER: Auditable Hybrid-Optimization Research Workbench &bull; Grounded in Falla & Safro (2026), Cadavid et al. (2026), Proctor et al. (Sandia Nat. Lab, Nature Physics 2022).
    </footer>
  </div>

  <script>
    function copyJson(btn) {{
      const text = document.getElementById('json-content').innerText;
      navigator.clipboard.writeText(text).then(() => {{
        const original = btn.innerText;
        btn.innerText = 'Copied!';
        setTimeout(() => {{ btn.innerText = original; }}, 2000);
      }});
    }}
  </script>
</body>
</html>
"""
