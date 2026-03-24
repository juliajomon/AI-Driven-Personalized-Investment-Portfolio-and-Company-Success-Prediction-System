import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { useNavigate } from 'react-router-dom';
import '../styles/dashboard.css';
import { optimizePortfolio, saveOptimizedPortfolio } from '../api/apiService';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#AF19FF', '#FF4560', '#775DD0'];

const DashboardPage = () => {
  const [amount, setAmount] = useState();
  const [targetReturn, setTargetReturn] = useState();
  const [portfolioData, setPortfolioData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('Enter your goals and optimize the portfolio!');
  const [saving, setSaving] = useState(false);
  const navigate = useNavigate();

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
      const userId = localStorage.getItem('userId') || 1;
      const response = await optimizePortfolio(Number(amount), Number(targetReturn), userId);
      setMessage(response.message);
      setPortfolioData(response);
    } catch (err) {
      const apiError = err.response?.data?.error || err.message || 'Optimization failed due to an internal server error.';
      setMessage(`ERROR: ${apiError}`);
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('userToken');
    localStorage.removeItem('userId');
    navigate('/login');
  };

  const handleSave = async () => {
    if (!portfolioData) return;
    try {
      setSaving(true);
      const userId = localStorage.getItem('userId') || 1; // adjust once you wire real auth IDs
      await saveOptimizedPortfolio({
        userId,
        amount: Number(amount),
        riskRate: portfolioData.metrics.estimated_risk,
        expectedReturn: portfolioData.metrics.expected_return,
        portfolio: portfolioData.portfolio,
      });
      setMessage('Portfolio saved successfully.');
    } catch (err) {
      const apiError = err.response?.data?.error || err.message || 'Failed to save portfolio.';
      setMessage(`ERROR: ${apiError}`);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="dashboard-page">
      <button type="button" onClick={logout} className="logout-button">
        Logout
      </button>
      <button type="button" className="profile-button" onClick={() => navigate('/chatbot')}>
        🤖
      </button>

      <div className="dashboard-container">
        <div className="dashboard-title-section">
          <h1 className="dashboard-title">Personalized Portfolio Engine</h1>
          <p className="dashboard-subtitle">Tune your investment goals and let the AI handle the rest.</p>
        </div>

        <div className="category-buttons">
          <button
            type="button"
            className="dashboard-button"
            onClick={() => navigate('/saved-portfolios')}
          >
            Saved Portfolio
          </button>
          <button
            type="button"
            className="dashboard-button"
            onClick={() => navigate('/history')}
          >
            Optimization History
          </button>
        </div>

        <div className="control-panel">
          <div className="input-group">
            <label htmlFor="amount">Investment Amount (₹)</label>
            <input
              id="amount"
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="control-input"
              min="0"
            />
          </div>
          <div className="input-group">
            <label htmlFor="target-return">Target Return (%)</label>
            <input
              id="target-return"
              type="number"
              value={targetReturn}
              onChange={(e) => setTargetReturn(e.target.value)}
              className="control-input"
              min="0"
            />
          </div>
          <button type="button" onClick={handleOptimize} disabled={loading} className="optimize-btn">
            {loading ? 'Optimizing...' : 'Run Optimization'}
          </button>
        </div>

        {portfolioData ? (
          <div className="dashboard-results">
            <div className={`status-banner ${portfolioData.status === 'ADJUST' ? 'status-warning' : 'status-success'}`}>
              STATUS: {message}
            </div>

            <div className="results-grid">
              <div className="metrics-card">
                <h3>Portfolio Metrics</h3>
                <p>
                  Expected Return:{' '}
                  <strong>{portfolioData.metrics.expected_return}%</strong>
                </p>
                <p>
                  Estimated Risk (Vol.):{' '}
                  <strong>{portfolioData.metrics.estimated_risk}%</strong>
                </p>
                <p>
                  Sharpe Ratio: <strong>{portfolioData.metrics.sharpe_ratio}</strong>
                </p>
                <p>
                  Total Value: <strong>₹{Number(amount).toLocaleString()}</strong>
                </p>
              </div>

              <div className="chart-card">
                <h3>Optimal Asset Allocation</h3>
                <div style={{ width: '100%', height: 360 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={portfolioData.portfolio}
                        dataKey="value"
                        nameKey="name"
                        cx="50%"
                        cy="50%"
                        outerRadius={120}
                        fill="#8884d8"
                        labelLine={false}
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
            </div>

            <div className="table-card">
              <h3>Recommended Holdings</h3>
              <div className="table-scroll">
                <table className="holdings-table">
                  <thead>
                    <tr>
                      <th>Company (Ticker)</th>
                      <th>Sector</th>
                      <th>Optimal Weight</th>
                      <th>Investment Value (₹)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {portfolioData.portfolio.map((stock, idx) => (
                      <tr key={idx}>
                        <td>
                          {stock.name} ({stock.ticker})
                        </td>
                        <td>{stock.sector}</td>
                        <td>{(stock.weight * 100).toFixed(2)}%</td>
                        <td>₹{stock.value.toLocaleString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <button
                type="button"
                className="optimize-btn"
                onClick={handleSave}
                disabled={saving}
                style={{ marginTop: '1rem' }}
              >
                {saving ? 'Saving...' : 'Save Portfolio'}
              </button>
            </div>
          </div>
        ) : (
          <div className="placeholder-card">
            Click “Run Optimization” to generate your first AI-driven portfolio.
          </div>
        )}
      </div>
    </div>
  );
};

export default DashboardPage;