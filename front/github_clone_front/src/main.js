import { createApp } from 'vue'
import { createRouter, createWebHistory } from "vue-router"
import App from './App.vue'
import DeveloperRegistration from './components/auth/DeveloperRegistration.vue'
import CodeVerification from './components/auth/CodeVerification.vue'
import LoginPage from './components/auth/LoginPage.vue'
import MainPage from './components/pages/MainPage.vue'

import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import "bootstrap/dist/js/bootstrap"
import 'vue3-toastify/dist/index.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faAngleRight } from '@fortawesome/free-solid-svg-icons'
import { faFlask } from '@fortawesome/free-solid-svg-icons'

library.add(faAngleRight);
library.add(faFlask);

const routes = [
    {
        path: "/main_page",
        component: MainPage
    },
    {
        path: "/register",
        component: DeveloperRegistration
    },
    {
        path: "/account_verification",
        component: CodeVerification
    },
    {
        path: "/",
        component: LoginPage
    }
]

const router = createRouter({
    history: createWebHistory(""),
    routes,
});

const app = createApp(App).use(router).component('font-awesome-icon', FontAwesomeIcon);
app.mount("#app");
