import axios from 'axios';

let instance = axios.create({
    baseURL: process.env.VUE_APP_BACKEND_BASE_URL
});

instance.interceptors.request.use(config => {
        const token = localStorage.getItem('access_token');
        console.log(token);
        if (token) {
            config.headers['Authorization'] = 'Bearer ' + token;
        }
        return config;
    },
    error => {
        Promise.reject(error)
    });

export default instance;