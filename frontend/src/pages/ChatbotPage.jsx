import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/dashboard.css';

const ChatbotPage = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I\'m your investment advisor chatbot. I can help you understand portfolio optimization, explain investment terms, analyze your portfolio, and answer questions about the market. How can I assist you today?'
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = { role: 'user', content: input.trim() };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    // Simulate API call (replace with actual backend endpoint later)
    setTimeout(() => {
      const botResponse = {
        role: 'assistant',
        content: generateResponse(userMessage.content)
      };
      setMessages(prev => [...prev, botResponse]);
      setLoading(false);
    }, 1000);
  };

  const generateResponse = (userInput) => {
    const lowerInput = userInput.toLowerCase();
    
    if (lowerInput.includes('portfolio') || lowerInput.includes('optimization')) {
      return 'Portfolio optimization uses Modern Portfolio Theory to balance risk and return. Our system analyzes top-performing stocks, calculates their expected returns and volatility, and uses mathematical optimization to find the best allocation that meets your target return while minimizing risk.';
    }
    
    if (lowerInput.includes('sharpe') || lowerInput.includes('ratio')) {
      return 'The Sharpe Ratio measures risk-adjusted return. It\'s calculated as (Expected Return - Risk-Free Rate) / Volatility. A higher Sharpe ratio (typically >1.0) indicates better risk-adjusted performance. Our system aims for Sharpe ratios above 1.2 for optimal portfolios.';
    }
    
    if (lowerInput.includes('risk') || lowerInput.includes('volatility')) {
      return 'Risk (volatility) measures how much your portfolio value might fluctuate. Lower volatility means more stable returns. Our optimizer balances your target return with acceptable risk levels. If you see a warning about high risk, consider lowering your target return.';
    }
    
    if (lowerInput.includes('stock') || lowerInput.includes('company')) {
      return 'Our AI analyzes companies using multiple factors: ROE (Return on Equity), debt ratios, profit margins, cash flow, and financial stability metrics. Only stocks with AI Success Probability >80% are considered for your portfolio.';
    }
    
    if (lowerInput.includes('hello') || lowerInput.includes('hi')) {
      return 'Hello! I\'m here to help with your investment questions. Ask me about portfolio optimization, risk management, or any investment concepts!';
    }
    
    if (lowerInput.includes('help')) {
      return 'I can help you with:\n• Understanding portfolio optimization\n• Explaining investment metrics (Sharpe ratio, volatility, etc.)\n• Analyzing your portfolio recommendations\n• Answering questions about stocks and markets\n\nWhat would you like to know?';
    }
    
    return 'I understand you\'re asking about: "' + userInput + '". This is a demo chatbot. In a production system, this would connect to an AI model or knowledge base to provide detailed investment advice. For now, try asking about portfolio optimization, Sharpe ratio, or risk management!';
  };

  const logout = () => {
    localStorage.removeItem('userToken');
    navigate('/login');
  };

  return (
    <div className="dashboard-page">
      <button type="button" onClick={logout} className="logout-button">
        Logout
      </button>
      <button type="button" className="profile-button" onClick={() => navigate('/dashboard')}>
        ←
      </button>

      <div className="dashboard-container">
        <div className="dashboard-title-section">
          <h1 className="dashboard-title">Investment Advisor Chatbot</h1>
          <p className="dashboard-subtitle">Ask me anything about portfolio optimization and investments</p>
        </div>

        <div className="chatbot-container">
          <div className="chat-messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                <div className="message-content">
                  {msg.content}
                </div>
              </div>
            ))}
            {loading && (
              <div className="message assistant">
                <div className="message-content">
                  <span className="typing-indicator">●</span>
                  <span className="typing-indicator">●</span>
                  <span className="typing-indicator">●</span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form onSubmit={handleSend} className="chat-input-form">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question about investments..."
              className="chat-input"
              disabled={loading}
            />
            <button type="submit" disabled={loading || !input.trim()} className="chat-send-btn">
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChatbotPage;

