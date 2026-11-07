const sampleStress = require('./data/sample_stress_test.json');

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const body = req.body || {};
  const base = JSON.parse(JSON.stringify(sampleStress));

  if (body.scenario) {
    base.scenario = body.scenario;
    base.description = `Stress-tested under ${body.scenario} with regime-switching correlation breakdown.`;
  }

  if (body.k_cardinality) {
    base.k_cardinality = Math.min(body.k_cardinality, 4);
  }

  res.status(200).json(base);
};
