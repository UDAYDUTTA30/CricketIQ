import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  CartesianGrid, LineChart, Line, ReferenceLine
} from 'recharts';
import { Search, User, Award, Target, TrendingUp, Zap, Shield } from 'lucide-react';

function MiniStat({ label, value, highlight = false, sub = null }) {
  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-xl p-3.5 flex flex-col gap-0.5">
      <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-500">{label}</span>
      <span className={`font-heading font-bold text-2xl ${highlight ? 'text-emerald-400' : 'text-slate-100'}`}>{value}</span>
      {sub && <span className="text-[11px] text-slate-500">{sub}</span>}
    </div>
  );
}

export default function PlayerAnalytics() {
  const [players, setPlayers] = useState([]);
  const [search, setSearch] = useState('');
  const [selectedPlayer, setSelectedPlayer] = useState('');
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState('batting');

  useEffect(() => {
    axios.get('/api/players/')
      .then(res => {
        setPlayers(res.data);
        if (res.data.length > 0) setSelectedPlayer(res.data[0]);
      })
      .catch(console.error);
  }, []);

  useEffect(() => {
    if (!selectedPlayer) return;
    setLoading(true);
    axios.get(`/api/players/${encodeURIComponent(selectedPlayer)}`)
      .then(res => { setProfile(res.data); setLoading(false); })
      .catch(() => setLoading(false));
  }, [selectedPlayer]);

  const filtered = players.filter(p =>
    p.toLowerCase().includes(search.toLowerCase())
  );

  const bat = profile?.batting || {};
  const bowl = profile?.bowling || {};

  const phaseOrder = ['Powerplay', 'Middle', 'Death'];
  const sortedPhases = (bat.phase_breakdown || []).sort(
    (a, b) => phaseOrder.indexOf(a.match_phase) - phaseOrder.indexOf(b.match_phase)
  );

  const recentFormData = (bat.recent_form || []).map((d, i) => ({
    name: `Inn ${i + 1}`,
    runs: d.runs
  }));

  return (
    <div className="flex gap-6 h-full">
      {/* ── Left Sidebar: Player List ── */}
      <div className="w-64 flex-shrink-0 glass-card rounded-2xl p-4 flex flex-col gap-3">
        <h2 className="font-heading font-bold text-base text-slate-200 flex items-center gap-2">
          <User size={18} className="text-emerald-400" /> Players
        </h2>
        <div className="relative">
          <Search size={14} className="absolute left-3 top-2.5 text-slate-500" />
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search player..."
            className="w-full pl-8 pr-3 py-2 bg-slate-900 border border-slate-800 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-emerald-500"
          />
        </div>
        <div className="overflow-y-auto flex-1 space-y-1 max-h-[70vh]">
          {filtered.map(p => (
            <button
              key={p}
              onClick={() => setSelectedPlayer(p)}
              className={`w-full text-left px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                selectedPlayer === p
                  ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
              }`}
            >
              {p}
            </button>
          ))}
        </div>
      </div>

      {/* ── Right: Player Stats ── */}
      <div className="flex-1 min-w-0 space-y-5">
        {/* Header */}
        <div className="glass-card rounded-2xl p-5 flex items-center justify-between">
          <div>
            <h1 className="font-heading font-extrabold text-2xl text-slate-100">{selectedPlayer || 'Select a Player'}</h1>
            <p className="text-xs text-slate-400 mt-0.5">Full career T20 analytics — batting & bowling</p>
          </div>
          {/* Tab Switcher */}
          <div className="flex items-center gap-1 bg-slate-900 p-1 rounded-xl border border-slate-800">
            {['batting', 'bowling'].map(t => (
              <button
                key={t}
                onClick={() => setTab(t)}
                className={`px-4 py-1.5 rounded-lg text-xs font-semibold capitalize transition-all ${
                  tab === t
                    ? 'bg-emerald-500 text-slate-950 shadow'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >{t}</button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="glass-card rounded-2xl p-12 text-center text-slate-400">
            <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
            Loading player stats...
          </div>
        ) : !profile ? null : tab === 'batting' ? (
          <>
            {/* ── Batting Hero Stats ── */}
            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3">
              <MiniStat label="Innings" value={bat.innings ?? 0} />
              <MiniStat label="Runs" value={bat.runs ?? 0} highlight />
              <MiniStat label="Average" value={bat.average ?? 0} />
              <MiniStat label="Strike Rate" value={bat.strike_rate ?? 0} highlight />
              <MiniStat label="High Score" value={bat.highest_score ?? 0} sub="best innings" />
              <MiniStat label="50s / 100s" value={`${bat.fifty_plus ?? 0} / ${bat.hundred_plus ?? 0}`} />
              <MiniStat label="4s / 6s" value={`${bat.fours ?? 0} / ${bat.sixes ?? 0}`} />
              <MiniStat label="Ducks" value={bat.duck_count ?? 0} />
            </div>

            {/* Additional metrics row */}
            <div className="grid grid-cols-3 gap-3">
              <div className="glass-card rounded-xl p-4 flex items-center justify-between">
                <div>
                  <span className="text-xs text-slate-400">Boundary %</span>
                  <p className="font-heading font-bold text-xl text-amber-400">{bat.boundary_percentage ?? 0}%</p>
                  <span className="text-[11px] text-slate-500">runs from boundaries</span>
                </div>
                <Zap size={28} className="text-amber-400/30" />
              </div>
              <div className="glass-card rounded-xl p-4 flex items-center justify-between">
                <div>
                  <span className="text-xs text-slate-400">Dot Ball %</span>
                  <p className="font-heading font-bold text-xl text-red-400">
                    {bat.balls > 0 ? ((bat.dots / bat.balls) * 100).toFixed(1) : 0}%
                  </p>
                  <span className="text-[11px] text-slate-500">{bat.dots ?? 0} dot balls</span>
                </div>
                <Shield size={28} className="text-red-400/30" />
              </div>
              <div className="glass-card rounded-xl p-4 flex items-center justify-between">
                <div>
                  <span className="text-xs text-slate-400">Not Outs</span>
                  <p className="font-heading font-bold text-xl text-teal-400">{bat.not_outs ?? 0}</p>
                  <span className="text-[11px] text-slate-500">of {bat.innings ?? 0} innings</span>
                </div>
                <TrendingUp size={28} className="text-teal-400/30" />
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
              {/* Phase Breakdown Chart */}
              <div className="glass-card rounded-2xl p-5 space-y-3">
                <h3 className="font-heading font-semibold text-sm text-slate-300 uppercase tracking-wider">
                  Strike Rate by Phase
                </h3>
                {sortedPhases.length > 0 ? (
                  <div className="h-52">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={sortedPhases} margin={{ top: 5, right: 10, bottom: 5, left: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                        <XAxis dataKey="match_phase" stroke="#64748b" fontSize={11} />
                        <YAxis stroke="#64748b" fontSize={11} />
                        <Tooltip
                          contentStyle={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px', fontSize: '12px' }}
                          formatter={(v, n) => [v, n === 'strike_rate' ? 'Strike Rate' : n]}
                        />
                        <Bar dataKey="strike_rate" fill="#10b981" radius={[4, 4, 0, 0]} name="Strike Rate">
                        </Bar>
                        <Bar dataKey="runs" fill="#3b82f6" radius={[4, 4, 0, 0]} name="Runs" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                ) : (
                  <p className="text-xs text-slate-500 py-8 text-center">No phase data available for this player.</p>
                )}
                <div className="flex items-center gap-4 text-xs text-slate-500">
                  <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-sm bg-emerald-500 inline-block"></span>Strike Rate</span>
                  <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-sm bg-blue-500 inline-block"></span>Runs</span>
                </div>
              </div>

              {/* Recent Form */}
              <div className="glass-card rounded-2xl p-5 space-y-3">
                <h3 className="font-heading font-semibold text-sm text-slate-300 uppercase tracking-wider flex items-center gap-2">
                  <TrendingUp size={16} className="text-emerald-400" /> Recent Form (Last 5 Innings)
                </h3>
                {recentFormData.length > 0 ? (
                  <div className="h-52">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={recentFormData} margin={{ top: 5, right: 10, bottom: 5, left: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                        <XAxis dataKey="name" stroke="#64748b" fontSize={11} />
                        <YAxis stroke="#64748b" fontSize={11} />
                        <ReferenceLine y={bat.average} stroke="#f59e0b" strokeDasharray="4 4" label={{ value: 'Avg', fill: '#f59e0b', fontSize: 10 }} />
                        <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px', fontSize: '12px' }} />
                        <Line type="monotone" dataKey="runs" stroke="#10b981" strokeWidth={2} dot={{ fill: '#10b981', r: 4 }} name="Runs" />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                ) : (
                  <p className="text-xs text-slate-500 py-8 text-center">Insufficient innings data.</p>
                )}
                <p className="text-[11px] text-slate-500">Dashed line shows career batting average of <strong className="text-amber-400">{bat.average}</strong></p>
              </div>
            </div>
          </>
        ) : (
          /* ── Bowling Tab ── */
          <>
            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
              <MiniStat label="Innings" value={bowl.innings ?? 0} />
              <MiniStat label="Wickets" value={bowl.wickets ?? 0} highlight />
              <MiniStat label="Economy" value={bowl.economy ?? 0} />
              <MiniStat label="Average" value={bowl.average ?? 0} />
              <MiniStat label="Strike Rate" value={bowl.strike_rate ?? 0} sub="balls per wicket" />
              <MiniStat label="Overs" value={bowl.overs ?? 0} />
              <MiniStat label="Conceded" value={bowl.conceded ?? 0} />
            </div>

            <div className="glass-card rounded-2xl p-5 space-y-3">
              <h3 className="font-heading font-semibold text-sm text-slate-300 uppercase tracking-wider">
                Wickets & Economy by Phase
              </h3>
              {(bowl.phase_breakdown || []).length > 0 ? (
                <div className="h-56">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={(bowl.phase_breakdown || []).sort(
                        (a, b) => phaseOrder.indexOf(a.match_phase) - phaseOrder.indexOf(b.match_phase)
                      )}
                      margin={{ top: 5, right: 10, bottom: 5, left: 0 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                      <XAxis dataKey="match_phase" stroke="#64748b" fontSize={11} />
                      <YAxis stroke="#64748b" fontSize={11} />
                      <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px', fontSize: '12px' }} />
                      <Bar dataKey="wickets" fill="#3b82f6" radius={[4, 4, 0, 0]} name="Wickets" />
                      <Bar dataKey="conceded" fill="#f43f5e" radius={[4, 4, 0, 0]} name="Runs Conceded" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <p className="text-xs text-slate-500 py-8 text-center">No bowling data for this player.</p>
              )}
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="glass-card rounded-xl p-4">
                <span className="text-xs text-slate-400">Dot Ball %</span>
                <p className="font-heading font-bold text-2xl text-emerald-400">
                  {bowl.dot_percentage ?? 0}%
                </p>
                <p className="text-[11px] text-slate-500">{bowl.dots ?? 0} dot deliveries</p>
              </div>
              <div className="glass-card rounded-xl p-4">
                <span className="text-xs text-slate-400">Legal Balls Bowled</span>
                <p className="font-heading font-bold text-2xl text-blue-400">{bowl.legal_balls ?? 0}</p>
                <p className="text-[11px] text-slate-500">excluding wides & no-balls</p>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
