import React, { useState, useEffect } from 'react';
import {
  Cpu, Grid, Layers, ShieldCheck, Play, RefreshCw, CheckCircle2,
  AlertCircle, BarChart3, Radio
} from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, CartesianGrid
} from 'recharts';

export default function VolumetricView() {
  const [benchmarks, setBenchmarks] = useState(null);
  const [loading, setLoading] = useState(true);

  // Live QPU execution state
  const [selectedBackend, setSelectedBackend] = useState('ionq');
  const [qpuQubits, setQpuQubits] = useState(4);
  const [qpuDepth, setQpuDepth] = useState(1);
  const [qpuShots, setQpuShots] = useState(1024);
  const [isSubmittingQPU, setIsSubmittingQPU] = useState(false);
  const [qpuJobResult, setQpuJobResult] = useState(null);
  const [qpuError, setQpuError] = useState(null);

  useEffect(() => {
    fetch('/api/hardware/benchmarks')
      .then((res) => res.json())
      .then((data) => {
        setBenchmarks(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to load hardware benchmarks", err);
        setLoading(false);
      });
  }, []);

  const handleExecuteQPU = () => {
    setIsSubmittingQPU(true);
    setQpuError(null);

    const payload = {
      backend_target: selectedBackend,
      n_qubits: qpuQubits,
      k_cardinality: Math.max(1, Math.floor(qpuQubits / 2)),
      circuit_depth: qpuDepth,
      shots: qpuShots
    };

    fetch('/api/hardware/execute-qpu', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
      .then(async (res) => {
        if (!res.ok) {
          const errData = await res.json();
          throw new Error(errData.detail || 'QPU execution error');
        }
        return res.json();
      })
      .then((data) => {
        setQpuJobResult(data);
        setIsSubmittingQPU(false);
      })
      .catch((err) => {
        console.error("QPU execution failed", err);
        setQpuError(err.message);
        setIsSubmittingQPU(false);
      });
  };

  if (loading || !benchmarks) {
    return <div className="p-8 text-center text-slate-400">Loading Sandia & IonQ Hardware Benchmarks...</div>;
  }

  const { hardware_comparison, sandia_volumetric_grid } = benchmarks;
  const { ionq_trapped_ion, ibm_heavy_hex } = hardware_comparison;

  const widths = [4, 6, 8, 12];
  const depths = [1, 2, 3, 4, 5];

  // Prepare chart data for QPU shot distribution
  const shotCountsChartData = qpuJobResult?.raw_shot_counts
    ? Object.entries(qpuJobResult.raw_shot_counts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 8)
        .map(([bitstring, count]) => ({
          bitstring,
          count,
          prob: ((count / qpuJobResult.shots) * 100).toFixed(1),
          isFeasible: bitstring.split('').filter((c) => c === '1').length === qpuJobResult.selected_indices.length
        }))
    : [];

  return (
    <div className="space-y-6">
      {/* IonQ vs IBM Architecture Comparison Banner */}
      <div className="bg-[#0f172a]/80 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <h2 className="text-lg font-bold text-white flex items-center gap-2 mb-1">
          <Cpu className="h-5 w-5 text-purple-400" />
          Hardware Transpilation Audit: IonQ Trapped-Ion vs. IBM Heavy-Hex
        </h2>
        <p className="text-xs text-slate-400 mb-6">
          Transpiling complete-graph XY mixer ($H_M^{{XY}}$) and 3-body AGP counterdiabatic terms across distinct hardware coupling topologies.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-purple-950/20 border border-purple-500/30 rounded-xl p-5 shadow-lg">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-bold text-purple-300">IonQ Trapped-Ion</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-purple-900/60 text-purple-200">
                All-to-All Native (K_n)
              </span>
            </div>
            <div className="space-y-3 text-xs">
              <div className="flex justify-between border-b border-purple-500/10 pb-2">
                <span className="text-slate-400">Routing SWAP Overhead:</span>
                <span className="font-mono text-emerald-400 font-extrabold text-sm">
                  {ionq_trapped_ion.routing_swaps} SWAPs (Zero Overhead)
                </span>
              </div>
              <div className="flex justify-between border-b border-purple-500/10 pb-2">
                <span className="text-slate-400">Total 2-Qubit Gates:</span>
                <span className="font-mono text-purple-200 font-bold">{ionq_trapped_ion.two_qubit_gates}</span>
              </div>
              <div className="flex justify-between border-b border-purple-500/10 pb-2">
                <span className="text-slate-400">Circuit Depth:</span>
                <span className="font-mono text-purple-200 font-bold">{ionq_trapped_ion.circuit_depth}</span>
              </div>
              <div className="flex justify-between pt-1">
                <span className="text-slate-400">Fidelity Status:</span>
                <span className="text-emerald-300 font-medium">{ionq_trapped_ion.decoherence_risk}</span>
              </div>
            </div>
          </div>

          <div className="bg-indigo-950/20 border border-indigo-500/30 rounded-xl p-5 shadow-lg">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-bold text-indigo-300">IBM Heavy-Hex (Superconducting)</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-indigo-900/60 text-indigo-200">
                Sparse Planar Grid
              </span>
            </div>
            <div className="space-y-3 text-xs">
              <div className="flex justify-between border-b border-indigo-500/10 pb-2">
                <span className="text-slate-400">Routing SWAP Overhead:</span>
                <span className="font-mono text-rose-400 font-extrabold text-sm">
                  +{ibm_heavy_hex.routing_swaps} Additional SWAPs
                </span>
              </div>
              <div className="flex justify-between border-b border-indigo-500/10 pb-2">
                <span className="text-slate-400">Total 2-Qubit Gates:</span>
                <span className="font-mono text-indigo-200 font-bold">{ibm_heavy_hex.two_qubit_gates} (Inflated)</span>
              </div>
              <div className="flex justify-between border-b border-indigo-500/10 pb-2">
                <span className="text-slate-400">Circuit Depth:</span>
                <span className="font-mono text-indigo-200 font-bold">{ibm_heavy_hex.circuit_depth}</span>
              </div>
              <div className="flex justify-between pt-1">
                <span className="text-slate-400">Fidelity Status:</span>
                <span className="text-rose-300 font-medium">{ibm_heavy_hex.decoherence_risk}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Interactive QPU Execution Subsystem */}
      <div className="bg-[#0f172a]/90 border border-cyan-800/50 rounded-2xl p-6 shadow-xl">
        <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-800">
          <div>
            <h2 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
              <Radio className="h-4 w-4 text-cyan-400" />
              Direct Hardware QPU Job Execution & Calibration
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Execute parameterized QAOA circuits on hardware coupling topologies with real device noise models.
            </p>
          </div>
          <span className="text-[10px] font-mono px-2 py-1 rounded bg-cyan-950 text-cyan-300 border border-cyan-800">
            Mode: SIMULATED_NOISE_QPU
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-5">
          <div>
            <label className="text-xs font-semibold text-slate-300 block mb-1">Target QPU Architecture</label>
            <select
              value={selectedBackend}
              onChange={(e) => setSelectedBackend(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
            >
              <option value="ionq">IonQ Trapped-Ion (aria-1)</option>
              <option value="ibm">IBM Heavy-Hex (ibm_sherbrooke)</option>
              <option value="quantum_rings">Quantum Rings Virtual QPU</option>
              <option value="sandia">Sandia Volumetric Depolarizing</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-300 block mb-1">Qubits (Width N)</label>
            <select
              value={qpuQubits}
              onChange={(e) => setQpuQubits(parseInt(e.target.value, 10))}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-slate-200"
            >
              <option value="4">4 Qubits (Subproblem)</option>
              <option value="6">6 Qubits</option>
              <option value="8">8 Qubits</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-300 block mb-1">Circuit Depth (p)</label>
            <div className="flex gap-2">
              {[1, 2].map((p) => (
                <button
                  key={p}
                  onClick={() => setQpuDepth(p)}
                  className={`flex-1 py-1.5 rounded-lg text-xs font-bold border ${
                    qpuDepth === p
                      ? 'bg-cyan-500 text-black border-cyan-400'
                      : 'bg-slate-900 text-slate-400 border-slate-700'
                  }`}
                >
                  p = {p}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-300 block mb-1">Measurement Shots</label>
            <div className="flex gap-2">
              {[500, 1024, 2048].map((s) => (
                <button
                  key={s}
                  onClick={() => setQpuShots(s)}
                  className={`flex-1 py-1.5 rounded-lg text-xs font-mono font-bold border ${
                    qpuShots === s
                      ? 'bg-cyan-500 text-black border-cyan-400'
                      : 'bg-slate-900 text-slate-400 border-slate-700'
                  }`}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        </div>

        <button
          onClick={handleExecuteQPU}
          disabled={isSubmittingQPU}
          className="flex items-center gap-2 px-6 py-2.5 rounded-xl text-xs font-extrabold bg-gradient-to-r from-purple-500 to-indigo-600 hover:from-purple-400 hover:to-indigo-500 text-white shadow-lg shadow-purple-500/20 disabled:opacity-50 transition-all mb-4"
        >
          {isSubmittingQPU ? (
            <>
              <RefreshCw className="h-4 w-4 animate-spin" />
              Submitting to QPU Device...
            </>
          ) : (
            <>
              <Play className="h-4 w-4 fill-current" />
              Submit QPU Benchmark Job
            </>
          )}
        </button>

        {qpuError && (
          <div className="p-3 rounded-xl bg-red-950/60 border border-red-800 text-red-300 text-xs">
            {qpuError}
          </div>
        )}

        {qpuJobResult && (
          <div className="mt-4 p-5 rounded-xl bg-slate-950/90 border border-cyan-800/40 space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                <span className="text-xs font-bold text-white">
                  Job Completed: <span className="font-mono text-cyan-400">{qpuJobResult.job_id}</span>
                </span>
              </div>
              <div className="text-[11px] font-mono text-slate-400">
                Backend: <b className="text-slate-200">{qpuJobResult.backend_name}</b> ({qpuJobResult.provider}) • {qpuJobResult.shots} Shots
              </div>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
              <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
                <span className="text-[10px] text-slate-400 block">Measured Feasibility</span>
                <span className="text-lg font-mono font-bold text-emerald-400">
                  {(qpuJobResult.measured_feasibility * 100).toFixed(1)}%
                </span>
              </div>
              <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
                <span className="text-[10px] text-slate-400 block">Measured Approx. Ratio</span>
                <span className="text-lg font-mono font-bold text-cyan-400">
                  {(qpuJobResult.measured_approximation_ratio * 100).toFixed(1)}%
                </span>
              </div>
              <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
                <span className="text-[10px] text-slate-400 block">Routing SWAP Gates</span>
                <span className="text-lg font-mono font-bold text-purple-400">
                  {qpuJobResult.routing_swaps}
                </span>
              </div>
              <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
                <span className="text-[10px] text-slate-400 block">2-Qubit Gate Depth</span>
                <span className="text-lg font-mono font-bold text-indigo-400">
                  {qpuJobResult.transpiled_circuit_depth}
                </span>
              </div>
            </div>

            {/* Device Calibration Snapshot */}
            <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800 text-[11px] font-mono text-slate-400 flex flex-wrap gap-4">
              <span>Avg T1: <b className="text-slate-200">{qpuJobResult.calibration_snapshot?.avg_t1_us?.toFixed(1)} µs</b></span>
              <span>Avg T2: <b className="text-slate-200">{qpuJobResult.calibration_snapshot?.avg_t2_us?.toFixed(1)} µs</b></span>
              <span>2Q Error: <b className="text-slate-200">{(qpuJobResult.calibration_snapshot?.two_qubit_error * 100)?.toFixed(3)}%</b></span>
              <span>Readout Error: <b className="text-slate-200">{(qpuJobResult.calibration_snapshot?.readout_error * 100)?.toFixed(3)}%</b></span>
            </div>

            {/* Measured Shot Counts Histogram */}
            <div>
              <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider mb-2">
                Measured QPU Bitstring Histogram (Top 8 Basis States)
              </h4>
              <div className="h-44">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={shotCountsChartData} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="bitstring" stroke="#94a3b8" fontSize={10} />
                    <YAxis stroke="#94a3b8" fontSize={10} />
                    <Tooltip
                      contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '0.75rem', fontSize: '11px' }}
                    />
                    <Bar dataKey="count" name="Shots" fill="#8b5cf6" radius={[4, 4, 0, 0]}>
                      {shotCountsChartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.isFeasible ? '#06b6d4' : '#f43f5e'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Sandia Volumetric Benchmarking 2D Heatmap */}
      <div className="bg-[#0f172a]/60 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Grid className="h-5 w-5 text-emerald-400" />
              Sandia Volumetric Benchmarking Heatmap (Width w vs. Depth d)
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Citation: Timothy Proctor, Kenneth Rudinger et al. (Sandia National Laboratories, <i>Nature Physics</i> 2022).
            </p>
          </div>
          <div className="flex items-center gap-2 text-xs">
            <span className="h-3 w-3 rounded bg-emerald-500 inline-block"></span>
            <span className="text-slate-300">Optimal (&gt;85%)</span>
            <span className="h-3 w-3 rounded bg-amber-500 inline-block ml-2"></span>
            <span className="text-slate-300">Feasible (&gt;60%)</span>
            <span className="h-3 w-3 rounded bg-rose-500 inline-block ml-2"></span>
            <span className="text-slate-300">Decayed</span>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs font-mono">
            <thead>
              <tr>
                <th className="p-3 text-left text-slate-400">Circuit Width (w Qubits)</th>
                {depths.map((d) => (
                  <th key={d} className="p-3 text-center text-slate-300">
                    Depth p = {d}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {widths.map((w) => (
                <tr key={w} className="border-t border-slate-800">
                  <td className="p-3 font-bold text-slate-200">
                    {w} Qubits ({w === 4 ? 'Cluster Base' : w === 12 ? 'Folded 3-Cluster' : `${w} Qubits`})
                  </td>
                  {depths.map((d) => {
                    const cell = sandia_volumetric_grid.find((item) => item.width === w && item.depth === d);
                    if (!cell) return <td key={d}>-</td>;

                    const bgClass =
                      cell.approximation_ratio > 0.85
                        ? 'bg-emerald-950/40 border-emerald-500/50 text-emerald-300'
                        : cell.approximation_ratio > 0.60
                        ? 'bg-amber-950/40 border-amber-500/50 text-amber-300'
                        : 'bg-rose-950/40 border-rose-500/50 text-rose-300';

                    return (
                      <td key={d} className="p-2 text-center">
                        <div className={`p-2.5 rounded-xl border ${bgClass} transition-all hover:scale-105`}>
                          <div className="text-sm font-extrabold">
                            {(cell.approximation_ratio * 100).toFixed(0)}% AR
                          </div>
                          <div className="text-[10px] opacity-75 mt-0.5">
                            Fid: {(cell.fidelity * 100).toFixed(0)}% | Q_R: {cell.reachable_quality_qr}
                          </div>
                        </div>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
