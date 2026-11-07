import React, { useState, useEffect } from 'react';
import { Cpu, Grid, Layers, ShieldCheck, HelpCircle } from 'lucide-react';

export default function VolumetricView() {
  const [benchmarks, setBenchmarks] = useState(null);
  const [loading, setLoading] = useState(true);

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

  if (loading || !benchmarks) {
    return <div className="p-8 text-center text-slate-400">Loading Sandia & IonQ Hardware Benchmarks...</div>;
  }

  const { hardware_comparison, sandia_volumetric_grid } = benchmarks;
  const { ionq_trapped_ion, ibm_heavy_hex } = hardware_comparison;

  const widths = [4, 6, 8, 12];
  const depths = [1, 2, 3, 4, 5];

  return (
    <div className="space-y-6">
      {/* IonQ vs IBM Architecture Comparison Banner */}
      <div className="bg-[#0f172a]/80 border border-slate-800 rounded-2xl p-6">
        <h2 className="text-lg font-bold text-white flex items-center gap-2 mb-1">
          <Cpu className="h-5 w-5 text-purple-400" />
          Hardware Transpilation Audit: IonQ Trapped-Ion vs. IBM Heavy-Hex
        </h2>
        <p className="text-xs text-slate-400 mb-6">
          Transpiling complete-graph XY mixer ($H_M^{XY}$) and 3-body AGP counterdiabatic terms across distinct hardware coupling topologies.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-purple-950/20 border border-purple-500/30 rounded-xl p-5">
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

          <div className="bg-indigo-950/20 border border-indigo-500/30 rounded-xl p-5">
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

      {/* Sandia Volumetric Benchmarking 2D Heatmap */}
      <div className="bg-[#0f172a]/60 border border-slate-800 rounded-2xl p-6">
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
