// frontend/src/hooks/useAuth.js

import { useState, useEffect } from "react";

export default function useAuth() {
  const [token, setToken] = useState(null);

  useEffect(() => {
    const storedToken = localStorage.getItem("access_token");
    if (storedToken) setToken(storedToken);
  }, []);

  const login = (newToken) => {
    localStorage.setItem("access_token", newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setToken(null);
  };

  return { token, login, logout, isAuthenticated: !!token };
}
