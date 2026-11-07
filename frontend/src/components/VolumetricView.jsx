import React, { useState, useEffect } from 'react';
import { Cpu, Grid } from 'lucide-react';

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
    return <div className="p-12 text-center text-zinc-500 font-mono text-xs animate-pulse">Loading Sandia & IonQ Hardware Benchmarks...</div>;
  }

  const { hardware_comparison, sandia_volumetric_grid } = benchmarks;
  const { ionq_trapped_ion, ibm_heavy_hex } = hardware_comparison;

  const widths = [4, 6, 8, 12];
  const depths = [1, 2, 3, 4, 5];

  return (
    <div className="space-y-6 animate-fade-in">
      {/* IonQ vs IBM Architecture Comparison Banner */}
      <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-6">
        <h2 className="text-sm font-bold text-white flex items-center gap-2 mb-1 uppercase tracking-wider font-mono">
          <Cpu className="h-4 w-4 text-zinc-300" />
          Hardware Transpilation Audit: IonQ Trapped-Ion vs. IBM Heavy-Hex
        </h2>
        <p className="text-xs text-zinc-400 mb-6">
          Transpiling complete-graph XY mixer ($H_M^{XY}$) across distinct hardware coupling topologies.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-zinc-900/70 border border-zinc-700 rounded-xl p-5 hover:border-zinc-500 transition-all">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-bold text-white font-mono">IonQ Trapped-Ion</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-800 text-zinc-200 border border-zinc-700">
                All-to-All Native (K_n)
              </span>
            </div>
            <div className="space-y-3 text-xs">
              <div className="flex justify-between border-b border-zinc-800 pb-2">
                <span className="text-zinc-400">Routing SWAP Overhead:</span>
                <span className="font-mono text-white font-extrabold text-sm">
                  {ionq_trapped_ion.routing_swaps} SWAPs (Zero Overhead)
                </span>
              </div>
              <div className="flex justify-between border-b border-zinc-800 pb-2">
                <span className="text-zinc-400">Total 2-Qubit Gates:</span>
                <span className="font-mono text-zinc-200 font-bold">{ionq_trapped_ion.two_qubit_gates}</span>
              </div>
              <div className="flex justify-between border-b border-zinc-800 pb-2">
                <span className="text-zinc-400">Circuit Depth:</span>
                <span className="font-mono text-zinc-200 font-bold">{ionq_trapped_ion.circuit_depth}</span>
              </div>
              <div className="flex justify-between pt-1">
                <span className="text-zinc-400">Fidelity Status:</span>
                <span className="text-zinc-200 font-medium font-mono">{ionq_trapped_ion.decoherence_risk}</span>
              </div>
            </div>
          </div>

          <div className="bg-zinc-950 border border-zinc-800 rounded-xl p-5 hover:border-zinc-700 transition-all">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm font-bold text-zinc-300 font-mono">IBM Heavy-Hex (Superconducting)</span>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-900 text-zinc-400 border border-zinc-800">
                Sparse Planar Grid
              </span>
            </div>
            <div className="space-y-3 text-xs">
              <div className="flex justify-between border-b border-zinc-800 pb-2">
                <span className="text-zinc-400">Routing SWAP Overhead:</span>
                <span className="font-mono text-zinc-400 font-extrabold text-sm">
                  +{ibm_heavy_hex.routing_swaps} Additional SWAPs
                </span>
              </div>
              <div className="flex justify-between border-b border-zinc-800 pb-2">
                <span className="text-zinc-400">Total 2-Qubit Gates:</span>
                <span className="font-mono text-zinc-400 font-bold">{ibm_heavy_hex.two_qubit_gates}</span>
              </div>
              <div className="flex justify-between border-b border-zinc-800 pb-2">
                <span className="text-zinc-400">Circuit Depth:</span>
                <span className="font-mono text-zinc-400 font-bold">{ibm_heavy_hex.circuit_depth}</span>
              </div>
              <div className="flex justify-between pt-1">
                <span className="text-zinc-400">Fidelity Status:</span>
                <span className="text-zinc-400 font-medium font-mono">{ibm_heavy_hex.decoherence_risk}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Sandia Volumetric Benchmarking 2D Heatmap */}
      <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-6">
          <div>
            <h2 className="text-sm font-bold text-white flex items-center gap-2 uppercase tracking-wider font-mono">
              <Grid className="h-4 w-4 text-zinc-300" />
              Sandia Volumetric Benchmarking Heatmap (Width w vs. Depth d)
            </h2>
            <p className="text-xs text-zinc-400 mt-0.5">
              Citation: Timothy Proctor, Kenneth Rudinger et al. (Sandia National Laboratories, <i>Nature Physics</i> 2022).
            </p>
          </div>
          <div className="flex items-center gap-2 text-xs font-mono">
            <span className="h-2.5 w-2.5 rounded bg-white inline-block"></span>
            <span className="text-zinc-300">Optimal (&gt;85%)</span>
            <span className="h-2.5 w-2.5 rounded bg-zinc-600 inline-block ml-2"></span>
            <span className="text-zinc-400">Feasible (&gt;60%)</span>
            <span className="h-2.5 w-2.5 rounded bg-zinc-800 inline-block ml-2"></span>
            <span className="text-zinc-600">Decayed</span>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs font-mono">
            <thead>
              <tr>
                <th className="p-3 text-left text-zinc-400">Circuit Width (w Qubits)</th>
                {depths.map((d) => (
                  <th key={d} className="p-3 text-center text-zinc-300">
                    Depth p = {d}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {widths.map((w) => (
                <tr key={w} className="border-t border-zinc-800">
                  <td className="p-3 font-bold text-zinc-200">
                    {w} Qubits ({w === 4 ? 'Cluster Base' : w === 12 ? 'Folded 3-Cluster' : `${w} Qubits`})
                  </td>
                  {depths.map((d) => {
                    const cell = sandia_volumetric_grid.find((item) => item.width === w && item.depth === d);
                    if (!cell) return <td key={d}>-</td>;

                    const cellStyle =
                      cell.approximation_ratio > 0.85
                        ? 'bg-zinc-800 border-zinc-500 text-white shadow-sm'
                        : cell.approximation_ratio > 0.60
                        ? 'bg-zinc-900 border-zinc-700 text-zinc-300'
                        : 'bg-zinc-950 border-zinc-800 text-zinc-600';

                    return (
                      <td key={d} className="p-2 text-center">
                        <div className={`p-2.5 rounded-xl border ${cellStyle} transition-all duration-200 hover:scale-105`}>
                          <div className="text-sm font-extrabold font-mono">
                            {(cell.approximation_ratio * 100).toFixed(0)}% AR
                          </div>
                          <div className="text-[10px] opacity-75 mt-0.5 font-mono">
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
