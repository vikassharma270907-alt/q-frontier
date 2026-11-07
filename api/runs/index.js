const sampleRun = require('../data/sample_run.json');

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method === 'GET') {
    return res.status(200).json([sampleRun.run]);
  }

  const body = req.body || {};
  const newRunId = `run_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 6)}`;
  const runResponse = {
    ...sampleRun.run,
    run_id: newRunId,
    timestamp: new Date().toISOString(),
    parameters: {
      ...sampleRun.run.parameters,
      asset_count: body.asset_count || sampleRun.run.parameters.asset_count,
      k_cardinality: body.k_cardinality || sampleRun.run.parameters.k_cardinality,
      lambda_risk: body.lambda_risk !== undefined ? body.lambda_risk : sampleRun.run.parameters.lambda_risk,
      circuit_depth: body.circuit_depth || sampleRun.run.parameters.circuit_depth
    }
  };

  res.status(200).json(runResponse);
};
