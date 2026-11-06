import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Cpu, Play, Sparkles, AlertCircle, Lightbulb, TrendingUp, TrendingDown, Target } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, ReferenceLine, CartesianGrid } from 'recharts';

const MODELS = [
  { value: 'random_forest', label: 'Random Forest (R² 0.9985) — Recommended' },
  { value: 'xgboost', label: 'XGBoost (R² 0.9977)' },
  { value: 'linear_regression', label: 'Linear Regression (R² 0.9738)' },
];

function ScoreGauge({ predicted, low, high }) {
  const pct = Math.min(Math.max(((predicted - 80) / (280 - 80)) * 100, 0), 100);
  return (
    <div className="space-y-3">
      <div className="text-center">
        <span className="text-xs font-semibold uppercase tracking-wider text-emerald-400 block mb-1">Projected 1st Innings Score</span>
        <span className="font-heading font-extrabold text-7xl text-slate-100 drop-shadow-md leading-none">{predicted}</span>
        <span className="text-slate-400 text-sm block mt-1">
          Confidence range: <strong className="text-slate-200">{low}</strong> – <strong className="text-slate-200">{high}</strong>
        </span>
      </div>
      <div className="relative w-full h-3 bg-slate-800 rounded-full overflow-hidden">
        <div
          className="absolute left-0 top-0 h-full rounded-full bg-gradient-to-r from-blue-500 via-emerald-400 to-amber-400 transition-all duration-700"
          style={{ width: `${pct}%` }}
        />
      </div>
      <div className="flex justify-between text-[10px] text-slate-500 font-mono">
        <span>80</span><span>120</span><span>160</span><span>200</span><span>240</span><span>280</span>
      </div>
    </div>
  );
}

function InsightBullet({ text }) {
  const isPositive = text.includes('Excellent') || text.includes('ideal') || text.includes('strong runway')
    || text.includes('Strong recent') || text.includes('No wickets lost') || text.includes('all 10') || text.includes('All 10');
  const isNegative = text.includes('Below-par') || text.includes('Heavy') || text.includes('Slowing')
    || text.includes('destabilised') || text.includes('limit');

  const Icon = isPositive ? TrendingUp : isNegative ? TrendingDown : Target;
  const color = isPositive ? 'text-emerald-400' : isNegative ? 'text-red-400' : 'text-amber-400';

  return (
    <li className="flex items-start gap-2.5 text-sm text-slate-300 leading-relaxed">
      <Icon size={15} className={`${color} flex-shrink-0 mt-0.5`} />
      <span>{text}</span>
    </li>
  );
}

