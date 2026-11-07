const samplePayloads = require('./data/sample_payloads.json');

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const accept = req.headers['accept'] || '';
  const isHtml = accept.includes('text/html') && req.query.format !== 'json';

  if (isHtml) {
    const data = samplePayloads.health;
    const jsonStr = JSON.stringify(data, null, 2);
    const sponsorsHtml = (data.sponsors || []).map(s => `<span style="background:#18181b;color:#d4d4d8;border:1px solid #27272a;font-size:11px;padding:4px 10px;border-radius:6px;font-family:monospace;margin:3px;display:inline-block;">${s}</span>`).join('');

    const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Q-FRONTIER | System Health & Diagnostics</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: #050505; color: #e4e4e7; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 24px; min-height: 100vh; }
    .container { max-width: 900px; margin: 0 auto; }
    header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #27272a; padding-bottom: 20px; margin-bottom: 24px; }
    .brand h1 { font-size: 20px; font-weight: 800; color: #fff; }
    .brand p { font-size: 12px; color: #a1a1aa; margin-top: 4px; }
    .pill { display: inline-flex; align-items: center; gap: 8px; background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.35); color: #34d399; padding: 6px 14px; border-radius: 9999px; font-family: monospace; font-size: 12px; font-weight: 700; }
    .dot { width: 8px; height: 8px; border-radius: 50%; background: #10b981; }
    .banner { background: #09090b; border: 1px solid #27272a; border-radius: 12px; padding: 12px 16px; margin-bottom: 24px; font-family: monospace; font-size: 11px; color: #a1a1aa; }
    .actions { display: flex; gap: 12px; margin-bottom: 24px; }
    .btn { padding: 10px 18px; border-radius: 12px; font-weight: 700; text-decoration: none; font-size: 13px; }
    .btn-primary { background: #fff; color: #000; }
    .btn-secondary { background: #18181b; color: #e4e4e7; border: 1px solid #3f3f46; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px; }
    .card { background: #09090b; border: 1px solid #27272a; border-radius: 16px; padding: 18px; }
    .card-label { font-size: 11px; color: #71717a; font-family: monospace; text-transform: uppercase; margin-bottom: 6px; }
    .card-val { font-size: 16px; font-weight: 800; color: #fff; font-family: monospace; }
    pre { background: #09090b; border: 1px solid #27272a; border-radius: 16px; padding: 18px; font-family: monospace; font-size: 11px; color: #a1a1aa; overflow-x: auto; }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="brand">
        <h1>Q-FRONTIER v2.0 &bull; System Health & Diagnostics</h1>
        <p>Intermountain Quantum Competition (IQC) 2026 &bull; Brigham Young University</p>
      </div>
      <div class="pill"><div class="dot"></div> 200 OK &bull; SYSTEM HEALTHY</div>
    </header>
    <div class="banner">RESEARCH PROTOTYPE ONLY &mdash; NOT INVESTMENT ADVICE. NO QUANTUM ADVANTAGE CLAIMED.</div>
    <div class="actions">
      <a href="/" class="btn btn-primary">&larr; Launch Research Workbench</a>
      <a href="/demo" class="btn btn-secondary">&#9654; 3-Min Video Presentation</a>
      <a href="/api/health?format=json" class="btn btn-secondary">&#123; &#125; Raw JSON API</a>
    </div>
    <div class="grid">
      <div class="card"><div class="card-label">Quantum Simulation</div><div class="card-val">Qiskit Aer (Active)</div></div>
      <div class="card"><div class="card-label">Hardware Transpiler</div><div class="card-val">IonQ Native (Ready)</div></div>
      <div class="card"><div class="card-label">Sponsors</div><div style="margin-top:8px">${sponsorsHtml}</div></div>
    </div>
    <pre>${jsonStr}</pre>
  </div>
</body>
</html>`;
    res.setHeader('Content-Type', 'text/html; charset=utf-8');
    return res.status(200).send(html);
  }

  res.status(200).json(samplePayloads.health);
};
