import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/dashboard.css';

const ChatbotPage = () => {

  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Hello! I'm your Decision Advisor AI. Ask me why a company was selected, compare options, or explore what-if scenarios."
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

  // ✅ Send message
  const handleSend = async (e) => {
    e.preventDefault();

    if (!input.trim() || loading) return;

    const userMessage = { role: 'user', content: input.trim() };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch("http://localhost:5000/decision-chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          query: userMessage.content
        })
      });

      const data = await res.json();

      const botResponse = {
        role: 'assistant',
        content: data.response || "No response from AI."
      };

      setMessages(prev => [...prev, botResponse]);

    } catch (error) {
      console.error("Chatbot error:", error);

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: "⚠️ Error connecting to AI server."
      }]);
    }

    setLoading(false);
  };

  const logout = () => {
    localStorage.removeItem('userToken');
    navigate('/login');
  };

  return (
    <div className="dashboard-page">

      <button onClick={logout} className="logout-button">
        Logout
      </button>

      <button
        className="profile-button"
        onClick={() => navigate('/dashboard')}
      >
        ←
      </button>

      <div className="dashboard-container">

        <div className="dashboard-title-section">
          <h1 className="dashboard-title">Decision Advisor Chatbot</h1>
          <p className="dashboard-subtitle">
            Ask why a company was selected, compare alternatives, or explore what-if scenarios
          </p>
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
              placeholder="Ask about this company or your portfolio..."
              className="chat-input"
              disabled={loading}
            />

            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="chat-send-btn"
            >
              Send
            </button>

          </form>

        </div>
      </div>
    </div>
  );
};

export default ChatbotPage;