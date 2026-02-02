// import { getCookie } from "./cookies";
// import { jwtDecode } from "jwt-decode";

// function isTokenExpired(token) {
//   try {
//     const decoded = jwtDecode(token);
//     const now = Date.now() / 1000;
//     return decoded.exp < now;
//   } catch (e) {
//     return true; 
//   }
// }

// function normalizeEndpoint(endpoint) {
//   return endpoint.replace(/\/+$/, ""); 
// }

// export async function api(endpoint, method, body = null, token = null) {
//   try {
//     console.log("inside the api function");
//     const cleanEndpoint = normalizeEndpoint(endpoint); 
//     const url = `http://localhost:8000/api/${cleanEndpoint}/`;
//     const isFileUpload = body instanceof FormData;
//     const options = {
//       method: method,
//       headers: {},
//       credentials: "include",
//     };
//     if (!isFileUpload) {
//     options.headers["Content-Type"] = "application/json";
//     }
//     // Attach token if valid
//     if (token && !isTokenExpired(token)) {
//       console.log("Access token exists");
//       options.headers["Authorization"] = `Bearer ${token}`;
//     } else {
//       // Only refresh if endpoint is not login/signup/csrf-token
//       if (!["login", "csrf-token", "user-account-delete"].includes(cleanEndpoint)) {
//         const newAccessToken = await refreshAccessToken("refresh-token", "GET");
//         if (newAccessToken.status && newAccessToken.access) {
//           options.headers["Authorization"] = `Bearer ${newAccessToken.access}`;
//         } else {
//           console.error("Failed to refresh access token");
//           return { error: "Failed to refresh access token" };
//         }
//       }
//     }

//     // Add CSRF token for non-GET requests (including login)
//     if (method !== "GET") {
//       const csrfToken = getCookie("csrftoken");
//       if (csrfToken) {
//         options.headers["X-CSRFToken"] = csrfToken;
//       }
//     }

//     // Attach body if present
//     // --- CRITICAL CHANGE 3: Conditionally attach body ---
//     if (body !== null) {
//       if (isFileUpload) {
//         // 1. If it's a file, pass the raw FormData object directly
//         options.body = body; 
//         console.log("Attaching raw FormData body for file upload.");
//       } else {
//         // 2. If it's JSON, stringify it
//         options.body = JSON.stringify(body);
//         console.log("Attaching stringified JSON body.");
//       }
//     }

//     const response = await fetch(url, options);

//     if (response.ok) {
//       const result = await response.json();
//       return result;
//     } else {
//       return { error: `Error: ${response.status} ${response.statusText}` };
//     }
//   } catch (error) {
//     console.error("Error:", error);
//     alert("An error occurred. Please try again.");
//     return { error: error.message };
//   }
// }

// async function refreshAccessToken(endpoint, method, body = null) {
//   try {
//     const csrfToken = getCookie("csrftoken");
//     const url = `http://localhost:8000/api/${normalizeEndpoint(endpoint)}/`;

//     const options = {
//       method: method,
//       headers: {
//         "Content-Type": "application/json",
//       },
//       credentials: "include",
//     };

//     if (method !== "GET" && csrfToken) {
//       options.headers["X-CSRFToken"] = csrfToken;
//     }
//     if (body !== null) {
//       options.body = JSON.stringify(body);
//     }

//     const response = await fetch(url, options);

//     if (response.ok) {
//       const result = await response.json();
//       return result;
//     } else {
//       return { error: `Error: ${response.status} ${response.statusText}` };
//     }
//   } catch (error) {
//     console.error("Error:", error);
//     alert("An error occurred. Please try again.");
//     return { error: error.message };
//   }
// }

import { getCookie } from "./cookies";
import { jwtDecode } from "jwt-decode";

// Get the base URL from environment variable
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Helper function to get full URL
function getFullUrl(endpoint) {
  const cleanEndpoint = normalizeEndpoint(endpoint);
  // Remove trailing slash from base URL if present, add it back properly
  const base = API_BASE_URL.endsWith('/') 
    ? API_BASE_URL.slice(0, -1) 
    : API_BASE_URL;
  
  // If base already includes '/api', don't add it again
  if (base.includes('/api')) {
    return `${base}/${cleanEndpoint}/`;
  }
  
  return `${base}/${cleanEndpoint}/`;
}

function isTokenExpired(token) {
  try {
    const decoded = jwtDecode(token);
    const now = Date.now() / 1000;
    return decoded.exp < now;
  } catch (e) {
    return true;
  }
}

function normalizeEndpoint(endpoint) {
  return endpoint.replace(/\/+$/, "");
}

export async function api(endpoint, method, body = null, token = null) {
  try {
    console.log("API Base URL:", API_BASE_URL);
    const url = getFullUrl(endpoint);
    console.log("Making request to:", url);
    
    const isFileUpload = body instanceof FormData;
    const options = {
      method: method,
      headers: {},
      credentials: "include",
    };
    
    if (!isFileUpload) {
      options.headers["Content-Type"] = "application/json";
    }
    
    // Attach token if valid
    if (token && !isTokenExpired(token)) {
      console.log("Access token exists");
      options.headers["Authorization"] = `Bearer ${token}`;
    } else {
      // Only refresh if endpoint is not login/signup/csrf-token
      if (!["login", "csrf-token", "user-account-delete", "register", "signup", "logout"].includes(normalizeEndpoint(endpoint))) {
        const newAccessToken = await refreshAccessToken("refresh-token", "GET");
        if (newAccessToken.status && newAccessToken.access) {
          options.headers["Authorization"] = `Bearer ${newAccessToken.access}`;
        } else {
          console.error("Failed to refresh access token");
          return { error: "Failed to refresh access token" };
        }
      }
    }

    // Add CSRF token for non-GET requests
    if (method !== "GET") {
      const csrfToken = getCookie("csrftoken");
      if (csrfToken) {
        options.headers["X-CSRFToken"] = csrfToken;
      }
    }

    // Attach body if present
    if (body !== null) {
      if (isFileUpload) {
        options.body = body;
        console.log("Attaching raw FormData body for file upload.");
      } else {
        options.body = JSON.stringify(body);
        console.log("Attaching stringified JSON body.");
      }
    }

    const response = await fetch(url, options);

    if (response.ok) {
      const result = await response.json();
      return result;
    } else {
      return { error: `Error: ${response.status} ${response.statusText}` };
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred. Please try again.");
    return { error: error.message };
  }
}

async function refreshAccessToken(endpoint, method, body = null) {
  try {
    const csrfToken = getCookie("csrftoken");
    const url = getFullUrl(endpoint);

    const options = {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
    };

    if (method !== "GET" && csrfToken) {
      options.headers["X-CSRFToken"] = csrfToken;
    }
    if (body !== null) {
      options.body = JSON.stringify(body);
    }

    const response = await fetch(url, options);

    if (response.ok) {
      const result = await response.json();
      return result;
    } else {
      return { error: `Error: ${response.status} ${response.statusText}` };
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred. Please try again.");
    return { error: error.message };
  }
}

