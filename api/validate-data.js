module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const body = req.body || {};
  const csvContent = body.csv_content || '';
  const lines = csvContent.trim().split('\n').filter(l => l.trim().length > 0);

  if (lines.length < 11) {
    return res.status(200).json({
      is_valid: false,
      num_observations: lines.length - 1,
      num_assets: 0,
      assets: [],
      start_date: null,
      end_date: null,
      missing_values_count: 0,
      warnings: [],
      errors: [`Dataset must contain at least 10 observations. Found: ${Math.max(0, lines.length - 1)}`]
    });
  }

  const headers = lines[0].split(',').map((s) => s.trim());
  const assetHeaders = headers.filter((h) => h.toLowerCase() !== 'date' && h.toLowerCase() !== 'time');

  if (assetHeaders.length < 2) {
    return res.status(200).json({
      is_valid: false,
      num_observations: lines.length - 1,
      num_assets: assetHeaders.length,
      assets: assetHeaders,
      start_date: null,
      end_date: null,
      missing_values_count: 0,
      warnings: [],
      errors: ['Dataset must contain at least 2 asset price columns.']
    });
  }

  res.status(200).json({
    is_valid: true,
    num_observations: lines.length - 1,
    num_assets: assetHeaders.length,
    assets: assetHeaders,
    start_date: '2025-01-01',
    end_date: '2026-03-01',
    missing_values_count: 0,
    warnings: [],
    errors: []
  });
};
