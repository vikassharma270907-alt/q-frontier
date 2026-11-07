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
    <div className="space-y-6 animate-fade-in">
      {/* KPI Cards Banner */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="bg-zinc-900/40 border border-zinc-800 rounded-xl p-4 hover:border-zinc-700 transition-all">
          <div className="flex items-center gap-1.5 text-zinc-400 text-xs font-medium font-mono">
            <DollarSign className="h-4 w-4 text-zinc-300" />
            Final Value ($100 Base)
          </div>
          <div className="text-2xl font-bold text-white font-mono mt-1">
            ${backtest.final_portfolio_value}
          </div>
          <div className="text-[11px] text-zinc-500 mt-1 font-mono">
            vs ${backtest.benchmark_final_value} Benchmark
          </div>
        </div>

        <div className="bg-zinc-900/40 border border-zinc-800 rounded-xl p-4 hover:border-zinc-700 transition-all">
          <div className="flex items-center gap-1.5 text-zinc-400 text-xs font-medium font-mono">
            <TrendingUp className="h-4 w-4 text-zinc-300" />
            Annualized Return
          </div>
          <div className="text-2xl font-bold text-white font-mono mt-1">
            +{backtest.annualized_return_pct}%
          </div>
          <div className="text-[11px] text-zinc-500 mt-1 font-mono">Net of 5 bps Costs</div>
        </div>

        <div className="bg-zinc-900/40 border border-zinc-800 rounded-xl p-4 hover:border-zinc-700 transition-all">
          <div className="flex items-center gap-1.5 text-zinc-400 text-xs font-medium font-mono">
            <Activity className="h-4 w-4 text-zinc-300" />
            Net Sharpe Ratio
          </div>
          <div className="text-2xl font-bold text-zinc-200 font-mono mt-1">
            {backtest.net_sharpe_ratio}
          </div>
          <div className="text-[11px] text-zinc-500 mt-1 font-mono">Rf = 4.0% annualized</div>
        </div>

        <div className="bg-zinc-900/40 border border-zinc-800 rounded-xl p-4 hover:border-zinc-700 transition-all">
          <div className="flex items-center gap-1.5 text-zinc-400 text-xs font-medium font-mono">
            <Percent className="h-4 w-4 text-zinc-300" />
            Ann. Volatility
          </div>
          <div className="text-2xl font-bold text-zinc-200 font-mono mt-1">
            {backtest.annualized_volatility_pct}%
          </div>
          <div className="text-[11px] text-zinc-500 mt-1 font-mono">Sigma (Risk Controlled)</div>
        </div>

        <div className="bg-zinc-900/40 border border-zinc-800 rounded-xl p-4 col-span-2 md:col-span-1 hover:border-zinc-700 transition-all">
          <div className="flex items-center gap-1.5 text-zinc-400 text-xs font-medium font-mono">
            <ArrowUpRight className="h-4 w-4 text-zinc-400" />
            Max Drawdown
          </div>
          <div className="text-2xl font-bold text-zinc-300 font-mono mt-1">
            {backtest.max_drawdown_pct}%
          </div>
          <div className="text-[11px] text-zinc-500 mt-1 font-mono">Downside Protected</div>
        </div>
      </div>

      {/* Main Walk-Forward Equity Curve Chart */}
      <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-sm font-bold text-white flex items-center gap-2 uppercase tracking-wider font-mono">
              <TrendingUp className="h-4 w-4 text-zinc-300" />
              Walk-Forward Out-of-Sample Performance (Net of 5 bps Costs)
            </h2>
            <p className="text-xs text-zinc-400 mt-0.5">
              Monthly rebalancing across the quantum-selected 6-asset portfolio with continuity bonus κ = 0.05.
            </p>
          </div>
        </div>

        <div className="h-80 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={equity_curve}>
              <CartesianGrid strokeDasharray="2 2" stroke="#27272a" />
              <XAxis dataKey="date" stroke="#71717a" fontSize={11} fontFamily="JetBrains Mono" />
              <YAxis stroke="#71717a" fontSize={11} domain={['auto', 'auto']} />
              <Tooltip
                contentStyle={{ backgroundColor: "#09090b", borderColor: "#27272a", fontSize: 12, borderRadius: 8 }}
                formatter={(val, name) => [`$${val}`, name === "q_frontier" ? "Q-FRONTIER (Net)" : "Equal-Weight Benchmark"]}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="q_frontier"
                name="Q-FRONTIER (Net of Costs)"
                stroke="#ffffff"
                strokeWidth={2.5}
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="benchmark_ew"
                name="Equal-Weight Benchmark (1/N)"
                stroke="#71717a"
                strokeWidth={1.5}
                strokeDasharray="4 4"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Continuous Weight Allocation Table */}
      <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-6">
        <h3 className="text-sm font-bold text-white mb-3 uppercase tracking-wider font-mono">
          SLSQP Sharpe-Optimal Continuous Weight Allocation (K = 6 Assets Selected)
        </h3>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-3">
          {weights.map((w) => (
            <div key={w.ticker} className="bg-zinc-950 border border-zinc-800 hover:border-zinc-700 rounded-xl p-3 text-center transition-all duration-200">
              <span className="text-xs font-mono font-bold text-white block">{w.ticker}</span>
              <span className="text-lg font-mono font-extrabold text-zinc-100 mt-1 block">
                {(w.weight * 100).toFixed(1)}%
              </span>
              <span className="text-[10px] text-zinc-500 uppercase font-mono">Weight</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
