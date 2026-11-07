import React, { useState } from 'react';
import { Layers, Network, Database, Sparkles, TrendingUp } from 'lucide-react';

export default function RmtClusterView({ marketData }) {
  if (!marketData) {
    return (
      <div className="p-8 text-center text-slate-400">
        Loading Nasdaq RMT spectral decomposition...
      </div>
    );
  }

  const { tickers, clusters, marchenko_pastur_lambda_plus, denoised_correlation } = marketData;
  const [selectedCluster, setSelectedCluster] = useState(0);

  return (
    <div className="space-y-6">
      {/* Top Banner Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-[#0f172a]/80 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-medium">
            <Database className="h-4 w-4 text-cyan-400" />
            Asset Universe
          </div>
          <div className="text-2xl font-bold text-white mt-1">
            {tickers.length} Equities
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Nasdaq Liquid Large-Cap</div>
        </div>

        <div className="bg-[#0f172a]/80 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-medium">
            <Sparkles className="h-4 w-4 text-purple-400" />
            RMT Marchenko-Pastur Bound
          </div>
          <div className="text-2xl font-bold text-purple-300 font-mono mt-1">
            λ+ = {marchenko_pastur_lambda_plus}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Noise Eigenvalue Cutoff</div>
        </div>

        <div className="bg-[#0f172a]/80 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-medium">
            <Layers className="h-4 w-4 text-emerald-400" />
            Hardware Decomposition
          </div>
          <div className="text-2xl font-bold text-emerald-300 mt-1">
            {clusters.length} Sub-Clusters
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Max 4 Qubits / Subproblem</div>
        </div>

        <div className="bg-[#0f172a]/80 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center gap-2 text-slate-400 text-xs font-medium">
            <Network className="h-4 w-4 text-amber-400" />
            Covariance Shrinkage
          </div>
          <div className="text-2xl font-bold text-amber-300 mt-1">
            Ledoit-Wolf
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Annualized 252 Days</div>
        </div>
      </div>

      {/* Cluster Navigation & Cards */}
      <div className="bg-[#0f172a]/60 border border-slate-800 rounded-2xl p-6">
        <h2 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
          <Network className="h-5 w-5 text-cyan-400" />
          Hardware-Bounded Clusters (GetClusters Algorithm)
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {clusters.map((c, idx) => (
            <div
              key={idx}
              onClick={() => setSelectedCluster(idx)}
              className={`cursor-pointer rounded-xl p-5 border transition-all duration-200 ${
                selectedCluster === idx
                  ? 'bg-cyan-950/40 border-cyan-500/60 shadow-lg shadow-cyan-500/10'
                  : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-bold uppercase tracking-wider text-cyan-400">
                  Cluster C_{c.cluster_id + 1}
                </span>
                <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                  {c.size} Qubits
                </span>
              </div>
              <div className="flex flex-wrap gap-1.5 mb-3">
                {c.tickers.map((t) => (
                  <span
                    key={t}
                    className="text-xs font-mono font-semibold px-2.5 py-1 rounded bg-slate-800/80 border border-slate-700 text-white"
                  >
                    {t}
                  </span>
                ))}
              </div>
              <p className="text-[11px] text-slate-400">
                Subproblem solved at shallow depth (p=1, 2) via CCD-QAOA with K=2 cardinality constraint.
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Denoised Correlation Matrix Heatmap */}
      <div className="bg-[#0f172a]/60 border border-slate-800 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-indigo-400" />
              Marchenko-Pastur Denoised Correlation Matrix (C*)
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Noise modes below λ+ filtered out; genuine market structure and industry factors preserved.
            </p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs font-mono">
            <thead>
              <tr>
                <th className="p-2 text-left text-slate-500">Asset</th>
                {tickers.map((t) => (
                  <th key={t} className="p-2 text-center text-slate-400">
                    {t}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {denoised_correlation.map((row, i) => (
                <tr key={tickers[i]} className="border-t border-slate-800/50 hover:bg-slate-800/30">
                  <td className="p-2 font-bold text-slate-300 text-left">{tickers[i]}</td>
                  {row.map((val, j) => {
                    const isDiag = i === j;
                    const opacity = Math.min(1.0, Math.max(0.15, val));
                    return (
                      <td
                        key={j}
                        className={`p-2 text-center rounded transition-colors ${
                          isDiag
                            ? 'bg-cyan-500/20 text-cyan-300 font-bold'
                            : val > 0.6
                            ? 'bg-indigo-500/20 text-indigo-300'
                            : 'text-slate-400'
                        }`}
                        title={`${tickers[i]} - ${tickers[j]}: ${val}`}
                      >
                        {val.toFixed(2)}
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
