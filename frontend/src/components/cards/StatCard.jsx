import React from 'react';

export default function StatCard({ title, value, subtitle, icon: Icon, color = 'emerald' }) {
  const colorMap = {
    emerald: 'from-emerald-500/20 to-teal-500/5 text-emerald-400 border-emerald-500/20',
    blue: 'from-blue-500/20 to-cyan-500/5 text-blue-400 border-blue-500/20',
    purple: 'from-purple-500/20 to-indigo-500/5 text-purple-400 border-purple-500/20',
    amber: 'from-amber-500/20 to-orange-500/5 text-amber-400 border-amber-500/20'
  };

  return (
    <div className={`glass-card glass-card-hover p-5 rounded-2xl bg-gradient-to-br ${colorMap[color] || colorMap.emerald}`}>
      <div className="flex items-center justify-between mb-3">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">{title}</span>
        {Icon && (
          <div className="p-2.5 rounded-xl bg-slate-900/60 border border-slate-800">
            <Icon size={18} />
          </div>
        )}
      </div>
      <div className="font-heading font-bold text-3xl text-slate-100 mb-1">{value}</div>
      {subtitle && <p className="text-xs text-slate-400 font-medium">{subtitle}</p>}
    </div>
  );
}
