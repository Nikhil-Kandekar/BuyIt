import axios from 'axios'

const baseapi = axios.create({
    baseURL:"http://127.0.0.1:5000",
    headers: {
        "Content-type": "application/json",
        "Access-Control-Allow-Origin" : "*",
      }
})

export default baseapi;