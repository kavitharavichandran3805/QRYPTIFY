// import React, { createContext, useState, useEffect } from 'react';

// export const AuthContext = createContext();

// export function AuthProvider({ children }) {
//   const [accessToken, setAccessToken] = useState(() => {
//     // Initialize from localStorage
//     return localStorage.getItem('accessToken') || null;
//   });

//   // Persist token to localStorage whenever it changes
//   useEffect(() => {
//     if (accessToken) {
//       localStorage.setItem('accessToken', accessToken);
//     } else {
//       localStorage.removeItem('accessToken');
//     }
//   }, [accessToken]);

//   return (
//     <AuthContext.Provider value={{ accessToken, setAccessToken }}>
//       {children}
//     </AuthContext.Provider>
//   );
// }

import React, { createContext, useState, useEffect } from 'react';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(() => {
    // Initialize from localStorage (backward compatibility)
    return localStorage.getItem('accessToken') || null;
  });

  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Function to check auth status by calling an endpoint
  const checkAuthStatus = async () => {
    try {
      // This endpoint should verify cookies and return user info
      const response = await fetch('/api/user-details/', {
        credentials: 'include',
      });
      
      if (response.ok) {
        setIsAuthenticated(true);
        return true;
      }
    } catch (error) {
      console.error('Auth check failed:', error);
    }
    
    setIsAuthenticated(false);
    return false;
  };

  // Check auth on mount
  useEffect(() => {
    checkAuthStatus();
  }, []);

  // ✅ NEW: Get token from cookies via backend endpoint
  const getTokenFromCookies = async () => {
    try {
      const response = await fetch('/api/get-access-token/', {
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        if (data.access) {
          setAccessToken(data.access);
          localStorage.setItem('accessToken', data.access);
          return data.access;
        }
      }
    } catch (error) {
      console.error('Failed to get token from cookies:', error);
    }
    return null;
  };

  // Persist token to localStorage (backward compatibility)
  useEffect(() => {
    if (accessToken) {
      localStorage.setItem('accessToken', accessToken);
    } else {
      localStorage.removeItem('accessToken');
    }
  }, [accessToken]);

  // Function to logout (clear both frontend and backend)
  const logout = async () => {
    try {
      await fetch('/api/logout/', {
        credentials: 'include',
      });
    } catch (error) {
      console.error('Logout error:', error);
    }
    setAccessToken(null);
    localStorage.removeItem('accessToken');
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider value={{ 
      accessToken, 
      setAccessToken,
      isAuthenticated,
      setIsAuthenticated,
      checkAuthStatus,
      getTokenFromCookies,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  );
}