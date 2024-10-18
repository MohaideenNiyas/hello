import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../CSS/Login.css'; // Ensure you import the CSS file

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLoginSubmit = (e) => {
    e.preventDefault();
    // Handle login logic here, such as verifying username and password
    navigate('/dashboard'); // Redirect to dashboard upon successful login
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
