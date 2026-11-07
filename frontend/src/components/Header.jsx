import React from 'react';
import { Cpu, ShieldCheck, Activity, Award } from 'lucide-react';

export default function Header() {
  const sponsors = [
    { name: "Nasdaq", color: "bg-blue-500/10 text-blue-400 border-blue-500/20" },
    { name: "Quantum Rings", color: "bg-cyan-500/10 text-cyan-400 border-cyan-500/20" },
    { name: "IonQ", color: "bg-purple-500/10 text-purple-400 border-purple-500/20" },
    { name: "Sandia Nat Lab", color: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20" },
    { name: "IBM Quantum", color: "bg-indigo-500/10 text-indigo-400 border-indigo-500/20" },
    { name: "Classiq", color: "bg-amber-500/10 text-amber-400 border-amber-500/20" },
    { name: "BYU Physics", color: "bg-sky-500/10 text-sky-400 border-sky-500/20" }
  ];

  return (
    <header className="border-b border-slate-800/80 bg-[#0a0f1d]/90 backdrop-blur-md sticky top-0 z-50 px-6 py-4">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <Cpu className="h-5 w-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2 flex-wrap">
                <h1 className="text-2xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-cyan-400 bg-clip-text text-transparent">
                  Q-FRONTIER
                </h1>
                <span className="text-[11px] font-semibold tracking-wider uppercase px-2 py-0.5 rounded-full bg-cyan-950 text-cyan-300 border border-cyan-800/50">
                  Auditable Hybrid Workbench
                </span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-amber-950/60 text-amber-400 border border-amber-800/40">
                  Research Prototype — Not Investment Advice
                </span>
              </div>
              <p className="text-xs text-slate-400 font-medium mt-0.5">
                Constraint-Preserving Quantum & Classical Hybrid Portfolio Optimization • IQC 2026
              </p>
            </div>
          </div>
        </div>

        {/* Sponsor Badges & System Status */}
        <div className="flex flex-col items-start md:items-end gap-2">
          <div className="flex items-center gap-2">
            <span className="flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
            </span>
            <span className="text-xs font-mono text-cyan-300 font-medium">
              Quantum Simulator: Aer / Statevector (SIMULATED)
            </span>
          </div>

          <div className="flex flex-wrap gap-1.5 items-center">
            {sponsors.map((s, idx) => (
              <span
                key={idx}
                className={`text-[10px] font-medium px-2 py-0.5 rounded-md border ${s.color}`}
              >
                {s.name}
              </span>
            ))}
          </div>
        </div>
      </div>
    </header>
  );
}
