import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, Legend
} from 'recharts';
import { Zap, CheckCircle2, AlertTriangle, ShieldCheck, Gauge } from 'lucide-react';

export default function QaoaBenchmarkView({
  optimizationResult,
  loading,
  onRunOptimization,
  params,
  setParams
}) {
  if (!optimizationResult) return null;

  const { quantum_solver_benchmark, regime_sensor, caf_metrics } = optimizationResult;
  const { ccd_qaoa, xy_qaoa, penalty_qaoa, state_distribution } = quantum_solver_benchmark;

  const comparisonData = [
    {
      name: "Penalty-QAOA",
      ar: Math.round(penalty_qaoa.approximation_ratio * 100),
      feas: Math.round(penalty_qaoa.feasibility * 100),
      optProb: Math.round(penalty_qaoa.optimal_probability * 100),
      fill: "#f43f5e"
    },
    {
      name: "Standard XY-QAOA",
      ar: Math.round(xy_qaoa.approximation_ratio * 100),
      feas: Math.round(xy_qaoa.feasibility * 100),
      optProb: Math.round(xy_qaoa.optimal_probability * 100),
      fill: "#6366f1"
    },
    {
      name: "CCD-QAOA (Ours)",
      ar: Math.round(ccd_qaoa.approximation_ratio * 100),
      feas: Math.round(ccd_qaoa.feasibility * 100),
      optProb: Math.round(ccd_qaoa.optimal_probability * 100),
      fill: "#06b6d4"
    }
  ];

  return (
    <div className="space-y-6">
      {/* Interactive Controls & QCL Regime Sensor Status */}
      <div className="bg-[#0f172a]/80 border border-slate-800 rounded-2xl p-6">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div className="flex-1">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Zap className="h-5 w-5 text-cyan-400" />
              Quantum Circuit Parameter Controls
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Trotterized Counterdiabatic driving (H_CD) with Dicke state |D_2^4⟩ initialization.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-4">
              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">
                  Circuit Depth (p Layers)
                </label>
                <div className="flex gap-2">
                  {[1, 2].map((p) => (
                    <button
                      key={p}
                      onClick={() => setParams({ ...params, depth: p })}
                      className={`px-3 py-1.5 rounded-lg text-xs font-bold border transition-colors ${
                        params.depth === p
                          ? 'bg-cyan-500 text-black border-cyan-400 font-extrabold shadow-md shadow-cyan-500/20'
                          : 'bg-slate-800 text-slate-300 border-slate-700 hover:bg-slate-700'
                      }`}
                    >
                      p = {p} {p === 1 ? '(Fast)' : '(Optimal)'}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">
                  Turnover Continuity Bonus (κ)
                </label>
                <input
                  type="range"
                  min="0.0"
                  max="0.2"
                  step="0.01"
                  value={params.continuity_bonus}
                  onChange={(e) => setParams({ ...params, continuity_bonus: parseFloat(e.target.value) })}
                  className="w-full accent-cyan-400"
                />
                <span className="text-[11px] font-mono text-cyan-300">{params.continuity_bonus.toFixed(2)}</span>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-300 block mb-1">
                  Dynamic QCL Regime Sensor
                </label>
                <button
                  onClick={() => setParams({ ...params, use_qcl_sensor: !params.use_qcl_sensor })}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold border transition-colors ${
                    params.use_qcl_sensor
                      ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40'
                      : 'bg-slate-800 text-slate-400 border-slate-700'
                  }`}
                >
                  {params.use_qcl_sensor ? "Enabled (Adaptive q_t)" : "Fixed Risk Aversion"}
                </button>
              </div>
            </div>
          </div>

          <div className="flex flex-col items-start lg:items-end justify-center">
            <button
              disabled={loading}
              onClick={onRunOptimization}
              className="px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-indigo-600 hover:from-cyan-400 hover:to-indigo-500 text-white font-bold text-sm shadow-lg shadow-cyan-500/25 transition-all flex items-center gap-2 disabled:opacity-50"
            >
              <Zap className="h-4 w-4" />
              {loading ? "Simulating Quantum Evolution..." : "Run Quantum Rebalance"}
            </button>
          </div>
        </div>

        {/* QCL Volatility Readout */}
        <div className="mt-4 pt-4 border-t border-slate-800/80 flex flex-wrap items-center gap-6 text-xs">
          <div className="flex items-center gap-2">
            <Gauge className="h-4 w-4 text-emerald-400" />
            <span className="text-slate-400">Predicted Rough Volatility:</span>
            <span className="font-mono font-bold text-emerald-300">
              {regime_sensor.predicted_volatility}%
            </span>
          </div>
          <div className="flex items-center gap-2">
            <ShieldCheck className="h-4 w-4 text-cyan-400" />
            <span className="text-slate-400">Dynamic Risk Aversion (q_t):</span>
            <span className="font-mono font-bold text-cyan-300">
              {regime_sensor.dynamic_q_risk}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-slate-400">CAF Cross-Cluster Risk Reduction:</span>
            <span className="font-mono font-bold text-indigo-300">
              -{caf_metrics.risk_reduction_pct}%
            </span>
          </div>
        </div>
      </div>

      {/* Solver Benchmarks 3-Card Comparison */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-[#0f172a]/70 border border-rose-500/20 rounded-2xl p-5">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-rose-400 uppercase tracking-wider">
              Penalty-QAOA (Standard)
            </span>
            <AlertTriangle className="h-4 w-4 text-rose-400" />
          </div>
          <div className="text-3xl font-extrabold text-white font-mono">
            {Math.round(penalty_qaoa.approximation_ratio * 100)}%
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Approximation Ratio</p>
          <div className="mt-4 pt-4 border-t border-slate-800/80 space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-400">Feasible Shots (|z|=2):</span>
              <span className="font-mono text-rose-300 font-bold">{Math.round(penalty_qaoa.feasibility * 100)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Infeasible Shot Leakage:</span>
              <span className="font-mono text-rose-400 font-bold">{Math.round((1 - penalty_qaoa.feasibility) * 100)}%</span>
            </div>
          </div>
        </div>

        <div className="bg-[#0f172a]/70 border border-indigo-500/20 rounded-2xl p-5">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-indigo-400 uppercase tracking-wider">
              Standard XY-QAOA
            </span>
            <CheckCircle2 className="h-4 w-4 text-indigo-400" />
          </div>
          <div className="text-3xl font-extrabold text-white font-mono">
            {Math.round(xy_qaoa.approximation_ratio * 100)}%
          </div>
          <p className="text-[11px] text-slate-400 mt-1">Approximation Ratio</p>
          <div className="mt-4 pt-4 border-t border-slate-800/80 space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-400">Feasible Shots (|z|=2):</span>
              <span className="font-mono text-indigo-300 font-bold">100.0%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-400">Ground State P(x*):</span>
              <span className="font-mono text-indigo-300 font-bold">{Math.round(xy_qaoa.optimal_probability * 100)}%</span>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-b from-cyan-950/40 to-[#0f172a] border border-cyan-500/40 rounded-2xl p-5 shadow-lg shadow-cyan-500/10">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
              <Zap className="h-3.5 w-3.5" /> CCD-QAOA (Q-FRONTIER)
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-900/60 text-cyan-200">
              AGP Shortcuts
            </span>
          </div>
          <div className="text-3xl font-extrabold text-white font-mono">
            {Math.round(ccd_qaoa.approximation_ratio * 100)}%
          </div>
          <p className="text-[11px] text-cyan-300 mt-1">Approximation Ratio (Near-Unitary)</p>
          <div className="mt-4 pt-4 border-t border-slate-800/80 space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-300">Feasible Shots:</span>
              <span className="font-mono text-emerald-400 font-bold">100.0% (Zero Leakage)</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-300">Ground State P(x*):</span>
              <span className="font-mono text-cyan-300 font-bold">{Math.round(ccd_qaoa.optimal_probability * 100)}%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Statevector Probability Distribution Chart */}
      <div className="bg-[#0f172a]/60 border border-slate-800 rounded-2xl p-6">
        <h3 className="text-md font-bold text-white mb-1">
          Cluster Statevector Probability Distribution (6 Feasible |z|=2 Subspace States)
        </h3>
        <p className="text-xs text-slate-400 mb-4">
          Comparing sampling probabilities across computational basis states. Green badge indicates exact optimal asset pair.
        </p>

        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={state_distribution}>
              <XAxis dataKey="bitstring" stroke="#64748b" fontSize={11} fontFamily="JetBrains Mono" />
              <YAxis stroke="#64748b" fontSize={11} domain={[0, 1]} tickFormatter={(v) => `${Math.round(v * 100)}%`} />
              <Tooltip
                contentStyle={{ backgroundColor: "#0f172a", borderColor: "#1e293b", fontSize: 12 }}
                formatter={(val, name) => [`${(val * 100).toFixed(1)}%`, name]}
              />
              <Legend />
              <Bar dataKey="p_ccd" name="CCD-QAOA (Counterdiabatic)" fill="#06b6d4" radius={[4, 4, 0, 0]} />
              <Bar dataKey="p_xy" name="Standard XY-QAOA" fill="#6366f1" radius={[4, 4, 0, 0]} />
              <Bar dataKey="p_penalty" name="Penalty-QAOA" fill="#f43f5e" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
