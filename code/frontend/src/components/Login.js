import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../CSS/Login.css'; // Ensure you import the CSS file

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('http://localhost:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      // Redirect to dashboard upon successful login
      navigate('/dashboard');
    } else {
      // Handle specific error messages based on the status code
      const errorData = await response.json();
      if (response.status === 404) {
        alert('No user exists. Please register.');
      } else if (response.status === 401) {
        alert('Incorrect password. Please try again.');
      } else {
        alert(`An error occurred: ${errorData.error || 'Unknown error'}`);
      }
    }
  };

  return (
    <div className="login-container">
      <div className="login-form">
        <h2>Login</h2>
        <form onSubmit={handleLoginSubmit}>
          <div className="form-group">
            <input 
              type="text" 
              value={username} 
              onChange={(e) => setUsername(e.target.value)} 
              required 
              placeholder=" " // To trigger :not(:placeholder-shown)
            />
            <label>Username</label>
          </div>
          <div className="form-group">
            <input 
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              required 
              placeholder=" " // To trigger :not(:placeholder-shown)
            />
            <label>Password</label>
          </div>
          <button type="submit">Login</button>
        </form>
        <p>
          Don't have an account? 
          <Link to="/register"> Register Here</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;
