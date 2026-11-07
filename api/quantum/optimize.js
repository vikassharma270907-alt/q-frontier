const samplePayloads = require('../data/sample_payloads.json');

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // Handle dynamic parameters if supplied
  const body = req.body || {};
  const base = JSON.parse(JSON.stringify(samplePayloads.quantum_optimize));

  if (body.depth !== undefined) {
    base.quantum_solver_benchmark.depth = body.depth;
  }
  if (body.use_qcl_sensor !== undefined) {
    base.regime_sensor.sensor_active = Boolean(body.use_qcl_sensor);
  }

  res.status(200).json(base);
};

