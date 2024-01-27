import { createApp } from 'vue'
import { createRouter, createWebHistory } from "vue-router"
import App from './App.vue'
import DeveloperRegistration from './components/auth/DeveloperRegistration.vue'
import CodeVerification from './components/auth/CodeVerification.vue'
import LoginPage from './components/auth/LoginPage.vue'
import CreateRepo from './components/repository/CreateRepo.vue'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import 'vue3-toastify/dist/index.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faAngleRight } from '@fortawesome/free-solid-svg-icons'
import { faCircleInfo } from '@fortawesome/free-solid-svg-icons'
import { faBookBookmark } from '@fortawesome/free-solid-svg-icons'
import { faLock } from '@fortawesome/free-solid-svg-icons'

library.add(faAngleRight);
library.add(faCircleInfo);
library.add(faBookBookmark);
library.add(faLock);

const routes = [
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
    },
    {
        path: "/new",
        component: CreateRepo
    }
]

const router = createRouter({
    history: createWebHistory(""),
    routes,
});

const app = createApp(App).use(router).component('font-awesome-icon', FontAwesomeIcon);
app.mount("#app");