export default function ScorePrediction() {
  const [venues, setVenues] = useState([]);
  const [teams, setTeams] = useState([]);

  const [form, setForm] = useState({
    venue: '', team1: '', team2: '',
    over: 10, ball: 3,
    cumulative_runs: 85, cumulative_wickets: 2,
    runs_last_5_overs: 42, wickets_last_5_overs: 1,
    model_name: 'random_forest'
  });
  const [prediction, setPrediction] = useState(null);
  const [shapData, setShapData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [dataReady, setDataReady] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    Promise.all([
      axios.get('/api/venues/'),
      axios.get('/api/teams/')
    ]).then(([venueRes, teamRes]) => {
      const v = venueRes.data;
      const t = teamRes.data;
      setVenues(v);
      setTeams(t);
      setForm(prev => ({
        ...prev,
        venue: v.length > 0 ? v[0] : prev.venue,
        team1: t.length > 0 ? t[0] : prev.team1,
        team2: t.length > 1 ? t[1] : prev.team2,
      }));
      setDataReady(true);
    }).catch(console.error);
  }, []);

  const handleChange = e => {
    const { name, value } = e.target;
    const numFields = ['over', 'ball', 'cumulative_runs', 'cumulative_wickets', 'runs_last_5_overs', 'wickets_last_5_overs'];
    setForm(prev => ({ ...prev, [name]: numFields.includes(name) ? Number(value) : value }));
  };

  const handlePredict = async e => {
    e.preventDefault();
    setError('');
    if (!form.venue || !form.team1 || !form.team2) {
      setError('Please wait for venues and teams to finish loading.');
      return;
    }
    if (form.over === 0 && form.ball === 0) {
      setError('Over and ball cannot both be 0.');
      return;
    }
    setLoading(true);
    try {
      const [predRes, shapRes] = await Promise.all([
        axios.post('/api/prediction/predict', form),
        axios.post('/api/prediction/explain', form),
      ]);
      console.log('[Prediction] predict response:', predRes.data);
      console.log('[Prediction] explain response:', shapRes.data);
      setPrediction(predRes.data);
      setShapData(shapRes.data);
    } catch (err) {
      console.error('[Prediction] Error:', err);
      console.error('[Prediction] Response:', err.response?.data);
      setError(
        err.response?.data?.detail ||
        err.message ||
        'Prediction failed. Check server connection.'
      );
    } finally {
      setLoading(false);
    }
  };

  const shapChartData = (shapData?.top_feature_contributions || []).map(item => ({
    name: item.feature
      .replace('num__', '')
      .replace('cat__', '')
      .replace(/_/g, ' ')
      .replace(/venue /gi, '')
      .replace(/team1 /gi, 'Team A: ')
      .replace(/team2 /gi, 'Team B: '),
    value: parseFloat(item.shap_value.toFixed(3))
  }));

  const inputCls = "w-full px-3 py-2.5 bg-slate-900 border border-slate-800 rounded-xl text-xs text-slate-200 focus:outline-none focus:border-emerald-500 transition-colors";
  const labelCls = "text-[11px] font-semibold uppercase tracking-wider text-slate-500 block mb-1";

  return (
    <div className="space-y-5">
      {/* Header */}
      <div className="glass-card p-5 rounded-2xl flex items-center justify-between border-emerald-500/15">
        <div>
          <h2 className="font-heading font-bold text-xl text-slate-100 flex items-center gap-2">
            <Cpu className="text-emerald-400" size={22} /> AI Score Predictor
          </h2>
          <p className="text-xs text-slate-400 mt-0.5">Machine learning inference with SHAP explainability & contextual insights</p>
        </div>
        <div className="hidden sm:flex items-center gap-2 bg-emerald-500/10 px-3 py-1.5 rounded-full border border-emerald-500/20 text-emerald-400 text-xs font-semibold">
          <Sparkles size={14} /> Models loaded
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-5">
        {/* ── Input Form ── */}
        <form onSubmit={handlePredict} className="glass-card p-5 rounded-2xl lg:col-span-2 space-y-4">
          <h3 className="font-heading font-semibold text-sm text-slate-300 border-b border-slate-800 pb-2">Match State</h3>

          <div>
            <label className={labelCls}>Venue</label>
            <select name="venue" value={form.venue} onChange={handleChange} className={inputCls}>
              {venues.map(v => <option key={v} value={v}>{v}</option>)}
            </select>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className={labelCls}>Batting Team</label>
              <select name="team1" value={form.team1} onChange={handleChange} className={inputCls}>
                {teams.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
            </div>
            <div>
              <label className={labelCls}>Bowling Team</label>
              <select name="team2" value={form.team2} onChange={handleChange} className={inputCls}>
                {teams.map(t => <option key={t} value={t}>{t}</option>)}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className={labelCls}>Over (0–19)</label>
              <input type="number" name="over" min={0} max={19} value={form.over} onChange={handleChange} className={inputCls} />
            </div>
            <div>
              <label className={labelCls}>Ball (1–6)</label>
              <input type="number" name="ball" min={1} max={6} value={form.ball} onChange={handleChange} className={inputCls} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className={labelCls}>Runs Scored</label>
              <input type="number" name="cumulative_runs" min={0} value={form.cumulative_runs} onChange={handleChange} className={inputCls} />
            </div>
            <div>
              <label className={labelCls}>Wickets Lost</label>
              <input type="number" name="cumulative_wickets" min={0} max={10} value={form.cumulative_wickets} onChange={handleChange} className={inputCls} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className={labelCls}>Runs Last 5 Overs</label>
              <input type="number" name="runs_last_5_overs" min={0} value={form.runs_last_5_overs} onChange={handleChange} className={inputCls} />
            </div>
            <div>
              <label className={labelCls}>Wkts Last 5 Overs</label>
              <input type="number" name="wickets_last_5_overs" min={0} max={10} value={form.wickets_last_5_overs} onChange={handleChange} className={inputCls} />
            </div>
          </div>

          <div>
            <label className={labelCls}>ML Model</label>
            <select name="model_name" value={form.model_name} onChange={handleChange} className={inputCls}>
              {MODELS.map(m => <option key={m.value} value={m.value}>{m.label}</option>)}
            </select>
          </div>

          {error && <p className="text-xs text-red-400 bg-red-500/10 border border-red-500/20 rounded-lg px-3 py-2">{error}</p>}

          {!dataReady && (
            <p className="text-xs text-slate-500 text-center animate-pulse">Loading venues and teams...</p>
          )}

          <button
            type="submit"
            disabled={loading || !dataReady}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 text-slate-950 font-bold text-sm flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20 hover:shadow-emerald-500/35 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {!dataReady ? 'Loading...' : loading ? 'Running Inference...' : <><Play size={16} /> Predict Score</>}
          </button>
        </form>

        {/* ── Results Panel ── */}
        <div className="lg:col-span-3 space-y-5">
          {!prediction && !loading ? (
            <div className="glass-card p-12 rounded-2xl text-center space-y-2 text-slate-500">
              <AlertCircle size={36} className="mx-auto text-slate-700 mb-3" />
              <p className="font-heading font-bold text-lg text-slate-300">No prediction yet</p>
              <p className="text-xs max-w-xs mx-auto">Fill in the match state on the left and hit Predict Score.</p>
            </div>
          ) : prediction ? (
            <>
              {/* Score gauge */}
              <div className="glass-card p-6 rounded-2xl space-y-4 bg-gradient-to-b from-emerald-950/20 to-slate-900">
                <ScoreGauge
                  predicted={prediction.predicted_final_score}
                  low={prediction.confidence_range.low}
                  high={prediction.confidence_range.high}
                />

                {/* Live state pills */}
                <div className="flex flex-wrap gap-2 justify-center text-xs">
                  {[
                    { label: 'Runs', val: prediction.current_state.runs },
                    { label: 'Wickets', val: `${prediction.current_state.wickets} / 10` },
                    { label: 'Current RR', val: prediction.current_state.current_rr },
                    { label: 'Momentum RR', val: prediction.current_state.momentum_rr },
                    { label: 'Overs Left', val: prediction.current_state.overs_remaining },
                    { label: 'Model', val: prediction.model_used.replace('_', ' ') },
                  ].map((p, i) => (
                    <span key={i} className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-slate-300">
                      <span className="text-slate-500">{p.label}: </span>
                      <strong>{p.val}</strong>
                    </span>
                  ))}
                </div>
              </div>

              {/* Key Insights */}
              {prediction.insights?.length > 0 && (
                <div className="glass-card p-5 rounded-2xl space-y-3">
                  <h4 className="font-heading font-bold text-sm text-slate-200 flex items-center gap-2">
                    <Lightbulb size={16} className="text-amber-400" /> Why this prediction?
                  </h4>
                  <ul className="space-y-2.5">
                    {prediction.insights.map((insight, i) => (
                      <InsightBullet key={i} text={insight} />
                    ))}
                  </ul>
                </div>
              )}

              {/* SHAP Explanation */}
              {shapChartData.length > 0 && (
                <div className="glass-card p-5 rounded-2xl space-y-3">
                  <h4 className="font-heading font-bold text-sm text-slate-200">
                    SHAP Feature Contributions
                  </h4>
                  <p className="text-[11px] text-slate-500">
                    Each bar shows how much a feature pushed the predicted score up (green) or down (red) from the baseline of <strong className="text-slate-300">{shapData?.base_value}</strong>.
                  </p>
                  <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart layout="vertical" data={shapChartData} margin={{ left: 0, right: 20, top: 5, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
                        <XAxis type="number" stroke="#64748b" fontSize={10} />
                        <YAxis type="category" dataKey="name" stroke="#64748b" fontSize={10} width={160} />
                        <ReferenceLine x={0} stroke="#475569" strokeWidth={1} />
                        <Tooltip
                          contentStyle={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px', fontSize: '11px' }}
                          formatter={(v) => [`${v > 0 ? '+' : ''}${v} runs impact`, 'SHAP Value']}
                        />
                        <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                          {shapChartData.map((entry, i) => (
                            <Cell key={i} fill={entry.value >= 0 ? '#10b981' : '#f43f5e'} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="flex gap-4 text-[11px] text-slate-500">
                    <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-sm bg-emerald-500 inline-block"></span>Pushed score up</span>
                    <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-sm bg-red-500 inline-block"></span>Pushed score down</span>
                  </div>
                </div>
              )}
            </>
          ) : null}
        </div>
      </div>
    </div>
  );
}
