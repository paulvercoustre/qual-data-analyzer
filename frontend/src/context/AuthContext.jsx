import React, { createContext, useState, useContext, useEffect } from 'react';

// 1. Create the context
const AuthContext = createContext(null);

// 2. Create the AuthProvider component
export const AuthProvider = ({ children }) => {
  const [authToken, setAuthToken] = useState(() => localStorage.getItem('authToken')); // Initialize from localStorage

  // Function to handle login: stores token in state and localStorage
  const login = (token) => {
    localStorage.setItem('authToken', token);
    setAuthToken(token);
    console.log("Context: Token set");
  };

  // Function to handle logout: removes token from state and localStorage
  const logout = () => {
    localStorage.removeItem('authToken');
    setAuthToken(null);
    console.log("Context: Token removed");
    // Optionally navigate user to login page
    // (Navigation is typically handled in the component calling logout)
  };

  // Determine if user is authenticated based on token existence
  const isAuthenticated = !!authToken;

  // Value provided to consuming components
  const value = {
    authToken,
    isAuthenticated,
    login,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// 3. Create a custom hook to use the AuthContext
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}; 