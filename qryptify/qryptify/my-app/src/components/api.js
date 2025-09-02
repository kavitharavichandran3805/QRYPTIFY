import { getCookie } from "./cookies";

export async function api(endpoint,method,body=null){
  try{
      console.log("inside the api function")
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