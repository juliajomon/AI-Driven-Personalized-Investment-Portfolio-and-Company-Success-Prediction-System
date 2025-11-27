import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

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
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <form onSubmit={handleSignup} className="bg-white p-8 rounded-lg shadow-xl w-full max-w-sm">
        <h2 className="text-2xl font-bold mb-6 text-center text-green-600">Create Investoo Account</h2>
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)}
            className="mt-1 p-3 w-full border border-gray-300 rounded-md" required
          />
        </div>
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700">Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}
            className="mt-1 p-3 w-full border border-gray-300 rounded-md" required
          />
        </div>
        <button type="submit"
          className="w-full bg-green-600 text-white p-3 rounded-md font-semibold hover:bg-green-700 transition duration-150"
        >
          Sign Up
        </button>
        {message && <p className="mt-4 text-center text-green-500">{message}</p>}
        <p className="mt-4 text-center text-sm">
          Already have an account? <span onClick={() => navigate('/login')} className="text-blue-600 cursor-pointer hover:underline">Sign In</span>
        </p>
      </form>
    </div>
  );
};

export default SignupPage;