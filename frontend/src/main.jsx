import React from 'react'
import ReactDOM from 'react-dom/client'
import axios from 'axios'
import App from './App.jsx'
import './index.css'

// Configure global API base URL for deployment (Vercel -> Render)
const apiBaseUrl = import.meta.env.VITE_API_URL;
if (apiBaseUrl) {
  axios.defaults.baseURL = apiBaseUrl.replace(/\/$/, '');
}

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
