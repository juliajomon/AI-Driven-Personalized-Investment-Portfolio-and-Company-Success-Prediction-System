import React from 'react';
import { useNavigate } from 'react-router-dom';

const HistoryPage = () => {
  const navigate = useNavigate();

  // In a real application, this component would:
  // 1. Fetch data from Flask endpoint: /api/portfolio/history
  // 2. Display the saved portfolios (Date, Target Return, Final Value).

  return (
    <div className="p-8 min-h-screen bg-gray-100">
      <header className="mb-8">
        <button onClick={() => navigate('/dashboard')} className="text-blue-600 hover:text-blue-800 flex items-center mb-4">
          ← Back to Dashboard
        </button>
        <h1 className="text-3xl font-extrabold text-gray-900">Historical Optimizations</h1>
        <p className="text-gray-600 mt-2">Review your past investment strategies and market conditions.</p>
      </header>

      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h2 className="text-xl font-semibold mb-4">Portfolio History Log</h2>
        <div className="space-y-4">
          <div className="p-4 border rounded-md bg-gray-50">
            <p className="font-bold">Optimization Run: 2025-11-27 (Latest)</p>
            <p className="text-sm">Target: 22.0% | Achieved: 22.0% | Volatility: 15.52%</p>
            <p className="text-sm text-yellow-700">Status: HIGH RISK WARNING (ADJUST)</p>
          </div>
          <div className="p-4 border rounded-md bg-gray-50">
            <p className="font-bold">Optimization Run: 2025-11-20</p>
            <p className="text-sm">Target: 18.0% | Achieved: 18.0% | Volatility: 10.05%</p>
            <p className="text-sm text-green-700">Status: SUCCESS</p>
          </div>
          <p className="text-sm text-gray-500">Note: To save history permanently, you need to set up a database (MySQL/Postgres) and corresponding Flask endpoints.</p>
        </div>
      </div>
    </div>
  );
};

export default HistoryPage;