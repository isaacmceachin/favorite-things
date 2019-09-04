import axios from 'axios';

axios.defaults.baseURL = process.env.API_ENDPOINT;

axios.defaults.xsrfHeaderName = "X-CSRFToken"
axios.defaults.xsrfCookieName = 'csrftoken'

export default axios;
