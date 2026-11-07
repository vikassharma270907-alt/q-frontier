import React from 'react';
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, CartesianGrid
} from 'recharts';
import { TrendingUp, DollarSign, Activity, Percent, ArrowUpRight } from 'lucide-react';

export default function EquityCurveView({ optimizationResult }) {
  if (!optimizationResult || !optimizationResult.backtest) return null;

  const { backtest, weights, selected_tickers } = optimizationResult;
  const { equity_curve } = backtest;

  return (
    <div className="space-y-6">
      {/* KPI Cards Banner */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="bg-[#0f172a]/80 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center gap-1.5 text-slate-400 text-xs font-medium">
            <DollarSign className="h-4 w-4 text-emerald-400" />
            Final Value ($100 Base)
          </div>
          <div className="text-2xl font-bold text-emerald-300 font-mono mt-1">
            ${backtest.final_portfolio_value}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">
            vs ${backtest.benchmark_final_value} Benchmark
          </div>
        </div>

        <div className="bg-[#0f172a]/80 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center gap-1.5 text-slate-400 text-xs font-medium">
            <TrendingUp className="h-4 w-4 text-cyan-400" />
            Annualized Return
          </div>
          <div className="text-2xl font-bold text-white font-mono mt-1">
            +{backtest.annualized_return_pct}%
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Net of 5 bps Costs</div>
        </div>

        <div className="bg-[#0f172a]/80 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center gap-1.5 text-slate-400 text-xs font-medium">
            <Activity className="h-4 w-4 text-indigo-400" />
            Net Sharpe Ratio
          </div>
          <div className="text-2xl font-bold text-indigo-300 font-mono mt-1">
            {backtest.net_sharpe_ratio}
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Rf = 4.0% annualized</div>
        </div>

        <div className="bg-[#0f172a]/80 border border-slate-800 rounded-xl p-4">
          <div className="flex items-center gap-1.5 text-slate-400 text-xs font-medium">
            <Percent className="h-4 w-4 text-purple-400" />
            Ann. Volatility
          </div>
          <div className="text-2xl font-bold text-purple-300 font-mono mt-1">
            {backtest.annualized_volatility_pct}%
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Sigma (Risk Controlled)</div>
        </div>

        <div className="bg-[#0f172a]/80 border border-slate-800 rounded-xl p-4 col-span-2 md:col-span-1">
          <div className="flex items-center gap-1.5 text-slate-400 text-xs font-medium">
            <ArrowUpRight className="h-4 w-4 text-rose-400" />
            Max Drawdown
          </div>
          <div className="text-2xl font-bold text-rose-400 font-mono mt-1">
            {backtest.max_drawdown_pct}%
          </div>
          <div className="text-[11px] text-slate-500 mt-1">Controlled Downside</div>
        </div>
      </div>

      {/* Main Walk-Forward Equity Curve Chart */}
      <div className="bg-[#0f172a]/60 border border-slate-800 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <TrendingUp className="h-5 w-5 text-cyan-400" />
              Walk-Forward Out-of-Sample Performance (Net of 5 bps Costs)
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Simulating monthly rebalancing across the quantum-selected 6-asset portfolio with continuity bonus κ = 0.05.
            </p>
          </div>
        </div>

        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={equity_curve}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="date" stroke="#64748b" fontSize={11} fontFamily="JetBrains Mono" />
              <YAxis stroke="#64748b" fontSize={11} domain={['auto', 'auto']} />
              <Tooltip
                contentStyle={{ backgroundColor: "#0f172a", borderColor: "#1e293b", fontSize: 12 }}
                formatter={(val, name) => [`$${val}`, name === "q_frontier" ? "Q-FRONTIER (Net)" : "Equal-Weight Benchmark"]}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="q_frontier"
                name="Q-FRONTIER (Net of Costs)"
                stroke="#06b6d4"
                strokeWidth={2.5}
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="benchmark_ew"
                name="Equal-Weight Benchmark (1/N)"
                stroke="#64748b"
                strokeWidth={1.5}
                strokeDasharray="4 4"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Continuous Weight Allocation Table */}
      <div className="bg-[#0f172a]/60 border border-slate-800 rounded-2xl p-6">
        <h3 className="text-md font-bold text-white mb-3">
          SLSQP Sharpe-Optimal Continuous Weight Allocation (K = 6 Assets Selected)
        </h3>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
          {weights.map((w) => (
            <div key={w.ticker} className="bg-slate-900/60 border border-slate-800 rounded-xl p-3 text-center">
              <span className="text-xs font-mono font-bold text-cyan-400 block">{w.ticker}</span>
              <span className="text-lg font-mono font-extrabold text-white mt-1 block">
                {(w.weight * 100).toFixed(1)}%
              </span>
              <span className="text-[10px] text-slate-500 uppercase">Weight</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
