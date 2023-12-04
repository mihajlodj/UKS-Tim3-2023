import { createApp } from 'vue'
import { createRouter, createWebHistory } from "vue-router";
import App from './App.vue'
import DeveloperRegistration from './components/auth/DeveloperRegistration.vue'
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import 'vue3-toastify/dist/index.css';

const routes = [
    {
        path: "/register",
        component: DeveloperRegistration
    },
]

const router = createRouter({
    history: createWebHistory(""),
    routes,
});

const app = createApp(App).use(router);
app.mount("#app");
