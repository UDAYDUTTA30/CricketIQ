import React, { useState } from 'react';
import Navbar from './components/navbar/Navbar';
import Overview from './pages/Dashboard/Overview';
import PlayerAnalytics from './pages/PlayerAnalytics/PlayerAnalytics';
import TeamAnalytics from './pages/TeamAnalytics/TeamAnalytics';
import ScorePrediction from './pages/Prediction/ScorePrediction';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100 font-sans">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="flex-1 max-w-7xl w-full mx-auto p-6 md:p-8">
        {activeTab === 'overview' && <Overview onSelectTab={setActiveTab} />}
        {activeTab === 'players' && <PlayerAnalytics />}
        {activeTab === 'teams' && <TeamAnalytics />}
        {activeTab === 'prediction' && <ScorePrediction />}
      </main>

      <footer className="glass-card border-t border-slate-800/80 py-6 px-8 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
          <div>
            <span className="font-semibold text-slate-300">CricketIQ AI Platform 2.0</span> • Built with FastAPI, React & Random Forest ML
          </div>
          <div>
            Data Source: Cricsheet T20 Ball-by-Ball Dataset
          </div>
        </div>
      </footer>
    </div>
  );
}
