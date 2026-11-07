import React, { useState, useEffect, useMemo } from 'react';
import { Cpu, Grid, RefreshCw, AlertTriangle } from 'lucide-react';

const WIDTHS = [4, 6, 8, 12];
const DEPTHS = [1, 2, 3, 4, 5];

function HardwareCard({ title, badge, isHighlighted, metrics }) {
  const cardBorder = isHighlighted
    ? 'bg-zinc-900/70 border-zinc-700 hover:border-zinc-500'
    : 'bg-zinc-950 border-zinc-800 hover:border-zinc-700';

  return (
    <div className={`border rounded-xl p-5 transition-all ${cardBorder}`}>
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm font-bold text-white font-mono">{title}</span>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-800 text-zinc-300 border border-zinc-700">
          {badge}
        </span>
      </div>
      <div className="space-y-3 text-xs">
        <div className="flex justify-between border-b border-zinc-800 pb-2">
          <span className="text-zinc-400">Routing SWAP Overhead:</span>
          <span className="font-mono text-white font-extrabold text-sm">
            {metrics.routing_swaps === 0 ? '0 SWAPs (Native K_n)' : `+${metrics.routing_swaps} Additional SWAPs`}
          </span>
        </div>
        <div className="flex justify-between border-b border-zinc-800 pb-2">
          <span className="text-zinc-400">Total 2-Qubit Gates:</span>
          <span className="font-mono text-zinc-200 font-bold">{metrics.two_qubit_gates}</span>
        </div>
        <div className="flex justify-between border-b border-zinc-800 pb-2">
          <span className="text-zinc-400">Circuit Depth:</span>
          <span className="font-mono text-zinc-200 font-bold">{metrics.circuit_depth}</span>
        </div>
        <div className="flex justify-between pt-1">
          <span className="text-zinc-400">Fidelity Status:</span>
          <span className="text-zinc-300 font-medium font-mono">{metrics.decoherence_risk}</span>
        </div>
      </div>
    </div>
  );
}

function HardwareComparisonSection({ comparison }) {
  const { ionq_trapped_ion, ibm_heavy_hex } = comparison;

  return (
    <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-6">
      <h2 className="text-sm font-bold text-white flex items-center gap-2 mb-1 uppercase tracking-wider font-mono">
        <Cpu className="h-4 w-4 text-zinc-300" />
        Hardware Transpilation Audit: IonQ Trapped-Ion vs. IBM Heavy-Hex
      </h2>
      <p className="text-xs text-zinc-400 mb-6">
        Transpiling complete-graph XY mixer (<i>H</i><sub>M</sub><sup>XY</sup>) across distinct hardware topologies.
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <HardwareCard
          title="IonQ Trapped-Ion"
          badge="All-to-All Native (K_n)"
          isHighlighted={true}
          metrics={ionq_trapped_ion}
        />
        <HardwareCard
          title="IBM Heavy-Hex (Superconducting)"
          badge="Sparse Planar Grid"
          isHighlighted={false}
          metrics={ibm_heavy_hex}
        />
      </div>
    </div>
  );
}

function SandiaHeatmapTable({ sandiaGrid }) {
  const gridMap = useMemo(() => {
    const map = new Map();
    if (Array.isArray(sandiaGrid)) {
      sandiaGrid.forEach((cell) => map.set(`${cell.width}_${cell.depth}`, cell));
    }
    return map;
  }, [sandiaGrid]);

  return (
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
              {DEPTHS.map((d) => (
                <th key={d} className="p-3 text-center text-zinc-300">Depth p = {d}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {WIDTHS.map((w) => (
              <tr key={w} className="border-t border-zinc-800">
                <td className="p-3 font-bold text-zinc-200">
                  {w} Qubits ({w === 4 ? 'Cluster Base' : w === 12 ? 'Folded 3-Cluster' : `${w} Qubits`})
                </td>
                {DEPTHS.map((d) => {
                  const cell = gridMap.get(`${w}_${d}`);
                  if (!cell) {
                    return <td key={d} className="p-2 text-center text-zinc-600">-</td>;
                  }
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
  );
}

export default function VolumetricView() {
  const [benchmarks, setBenchmarks] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchBenchmarks = (signal) => {
    setLoading(true);
    setError(null);
    fetch('/api/hardware/benchmarks', { signal })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}: Failed to load hardware benchmarks`);
        return res.json();
      })
      .then((data) => {
        setBenchmarks(data);
        setLoading(false);
      })
      .catch((err) => {
        if (err.name === 'AbortError') return;
        console.error("Hardware benchmark fetch error:", err);
        setError(err.message || "Failed to load hardware benchmarks");
        setLoading(false);
      });
  };

  useEffect(() => {
    const controller = new AbortController();
    fetchBenchmarks(controller.signal);
    return () => controller.abort();
  }, []);

  if (loading) {
    return <div className="p-12 text-center text-zinc-500 font-mono text-xs animate-pulse">Loading Sandia & IonQ Hardware Benchmarks...</div>;
  }

  if (error || !benchmarks?.hardware_comparison) {
    return (
      <div className="bg-zinc-950 border border-zinc-800 rounded-2xl p-8 text-center space-y-3 font-mono text-xs">
        <AlertTriangle className="h-6 w-6 text-zinc-400 mx-auto" />
        <p className="text-zinc-300">Failed to load hardware benchmarks: {error || "Invalid response structure"}</p>
        <button
          onClick={() => fetchBenchmarks()}
          className="px-4 py-2 rounded-xl text-xs font-bold bg-white text-black hover:bg-zinc-200 transition-colors inline-flex items-center gap-2"
        >
          <RefreshCw className="h-3.5 w-3.5" /> Retry Benchmarks
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <HardwareComparisonSection comparison={benchmarks.hardware_comparison} />
      <SandiaHeatmapTable sandiaGrid={benchmarks.sandia_volumetric_grid} />
    </div>
  );
}
