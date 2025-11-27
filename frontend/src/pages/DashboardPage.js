import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';
import { useNavigate } from 'react-router-dom';

const API_OPTIMIZE_URL = 'http://127.0.0.1:5000/api/optimize';
const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#AF19FF', '#FF4560', '#775DD0'];

const DashboardPage = () => {
  const [amount, setAmount] = useState(50000); // Default investment amount
  const [targetReturn, setTargetReturn] = useState(20); // Default target return
  const [portfolioData, setPortfolioData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('Enter your goals and optimize the portfolio!');
  const navigate = useNavigate();

  // Redirect if not logged in (basic guard)
  useEffect(() => {
    if (!localStorage.getItem('userToken')) {
      navigate('/login');
    }
  }, [navigate]);


  const handleOptimize = async () => {
    setLoading(true);
    setMessage('');
    setPortfolioData(null);

    try {
      const response = await axios.post(API_OPTIMIZE_URL, {
        amount: Number(amount),
        target_return: Number(targetReturn)
      });

      // Set the message based on the API response (SUCCESS, ADJUST)
      setMessage(response.data.message);
      setPortfolioData(response.data);

    } catch (err) {
      const apiError = err.response?.data?.error || 'Optimization failed due to an internal server error.';
      setMessage(`❌ ERROR: ${apiError}`);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('userToken');
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* HEADER/NAV */}
      <header className="bg-blue-600 shadow-md p-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-white">Investoo Dashboard</h1>
        <div className="space-x-4">
          <button onClick={() => navigate('/history')} className="text-white hover:text-blue-200">History</button>
          <button onClick={logout} className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600">Logout</button>
        </div>
      </header>

      <div className="p-8">
        <h2 className="text-3xl font-extrabold text-gray-900 mb-6">Personalized Portfolio Engine</h2>

        {/* INPUT/CONTROL PANEL */}
        <div className="bg-white p-6 rounded-lg shadow-lg mb-8 grid grid-cols-1 md:grid-cols-4 gap-4 items-end">
          {/* Amount Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Investment Amount (₹)</label>
            <input type="number" value={amount} onChange={(e) => setAmount(e.target.value)}
              className="mt-1 p-3 border border-gray-300 rounded-md w-full"
            />
          </div>
          {/* Return Target Input */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Target Return (%)</label>
            <input type="number" value={targetReturn} onChange={(e) => setTargetReturn(e.target.value)}
              className="mt-1 p-3 border border-gray-300 rounded-md w-full"
            />
          </div>
          {/* Optimization Button */}
          <button onClick={handleOptimize} disabled={loading}
            className="col-span-2 bg-green-600 text-white p-3 rounded-md font-semibold hover:bg-green-700 disabled:bg-gray-400 h-11"
          >
            {loading ? 'Optimizing...' : 'Run Optimization (Step 5)'}
          </button>
        </div>

        {/* RESULTS DISPLAY */}
        {portfolioData ? (
          <div className="space-y-6">
            
            {/* STATUS MESSAGE */}
            <div className={`p-4 rounded-lg font-bold ${portfolioData.status === 'ADJUST' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'}`}>
              STATUS: {message}
            </div>

            {/* METRICS & CHART */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              
              {/* Metrics */}
              <div className="lg:col-span-1 bg-white p-6 rounded-lg shadow-md space-y-4">
                <h3 className="text-xl font-semibold mb-3 border-b pb-2">Portfolio Metrics</h3>
                <p>Expected Return: <span className="font-bold text-green-600">{portfolioData.metrics.expected_return}%</span></p>
                <p>Estimated Risk (Vol.): <span className="font-bold text-red-600">{portfolioData.metrics.estimated_risk}%</span></p>
                <p>Sharpe Ratio: <span className="font-bold">{portfolioData.metrics.sharpe_ratio}</span></p>
                <p>Total Value: <span className="font-bold">₹{Number(amount).toLocaleString()}</span></p>
              </div>

              {/* Pie Chart */}
              <div className="lg:col-span-2 bg-white p-6 rounded-lg shadow-md h-96">
                <h3 className="text-xl font-semibold mb-4 text-center">Optimal Asset Allocation</h3>
                <ResponsiveContainer width="100%" height="90%">
                  <PieChart>
                    <Pie data={portfolioData.portfolio} dataKey="value" nameKey="name" 
                         cx="50%" cy="50%" outerRadius={120} fill="#8884d8" labelLine={false}
                         label={({ percent }) => `${(percent * 100).toFixed(0)}%`}
                         legendType="square"
                    >
                      {portfolioData.portfolio.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value, name, props) => [`₹${value.toLocaleString()}`, props.payload.name]} />
                    <Legend layout="vertical" verticalAlign="middle" align="right" />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* ALLOCATION TABLE */}
            <h3 className="text-2xl font-semibold mt-8 mb-4">Recommended Holdings</h3>
            <div className="overflow-x-auto bg-white p-4 rounded-lg shadow-md">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Company (Ticker)</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Sector</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Optimal Weight</th>
                    <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Investment Value (₹)</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {portfolioData.portfolio.map((stock, idx) => (
                    <tr key={idx}>
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{stock.name} ({stock.ticker})</td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{stock.sector}</td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-semibold text-blue-600">{(stock.weight * 100).toFixed(2)}%</td>
                      <td className="px-6 py-4 whitespace-nowrap text-right text-base font-bold">₹{stock.value.toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ) : (
          <div className="text-center p-20 text-gray-500">
            Click 'Run Optimization' to generate your first AI-driven portfolio.
          </div>
        )}
      </div>
    </div>
  );
};

export default DashboardPage;