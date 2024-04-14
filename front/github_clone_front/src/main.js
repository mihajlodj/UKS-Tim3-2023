import { createApp } from 'vue'
import { createRouter, createWebHistory } from "vue-router"
import App from './App.vue'
import DeveloperRegistration from './components/auth/DeveloperRegistration.vue'
import CodeVerification from './components/auth/CodeVerification.vue'
import LoginPage from './components/auth/LoginPage.vue'
import CreateRepo from './components/repository/CreateRepo.vue'
import ViewRepo from './components/repository/ViewRepo.vue'
import RepoSettings from './components/repository/settings/RepoSettings.vue';
import MainPage from './components/pages/MainPage.vue'
import ProfilePage from './components/profile/ProfilePage.vue'
import SettingsProfile from './components/settingsProfile/SettingsProfile.vue'
import BranchesView from './components/repository/branch/BranchesView.vue';
import FileDisplay from './components/repository/content/FileDisplay.vue';
import CreateFile from './components/repository/content/CreateFile.vue';
import UploadFile from './components/repository/content/upload/UploadFile.vue';
import ListMilestoneComponent from '@/components/milestone/ListMilestoneComponent.vue'
import CreatePrPage from '@/components/pullRequest/CreatePrPage.vue'
import PrDisplay from '@/components/pullRequest/PrDisplay.vue'
import PrList from '@/components/pullRequest/PrList.vue'
import HistoryView from '@/components/repository/HistoryView.vue'
import CommitDisplay from './components/commit/CommitDisplay.vue'
import CollaborationInvitation from './components/repository/CollaborationInvitation.vue'
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
import { faCodePullRequest, faCodeBranch, faUserLock, faXmark } from '@fortawesome/free-solid-svg-icons'
import { faCircleDot, faComments } from '@fortawesome/free-regular-svg-icons'
import { faGear, faCodeFork, faPlus, faUpload, faPen, faArrowRightArrowLeft, faArrowLeftLong, faClockRotateLeft } from '@fortawesome/free-solid-svg-icons'
import { faEye, faStar, faFile, faFolder, faTrashCan, faCircleXmark, faCopy } from '@fortawesome/free-regular-svg-icons'
import { faFlask, faDownload, faTag, faCheck, faCodeCommit, faAngleDown, faCirclePlus, faCircleMinus, faCircleStop, faUsers } from '@fortawesome/free-solid-svg-icons'
import 'vue-pdf-embed/dist/style/index.css'
import 'vue-pdf-embed/dist/style/annotationLayer.css'
import 'vue-pdf-embed/dist/style/textLayer.css'

import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

// test
// import IssueComponent from './components/issue/IssueComponent'
import ListIssueComponent from './components/issue/ListIssueComponent.vue'

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
library.add(faCodeBranch);
library.add(faPlus);
library.add(faUpload);
library.add(faFile);
library.add(faFolder);
library.add(faPen);
library.add(faArrowRightArrowLeft);
library.add(faFlask);
library.add(faTrashCan);
library.add(faDownload);
library.add(faArrowLeftLong);
library.add(faCircleXmark);
library.add(faTag);
library.add(faCheck);
library.add(faCopy);
library.add(faComments);
library.add(faCodeCommit);
library.add(faAngleDown);
library.add(faCirclePlus);
library.add(faCircleMinus);
library.add(faCircleStop);
library.add(faClockRotateLeft);
library.add(faUsers);
library.add(faUserLock);
library.add(faXmark);

const routes = [
    {
        path: "/main",
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
    },
    {
        path: "/new",
        component: CreateRepo
    },
    {
        path: "/view/:username/:repoName",
        component: ViewRepo
    },
    {
        path: "/settings/:username/:repoName",
        component: RepoSettings
    },
    {
        path: "/profile",
        component: ProfilePage
    },
    {
        path: "/profile/settings",
        component: SettingsProfile
    },
    {
        path: "/view/:username/:repoName/branches",
        component: BranchesView
    },
    {
        path: "/view/:username/:repoName/blob/:branchName/:path(.*)",
        component: FileDisplay
    },
    {
        path: "/:username/:repoName/new/:branchName",
        component: CreateFile
    },
    {
        path: "/:username/:repoName/upload/:branchName",
        component: UploadFile
    },
    {
        path: "/view/:username/:repoName/milestones",
        component:ListMilestoneComponent
    },
    {
        path: "/view/:username/:repoName/compare",
        component: CreatePrPage
    },
    {
        path: "/view/:username/:repoName/pulls",
        component: PrList
    },
    {
        path: "/view/:username/:repoName/pulls/:id",
        component: PrDisplay
    },
    {
        path: '/view/:username/:repoName/issues',
        component: ListIssueComponent
    },
    {
        path: "/view/:username:/:repoName/commits/:branchName",
        component: HistoryView
    },
    {
        path: "/view/:username/:repoName/commit/:sha",
        component: CommitDisplay
    },
    {
        path: "/view/:username/:repoName/invitations/:invitedUsername",
        component: CollaborationInvitation
    }
]

const router = createRouter({
    history: createWebHistory(""),
    routes,
});

const app = createApp(App).use(router).component('font-awesome-icon', FontAwesomeIcon);
app.component('VueDatePicker', VueDatePicker);
app.mount("#app");
