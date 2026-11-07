import React, { useState } from 'react';
import { Layers, Network, Database, Sparkles, TrendingUp } from 'lucide-react';

export default function RmtClusterView({ marketData }) {
  if (!marketData) {
    return (
      <div className="p-12 text-center text-zinc-500 font-mono text-xs animate-pulse">
        Loading Nasdaq RMT spectral decomposition...
      </div>
    );
  }

  const { tickers, clusters, marchenko_pastur_lambda_plus, denoised_correlation } = marketData;
  const [selectedCluster, setSelectedCluster] = useState(0);

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Top Banner Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-4 transition-all hover:border-zinc-700">
          <div className="flex items-center gap-2 text-zinc-400 text-xs font-medium">
            <Database className="h-4 w-4 text-zinc-300" />
            Asset Universe
          </div>
          <div className="text-2xl font-bold text-white font-mono mt-1">
            {tickers.length} Equities
          </div>
          <div className="text-[11px] text-zinc-500 mt-1 font-mono">Nasdaq Liquid Large-Cap</div>
        </div>

        <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-4 transition-all hover:border-zinc-700">
          <div className="flex items-center gap-2 text-zinc-400 text-xs font-medium">
            <Sparkles className="h-4 w-4 text-zinc-300" />
            RMT Marchenko-Pastur Bound
          </div>
          <div className="text-2xl font-bold text-zinc-100 font-mono mt-1">
            λ+ = {marchenko_pastur_lambda_plus}
          </div>
          <div className="text-[11px] text-zinc-500 mt-1 font-mono">Noise Cutoff Threshold</div>
        </div>

        <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-4 transition-all hover:border-zinc-700">
          <div className="flex items-center gap-2 text-zinc-400 text-xs font-medium">
            <Layers className="h-4 w-4 text-zinc-300" />
            Hardware Decomposition
          </div>
          <div className="text-2xl font-bold text-zinc-100 font-mono mt-1">
            {clusters.length} Sub-Clusters
          </div>
          <div className="text-[11px] text-zinc-500 mt-1 font-mono">Max 4 Qubits / Subproblem</div>
        </div>

        <div className="bg-zinc-900/60 border border-zinc-800 rounded-xl p-4 transition-all hover:border-zinc-700">
          <div className="flex items-center gap-2 text-zinc-400 text-xs font-medium">
            <Network className="h-4 w-4 text-zinc-300" />
            Covariance Shrinkage
          </div>
          <div className="text-2xl font-bold text-zinc-100 mt-1">
            Ledoit-Wolf
          </div>
          <div className="text-[11px] text-zinc-500 mt-1 font-mono">Annualized 252 Days</div>
        </div>
      </div>

      {/* Cluster Navigation & Cards */}
      <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-6">
        <h2 className="text-sm font-bold text-white mb-4 flex items-center gap-2 uppercase tracking-wider font-mono">
          <Network className="h-4 w-4 text-zinc-400" />
          Hardware-Bounded Clusters (GetClusters Partitioning)
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {clusters.map((c, idx) => (
            <div
              key={idx}
              onClick={() => setSelectedCluster(idx)}
              className={`cursor-pointer rounded-xl p-5 border transition-all duration-300 transform hover:-translate-y-0.5 ${
                selectedCluster === idx
                  ? 'bg-zinc-800/80 border-white text-white shadow-lg shadow-black'
                  : 'bg-zinc-900/50 border-zinc-800 text-zinc-300 hover:border-zinc-600'
              }`}
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-mono font-bold uppercase tracking-wider text-zinc-200">
                  Cluster C_{c.cluster_id + 1}
                </span>
                <span className="text-xs font-mono px-2 py-0.5 rounded bg-zinc-950 text-zinc-400 border border-zinc-800">
                  {c.size} Qubits
                </span>
              </div>
              <div className="flex flex-wrap gap-1.5 mb-3">
                {c.tickers.map((t) => (
                  <span
                    key={t}
                    className="text-xs font-mono font-semibold px-2 py-0.5 rounded bg-zinc-950 border border-zinc-800 text-zinc-200"
                  >
                    {t}
                  </span>
                ))}
              </div>
              <p className="text-[11px] text-zinc-400 leading-relaxed">
                Solved at shallow depth (p=1, 2) via CCD-QAOA with K=2 cardinality constraint.
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Denoised Correlation Matrix Heatmap */}
      <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-sm font-bold text-white flex items-center gap-2 uppercase tracking-wider font-mono">
              <TrendingUp className="h-4 w-4 text-zinc-400" />
              Marchenko-Pastur Denoised Correlation Matrix (C*)
            </h2>
            <p className="text-xs text-zinc-400 mt-0.5">
              Noise modes below λ+ filtered out; genuine market correlations preserved.
            </p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs font-mono">
            <thead>
              <tr>
                <th className="p-2.5 text-left text-zinc-500">Asset</th>
                {tickers.map((t) => (
                  <th key={t} className="p-2.5 text-center text-zinc-400">
                    {t}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {denoised_correlation.map((row, i) => (
                <tr key={tickers[i]} className="border-t border-zinc-800/60 hover:bg-zinc-800/30 transition-colors">
                  <td className="p-2.5 font-bold text-zinc-200 text-left">{tickers[i]}</td>
                  {row.map((val, j) => {
                    const isDiag = i === j;
                    return (
                      <td
                        key={j}
                        className={`p-2.5 text-center transition-colors ${
                          isDiag
                            ? 'bg-zinc-800 font-extrabold text-white'
                            : val > 0.6
                            ? 'bg-zinc-900 text-zinc-200 font-semibold'
                            : 'text-zinc-500'
                        }`}
                        title={`${tickers[i]} - ${tickers[j]}: ${val.toFixed(3)}`}
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
