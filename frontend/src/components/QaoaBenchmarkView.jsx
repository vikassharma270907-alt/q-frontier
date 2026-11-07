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

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Interactive Controls & QCL Regime Sensor Status */}
      <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-6">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div className="flex-1">
            <h2 className="text-sm font-bold text-white flex items-center gap-2 uppercase tracking-wider font-mono">
              <Zap className="h-4 w-4 text-zinc-300" />
              Quantum Circuit Parameter Controls
            </h2>
            <p className="text-xs text-zinc-400 mt-0.5">
              Trotterized Counterdiabatic driving (H_CD) with Dicke state |D_2^4⟩ initialization.
            </p>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-4">
              <div>
                <label className="text-xs font-semibold text-zinc-300 block mb-1">
                  Circuit Depth (p Layers)
                </label>
                <div className="flex gap-2">
                  {[1, 2].map((p) => (
                    <button
                      key={p}
                      onClick={() => setParams({ ...params, depth: p })}
                      className={`px-3 py-1.5 rounded-lg text-xs font-bold border transition-all duration-200 ${
                        params.depth === p
                          ? 'bg-white text-black border-white font-extrabold shadow-sm'
                          : 'bg-zinc-950 text-zinc-400 border-zinc-800 hover:border-zinc-700 hover:text-white'
                      }`}
                    >
                      p = {p} {p === 1 ? '(Fast)' : '(Optimal)'}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-xs font-semibold text-zinc-300 block mb-1">
                  Turnover Continuity Bonus (κ)
                </label>
                <input
                  type="range"
                  min="0.0"
                  max="0.2"
                  step="0.01"
                  value={params.continuity_bonus}
                  onChange={(e) => setParams({ ...params, continuity_bonus: parseFloat(e.target.value) })}
                  className="w-full accent-zinc-200"
                />
                <span className="text-[11px] font-mono text-zinc-400">{params.continuity_bonus.toFixed(2)}</span>
              </div>

              <div>
                <label className="text-xs font-semibold text-zinc-300 block mb-1">
                  Dynamic QCL Regime Sensor
                </label>
                <button
                  onClick={() => setParams({ ...params, use_qcl_sensor: !params.use_qcl_sensor })}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold border transition-all duration-200 ${
                    params.use_qcl_sensor
                      ? 'bg-zinc-800 text-white border-zinc-600'
                      : 'bg-zinc-950 text-zinc-500 border-zinc-800 hover:text-zinc-300'
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
              className="px-6 py-3 rounded-xl bg-white hover:bg-zinc-200 text-black font-bold text-xs tracking-wider uppercase font-mono shadow-md transition-all duration-200 flex items-center gap-2 disabled:opacity-50 active:scale-95"
            >
              <Zap className="h-4 w-4" />
              {loading ? "Simulating Quantum Evolution..." : "Run Quantum Rebalance"}
            </button>
          </div>
        </div>

        {/* QCL Volatility Readout */}
        <div className="mt-4 pt-4 border-t border-zinc-800/80 flex flex-wrap items-center gap-6 text-xs">
          <div className="flex items-center gap-2">
            <Gauge className="h-4 w-4 text-zinc-400" />
            <span className="text-zinc-400">Predicted Rough Volatility:</span>
            <span className="font-mono font-bold text-white">
              {regime_sensor.predicted_volatility}%
            </span>
          </div>
          <div className="flex items-center gap-2">
            <ShieldCheck className="h-4 w-4 text-zinc-400" />
            <span className="text-zinc-400">Dynamic Risk Aversion (q_t):</span>
            <span className="font-mono font-bold text-white">
              {regime_sensor.dynamic_q_risk}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-zinc-400">CAF Cross-Cluster Risk Reduction:</span>
            <span className="font-mono font-bold text-zinc-300">
              -{caf_metrics.risk_reduction_pct}%
            </span>
          </div>
        </div>
      </div>

      {/* Solver Benchmarks 3-Card Comparison */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5 hover:border-zinc-700 transition-all duration-200">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-mono font-bold text-zinc-400 uppercase tracking-wider">
              Penalty-QAOA (Standard)
            </span>
            <AlertTriangle className="h-4 w-4 text-zinc-500" />
          </div>
          <div className="text-3xl font-extrabold text-zinc-300 font-mono">
            {Math.round(penalty_qaoa.approximation_ratio * 100)}%
          </div>
          <p className="text-[11px] text-zinc-500 mt-1 font-mono">Approximation Ratio</p>
          <div className="mt-4 pt-4 border-t border-zinc-800/80 space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-zinc-400">Feasible Shots (|z|=2):</span>
              <span className="font-mono text-zinc-300 font-bold">{Math.round(penalty_qaoa.feasibility * 100)}%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-zinc-400">Infeasible Shot Leakage:</span>
              <span className="font-mono text-zinc-400 font-bold">{Math.round((1 - penalty_qaoa.feasibility) * 100)}%</span>
            </div>
          </div>
        </div>

        <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5 hover:border-zinc-700 transition-all duration-200">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-mono font-bold text-zinc-400 uppercase tracking-wider">
              Standard XY-QAOA
            </span>
            <CheckCircle2 className="h-4 w-4 text-zinc-400" />
          </div>
          <div className="text-3xl font-extrabold text-zinc-200 font-mono">
            {Math.round(xy_qaoa.approximation_ratio * 100)}%
          </div>
          <p className="text-[11px] text-zinc-500 mt-1 font-mono">Approximation Ratio</p>
          <div className="mt-4 pt-4 border-t border-zinc-800/80 space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-zinc-400">Feasible Shots (|z|=2):</span>
              <span className="font-mono text-zinc-300 font-bold">100.0%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-zinc-400">Ground State P(x*):</span>
              <span className="font-mono text-zinc-300 font-bold">{Math.round(xy_qaoa.optimal_probability * 100)}%</span>
            </div>
          </div>
        </div>

        <div className="bg-zinc-900 border border-zinc-600 rounded-2xl p-5 shadow-xl shadow-black transition-all duration-200">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-mono font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
              <Zap className="h-3.5 w-3.5" /> CCD-QAOA (Q-FRONTIER)
            </span>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-800 text-zinc-200 border border-zinc-700">
              AGP Shortcuts
            </span>
          </div>
          <div className="text-3xl font-extrabold text-white font-mono">
            {Math.round(ccd_qaoa.approximation_ratio * 100)}%
          </div>
          <p className="text-[11px] text-zinc-400 mt-1 font-mono">Approximation Ratio (Near-Unitary)</p>
          <div className="mt-4 pt-4 border-t border-zinc-800 space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-zinc-300">Feasible Shots:</span>
              <span className="font-mono text-white font-bold">100.0% (Zero Leakage)</span>
            </div>
            <div className="flex justify-between">
              <span className="text-zinc-300">Ground State P(x*):</span>
              <span className="font-mono text-white font-bold">{Math.round(ccd_qaoa.optimal_probability * 100)}%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Statevector Probability Distribution Chart */}
      <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-6">
        <h3 className="text-sm font-bold text-white mb-1 uppercase tracking-wider font-mono">
          Cluster Statevector Probability Distribution (6 Feasible |z|=2 Subspace States)
        </h3>
        <p className="text-xs text-zinc-400 mb-4">
          Comparing sampling probabilities across computational basis states.
        </p>

        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={state_distribution}>
              <XAxis dataKey="bitstring" stroke="#71717a" fontSize={11} fontFamily="JetBrains Mono" />
              <YAxis stroke="#71717a" fontSize={11} domain={[0, 1]} tickFormatter={(v) => `${Math.round(v * 100)}%`} />
              <Tooltip
                contentStyle={{ backgroundColor: "#09090b", borderColor: "#27272a", fontSize: 12, borderRadius: 8 }}
                formatter={(val, name) => [`${(val * 100).toFixed(1)}%`, name]}
              />
              <Legend />
              <Bar dataKey="p_ccd" name="CCD-QAOA (Counterdiabatic)" fill="#ffffff" radius={[4, 4, 0, 0]} />
              <Bar dataKey="p_xy" name="Standard XY-QAOA" fill="#a1a1aa" radius={[4, 4, 0, 0]} />
              <Bar dataKey="p_penalty" name="Penalty-QAOA" fill="#52525b" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
