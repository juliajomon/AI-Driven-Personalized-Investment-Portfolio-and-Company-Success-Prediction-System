import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/auth.css';

// Note: API_URL and axios are kept as comments for future implementation
// import axios from 'axios';
// const API_URL = 'http://127.0.0.1:5000/api/auth/login'; // Placeholder Flask Auth Endpoint

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setMessage('');
    try {
      // In a real app, this sends credentials and gets a JWT token back
      // const response = await axios.post(API_URL, { email, password });

      // MOCK SUCCESS for Project Demo
      localStorage.setItem('userToken', 'fake-jwt-token-for-demo');
      navigate('/dashboard'); // Redirect to dashboard on success
    } catch (err) {
      setMessage('Login failed. Please check credentials.');
    }
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-content">
          <h1 className="login-title">Welcome back</h1>
          <p className="login-subtitle">Sign in to continue building your portfolio</p>

          <form onSubmit={handleLogin} className="login-form">
            <div className="form-group">
              <label className="form-label" htmlFor="email">
                Email address
              </label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="form-input"
                placeholder="you@example.com"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label" htmlFor="password">
                Password
              </label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="form-input"
                placeholder="Enter your password"
                required
              />
            </div>

            <button type="submit" className="submit-btn">
              Sign In
            </button>

            {message && <div className="error-message">{message}</div>}
          </form>

          <div className="register-link">
            Don&apos;t have an account?{' '}
            <button type="button" onClick={() => navigate('/signup')} className="link">
              Create one
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;