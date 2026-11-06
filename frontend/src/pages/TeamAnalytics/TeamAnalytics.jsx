import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Swords, Trophy, Zap, MapPin, TrendingUp, Shield } from 'lucide-react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

function TeamStatCard({ label, team1Val, team2Val, team1, team2, highlightHigher = true }) {
  const t1Better = highlightHigher ? team1Val >= team2Val : team1Val <= team2Val;
  return (
    <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-3 grid grid-cols-3 items-center gap-2">
      <div className="text-right">
        <span className={`font-heading font-bold text-xl ${t1Better ? 'text-emerald-400' : 'text-slate-300'}`}>{team1Val}</span>
        {t1Better && <span className="ml-1 text-emerald-400 text-xs">✦</span>}
      </div>
      <div className="text-center">
        <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-500 block">{label}</span>
      </div>
      <div className="text-left">
        {!t1Better && <span className="mr-1 text-blue-400 text-xs">✦</span>}
        <span className={`font-heading font-bold text-xl ${!t1Better ? 'text-blue-400' : 'text-slate-300'}`}>{team2Val}</span>
      </div>
    </div>
  );
}

export default function TeamAnalytics() {
  const [teams, setTeams] = useState([]);
  const [team1, setTeam1] = useState('');
  const [team2, setTeam2] = useState('');
  const [h2h, setH2H] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    axios.get('/api/teams/')
      .then(res => {
        setTeams(res.data);
        if (res.data.length >= 2) {
          setTeam1(res.data[0]);
          setTeam2(res.data[1]);
        }
      })
      .catch(console.error);
  }, []);

  useEffect(() => {
    if (!team1 || !team2 || team1 === team2) return;
    setLoading(true);
    axios.get(`/api/teams/h2h?team1=${encodeURIComponent(team1)}&team2=${encodeURIComponent(team2)}`)
      .then(res => { setH2H(res.data); setLoading(false); })
      .catch(() => setLoading(false));
  }, [team1, team2]);

  const pieData = h2h ? [
    { name: h2h.team1, value: h2h.team1_wins, color: '#10b981' },
    { name: h2h.team2, value: h2h.team2_wins, color: '#3b82f6' },
    ...(h2h.no_results > 0 ? [{ name: 'No Result/Tie', value: h2h.no_results, color: '#475569' }] : [])
  ] : [];

  const tossData = h2h ? [
    { name: h2h.team1, toss_wins: h2h.toss_analysis.team1_toss_wins, match_wins: h2h.toss_analysis.team1_wins_after_toss },
    { name: h2h.team2, toss_wins: h2h.toss_analysis.team2_toss_wins, match_wins: h2h.toss_analysis.team2_wins_after_toss },
  ] : [];

  return (
    <div className="space-y-5">
      {/* Team Selector */}
      <div className="glass-card p-5 rounded-2xl">
        <div className="flex items-center gap-3 mb-4">
          <div className="p-2.5 rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
            <Swords size={20} />
          </div>
          <div>
            <h2 className="font-heading font-bold text-xl text-slate-100">Head-to-Head Team Comparison</h2>
            <p className="text-xs text-slate-400">Full historical analysis, toss trends, batting comparisons & recent encounters</p>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-semibold text-slate-400 mb-1.5 block">Team A</label>
            <select
              value={team1}
              onChange={e => setTeam1(e.target.value)}
              className="w-full px-4 py-2.5 bg-slate-900 border border-slate-800 rounded-xl text-sm font-medium text-emerald-400 focus:outline-none focus:border-emerald-500"
            >
              {teams.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
          <div>
            <label className="text-xs font-semibold text-slate-400 mb-1.5 block">Team B</label>
            <select
              value={team2}
              onChange={e => setTeam2(e.target.value)}
              className="w-full px-4 py-2.5 bg-slate-900 border border-slate-800 rounded-xl text-sm font-medium text-blue-400 focus:outline-none focus:border-blue-500"
            >
              {teams.map(t => <option key={t} value={t}>{t}</option>)}
            </select>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="glass-card p-12 rounded-2xl text-center text-slate-400">
          <div className="w-8 h-8 border-2 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
          Crunching head-to-head data...
        </div>
      ) : h2h && h2h.total_matches === 0 ? (
        <div className="glass-card p-10 rounded-2xl text-center text-slate-400 text-sm">
          No matches found between <strong className="text-emerald-400">{team1}</strong> and <strong className="text-blue-400">{team2}</strong> in the current dataset.
        </div>
      ) : h2h ? (
        <>
          {/* Win summary banner */}
          <div className="grid grid-cols-3 gap-4">
            <div className="glass-card rounded-2xl p-5 text-center border-emerald-500/20">
              <span className="text-xs font-semibold text-emerald-400 block uppercase tracking-wider">{h2h.team1}</span>
              <span className="font-heading font-extrabold text-5xl text-emerald-400">{h2h.team1_wins}</span>
              <span className="text-xs text-slate-500 block mt-1">wins</span>
            </div>
            <div className="glass-card rounded-2xl p-5 text-center">
              <span className="text-xs font-semibold text-slate-400 block uppercase tracking-wider">Total</span>
              <span className="font-heading font-extrabold text-5xl text-slate-200">{h2h.total_matches}</span>
              <span className="text-xs text-slate-500 block mt-1">encounters · {h2h.no_results} no result</span>
            </div>
            <div className="glass-card rounded-2xl p-5 text-center border-blue-500/20">
              <span className="text-xs font-semibold text-blue-400 block uppercase tracking-wider">{h2h.team2}</span>
              <span className="font-heading font-extrabold text-5xl text-blue-400">{h2h.team2_wins}</span>
              <span className="text-xs text-slate-500 block mt-1">wins</span>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
            {/* Head-to-head stat comparison */}
            <div className="lg:col-span-2 glass-card rounded-2xl p-5 space-y-3">
              <h3 className="font-heading font-bold text-sm text-slate-300 uppercase tracking-wider flex items-center gap-2">
                <TrendingUp size={16} className="text-emerald-400" /> Performance Comparison
              </h3>
              <div className="flex text-[11px] font-semibold uppercase tracking-wider text-center mb-1">
                <div className="flex-1 text-emerald-400">{h2h.team1}</div>
                <div className="w-40 text-slate-500">Metric</div>
                <div className="flex-1 text-blue-400">{h2h.team2}</div>
              </div>
              <div className="space-y-2">
                <TeamStatCard
                  label="Wins" team1={h2h.team1} team2={h2h.team2}
                  team1Val={h2h.team1_wins} team2Val={h2h.team2_wins}
                />
                <TeamStatCard
                  label="Avg Score" team1={h2h.team1} team2={h2h.team2}
                  team1Val={h2h.innings_batting.team1_avg_score}
                  team2Val={h2h.innings_batting.team2_avg_score}
                />
                <TeamStatCard
                  label="High Score" team1={h2h.team1} team2={h2h.team2}
                  team1Val={h2h.innings_batting.team1_high}
                  team2Val={h2h.innings_batting.team2_high}
                />
                <TeamStatCard
                  label="Toss Wins" team1={h2h.team1} team2={h2h.team2}
                  team1Val={h2h.toss_analysis.team1_toss_wins}
                  team2Val={h2h.toss_analysis.team2_toss_wins}
                />
                <TeamStatCard
                  label="Win after Toss" team1={h2h.team1} team2={h2h.team2}
                  team1Val={h2h.toss_analysis.team1_wins_after_toss}
                  team2Val={h2h.toss_analysis.team2_wins_after_toss}
                />
                <TeamStatCard
                  label="Bat 1st Wins" team1={h2h.team1} team2={h2h.team2}
                  team1Val={h2h.first_innings_wins.team1_bat_first_wins}
                  team2Val={h2h.first_innings_wins.team2_bat_first_wins}
                />
                <TeamStatCard
                  label="Field 1st Wins" team1={h2h.team1} team2={h2h.team2}
                  team1Val={h2h.first_innings_wins.team1_field_first_wins}
                  team2Val={h2h.first_innings_wins.team2_field_first_wins}
                />
              </div>
            </div>

            {/* Right column: Pie + Toss chart */}
            <div className="space-y-4">
              {/* Win distribution donut */}
              <div className="glass-card rounded-2xl p-4 text-center">
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Win Split</h4>
                <div className="h-44">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie data={pieData} cx="50%" cy="50%" innerRadius={45} outerRadius={72} paddingAngle={3} dataKey="value">
                        {pieData.map((e, i) => <Cell key={i} fill={e.color} />)}
                      </Pie>
                      <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px', fontSize: '12px' }} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
                <div className="flex justify-center gap-4 text-[11px]">
                  {pieData.map((d, i) => (
                    <span key={i} className="flex items-center gap-1">
                      <span className="w-2 h-2 rounded-full inline-block" style={{ background: d.color }} />
                      {d.name}: <strong>{d.value}</strong>
                    </span>
                  ))}
                </div>
              </div>

              {/* Toss bar chart */}
              <div className="glass-card rounded-2xl p-4">
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Toss Wins vs Match Wins</h4>
                <div className="h-36">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={tossData} margin={{ top: 0, right: 5, bottom: 0, left: -20 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                      <XAxis dataKey="name" stroke="#64748b" fontSize={10} />
                      <YAxis stroke="#64748b" fontSize={10} />
                      <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px', fontSize: '11px' }} />
                      <Bar dataKey="toss_wins" fill="#7c3aed" radius={[3, 3, 0, 0]} name="Toss Wins" />
                      <Bar dataKey="match_wins" fill="#10b981" radius={[3, 3, 0, 0]} name="Won After Toss" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </div>

          {/* Recent matches table */}
          {h2h.recent_matches?.length > 0 && (
            <div className="glass-card rounded-2xl p-5 space-y-3">
              <h3 className="font-heading font-bold text-sm text-slate-300 uppercase tracking-wider">
                Recent Encounters (Last {h2h.recent_matches.length})
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="text-slate-500 uppercase text-[10px] tracking-wider border-b border-slate-800">
                    <tr>
                      <th className="pb-2 pr-4">Date</th>
                      <th className="pb-2 pr-4">Venue</th>
                      <th className="pb-2 pr-4">Toss</th>
                      <th className="pb-2 pr-4">Winner</th>
                      <th className="pb-2">Margin</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/50">
                    {h2h.recent_matches.map((m, i) => {
                      const margin = m.win_by_runs > 0 ? `${m.win_by_runs} runs` : m.win_by_wickets > 0 ? `${m.win_by_wickets} wkts` : '—';
                      const isT1Win = m.winner === h2h.team1;
                      const isT2Win = m.winner === h2h.team2;
                      return (
                        <tr key={i} className="hover:bg-slate-900/30 transition-colors">
                          <td className="py-2 pr-4 font-mono text-slate-400">{m.date}</td>
                          <td className="py-2 pr-4 text-slate-300 flex items-center gap-1">
                            <MapPin size={10} className="text-slate-600 flex-shrink-0" />{m.venue}
                          </td>
                          <td className="py-2 pr-4 text-slate-400">{m.toss_winner} ({m.toss_decision})</td>
                          <td className={`py-2 pr-4 font-semibold ${isT1Win ? 'text-emerald-400' : isT2Win ? 'text-blue-400' : 'text-slate-400'}`}>
                            {m.winner || 'No result'}
                          </td>
                          <td className="py-2 text-slate-400">{margin}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </>
      ) : null}
    </div>
  );
}
