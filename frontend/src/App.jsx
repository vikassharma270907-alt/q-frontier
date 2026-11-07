import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import AuditWorkbenchView from './components/AuditWorkbenchView';
import RmtClusterView from './components/RmtClusterView';
import QaoaBenchmarkView from './components/QaoaBenchmarkView';
import EquityCurveView from './components/EquityCurveView';
import VolumetricView from './components/VolumetricView';
import { Layers, Zap, TrendingUp, Cpu, SlidersHorizontal, Check } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('workbench');
  const [marketData, setMarketData] = useState(null);
  const [optimizationResult, setOptimizationResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState(null);
  const [params, setParams] = useState({
    depth: 1,
    continuity_bonus: 0.05,
    use_qcl_sensor: true,
    transaction_cost_bps: 5.0
  });

  // Initial data loading
  useEffect(() => {
    fetch('/api/market/clusters')
      .then((res) => res.json())
      .then((data) => {
        setMarketData(data);
      })
      .catch((err) => console.error("Failed to load market data", err));

    runOptimization();
  }, []);

  const runOptimization = () => {
    setLoading(true);
    fetch('/api/quantum/optimize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    })
      .then((res) => res.json())
      .then((data) => {
        setOptimizationResult(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Optimization failed", err);
        setLoading(false);
      });
  };

  const handleExportSuccess = () => {
    setNotification('Reproducibility bundle downloaded successfully!');
    setTimeout(() => setNotification(null), 4000);
  };

  const tabs = [
    { id: 'workbench', label: 'Auditable Benchmark Workbench', icon: SlidersHorizontal },
    { id: 'qaoa', label: 'CCD-QAOA & QCL Engine', icon: Zap },
    { id: 'rmt', label: 'RMT Spectral Denoising', icon: Layers },
    { id: 'backtest', label: 'Walk-Forward Backtest', icon: TrendingUp },
    { id: 'hardware', label: 'Sandia & IonQ Hardware', icon: Cpu }
  ];

  return (
    <div className="min-h-screen bg-[#080c14] text-slate-100 flex flex-col">
      <Header />

      {/* Floating Notification */}
      {notification && (
        <div className="fixed bottom-6 right-6 z-50 bg-emerald-950 border border-emerald-700 text-emerald-200 px-4 py-3 rounded-xl shadow-2xl flex items-center gap-2 text-xs font-semibold animate-bounce">
          <Check className="h-4 w-4 text-emerald-400" />
          {notification}
        </div>
      )}

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-6 space-y-6">
        {/* Navigation Tabs */}
        <div className="flex border-b border-slate-800 space-x-2 overflow-x-auto">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-3 text-xs md:text-sm font-semibold border-b-2 transition-all whitespace-nowrap ${
                  isActive
                    ? 'border-cyan-400 text-cyan-400 bg-cyan-950/20'
                    : 'border-transparent text-slate-400 hover:text-slate-200 hover:border-slate-700'
                }`}
              >
                <Icon className="h-4 w-4" />
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Tab Content Panes */}
        {activeTab === 'workbench' && (
          <AuditWorkbenchView onExportSuccess={handleExportSuccess} />
        )}

        {activeTab === 'qaoa' && (
          <QaoaBenchmarkView
            optimizationResult={optimizationResult}
            loading={loading}
            onRunOptimization={runOptimization}
            params={params}
            setParams={setParams}
          />
        )}

        {activeTab === 'rmt' && <RmtClusterView marketData={marketData} />}

        {activeTab === 'backtest' && <EquityCurveView optimizationResult={optimizationResult} />}

        {activeTab === 'hardware' && <VolumetricView />}
      </main>

      {/* Footer with Academic Citations & Integrity Disclaimers */}
      <footer className="border-t border-slate-800/80 bg-[#0a0f1d] py-6 px-6 text-xs text-slate-500 text-center">
        <p>
          Q-FRONTIER: Auditable Hybrid Optimization Research Workbench • <b>Intermountain Quantum Competition 2026</b>
        </p>
        <p className="mt-1 text-[11px] text-slate-600">
          Formulation grounded in Falla & Safro (arXiv:2605.06858), Cadavid et al. (arXiv:2602.23976), Yang et al. (arXiv:2609.15708), and Proctor et al. (Sandia National Laboratories, Nature Physics 2022).
        </p>
        <p className="mt-1 text-[10px] text-slate-600">
          DISCLAIMER: All quantum calculations are executed via exact numerical simulation. This software is an academic prototype for research and educational purposes and does not constitute financial or investment advice.
        </p>
      </footer>
    </div>
  );
}
