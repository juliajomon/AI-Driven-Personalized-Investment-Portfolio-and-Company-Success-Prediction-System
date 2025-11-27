import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/auth.css';

const LandingPage = () => {
  return (
    <div className="homepage">
      <div className="container">
        <div className="content">
          <h1 className="title">Investoo AI Portfolio Engine</h1>
          <p className="subtitle">Optimize your wealth with predictive intelligence.</p>
          <p className="subtitle">
            We combine ensemble machine learning and Markowitz optimization to tailor a high-return,
            low-risk plan for your goals.
          </p>

          <div className="buttons">
            <Link to="/login" className="btn btn-primary">
              Start Investing
            </Link>
            <Link to="/signup" className="btn btn-secondary">
              Create Account
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LandingPage;