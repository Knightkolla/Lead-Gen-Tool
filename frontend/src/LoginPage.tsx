import React, { useState } from 'react'
import { Box, Button, TextField, Typography, Paper, styled } from '@mui/material'
import { API_BASE_URL } from './config'

// Reusing GlassmorphismPaper from App.tsx for consistent styling
const GlassmorphismPaper = styled(Paper)(({ theme }) => ({
  background: theme.palette.mode === 'dark' ? 'rgba(25, 25, 25, 0.7)' : 'rgba(255, 255, 255, 0.7)',
  backdropFilter: 'blur(10px)',
  border: '1px solid rgba(255, 255, 255, 0.1)',
  borderRadius: theme.shape.borderRadius === 4 ? '16px' : theme.shape.borderRadius, // Rounded 2xl borders
  boxShadow: theme.palette.mode === 'dark' ? '0px 8px 30px rgba(0, 0, 0, 0.6)' : '0px 8px 30px rgba(0, 0, 0, 0.1)',
  padding: theme.spacing(3),
  transition: 'box-shadow 0.3s ease-in-out',
  '&:hover': {
    boxShadow: theme.palette.mode === 'dark' ? '0px 12px 40px rgba(0, 0, 0, 0.8)' : '0px 12px 40px rgba(0, 0, 0, 0.2)',
  },
}))

interface LoginPageProps {
  onLoginSuccess: () => void;
  onNavigateToSignUp: () => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ onLoginSuccess, onNavigateToSignUp }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    setError(''); // Clear previous errors
    try {
      const response = await fetch(`${API_BASE_URL}/api/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      })

      if (response.ok) {
        onLoginSuccess();
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Login failed');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError('An error occurred during login.');
    }
  };

  return (
    <Box
      sx={{
        height: '100vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        bgcolor: 'background.default',
        background: 'linear-gradient(135deg, #1a1a2e 0%, #151525 100%)', // Dark themed background for login
      }}
    >
      <GlassmorphismPaper sx={{ maxWidth: 400, width: '100%' }}>
        <Typography variant="h5" gutterBottom align="center" color="text.primary">
          Login to Dashboard
        </Typography>
        {error && (
          <Typography color="error" align="center" sx={{ mb: 2 }}>
            {error}
          </Typography>
        )}
        <TextField
          label="Username"
          variant="outlined"
          fullWidth
          margin="normal"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          sx={{ input: { color: 'text.primary' }, label: { color: 'text.secondary' } }}
          InputProps={{
            style: { borderRadius: '12px', background: 'rgba(255, 255, 255, 0.1)' },
          }}
        />
        <TextField
          label="Password"
          variant="outlined"
          type="password"
          fullWidth
          margin="normal"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          sx={{ input: { color: 'text.primary' }, label: { color: 'text.secondary' } }}
          InputProps={{
            style: { borderRadius: '12px', background: 'rgba(255, 255, 255, 0.1)' },
          }}
        />
        <Button
          variant="contained"
          color="primary"
          fullWidth
          sx={{ mt: 3, py: 1.5, borderRadius: '12px' }}
          onClick={handleLogin}
        >
          Login
        </Button>
        <Button
          variant="text"
          fullWidth
          sx={{ mt: 2, color: 'text.secondary' }}
          onClick={onNavigateToSignUp}
        >
          Don't have an account? Sign Up
        </Button>
      </GlassmorphismPaper>
    </Box>
  );
};

export default LoginPage; 