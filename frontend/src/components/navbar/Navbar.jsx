import React from 'react';
import { Activity, User, Users, Cpu, ShieldAlert } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab }) {
  const navItems = [
    { id: 'overview', label: 'Dashboard Overview', icon: Activity },
    { id: 'players', label: 'Player Analytics', icon: User },
    { id: 'teams', label: 'Team & H2H', icon: Users },
    { id: 'prediction', label: 'AI Score Prediction', icon: Cpu },
  ];

  return (
    <header className="sticky top-0 z-50 glass-card border-b border-slate-800/80 bg-slate-950/80 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <span className="font-heading font-extrabold text-slate-950 text-xl tracking-wider">IQ</span>
          </div>
          <div>
            <h1 className="font-heading font-bold text-lg text-slate-100 flex items-center gap-2">
              CricketIQ <span className="text-emerald-400 text-xs px-2 py-0.5 rounded-md bg-emerald-500/10 border border-emerald-500/20">AI 2.0</span>
            </h1>
            <p className="text-xs text-slate-400">Sports Analytics & Predictor</p>
          </div>
        </div>

        <nav className="flex items-center gap-1 bg-slate-900/60 p-1.5 rounded-xl border border-slate-800">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  isActive
                    ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-semibold shadow-md shadow-emerald-500/20'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <Icon size={16} />
                {item.label}
              </button>
            );
          })}
        </nav>

        <div className="flex items-center gap-2 text-xs text-slate-400">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>FastAPI Engine Online</span>
        </div>
      </div>
    </header>
  );
}
