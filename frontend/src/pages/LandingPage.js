import React from 'react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-6">
      <div className="text-center max-w-2xl">
        <h1 className="text-6xl font-extrabold text-blue-800 mb-4">
          Investoo AI Portfolio Engine
        </h1>
        <p className="text-2xl text-gray-600 mb-8">
          Optimize your wealth with predictive intelligence.
        </p>
        <p className="text-lg text-gray-700 mb-10">
          We use Ensemble Machine Learning and Markowitz Optimization to find the highest-return, lowest-risk portfolio tailored to your financial goals.
        </p>
        <div className="space-x-4">
          <Link
            to="/login"
            className="bg-green-600 text-white px-8 py-3 rounded-lg text-xl font-semibold hover:bg-green-700 transition duration-150 shadow-lg"
          >
            Start Investing
          </Link>
          <Link
            to="/signup"
            className="bg-transparent border-2 border-blue-600 text-blue-800 px-8 py-3 rounded-lg text-xl font-semibold hover:bg-blue-100 transition duration-150"
          >
            Create Account
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;