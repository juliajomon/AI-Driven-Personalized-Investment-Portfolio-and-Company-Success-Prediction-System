import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { getSearchHistory } from '../api/apiService';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#AF19FF', '#FF4560', '#775DD0'];

const HistoryPage = () => {
  const navigate = useNavigate();
  const [historicalData, setHistoricalData] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const userId = localStorage.getItem('userId') || 1;
        const data = await getSearchHistory(userId);
        setHistoricalData(
          data.map((item) => ({
            id: item.id,
            target: item.expected_return,
            achieved: item.expected_return,
            volatility: item.risk_rate,
            status: 'SUCCESS',
            portfolio: item.portfolio || [],
          }))
        );
      } catch {
        setHistoricalData([]);
      }
    };
    fetchHistory();
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'SUCCESS':
        return 'text-green-700';
      case 'HIGH_RISK':
        return 'text-yellow-700';
      default:
        return 'text-gray-700';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'SUCCESS':
        return 'SUCCESS';
      case 'HIGH_RISK':
        return 'HIGH RISK WARNING (ADJUST)';
      default:
        return 'PENDING';
    }
  };

  return (
    <div className="p-4 md:p-8 min-h-screen bg-gray-100">
      <header className="mb-8">
        <button 
          onClick={() => navigate('/dashboard')} 
          className="text-blue-600 hover:text-blue-800 flex items-center mb-4" 
        >
          ← Back to Dashboard
        </button>
        <h1 className="text-2xl md:text-3xl font-extrabold text-gray-900">Historical Optimizations</h1>
        <p className="text-gray-600 mt-2">Review your past investment strategies and market conditions.</p>
      </header>

      <div className="space-y-6">
        {historicalData.map((item) => (
          <div key={item.id} className="bg-white p-4 md:p-6 rounded-lg shadow-lg">
            <div className="flex flex-col md:flex-row md:justify-between md:items-center mb-4">
              <div>
                <h3 className="text-lg font-bold">Optimization Run: {item.id} {item.id === 1 && '(Latest)'}</h3>
                <p className="text-sm text-gray-600">
                  Target: {item.target}% | Achieved: {item.achieved}% | Volatility: {item.volatility}%
                </p>
                <p className={`text-sm font-medium ${getStatusColor(item.status)}`}>
                  Status: {getStatusText(item.status)}
                </p>
              </div>
            </div>
            
            <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h4 className="font-semibold mb-2">Portfolio Allocation</h4>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={item.portfolio}
                        dataKey="value"
                        nameKey="name"
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        fill="#8884d8"
                        label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                        labelLine={false}
                      >
                        {item.portfolio.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip 
                        formatter={(value, name, props) => [
                          `₹${value.toLocaleString()}`,
                          props.payload.name
                        ]}
                      />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>
              
              <div>
                <div className="overflow-x-auto" align="center">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Company</th>
                        <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase">Allocation</th>
                        <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase">Value (₹)</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {item.portfolio.map((stock, idx) => (
                        <tr key={idx}>
                          <td className="px-4 py-2 whitespace-nowrap text-sm">{stock.name}</td>
                          <td className="px-4 py-2 whitespace-nowrap text-right text-sm">
                            {((stock.value / item.portfolio.reduce((sum, s) => sum + s.value, 0)) * 100).toFixed(1)}%
                          </td>
                          <td className="px-4 py-2 whitespace-nowrap text-right text-sm font-medium">
                            ₹{stock.value.toLocaleString()}
                          </td>
                        </tr>
                      ))}
                      <tr className="font-semibold">
                        <td className="px-4 py-2 whitespace-nowrap">Total</td>
                        <td className="px-4 py-2 whitespace-nowrap text-right">100%</td>
                        <td className="px-4 py-2 whitespace-nowrap text-right">
                          ₹{item.portfolio.reduce((sum, s) => sum + s.value, 0).toLocaleString()}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        ))}
        
        
      </div>
    </div>
  );
};

export default HistoryPage;