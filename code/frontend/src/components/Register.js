import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../CSS/Register.css'; // Ensure the CSS file exists

const Register = () => {
  const [username, setUsername] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [preferredStock, setPreferredStock] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Reset error before new submission

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (newPassword.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }

    setLoading(true); // Set loading state

    try {
      const response = await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password: newPassword, preferredStock }),
      });

      setLoading(false); // Remove loading state after response

      if (response.ok) {
        alert('Registration successful');
        navigate('/login');
      } else {
        const data = await response.json();
        setError(data.error || 'Registration failed'); // Display error message in the UI
      }
    } catch (error) {
      setLoading(false);
      console.error('Error during registration:', error);
      setError('An error occurred during registration. Please try again later.');
    }
  };

  // Updated to handle checkbox changes
  const handlePreferredStockChange = (e) => {
    const value = e.target.value;
    setPreferredStock((prev) => 
      prev.includes(value) 
        ? prev.filter(stock => stock !== value) // Remove stock if already selected
        : [...prev, value] // Add stock if not selected
    );
  };

  return (
    <div className="register-container">
      <div className="register-form">
        <h2>Register</h2>
        <form onSubmit={handleRegisterSubmit}>
          {error && <p className="error-message">{error}</p>}
          <div className="form-group">
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              placeholder=" "
            />
            <label>Username</label>
          </div>
          <div className="form-group">
            <input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
              placeholder=" "
            />
            <label>New Password</label>
          </div>
          <div className="form-group">
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              placeholder=" "
            />
            <label>Confirm Password</label>
          </div>
          <div className="form-group">
            <label>Select Your Stocks:</label>
            <div className="checkbox-group">
              {/* Add checkboxes for stock selection */}
              {['AAPL', 'MSFT', 'AMZN', 'TSLA', 'GOOGL', 'GOOG', 'META', 'NVDA', 'BRK-A', 'BRK-B', 'JPM', 'JNJ', 'V', 'WMT', 'PG', 'UNH', 'HD', 'DIS', 'NFLX', 'XOM'].map((stock) => (
                <label key={stock}>
                  <input
                    type="checkbox"
                    value={stock}
                    checked={preferredStock.includes(stock)}
                    onChange={handlePreferredStockChange}
                  />
                  {stock}
                </label>
              ))}
            </div>
            {preferredStock.length > 0 && (
              <div className="selected-stocks">
                <h4>Selected Stocks:</h4>
                <ul>
                  {preferredStock.map((stock) => (
                    <li key={stock}>{stock}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
          <button type="submit" disabled={loading}>
            {loading ? 'Registering...' : 'Register'}
          </button>
        </form>
        <p>
          Already have an account? <Link to="/login">Login Here</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
