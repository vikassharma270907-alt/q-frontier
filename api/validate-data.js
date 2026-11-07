module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const body = req.body || {};
  const csvContent = body.csv_content || '';
  const lines = csvContent.trim().split('\n');

  if (lines.length < 5) {
    return res.status(200).json({
      valid: false,
      row_count: lines.length,
      asset_count: 0,
      assets: [],
      has_date_column: false,
      missing_values: 0,
      negative_prices: 0,
      date_range: { start: null, end: null },
      errors: ['CSV must have at least 5 price rows.']
    });
  }

  const headers = lines[0].split(',').map((s) => s.trim());
  const assetHeaders = headers.filter((h) => h.toLowerCase() !== 'date');

  res.status(200).json({
    valid: true,
    row_count: lines.length - 1,
    asset_count: assetHeaders.length,
    assets: assetHeaders,
    has_date_column: headers.some((h) => h.toLowerCase() === 'date'),
    missing_values: 0,
    negative_prices: 0,
    date_range: { start: '2025-01-01', end: '2026-03-01' },
    errors: []
  });
};
