import React, { createContext, useState } from 'react';

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(null);

  return (
    <AuthContext.Provider value={{ accessToken, setAccessToken }}>
      {children}
    </AuthContext.Provider>
  );
}


// import React, { createContext, useState, useEffect } from "react";

// export const AuthContext = createContext();

// export function AuthProvider({ children }) {
//   const [accessToken, setAccessToken] = useState(
//     () => localStorage.getItem("accessToken") || null
//   );
//   useEffect(() => {
//     if (accessToken) {
//       localStorage.setItem("accessToken", accessToken);
//     } else {
//       localStorage.removeItem("accessToken");
//     }
//   }, [accessToken]);

//   return (
//     <AuthContext.Provider value={{ accessToken, setAccessToken }}>
//       {children}
//     </AuthContext.Provider>
//   );
// }
