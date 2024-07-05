import axios from 'axios';

// Erstelle eine Instanz von Axios mit der Basis-URL
const axiosInstance = axios.create({
  baseURL: 'http://localhost:9000/',
});

export default axiosInstance;