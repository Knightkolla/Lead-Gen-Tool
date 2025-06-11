import React, { useState, StrictMode, useEffect } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import LoginPage from './LoginPage.tsx'
import SignUpPage from './SignUpPage.tsx'

function Main() {
  const [loggedIn, setLoggedIn] = useState<boolean>(
    localStorage.getItem('loggedIn') === 'true' // Initialize from localStorage
  )
  const [showSignUp, setShowSignUp] = useState<boolean>(false)

  useEffect(() => {
    localStorage.setItem('loggedIn', String(loggedIn)) // Persist loggedIn state
  }, [loggedIn])

  const handleLoginSuccess = () => {
    setLoggedIn(true);
  };

  const handleSignUpSuccess = () => {
    setLoggedIn(true);
  };

  const handleNavigateToLogin = () => {
    setShowSignUp(false);
  };

  const handleNavigateToSignUp = () => {
    setShowSignUp(true);
  };

  return (
    <StrictMode>
      {loggedIn ? (
        <App />
      ) : showSignUp ? (
        <SignUpPage onSignUpSuccess={handleSignUpSuccess} onNavigateToLogin={handleNavigateToLogin} />
      ) : (
        <LoginPage onLoginSuccess={handleLoginSuccess} onNavigateToSignUp={handleNavigateToSignUp} />
      )}
    </StrictMode>
  );
}

const root = createRoot(document.getElementById('root')!);
root.render(<Main />);
