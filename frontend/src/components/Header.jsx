import React from 'react';
import { Cpu, ShieldCheck } from 'lucide-react';

export default function Header({ status }) {
  const sponsors = [
    { name: "Nasdaq", tag: "FINTECH" },
    { name: "Quantum Rings", tag: "SDK" },
    { name: "IonQ", tag: "TRAPPED-ION" },
    { name: "Sandia Nat Lab", tag: "METROLOGY" },
    { name: "IBM Quantum", tag: "AER" },
    { name: "Classiq", tag: "SYNTHESIS" },
    { name: "BYU Physics", tag: "HOST" }
  ];

  return (
    <header className="border-b border-zinc-800/90 bg-[#09090b]/95 backdrop-blur-md sticky top-0 z-50 px-6 py-3.5 transition-all">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-gradient-to-b from-zinc-700 to-zinc-900 border border-zinc-700/80 flex items-center justify-center shadow-md shadow-black transition-transform duration-300 hover:scale-105">
              <Cpu className="h-5 w-5 text-zinc-200" />
            </div>
            <div>
              <div className="flex items-center gap-2.5">
                <h1 className="text-xl font-extrabold tracking-tight text-white flex items-center gap-2">
                  Q-FRONTIER
                  <span className="text-[10px] font-mono font-normal text-zinc-400">v2.0</span>
                </h1>
                <span className="text-[10px] font-mono font-bold tracking-wider uppercase px-2 py-0.5 rounded-full bg-zinc-800/90 text-zinc-300 border border-zinc-700/70">
                  IQC 2026
                </span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-zinc-900 text-zinc-400 border border-zinc-800">
                  SIMULATED
                </span>
              </div>
              <p className="text-xs text-zinc-400 font-medium tracking-tight">
                Context-Aware Counterdiabatic Optimization & Auditable Metrology
              </p>
            </div>
          </div>
        </div>

        {/* Sponsor Badges & System Status */}
        <div className="flex flex-col items-start md:items-end gap-2">
          <div className="flex items-center gap-2">
            <span className="flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-zinc-300 opacity-60"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-zinc-100"></span>
            </span>
            <span className="text-[11px] font-mono text-zinc-300 font-medium">
              Quantum Backend: Active (QuantumRingsLib / Aer)
            </span>
          </div>

          <div className="flex flex-wrap gap-1.5 items-center">
            {sponsors.map((s, idx) => (
              <span
                key={idx}
                className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-zinc-900/90 border border-zinc-800 text-zinc-300 hover:border-zinc-600 hover:text-white transition-all cursor-default"
                title={`${s.name} - ${s.tag}`}
              >
                <span className="font-semibold text-zinc-200">{s.name}</span>
              </span>
            ))}
          </div>
        </div>
      </div>
    </header>
  );
}
