const sampleRun = require('../../data/sample_run.json');

module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const runId = req.query?.id || 'sample_run';
  const exportBundle = {
    ...sampleRun.export,
    run_id: runId,
    generated_at: new Date().toISOString()
  };

  res.status(200).json(exportBundle);
};

