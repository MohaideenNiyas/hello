import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../CSS/Register.css'; // Make sure to link the CSS file

const Register = () => {
  const [username, setUsername] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [preferredStock, setPreferredStock] = useState('');
  const navigate = useNavigate();

  const handleRegisterSubmit = (e) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    // Handle registration logic, such as sending data to the backend
    // Example: POST request to backend with user details

    navigate('/login'); // Redirect back to login page after registration
  };

  return (
    <div className="register-container">
      <div className="register-form">
        <h2>Register</h2>
        <form onSubmit={handleRegisterSubmit}>
          <div className="form-group">
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              placeholder=" " // For the floating label effect
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
            <input
              type="text"
              value={preferredStock}
              onChange={(e) => setPreferredStock(e.target.value)}
              required
              placeholder=" "
            />
            <label>Preferred Stock</label>
          </div>
          <button type="submit">Register</button>
        </form>
        <p>
          Already have an account? <Link to="/login">Login Here</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
