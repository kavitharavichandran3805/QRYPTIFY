import { getCookie } from "./cookies";

export async function api(endpoint,method,body=null,token=null){
  try{
      console.log("inside the api function")
      const url = 'http://localhost:8000/api/' + endpoint + "/";
      const options={
        method:method,
        headers:{
          'Content-Type':'application/json',
        },
        credentials:'include'
      }
      if(token){
        options.headers['Authorization']=`Bearer ${token}`
      }
      else{
        if (!(endpoint === 'login' || endpoint === 'signup'|| endpoint === 'csrf-token')) {
          const newAccessToken = await refreshAccessToken('refresh-token', 'GET');
          if (newAccessToken.status && newAccessToken.access) {
            options.headers['Authorization'] = `Bearer ${newAccessToken.access}`;
          } else {
            console.error('Failed to refresh access token');
            return { error: 'Failed to refresh access token' };
          }
      }
      }
      if(method!="GET"){
        const csrfToken = getCookie('csrftoken');
        options.headers["X-CSRFToken"]=csrfToken
      }
      if(body!==null){
        options.body=JSON.stringify(body)
      }
      const response=await fetch(url,options)
      if(response.ok){
        const result=await response.json()
        return result;
      }
      else{
        return { error: `Error: ${response.statusText}` };
      }
  }
  catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
        return { error: error.message };
    }

}

async function refreshAccessToken(endpoint,method,body=null){
  try{
    const csrfToken = getCookie('csrftoken');
    const url = 'http://localhost:8000/api/' + endpoint + "/";
    const options={
      method:method,
      headers:{
        'Content-Type':'application/json',
      },
      credentials:'include'
    }
    if(method!="GET"){
        options.headers["X-CSRFToken"]=csrfToken
      }
      if(body!==null){
        options.body=JSON.stringify(body)
      }
      const response=await fetch(url,options)
      if(response.ok){
        const result=await response.json()
        return result;
      }
      else{
        return { error: `Error: ${response.statusText}` };
      }
  }
  catch (error) {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
        return { error: error.message };
    }
}


