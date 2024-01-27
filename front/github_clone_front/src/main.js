import { createApp } from 'vue'
import { createRouter, createWebHistory } from "vue-router"
import App from './App.vue'
import DeveloperRegistration from './components/auth/DeveloperRegistration.vue'
import CodeVerification from './components/auth/CodeVerification.vue'
import LoginPage from './components/auth/LoginPage.vue'
import CreateRepo from './components/repository/CreateRepo.vue'
import ViewRepo from './components/repository/ViewRepo.vue'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import 'vue3-toastify/dist/index.css'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faAngleRight } from '@fortawesome/free-solid-svg-icons'
import { faCircleInfo } from '@fortawesome/free-solid-svg-icons'
import { faBookBookmark } from '@fortawesome/free-solid-svg-icons'
import { faLock } from '@fortawesome/free-solid-svg-icons'
import { faTriangleExclamation } from '@fortawesome/free-solid-svg-icons'
import { faCode } from '@fortawesome/free-solid-svg-icons'
import { faCodePullRequest } from '@fortawesome/free-solid-svg-icons'
import { faCircleDot } from '@fortawesome/free-regular-svg-icons'
import { faGear, faCodeFork } from '@fortawesome/free-solid-svg-icons'
import { faEye, faStar } from '@fortawesome/free-regular-svg-icons'

library.add(faAngleRight);
library.add(faCircleInfo);
library.add(faBookBookmark);
library.add(faLock);
library.add(faTriangleExclamation);
library.add(faCode);
library.add(faCodePullRequest);
library.add(faCircleDot);
library.add(faGear);
library.add(faEye);
library.add(faCodeFork);
library.add(faStar);

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
    },
    {
        path: "/view/:username/:repoName",
        component: ViewRepo
    }
]

const router = createRouter({
    history: createWebHistory(""),
    routes,
});

const app = createApp(App).use(router).component('font-awesome-icon', FontAwesomeIcon);
app.mount("#app");
