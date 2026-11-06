import React from 'react';
import StatCard from '../../components/cards/StatCard';
import { Database, Cpu, Zap, Flame, Award, ArrowUpRight } from 'lucide-react';

export default function Overview({ onSelectTab }) {
  return (
    <div className="space-y-8">
      {/* Hero Banner */}
      <div className="relative overflow-hidden glass-card rounded-3xl p-8 bg-gradient-to-r from-slate-900 via-slate-900 to-emerald-950/40 border-emerald-500/20">
        <div className="relative z-10 max-w-2xl space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold">
            <Flame size={14} /> AI-Powered Sports Intelligence
          </div>
          <h2 className="font-heading font-extrabold text-4xl text-slate-100 leading-tight">
            Advanced T20 Visual Analytics & <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-teal-300">Live Score ML Predictor</span>
          </h2>
          <p className="text-slate-400 text-sm leading-relaxed">
            CricketIQ AI combines Cricsheet T20 ball-by-ball datasets with Random Forest and XGBoost regressors, delivering real-time 1st innings score predictions alongside SHAP explainable AI.
          </p>
          <div className="flex items-center gap-4 pt-2">
            <button
              onClick={() => onSelectTab('prediction')}
              className="flex items-center gap-2 px-6 py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-bold text-sm shadow-lg shadow-emerald-500/25 hover:shadow-emerald-500/40 transition-all"
            >
              <Cpu size={18} /> Launch AI Predictor
            </button>
            <button
              onClick={() => onSelectTab('players')}
              className="flex items-center gap-2 px-6 py-3 rounded-xl glass-card text-slate-300 font-semibold text-sm hover:text-slate-100 hover:bg-slate-800/60 transition-all"
            >
              Explore Player Stats <ArrowUpRight size={16} />
            </button>
          </div>
        </div>
      </div>

      {/* Quick Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-5">
        <StatCard title="Dataset Coverage" value="1,500+" subtitle="Cricsheet Men's T20 Matches" icon={Database} color="emerald" />
        <StatCard title="Deliveries Processed" value="300k+" subtitle="Normalized Ball-by-Ball Rows" icon={Zap} color="blue" />
        <StatCard title="ML Model Accuracy" value="99.85%" subtitle="Random Forest R² Score" icon={Award} color="purple" />
        <StatCard title="Average 1st Score" value="164.2" subtitle="T20 International & Leagues" icon={Flame} color="amber" />
      </div>

      {/* Feature Highlights Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-card p-6 rounded-2xl space-y-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold">
            01
          </div>
          <h3 className="font-heading font-bold text-lg text-slate-100">Global Filtering Engine</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Slice and dice stats by player, bowler, venue, opponent team, and match phase (Powerplay, Middle, Death overs).
          </p>
        </div>

        <div className="glass-card p-6 rounded-2xl space-y-3">
          <div className="w-10 h-10 rounded-xl bg-teal-500/10 border border-teal-500/20 text-teal-400 flex items-center justify-center font-bold">
            02
          </div>
          <h3 className="font-heading font-bold text-lg text-slate-100">AI Score Prediction</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Dynamic first innings score estimation using real-time match context, current run rate, and 5-over momentum.
          </p>
        </div>

        <div className="glass-card p-6 rounded-2xl space-y-3">
          <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 flex items-center justify-center font-bold">
            03
          </div>
          <h3 className="font-heading font-bold text-lg text-slate-100">Explainable AI (SHAP)</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Unpack black-box predictions with SHAP feature contributions showing exactly why the AI predicted a specific target.
          </p>
        </div>
      </div>
    </div>
  );
}
