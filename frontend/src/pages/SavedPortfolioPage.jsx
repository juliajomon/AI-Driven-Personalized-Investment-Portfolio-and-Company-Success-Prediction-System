import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getSavedPortfolios } from '../api/apiService';

const SavedPortfolioPage = () => {
  const navigate = useNavigate();
  const [items, setItems] = useState([]);

  useEffect(() => {
    const fetchSaved = async () => {
      try {
        const data = await getSavedPortfolios();
        setItems(data || []);
      } catch (e) {
        // keep empty on error
      }
    };
    fetchSaved();
  }, []);

  return (
    <div className="p-4 md:p-8 min-h-screen bg-gray-100">
      <header className="mb-8">
        <button
          onClick={() => navigate('/dashboard')}
          className="text-blue-600 hover:text-blue-800 flex items-center mb-4"
        >
          ← Back to Dashboard
        </button>
        <h1 className="text-2xl md:text-3xl font-extrabold text-gray-900">
          Saved Portfolio
        </h1>
      
      </header>

      <div className="space-y-6">
        {items.length === 0 ? (
          <div className="bg-white p-4 md:p-6 rounded-lg shadow-lg">
            <p className="text-gray-500 text-sm">
              You do not have any saved portfolios yet. Run an optimization and click &quot;Save
              Portfolio&quot; to store one.
            </p>
          </div>
        ) : (
          items.map((p) => (
            <div key={p.id} className="bg-white p-4 md:p-6 rounded-lg shadow-lg">
              <div className="mb-4">
                
                <p className="text-sm text-gray-600">
                  Expected Return: {p.expected_return?.toFixed(2)}% | Risk: {p.risk_rate?.toFixed(2)}% | Amount:{' '}
                  ₹{p.amount?.toLocaleString()}
                </p>
              </div>

              <div className="overflow-x-auto" align="center">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                        Company
                      </th>
                      <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">
                        Sector
                      </th>
                      <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase">
                        Weight (%)
                      </th>
                      <th className="px-4 py-2 text-right text-xs font-medium text-gray-500 uppercase">
                        Value (₹)
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {(p.portfolio || []).map((stock, idx) => (
                      <tr key={idx}>
                        <td className="px-4 py-2 whitespace-nowrap text-sm">
                          {stock.name}
                        </td>
                        <td className="px-4 py-2 whitespace-nowrap text-sm">
                          {stock.sector}
                        </td>
                        <td className="px-4 py-2 whitespace-nowrap text-right text-sm">
                          {(stock.weight * 100).toFixed(2)}
                        </td>
                        <td className="px-4 py-2 whitespace-nowrap text-right text-sm font-medium">
                          ₹{stock.value.toLocaleString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default SavedPortfolioPage;

