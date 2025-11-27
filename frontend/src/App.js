// frontend/src/App.js

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';

// Import all page components
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignUpPage';
import DashboardPage from './pages/DashboardPage'; // The core optimization view
import ChatbotPage from './pages/ChatbotPage';
import HistoryPage from './pages/HistoryPage';

// Simple authentication guard component
const AuthGuard = ({ children }) => {
  // Check if the user has a token. If not, redirect to login.
  const isAuthenticated = localStorage.getItem('userToken');
  return isAuthenticated ? children : <Navigate to="/login" />;
};

const App = () => {
  return (
    <Router>
      <Routes>
        {/* PUBLIC ROUTES */}
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

        {/* PROTECTED ROUTES (Requires Login) */}
        <Route path="/dashboard" element={<AuthGuard><DashboardPage /></AuthGuard>} />
        <Route path="/chatbot" element={<AuthGuard><ChatbotPage /></AuthGuard>} />
        <Route path="/history" element={<AuthGuard><HistoryPage /></AuthGuard>} />
        {/* FALLBACK */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
};

export default App;