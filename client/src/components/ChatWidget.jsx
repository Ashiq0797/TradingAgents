import React, { useState } from 'react';
import './ChatWidget.css'; // Optional styling

const ChatWidget = () => {
  const [chatHistory, setChatHistory] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { role: 'user', text: input };
    setChatHistory(prev => [...prev, userMsg]);
    setLoading(true);
    setInput('');

    try {
      const res = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      });
      const data = await res.json();
      const botMsg = { role: 'bot', text: data.response || data.error || 'No response' };
      setChatHistory(prev => [...prev, botMsg]);
    } catch (error) {
      setChatHistory(prev => [...prev, { role: 'bot', text: 'Error: ' + error.message }]);
    }
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') sendMessage();
  };

  return (
    <div className="chat-widget">
      <div className="chat-box">
        {chatHistory.map((msg, i) => (
          <div key={i} className={`msg ${msg.role}`}>{msg.text}</div>
        ))}
        {loading && <div className="msg bot">Typing...</div>}
      </div>
      <input
        type="text"
        placeholder="Ask something..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyPress}
      />
      <button onClick={sendMessage} disabled={loading}>Send</button>
    </div>
  );
};

export default ChatWidget;
