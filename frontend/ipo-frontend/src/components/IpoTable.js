import React, { useState, useEffect } from 'react';
import axios from 'axios';

function IpoTable() {
  const [upcoming, setUpcoming] = useState([]);
  const [recent, setRecent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showAllRecent, setShowAllRecent] = useState(false);
  const [email, setEmail] = useState('');
  const [subscribeMessage, setSubscribeMessage] = useState('');

  useEffect(() => {
    axios.get("/api/ipos/")
      .then((res) => {
        setUpcoming(res.data.upcoming_ipos || []);
        setRecent(res.data.recent_ipos || []);
        setLoading(false);
      })
      .catch(() => {
        setError("Error fetching data from backend");
        setLoading(false);
      });
  }, []);

  const handleSubscribe = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('/api/subscribe/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();
      if (response.ok) {
        setSubscribeMessage(data.message || "Subscribed successfully!");
        setEmail('');
      } else {
        setSubscribeMessage(data.error || "Subscription failed.");
      }
    } catch (error) {
      setSubscribeMessage("Something went wrong.");
    }
  };

  const formatNumber = (num) => num?.toLocaleString();
  const isToday = (dateStr) => dateStr === new Date().toISOString().split("T")[0];

  const columnWidths = {
    name: '25%',
    symbol: '10%',
    date: '15%',
    shares: '15%',
    exchange: '15%',
    price: '10%',
    status: '10%',
  };

  const renderTable = (data) => (
    <div style={tableWrapperStyle}>
      <table style={tableStyle}>
        <thead>
          <tr style={theadStyle}>
            <th style={{ ...thStyle, width: columnWidths.name }}>Company</th>
            <th style={{ ...thStyle, width: columnWidths.symbol }}>Symbol</th>
            <th style={{ ...thStyle, width: columnWidths.date }}>IPO Date</th>
            <th style={{ ...thStyle, width: columnWidths.shares }}>Shares</th>
            <th style={{ ...thStyle, width: columnWidths.exchange }}>Exchange</th>
            <th style={{ ...thStyle, width: columnWidths.price }}>Price</th>
            <th style={{ ...thStyle, width: columnWidths.status }}>Status</th>
          </tr>
        </thead>
        <tbody>
          {data.map((ipo, index) => {
            const rowStyle = isToday(ipo.date) ? todayRowStyle : index % 2 === 0 ? rowEvenStyle : rowOddStyle;

            return (
              <tr key={index} style={rowStyle}>
                <td style={tdStyle}>{ipo.name}</td>
                <td style={tdStyle}>
                  <a
                    href={`https://finance.yahoo.com/quote/${ipo.symbol}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={symbolLinkStyle}
                  >
                    {ipo.symbol}
                  </a>
                </td>
                <td style={tdStyle}>{ipo.date}</td>
                <td style={tdStyle}>{formatNumber(ipo.numberOfShares)}</td>
                <td style={tdStyle}>{ipo.exchange}</td>
                <td style={tdStyle}>{ipo.price}</td>
                <td style={tdStyle}>{ipo.status}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );

  return (
    <div style={{ padding: '40px', backgroundColor: '#f5faff', minHeight: '100vh' }}>
      <h1 style={{ textAlign: 'left', marginBottom: '20px', color: '#0b3d91' }}>NYSE IPO Tracker</h1>

      {/* Email Subscription Form */}
      <div style={formContainerStyle}>
        <h3 style={{ margin: 0, color: '#0b3d91' }}>Get Notified When New IPOs Are Added</h3>
        <form onSubmit={handleSubscribe} style={formStyle}>
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            style={inputStyle}
          />
          <button type="submit" style={subscribeButtonStyle}>Subscribe</button>
        </form>
        {subscribeMessage && (
          <p style={{ color: 'green', marginTop: '10px' }}>{subscribeMessage}</p>
        )}
      </div>

      {loading && <p style={{ textAlign: 'center' }}>Loading...</p>}
      {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}

      {!loading && (
        <>
          <h2 style={{ textAlign: 'left', marginBottom: '10px', color: '#0b3d91' }}>Upcoming IPOs</h2>
          {upcoming.length > 0 ? renderTable(upcoming) : <p style={{ textAlign: 'center' }}>No upcoming IPOs.</p>}

          <h2 style={{ textAlign: 'left', marginTop: '40px', marginBottom: '10px', color: '#0b3d91' }}>Recently Listed IPOs</h2>
          {recent.length > 0 ? (
            <>
              {renderTable(showAllRecent ? recent : recent.slice(0, 10))}
              {recent.length > 10 && (
                <div style={{ textAlign: 'center' }}>
                  <button
                    onClick={() => setShowAllRecent(!showAllRecent)}
                    style={buttonStyle}
                  >
                    {showAllRecent ? "View Less" : "View More"}
                  </button>
                </div>
              )}
            </>
          ) : <p style={{ textAlign: 'center' }}>No recent IPOs.</p>}
        </>
      )}
    </div>
  );
}

// === STYLES ===
const formContainerStyle = {
  backgroundColor: '#ffffff',
  borderRadius: '10px',
  padding: '20px',
  marginBottom: '40px',
  boxShadow: '0 4px 10px rgba(0, 0, 0, 0.05)',
  textAlign: 'left'
};

const formStyle = {
  display: 'flex',
  gap: '10px',
  flexWrap: 'wrap',
  marginTop: '10px',
};

const inputStyle = {
  padding: '10px',
  fontSize: '14px',
  flex: 1,
  minWidth: '250px',
  borderRadius: '5px',
  border: '1px solid #ccc',
};

const subscribeButtonStyle = {
  padding: '10px 20px',
  backgroundColor: '#0b3d91',
  color: 'white',
  border: 'none',
  borderRadius: '5px',
  cursor: 'pointer',
};

const buttonStyle = {
  padding: '10px 20px',
  backgroundColor: '#0b3d91',
  color: 'white',
  border: 'none',
  borderRadius: '5px',
  cursor: 'pointer',
  marginTop: '15px'
};

const symbolLinkStyle = {
  color: '#0b3d91',
  textDecoration: 'underline',
  fontWeight: 600,
};

const tableWrapperStyle = {
  margin: '0 auto',
  padding: '12px',
  width: '95%',
  border: '1px solid #d0e6f9',
  borderRadius: '10px',
  backgroundColor: '#ffffff',
  boxShadow: '0 4px 10px rgba(0,0,0,0.03)',
  overflow: 'hidden',
};

const tableStyle = {
  width: '100%',
  borderCollapse: 'collapse',
  fontFamily: 'Segoe UI, sans-serif',
  fontSize: '14px',
};

const theadStyle = {
  backgroundColor: '#f0f8ff',
};

const thStyle = {
  padding: '14px 10px',
  textAlign: 'left',
  fontWeight: '700',
  color: '#0b3d91',
  fontSize: '13px',
  textTransform: 'uppercase',
  borderBottom: '2px solid #cde3f9',
};

const tdStyle = {
  padding: '12px 10px',
  textAlign: 'left',
  verticalAlign: 'middle',
  whiteSpace: 'nowrap',
  borderBottom: '1px solid #eee',
};

const rowEvenStyle = {
  backgroundColor: '#ffffff',
  transition: 'background 0.2s',
};

const rowOddStyle = {
  backgroundColor: '#f8fbff',
  transition: 'background 0.2s',
};

const todayRowStyle = {
  backgroundColor: '#d1ecff',
  transition: 'background 0.2s',
};

export default IpoTable;
