import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/auth.css';

const SignupPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSignup = (e) => {
    e.preventDefault();
    setMessage('Registration successful! Redirecting to login...');

    // In a real app, you would send data to Flask /api/auth/signup

    setTimeout(() => {
      navigate('/login');
    }, 1500);
  };

  return (
    <div className="register-page">
      <div className="register-container">
        <div className="register-content">
          <h1 className="register-title">Create your account</h1>
          <p className="register-subtitle">Start personalizing your AI-driven portfolio</p>

          <form onSubmit={handleSignup} className="register-form">
            <div className="form-group">
              <label className="form-label" htmlFor="signup-email">
                Email address
              </label>
              <input
                id="signup-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="form-input"
                placeholder="you@example.com"
                required
              />
            </div>
            <div className="form-group">
              <label className="form-label" htmlFor="signup-password">
                Password
              </label>
              <input
                id="signup-password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="form-input"
                placeholder="Create a strong password"
                required
              />
            </div>

            <button type="submit" className="submit-btn">
              Sign Up
            </button>

            {message && <div className="message success-message">{message}</div>}
          </form>

          <div className="login-link">
            Already have an account?{' '}
            <button type="button" onClick={() => navigate('/login')} className="link">
              Sign in
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SignupPage;