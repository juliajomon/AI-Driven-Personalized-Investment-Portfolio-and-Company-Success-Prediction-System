
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignUpPage';
import DashboardPage from './pages/DashboardPage';
import ChatbotPage from './pages/ChatbotPage';
import HistoryPage from './pages/HistoryPage';
import SavedPortfolioPage from './pages/SavedPortfolioPage';

const AuthGuard = ({ children }) => {
  const isAuthenticated = localStorage.getItem('userToken');
  return isAuthenticated ? children : <Navigate to="/login" />;
};

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

        <Route path="/dashboard" element={<AuthGuard><DashboardPage /></AuthGuard>} />
        <Route path="/chatbot" element={<AuthGuard><ChatbotPage /></AuthGuard>} />
        <Route path="/history" element={<AuthGuard><HistoryPage /></AuthGuard>} />
        <Route path="/saved-portfolios" element={<AuthGuard><SavedPortfolioPage /></AuthGuard>} />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
};

export default App;