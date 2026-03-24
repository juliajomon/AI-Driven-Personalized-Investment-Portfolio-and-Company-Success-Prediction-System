// frontend/src/api/apiService.js

import axios from 'axios';

// Base URL for your Flask API (running locally on port 5000)
const BASE_URL = 'http://127.0.0.1:5000/api';

/**
 * Calls the Flask /optimize endpoint to calculate the personalized portfolio.
 * @param {number} amount - Total investment amount.
 * @param {number} targetReturn - Desired annual return percentage (e.g., 20).
 */
export const optimizePortfolio = async (amount, targetReturn, userId) => {
  const response = await axios.post(`${BASE_URL}/optimize`, {
    amount: amount,
    target_return: targetReturn,
    user_id: userId,
  });
  return response.data; // Returns the {status, message, portfolio, metrics} object
};

export const saveOptimizedPortfolio = async (data) => {
  const response = await axios.post(`${BASE_URL}/save-portfolio`, {
    userId: data.userId,
    amount: data.amount,
    riskRate: data.riskRate,
    expectedReturn: data.expectedReturn,
    portfolio: data.portfolio
  });

  return response.data;
};

/**
 * Calls the Flask /stocks endpoint to get the list of all AI predictions.
 */
export const getStockPredictions = async () => {
    const response = await axios.get(`${BASE_URL}/stocks`);
    return response.data; // Returns the full list of stocks with prediction scores
};

export const getSearchHistory = async (userId) => {
  const response = await axios.get(`${BASE_URL}/search-history`, {
    params: { user_id: userId },
  });
  return response.data;
};

export const getSavedPortfolios = async () => {
  const userId = localStorage.getItem('userId');
  const response = await axios.get(`${BASE_URL}/saved-portfolios`, {
    params: { user_id: userId },
  });
  return response.data;
};

export const loginUser = async (email, password) => {
  const response = await axios.post(`${BASE_URL}/login`, { email, password });
  return response.data;
};

export const signupUser = async (email, password) => {
  const response = await axios.post(`${BASE_URL}/signup`, { email, password });
  return response.data;
};

// You can add other utility functions here, like login/signup or data refreshing.