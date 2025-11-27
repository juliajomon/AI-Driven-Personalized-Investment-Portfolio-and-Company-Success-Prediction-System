// frontend/src/api/apiService.js

import axios from 'axios';

// Base URL for your Flask API (running locally on port 5000)
const BASE_URL = 'http://127.0.0.1:5000/api';

/**
 * Calls the Flask /optimize endpoint to calculate the personalized portfolio.
 * @param {number} amount - Total investment amount.
 * @param {number} targetReturn - Desired annual return percentage (e.g., 20).
 */
export const optimizePortfolio = async (amount, targetReturn) => {
    const response = await axios.post(`${BASE_URL}/optimize`, {
        amount: amount,
        target_return: targetReturn
    });
    return response.data; // Returns the {status, message, portfolio, metrics} object
};

/**
 * Calls the Flask /stocks endpoint to get the list of all AI predictions.
 */
export const getStockPredictions = async () => {
    const response = await axios.get(`${BASE_URL}/stocks`);
    return response.data; // Returns the full list of stocks with prediction scores
};

// You can add other utility functions here, like login/signup or data refreshing.