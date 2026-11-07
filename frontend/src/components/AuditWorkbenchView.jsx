import React, { useState, useEffect } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, Legend,
  LineChart, Line, CartesianGrid
} from 'recharts';
import {
  Play, Download, ShieldCheck, CheckCircle2, AlertTriangle, Cpu, Database,
  Sliders, RefreshCw, FileText, Check, Award, BarChart3, HelpCircle
} from 'lucide-react';

export default function AuditWorkbenchView({ onExportSuccess }) {
  const [datasets, setDatasets] = useState([]);
  const [selectedDatasetId, setSelectedDatasetId] = useState('synthetic_tech_4');
  const [assetCount, setAssetCount] = useState(4);
  const [kCardinality, setKCardinality] = useState(2);
  const [lambdaRisk, setLambdaRisk] = useState(0.5);
  const [covarianceMethod, setCovarianceMethod] = useState('ledoit_wolf');
  const [circuitDepth, setCircuitDepth] = useState(1);
  const [selectedSolvers, setSelectedSolvers] = useState(['exact', 'annealing', 'xy_qaoa', 'ccd_qaoa', 'penalty_qaoa']);
  const [seeds, setSeeds] = useState('42, 101');
  const [transactionCostBps, setTransactionCostBps] = useState(5.0);

  const [isRunning, setIsRunning] = useState(false);
  const [runResult, setRunResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  // CSV Upload state
  const [csvContent, setCsvContent] = useState('');
  const [customDatasetId, setCustomDatasetId] = useState('');
  const [uploadDiag, setUploadDiag] = useState(null);
  const [showUploadModal, setShowUploadModal] = useState(false);

  useEffect(() => {
    fetch('/api/datasets')
      .then((res) => res.json())
      .then((data) => {
        setDatasets(data);
      })
      .catch((err) => console.error('Failed to load datasets', err));

    // Run initial benchmark on mount
    handleRunBenchmark();
  }, []);

  const handleRunBenchmark = () => {
    setIsRunning(true);
    setErrorMsg(null);

    const parsedSeeds = seeds
      .split(',')
      .map((s) => parseInt(s.trim(), 10))
      .filter((n) => !isNaN(n));

    const payload = {
      dataset_id: selectedDatasetId,
      asset_count: assetCount,
      k_cardinality: kCardinality,
      lambda_risk: lambdaRisk,
      covariance_method: covarianceMethod,
      solvers: selectedSolvers,
      circuit_depth: circuitDepth,
      seeds: parsedSeeds.length > 0 ? parsedSeeds : [42, 101, 777],
      transaction_cost_bps: transactionCostBps,
      turnover_penalty: 0.05
    };

    fetch('/api/runs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(async (res) => {
        if (!res.ok) {
          const errData = await res.json();
          throw new Error(errData.detail || 'Execution error');
        }
        return res.json();
      })
      .then((data) => {
        setRunResult(data);
        setIsRunning(false);
      })
      .catch((err) => {
        console.error('Benchmark execution failed', err);
        setErrorMsg(err.message);
        setIsRunning(false);
      });
  };

  const handleExportBundle = () => {
    if (!runResult?.run_id) return;
    fetch(`/api/runs/${runResult.run_id}/export`)
      .then((res) => res.json())
      .then((bundle) => {
        const jsonStr = JSON.stringify(bundle, null, 2);
        const blob = new Blob([jsonStr], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `q_frontier_reproducibility_${runResult.run_id}.json`;
        a.click();
        URL.revokeObjectURL(url);
        if (onExportSuccess) onExportSuccess();
      })
      .catch((err) => console.error('Export download failed', err));
  };

  const handleValidateCsv = () => {
    if (!csvContent.trim()) return;
    const dsId = customDatasetId.trim() || `custom_${Date.now()}`;
    fetch('/api/validate-data', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ csv_content: csvContent, dataset_id: dsId })
    })
      .then((res) => res.json())
      .then((diag) => {
        setUploadDiag(diag);
        if (diag.is_valid) {
          // Refresh datasets list
          fetch('/api/datasets')
            .then((res) => res.json())
            .then((data) => {
              setDatasets(data);
              setSelectedDatasetId(dsId);
              setAssetCount(Math.min(diag.num_assets, 12));
            });
        }
      })
      .catch((err) => console.error('CSV validation failed', err));
  };

  const toggleSolver = (solverKey) => {
    if (selectedSolvers.includes(solverKey)) {
      if (selectedSolvers.length > 1) {
        setSelectedSolvers(selectedSolvers.filter((s) => s !== solverKey));
      }
    } else {
      setSelectedSolvers([...selectedSolvers, solverKey]);
    }
  };

  // Prepare chart comparison data with NaN and null guardrails
  const solverChartData = runResult?.solver_results?.map((s) => ({
    name: s.solver_name.replace(' (Simulated)', '').replace(' (Transverse Mixer)', '').replace(' Classical', ''),
    objective: roundVal(s.objective_value, 4),
    ar_pct: Math.round((s.approximation_ratio ?? 0) * 100) || 0,
    feasibility_pct: Math.round((s.feasibility_rate ?? 0) * 100) || 0,
    runtime_ms: s.runtime_ms ?? 0,
    isExact: s.solver_type === 'CLASSICAL_EXACT',
    type: s.solver_type
  })) || [];

  function roundVal(v, digits = 4) {
    if (typeof v !== 'number' || isNaN(v) || !isFinite(v)) return 0;
    return parseFloat(v.toFixed(digits));
  }

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Scientific Integrity & Audit Status Banner */}
      <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5 shadow-xl relative overflow-hidden transition-all duration-300 hover:border-zinc-700">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-start gap-3.5">
            <div className="p-2.5 rounded-xl bg-zinc-950 border border-zinc-800 text-zinc-300 shrink-0 mt-0.5">
              <ShieldCheck className="h-6 w-6" />
            </div>
            <div>
              <div className="flex items-center gap-2 flex-wrap">
                <span className="text-xs font-mono font-bold tracking-wider uppercase px-2.5 py-0.5 rounded-full bg-zinc-800 text-zinc-200 border border-zinc-700">
                  Audited Research Prototype
                </span>
                <span className="text-xs font-mono font-bold tracking-wider uppercase px-2.5 py-0.5 rounded-full bg-zinc-900 text-zinc-400 border border-zinc-800">
                  Not Investment Advice
                </span>
                <span className="text-xs font-mono font-bold tracking-wider uppercase px-2.5 py-0.5 rounded-full bg-zinc-900 text-zinc-300 border border-zinc-800">
                  Simulation Mode: Exact Statevector
                </span>
              </div>
              <p className="text-xs text-zinc-400 mt-2 leading-relaxed">
                <b className="text-zinc-200">Strict Scientific Guardrail:</b> Fair classical-vs-quantum comparison on identical inputs and constraints.
                All quantum circuits run on verified Qiskit statevector simulators. <b>No quantum advantage claimed.</b>
              </p>
              {runResult?.data_fingerprint && (
                <div className="flex items-center gap-2 mt-2 font-mono text-[11px] text-zinc-400">
                  <span className="text-zinc-500">Data SHA-256:</span>
                  <span className="text-zinc-200 font-semibold">{runResult.data_fingerprint.sha256}</span>
                  <span className="text-zinc-500">• Universe:</span>
                  <span className="text-zinc-300">{runResult.data_fingerprint.asset_count} assets ({runResult.data_fingerprint.tickers.slice(0, 4).join(', ')}...)</span>
                </div>
              )}
            </div>
          </div>

          <div className="flex items-center gap-3 shrink-0 self-start md:self-center">
            <button
              onClick={handleExportBundle}
              disabled={!runResult}
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-bold bg-zinc-900 hover:bg-zinc-800 text-zinc-200 border border-zinc-700 disabled:opacity-50 transition-all duration-200 shadow-md hover:border-zinc-500"
              title="Download full JSON audit package"
            >
              <Download className="h-4 w-4 text-zinc-300" />
              Export Reproducibility Bundle
            </button>

            <button
              onClick={handleRunBenchmark}
              disabled={isRunning}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-extrabold bg-white hover:bg-zinc-200 text-black shadow-lg shadow-black disabled:opacity-50 transition-all duration-200 active:scale-95"
            >
              {isRunning ? (
                <>
                  <RefreshCw className="h-4 w-4 animate-spin" />
                  Simulating...
                </>
              ) : (
                <>
                  <Play className="h-4 w-4 fill-current" />
                  Run Benchmark Suite
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {errorMsg && (
        <div className="p-4 rounded-xl bg-zinc-950 border border-zinc-800 text-zinc-300 text-xs flex items-center gap-3">
          <AlertTriangle className="h-5 w-5 text-zinc-400 shrink-0" />
          <span><b>Execution Error:</b> {errorMsg}</span>
        </div>
      )}

      {/* Control Panel Grid */}
      <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-6 shadow-xl transition-all duration-300 hover:border-zinc-700">
        <div className="flex items-center justify-between pb-4 mb-4 border-b border-zinc-800">
          <h2 className="text-sm font-bold text-white uppercase tracking-wider font-mono flex items-center gap-2">
            <Sliders className="h-4 w-4 text-zinc-300" />
            Auditable Experiment Configuration
          </h2>
          <button
            onClick={() => setShowUploadModal(!showUploadModal)}
            className="text-xs font-semibold text-zinc-300 hover:text-white flex items-center gap-1.5 transition-colors duration-200"
          >
            <Database className="h-3.5 w-3.5" />
            {showUploadModal ? 'Hide CSV Uploader' : 'Upload Custom CSV Price Data'}
          </button>
        </div>

        {/* CSV Uploader Sub-panel */}
        {showUploadModal && (
          <div className="mb-6 p-4 rounded-xl bg-zinc-950 border border-zinc-800 space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-xs font-bold text-zinc-200 font-mono">Custom Dataset Ingestion</h3>
              <span className="text-[11px] text-zinc-500 font-mono">CSV format: Date, Asset1, Asset2...</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div className="md:col-span-2">
                <textarea
                  rows={4}
                  value={csvContent}
                  onChange={(e) => setCsvContent(e.target.value)}
                  placeholder="Date,AAPL,MSFT,NVDA&#10;2026-01-01,150.0,300.0,400.0&#10;2026-01-02,152.0,302.0,405.0..."
                  className="w-full text-xs font-mono bg-zinc-900 border border-zinc-700 rounded-lg p-2.5 text-zinc-200 focus:outline-none focus:border-zinc-400 transition-colors"
                />
              </div>
              <div className="space-y-2 flex flex-col justify-between">
                <div>
                  <label className="text-[11px] font-semibold text-zinc-400 block mb-1">Dataset ID Name</label>
                  <input
                    type="text"
                    value={customDatasetId}
                    onChange={(e) => setCustomDatasetId(e.target.value)}
                    placeholder="my_portfolio_demo"
                    className="w-full text-xs bg-zinc-900 border border-zinc-700 rounded-lg p-2 text-zinc-200 focus:outline-none focus:border-zinc-400 transition-colors"
                  />
                </div>
                <button
                  onClick={handleValidateCsv}
                  className="w-full py-2 rounded-lg text-xs font-bold bg-white hover:bg-zinc-200 text-black transition-all duration-200 shadow-sm active:scale-95"
                >
                  Validate & Load CSV
                </button>
              </div>
            </div>

            {uploadDiag && (
              <div className={`p-3 rounded-lg text-xs border ${uploadDiag.is_valid ? 'bg-zinc-900 border-zinc-700 text-zinc-200' : 'bg-zinc-950 border-zinc-700 text-zinc-400'}`}>
                {uploadDiag.is_valid ? (
                  <div className="flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-white shrink-0" />
                    <span>Validated {uploadDiag.num_assets} assets across {uploadDiag.num_observations} observations. Ready for simulation!</span>
                  </div>
                ) : (
                  <div>
                    <span className="font-bold">Validation failed:</span>
                    <ul className="list-disc pl-4 mt-1 text-[11px]">
                      {uploadDiag.errors.map((e, i) => <li key={i}>{e}</li>)}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Primary Controls */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {/* Dataset Selector */}
          <div>
            <label className="text-xs font-semibold text-zinc-300 block mb-1.5 font-mono">
              Input Equity Universe
            </label>
            <select
              value={selectedDatasetId}
              onChange={(e) => {
                setSelectedDatasetId(e.target.value);
                if (e.target.value === 'synthetic_tech_4') setAssetCount(4);
                else if (e.target.value === 'synthetic_nasdaq_8') setAssetCount(8);
                else setAssetCount(12);
              }}
              className="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-3 py-2 text-xs text-zinc-200 focus:outline-none focus:border-zinc-500 transition-colors"
            >
              {datasets.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.name} ({d.asset_count} Assets)
                </option>
              ))}
            </select>
            <span className="text-[11px] text-zinc-500 block mt-1 font-mono">Deterministic, offline-safe seed</span>
          </div>

          {/* Asset Universe Count & Cardinality */}
          <div>
            <div className="flex justify-between items-center mb-1.5">
              <label className="text-xs font-semibold text-zinc-300 font-mono">
                Asset Universe (N Qubits): <span className="text-white font-bold">{assetCount}</span>
              </label>
            </div>
            <div className="flex gap-2 mb-2">
              {[4, 6, 8, 10, 12].map((n) => (
                <button
                  key={n}
                  onClick={() => {
                    setAssetCount(n);
                    if (kCardinality >= n) setKCardinality(Math.max(1, Math.floor(n / 2)));
                  }}
                  className={`flex-1 py-1 rounded-lg text-xs font-mono font-bold border transition-all duration-200 ${
                    assetCount === n
                      ? 'bg-white text-black border-white shadow-sm font-extrabold'
                      : 'bg-zinc-950 text-zinc-400 border-zinc-800 hover:border-zinc-700 hover:text-white'
                  }`}
                >
                  {n}
                </button>
              ))}
            </div>

            <div className="flex justify-between items-center mt-2 mb-1">
              <label className="text-xs font-semibold text-zinc-300 font-mono">
                Cardinality (K Assets): <span className="text-white font-bold">{kCardinality}</span>
              </label>
            </div>
            <input
              type="range"
              min="1"
              max={Math.max(1, assetCount - 1)}
              value={kCardinality}
              onChange={(e) => setKCardinality(parseInt(e.target.value, 10))}
              className="w-full accent-zinc-200 cursor-pointer"
            />
          </div>

          {/* Risk Aversion & Covariance */}
          <div>
            <div className="flex justify-between items-center mb-1.5">
              <label className="text-xs font-semibold text-zinc-300 font-mono">
                Risk Aversion (λ): <span className="text-white font-bold">{lambdaRisk.toFixed(2)}</span>
              </label>
              <span className="text-[10px] text-zinc-500 font-mono">
                {lambdaRisk >= 0.7 ? 'Risk Averse' : lambdaRisk <= 0.3 ? 'Return Seeking' : 'Balanced'}
              </span>
            </div>
            <input
              type="range"
              min="0.0"
              max="1.0"
              step="0.05"
              value={lambdaRisk}
              onChange={(e) => setLambdaRisk(parseFloat(e.target.value))}
              className="w-full accent-zinc-200 cursor-pointer mb-3"
            />

            <label className="text-xs font-semibold text-zinc-300 block mb-1 font-mono">
              Covariance Estimator
            </label>
            <select
              value={covarianceMethod}
              onChange={(e) => setCovarianceMethod(e.target.value)}
              className="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-3 py-1.5 text-xs text-zinc-200 focus:outline-none focus:border-zinc-500 transition-colors"
            >
              <option value="ledoit_wolf">Ledoit-Wolf Shrinkage (Recommended)</option>
              <option value="sample">Sample Covariance</option>
              <option value="rmt">RMT Marchenko-Pastur Denoised</option>
            </select>
          </div>

          {/* Solvers & Depth */}
          <div>
            <div className="flex justify-between items-center mb-1.5">
              <label className="text-xs font-semibold text-zinc-300 font-mono">
                Circuit Depth (p Layers): <span className="text-white font-bold">p={circuitDepth}</span>
              </label>
            </div>
            <div className="flex gap-2 mb-3">
              {[1, 2].map((p) => (
                <button
                  key={p}
                  onClick={() => setCircuitDepth(p)}
                  className={`flex-1 py-1 rounded-lg text-xs font-bold border transition-all duration-200 ${
                    circuitDepth === p
                      ? 'bg-white text-black border-white shadow-sm font-extrabold'
                      : 'bg-zinc-950 text-zinc-400 border-zinc-800 hover:border-zinc-700 hover:text-white'
                  }`}
                >
                  p = {p} {p === 1 ? '(Fast)' : '(Optimal)'}
                </button>
              ))}
            </div>

            <label className="text-xs font-semibold text-zinc-300 block mb-1 font-mono">
              Solvers Active ({selectedSolvers.length}/6)
            </label>
            <div className="flex flex-wrap gap-1">
              {[
                { id: 'exact', label: 'Exact' },
                { id: 'annealing', label: 'Annealing' },
                { id: 'xy_qaoa', label: 'XY-QAOA' },
                { id: 'ccd_qaoa', label: 'CCD-QAOA' },
                { id: 'penalty_qaoa', label: 'Penalty' },
                { id: 'qpu_hardware', label: 'QPU Hardware' }
              ].map((s) => (
                <button
                  key={s.id}
                  onClick={() => toggleSolver(s.id)}
                  className={`text-[10px] font-mono px-2 py-0.5 rounded border transition-all duration-200 ${
                    selectedSolvers.includes(s.id)
                      ? 'bg-zinc-800 text-white border-zinc-600 font-bold shadow-sm'
                      : 'bg-zinc-950 text-zinc-500 border-zinc-800 hover:border-zinc-700 hover:text-zinc-300'
                  }`}
                >
                  {s.label}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Main Results Section */}
      {runResult && (
        <div className="space-y-6">
          {/* Headline Ground Truth vs Quantum Status Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-4 hover:border-zinc-700 transition-all duration-200">
              <span className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider block font-mono">
                Ground Truth Min Energy (Exact)
              </span>
              <div className="text-2xl font-mono font-extrabold text-white mt-1">
                {runResult.ground_truth?.e_min?.toFixed(5)}
              </div>
              <span className="text-[11px] text-zinc-400 mt-1 block">
                Optimal: <b className="text-zinc-200">{runResult.ground_truth?.optimal_tickers?.join(', ')}</b>
              </span>
            </div>

            <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-4 hover:border-zinc-700 transition-all duration-200">
              <span className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider block font-mono">
                Selected Portfolio (SLSQP Weights)
              </span>
              <div className="text-2xl font-mono font-extrabold text-zinc-100 mt-1">
                {runResult.selected_portfolio?.expected_return_pct}% <span className="text-xs text-zinc-400">Exp. Ret</span>
              </div>
              <span className="text-[11px] text-zinc-400 mt-1 block">
                Vol: <b className="text-zinc-200">{runResult.selected_portfolio?.annualized_vol_pct}%</b> • Sharpe: <b className="text-zinc-200">{runResult.selected_portfolio?.theoretical_sharpe}</b>
              </span>
            </div>

            <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-4 hover:border-zinc-700 transition-all duration-200">
              <span className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider block font-mono">
                Net 5 bps Walk-Forward Value
              </span>
              <div className="text-2xl font-mono font-extrabold text-zinc-200 mt-1">
                ${runResult.backtest?.final_portfolio_value}
              </div>
              <span className="text-[11px] text-zinc-400 mt-1 block">
                Benchmark EW: <b className="text-zinc-200">${runResult.backtest?.benchmark_final_value}</b> • Net Sharpe: <b className="text-zinc-200">{runResult.backtest?.net_sharpe_ratio}</b>
              </span>
            </div>

            <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-4 hover:border-zinc-700 transition-all duration-200">
              <span className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider block font-mono">
                Constraint Preservation
              </span>
              <div className="text-2xl font-mono font-extrabold text-white mt-1">
                100% <span className="text-xs text-zinc-400">Dicke Subspace</span>
              </div>
              <span className="text-[11px] text-zinc-400 mt-1 block">
                Penalty-QAOA Leakage: <b className="text-zinc-300">{roundVal(100 - (runResult.solver_results.find(s => s.solver_name.includes('Penalty'))?.feasibility_rate || 1) * 100, 1)}%</b>
              </span>
            </div>
          </div>

          {/* Comparative Benchmark Table */}
          <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-6 shadow-xl overflow-x-auto hover:border-zinc-700 transition-all duration-300">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider font-mono mb-4 flex items-center gap-2">
              <BarChart3 className="h-4 w-4 text-zinc-300" />
              Auditable Solver Benchmark Comparison Table (Identical Inputs)
            </h3>
            <table className="w-full text-left text-xs border-collapse font-mono">
              <thead>
                <tr className="border-b border-zinc-800 text-zinc-400 font-semibold font-mono">
                  <th className="py-2.5 px-3">Solver</th>
                  <th className="py-2.5 px-3">Type</th>
                  <th className="py-2.5 px-3">Selected Assets</th>
                  <th className="py-2.5 px-3 text-right">Objective f(x)</th>
                  <th className="py-2.5 px-3 text-right">Feasibility</th>
                  <th className="py-2.5 px-3 text-right">Approx. Ratio (AR)</th>
                  <th className="py-2.5 px-3 text-right">P(opt)</th>
                  <th className="py-2.5 px-3 text-right">Runtime</th>
                  <th className="py-2.5 px-3 text-right">Quantum Resources</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800/60 font-mono">
                {runResult.solver_results?.map((s, idx) => {
                  const isExact = s.solver_type === 'CLASSICAL_EXACT';
                  const isCCD = s.solver_name.includes('CCD');
                  const isPenalty = s.solver_name.includes('Penalty');

                  return (
                    <tr
                      key={idx}
                      className={`hover:bg-zinc-800/40 transition-colors ${
                        isExact
                          ? 'bg-zinc-900/60'
                          : isCCD
                          ? 'bg-zinc-800/40 font-semibold'
                          : isPenalty
                          ? 'bg-zinc-950/60'
                          : ''
                      }`}
                    >
                      <td className="py-3 px-3 font-sans font-bold text-zinc-200 flex items-center gap-2">
                        {isExact && <Award className="h-4 w-4 text-white shrink-0" />}
                        {isCCD && <Cpu className="h-4 w-4 text-zinc-300 shrink-0" />}
                        {s.solver_name}
                      </td>
                      <td className="py-3 px-3 text-[11px]">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                          s.solver_type === 'CLASSICAL_EXACT'
                            ? 'bg-zinc-800 text-white border border-zinc-700'
                            : s.solver_type === 'CLASSICAL_HEURISTIC'
                            ? 'bg-zinc-900 text-zinc-300 border border-zinc-800'
                            : 'bg-zinc-800/80 text-zinc-200 border border-zinc-700'
                        }`}>
                          {s.solver_type}
                        </span>
                      </td>
                      <td className="py-3 px-3 text-zinc-300 font-sans font-semibold">
                        {s.selected_tickers?.join(', ')}
                      </td>
                      <td className="py-3 px-3 text-right font-bold text-zinc-100">
                        {s.objective_value?.toFixed(5)}
                      </td>
                      <td className="py-3 px-3 text-right font-bold">
                        <span className={s.feasibility_rate >= 0.99 ? 'text-white' : 'text-zinc-500'}>
                          {(s.feasibility_rate * 100).toFixed(1)}%
                        </span>
                      </td>
                      <td className="py-3 px-3 text-right font-bold text-white">
                        {(s.approximation_ratio * 100).toFixed(2)}%
                      </td>
                      <td className="py-3 px-3 text-right text-zinc-300">
                        {(s.optimal_probability * 100).toFixed(1)}%
                      </td>
                      <td className="py-3 px-3 text-right text-zinc-400">
                        {s.runtime_ms} ms
                      </td>
                      <td className="py-3 px-3 text-right text-[11px] text-zinc-400">
                        {s.qubits_used ? `${s.qubits_used}Q • Depth ${s.circuit_depth} • ${s.two_qubit_gates || 0} 2Q` : 'Classical CPU'}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>

          {/* Visual Benchmark Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Objective & Approximation Ratio Chart */}
            <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-6 shadow-xl hover:border-zinc-700 transition-all duration-300">
              <h4 className="text-xs font-bold text-zinc-200 uppercase tracking-wider font-mono mb-4 flex items-center justify-between">
                <span>Approximation Ratio vs Exact Optimum (%)</span>
                <span className="text-[11px] font-mono text-white">Ground Truth = 100%</span>
              </h4>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={solverChartData} margin={{ top: 10, right: 10, left: -10, bottom: 25 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
                    <XAxis
                      dataKey="name"
                      stroke="#71717a"
                      fontSize={10}
                      tickLine={false}
                      angle={-15}
                      textAnchor="end"
                      fontFamily="JetBrains Mono"
                    />
                    <YAxis stroke="#71717a" fontSize={10} domain={[0, 105]} fontFamily="JetBrains Mono" />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#09090b', borderColor: '#27272a', borderRadius: '0.75rem', fontSize: '12px' }}
                    />
                    <Bar dataKey="ar_pct" name="Approx Ratio (%)" radius={[6, 6, 0, 0]}>
                      {solverChartData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={
                            entry.isExact
                              ? '#ffffff'
                              : entry.name.includes('CCD')
                              ? '#e4e4e7'
                              : entry.name.includes('XY')
                              ? '#a1a1aa'
                              : entry.name.includes('Penalty')
                              ? '#52525b'
                              : '#71717a'
                          }
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Feasibility & Constraint Violation Chart */}
            <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-6 shadow-xl hover:border-zinc-700 transition-all duration-300">
              <h4 className="text-xs font-bold text-zinc-200 uppercase tracking-wider font-mono mb-4 flex items-center justify-between">
                <span>Feasibility Rate: Hamming-Weight Preservation (%)</span>
                <span className="text-[11px] font-mono text-zinc-300">Target = 100%</span>
              </h4>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={solverChartData} margin={{ top: 10, right: 10, left: -10, bottom: 25 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
                    <XAxis
                      dataKey="name"
                      stroke="#71717a"
                      fontSize={10}
                      tickLine={false}
                      angle={-15}
                      textAnchor="end"
                      fontFamily="JetBrains Mono"
                    />
                    <YAxis stroke="#71717a" fontSize={10} domain={[0, 105]} fontFamily="JetBrains Mono" />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#09090b', borderColor: '#27272a', borderRadius: '0.75rem', fontSize: '12px' }}
                    />
                    <Bar dataKey="feasibility_pct" name="Feasibility (%)" fill="#ffffff" radius={[6, 6, 0, 0]}>
                      {solverChartData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={entry.feasibility_pct >= 99 ? '#ffffff' : '#52525b'}
                        />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Basis State Probability Distribution (Dicke Subspace vs Penalty Leakage) */}
          {runResult.solver_results?.find(s => s.state_distribution)?.state_distribution && (
            <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-6 shadow-xl hover:border-zinc-700 transition-all duration-300">
              <h4 className="text-xs font-bold text-zinc-200 uppercase tracking-wider font-mono mb-4 flex items-center justify-between">
                <span>Quantum Computational Basis State Energy Spectrum (Hamming Weight K={kCardinality})</span>
                <span className="text-[11px] font-mono text-white">Ground State Concentration</span>
              </h4>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart
                    data={runResult.solver_results.find(s => s.solver_name.includes('CCD') || s.solver_name.includes('XY'))?.state_distribution || []}
                    margin={{ top: 10, right: 10, left: -10, bottom: 10 }}
                  >
                    <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
                    <XAxis dataKey="bitstring" stroke="#71717a" fontSize={10} fontFamily="JetBrains Mono" />
                    <YAxis stroke="#71717a" fontSize={10} fontFamily="JetBrains Mono" />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#09090b', borderColor: '#27272a', borderRadius: '0.75rem', fontSize: '12px' }}
                    />
                    <Bar dataKey="probability" name="Probability Mass" fill="#ffffff" radius={[6, 6, 0, 0]}>
                      {(runResult.solver_results.find(s => s.solver_name.includes('CCD') || s.solver_name.includes('XY'))?.state_distribution || []).map((entry, idx) => (
                        <Cell key={`bar-${idx}`} fill={entry.is_optimal ? '#ffffff' : '#52525b'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
