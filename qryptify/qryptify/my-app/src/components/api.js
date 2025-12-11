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


// export async function api(endpoint,method,body=null,token=null){
//   try{
//       console.log("inside the api function")
//       const url = 'http://localhost:8000/api/' + endpoint + "/";
//       const options={
//         method:method,
//         headers:{
//           'Content-Type':'application/json',
//         },
//         credentials:'include'
//       }
//       if(token && !isTokenExpired(token)){
//         console.log("Access token exists")
//         options.headers['Authorization']=`Bearer ${token}`
//       }
//       else{
//         if (!(endpoint === 'login' || endpoint === 'signup'|| endpoint === 'csrf-token')) {
//           const newAccessToken = await refreshAccessToken('refresh-token', 'GET');
//           if (newAccessToken.status && newAccessToken.access) {
//             options.headers['Authorization'] = `Bearer ${newAccessToken.access}`;
//           } else {
//             console.error('Failed to refresh access token');
//             return { error: 'Failed to refresh access token' };
//           }
//       }
//       }
//       if(method!="GET"){
//         const csrfToken = getCookie('csrftoken');
//         options.headers["X-CSRFToken"]=csrfToken
//       }
//       if(body!==null){
//         options.body=JSON.stringify(body)
//       }
//       const response=await fetch(url,options)
//       if(response.ok){
//         const result=await response.json()
//         return result;
//       }
//       else{
//         return { error: `Error: ${response.statusText}` };
//       }
//   }
//   catch (error) {
//         console.error('Error:', error);
//         alert('An error occurred. Please try again.');
//         return { error: error.message };
//     }

// }

// async function refreshAccessToken(endpoint,method,body=null){
//   try{
//     const csrfToken = getCookie('csrftoken');
//     const url = 'http://localhost:8000/api/' + endpoint + "/";
//     const options={
//       method:method,
//       headers:{
//         'Content-Type':'application/json',
//       },
//       credentials:'include'
//     }
//     if(method!="GET"){
//         options.headers["X-CSRFToken"]=csrfToken
//       }
//       if(body!==null){
//         options.body=JSON.stringify(body)
//       }
//       const response=await fetch(url,options)
//       if(response.ok){
//         const result=await response.json()
//         return result;
//       }
//       else{
//         return { error: `Error: ${response.statusText}` };
//       }
//   }
//   catch (error) {
//         console.error('Error:', error);
//         alert('An error occurred. Please try again.');
//         return { error: error.message };
//     }
// }

import { getCookie } from "./cookies";
import { jwtDecode } from "jwt-decode";

function isTokenExpired(token) {
  try {
    const decoded = jwtDecode(token);
    const now = Date.now() / 1000;
    return decoded.exp < now;
  } catch (e) {
    return true; // Treat invalid/absent token as expired
  }
}

// Utility: normalize endpoint (strip trailing slashes)
function normalizeEndpoint(endpoint) {
  return endpoint.replace(/\/+$/, ""); // remove trailing "/"
}

export async function api(endpoint, method, body = null, token = null) {
  try {
    console.log("inside the api function");
    const cleanEndpoint = normalizeEndpoint(endpoint); // normalize
    const url = `http://localhost:8000/api/${cleanEndpoint}/`;

    const options = {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
    };

    // Attach token if valid
    if (token && !isTokenExpired(token)) {
      console.log("Access token exists");
      options.headers["Authorization"] = `Bearer ${token}`;
    } else {
      // Only refresh if endpoint is not login/signup/csrf-token
      if (!["login", "csrf-token"].includes(cleanEndpoint)) {
        const newAccessToken = await refreshAccessToken("refresh-token", "GET");
        if (newAccessToken.status && newAccessToken.access) {
          options.headers["Authorization"] = `Bearer ${newAccessToken.access}`;
        } else {
          console.error("Failed to refresh access token");
          return { error: "Failed to refresh access token" };
        }
      }
    }

    // Add CSRF token for non-GET requests (including login)
    if (method !== "GET") {
      const csrfToken = getCookie("csrftoken");
      if (csrfToken) {
        options.headers["X-CSRFToken"] = csrfToken;
      }
    }

    // Attach body if present
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

async function refreshAccessToken(endpoint, method, body = null) {
  try {
    const csrfToken = getCookie("csrftoken");
    const url = `http://localhost:8000/api/${normalizeEndpoint(endpoint)}/`;

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



