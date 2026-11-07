import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import AuditWorkbenchView from './components/AuditWorkbenchView';
import RmtClusterView from './components/RmtClusterView';
import QaoaBenchmarkView from './components/QaoaBenchmarkView';
import EquityCurveView from './components/EquityCurveView';
import VolumetricView from './components/VolumetricView';
import { Layers, Zap, TrendingUp, Cpu, SlidersHorizontal, Check, ShieldAlert } from 'lucide-react';

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
    { id: 'hardware', label: 'Sandia & IonQ Benchmarks', icon: Cpu }
  ];

  return (
    <div className="min-h-screen bg-[#050505] text-zinc-100 flex flex-col font-sans selection:bg-zinc-700 selection:text-white">
      <Header />

      {/* Scientific Transparency Alert Banner */}
      <div className="bg-zinc-950 border-b border-zinc-800/80 px-6 py-2">
        <div className="max-w-7xl mx-auto flex items-center justify-between text-[11px] text-zinc-400 font-mono">
          <div className="flex items-center gap-2">
            <ShieldAlert className="h-3.5 w-3.5 text-zinc-400" />
            <span>RESEARCH PROTOTYPE ONLY — NOT INVESTMENT ADVICE. NO QUANTUM ADVANTAGE CLAIMED.</span>
          </div>
          <span className="hidden sm:inline text-zinc-500">
            SIMULATED BENCHMARK PARITY &bull; REPRODUCIBILITY GUARANTEED
          </span>
        </div>
      </div>

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-6 py-6 space-y-6">
        {/* Toast Notification */}
        {notification && (
          <div className="fixed bottom-6 right-6 z-50 bg-zinc-900 border border-zinc-700 text-zinc-100 px-4 py-3 rounded-xl shadow-2xl flex items-center gap-3 animate-slide-up">
            <Check className="h-4 w-4 text-white" />
            <span className="text-xs font-mono font-medium">{notification}</span>
          </div>
        )}

        {/* Animated Navigation Tabs */}
        <div className="flex border-b border-zinc-800/80 space-x-1 overflow-x-auto pb-px">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-4 py-3 text-xs font-semibold rounded-t-lg transition-all duration-200 border-b-2 whitespace-nowrap ${
                  isActive
                    ? 'border-white text-white bg-zinc-900/70 shadow-sm'
                    : 'border-transparent text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900/30'
                }`}
              >
                <Icon className={`h-4 w-4 transition-transform duration-200 ${isActive ? 'scale-110 text-white' : 'text-zinc-500'}`} />
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Animated Tab Content Panes */}
        <div className="animate-fade-in">
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
        </div>
      </main>

      {/* Footer with Academic Citations & Devpost Info */}
      <footer className="border-t border-zinc-800/80 bg-[#09090b] py-6 px-6 text-xs text-zinc-500 text-center">
        <p>
          Q-FRONTIER: Submitted to the <b className="text-zinc-300">Intermountain Quantum Competition 2026</b> (Brigham Young University).
        </p>
        <p className="mt-1 text-[11px] text-zinc-600 font-mono">
          Formulation grounded in Falla & Safro (arXiv:2605.06858), Cadavid et al. (arXiv:2602.23976), Yang et al. (arXiv:2609.15708), and Proctor et al. (Sandia National Laboratories, Nature Physics 2022).
        </p>
      </footer>
    </div>
  );
}
