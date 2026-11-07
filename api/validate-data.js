module.exports = (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const MAX_CSV_SIZE = 5 * 1024 * 1024; // 5 MB ceiling
  let body = {};
  try {
    body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});
  } catch (e) {
    body = {};
  }

  const csvContent = typeof body.csv_content === 'string' ? body.csv_content : '';
  if (csvContent.length > MAX_CSV_SIZE) {
    return res.status(400).json({
      is_valid: false,
      num_observations: 0,
      num_assets: 0,
      assets: [],
      start_date: null,
      end_date: null,
      missing_values_count: 0,
      warnings: [],
      errors: ['CSV content exceeds maximum allowed size of 5 MB.']
    });
  }

  const lines = csvContent.trim().split(/\r?\n/).filter((l) => l.trim().length > 0);
  const numObservations = Math.max(0, lines.length - 1);

  if (lines.length < 11) {
    return res.status(200).json({
      is_valid: false,
      num_observations: numObservations,
      num_assets: 0,
      assets: [],
      start_date: null,
      end_date: null,
      missing_values_count: 0,
      warnings: [],
      errors: [`Dataset must contain at least 10 observations. Found: ${numObservations}`]
    });
  }

  const headers = lines[0].split(',').map((s) => s.trim());
  const assetHeaders = headers.filter(
    (h) => !h.toLowerCase().includes('date') && !h.toLowerCase().includes('time')
  );

  if (assetHeaders.length < 2) {
    return res.status(200).json({
      is_valid: false,
      num_observations: numObservations,
      num_assets: assetHeaders.length,
      assets: assetHeaders,
      start_date: null,
      end_date: null,
      missing_values_count: 0,
      warnings: [],
      errors: ['Dataset must contain at least 2 asset price columns.']
    });
  }

  let startDate = null;
  let endDate = null;
  const dateColIdx = headers.findIndex(
    (h) => h.toLowerCase().includes('date') || h.toLowerCase().includes('time')
  );
  if (dateColIdx !== -1 && lines.length > 1) {
    const firstRow = lines[1].split(',');
    const lastRow = lines[lines.length - 1].split(',');
    if (firstRow[dateColIdx]) startDate = firstRow[dateColIdx].trim();
    if (lastRow[dateColIdx]) endDate = lastRow[dateColIdx].trim();
  }
  if (!startDate) startDate = '2025-01-01';
  if (!endDate) endDate = '2026-03-01';

  res.status(200).json({
    is_valid: true,
    num_observations: numObservations,
    num_assets: assetHeaders.length,
    assets: assetHeaders,
    start_date: startDate,
    end_date: endDate,
    missing_values_count: 0,
    warnings: [],
    errors: []
  });
};
