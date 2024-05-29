<template>
    <div class="bg min-vh-100 is-fullheight">
        <div v-if="allowed == true">
            <RepoNavbar starting="code" />

            <div class="d-flex justify-content-between w-100">
                <div class="d-flex justify-content-start ms-4 mt-3">
                    <button type="button" class="btn">
                        <img class="avatar" :src="owner.avatar" alt="User avatar" />
                    </button>
                    <span class="me-3 repo-name bright">{{ repo.name }}</span>
                    <span class="badge rounded-pill h-50 pb-3">{{ repo.accessModifier }}</span>
                </div>

                <div class="d-flex justify-content-end me-4">
                    <WatchChoice :key="watchKey" :watchInfo="repo.watch" />
                    <button v-if="!isUsersRepo()" type="button" class="btn-right me-2" @click="fork" style="background: #373e48; color: #a7b5c2; border-radius: 5px;">
                        <font-awesome-icon icon="fa-solid fa-code-fork" class="me-1" />
                        Fork
                    </button>
                    <button @click="toggleStar" type="button" class="btn-right" style="background: #373e48; color: #a7b5c2; border-radius: 5px;">
                        <font-awesome-icon v-if="!isStarred" icon="fa-regular fa-star" style="color: #b1aaaa;" />
                        <i v-if="isStarred" class="bi bi-star-fill" style="color: yellow; margin-right: 3px;"></i>
                        Star
                    </button>
                </div>
            </div>

            <div v-if="repo.forkedFrom" class="d-flex justify-content-start mx-4">
                <span class="ms-3">Forked from</span>
                <button type="button" class="btn-forked-from" @click="viewOriginalRepo">
                    {{ repo.forkedFrom.ownerUsername }}/{{ repo.forkedFrom.repositoryName }}
                </button>
            </div>

            <hr class="mx-4" style="color: #c5d1df;">

            <div class="d-flex justify-content-start mx-4">
                <div class="w-75">
                    <div class="d-flex justify-content-between">
                        <div class="d-flex justify-content-start">
                            <button class="branch nav-link dropdown-toggle btn-gray" type="button" role="button" data-bs-toggle="dropdown">
                                <font-awesome-icon icon="fa-solid fa-code-branch" class="me-1 mt-1" /> {{ repo.chosenBranch }}
                            </button>
                            <ul class="dropdown-menu" style="background-color: #2c333b;">
                                <li class="mx-2">
                                    <input type="text" placeholder="Search branches" class="px-1" v-model="branchesSearchTerm" @input="filterBranches" />
                                </li>
                                <li v-for="b in filteredBranches" :key="b.name">
                                    <button class="curr-branch-btn dropdown-item" @click="selectedBranchChanged(b.name)" style="color: #c5d1df;">
                                        {{ b.name }}
                                    </button>
                                </li>
                            </ul>
                            <button type="button" class="btn-gray ms-2" @click="viewBranches">
                                <font-awesome-icon icon="fa-solid fa-code-branch" class="mt-1" /> {{ numBranches }}
                                {{ branchesText }}
                            </button>
                            <button type="button" class="btn-gray ms-2" @click="viewTags">
                                <i class="bi bi-tag"></i> {{ this.numTags }}
                                {{ tagsText }}
                            </button>
                        </div>

                        <div class="d-flex justify-content-end">

                            <div v-if="canAddFiles()">
                                <button class="add-file nav-link dropdown-toggle btn-gray me-2" type="button" role="button" data-bs-toggle="dropdown">
                                    Add file
                                </button>
                                <ul class="dropdown-menu">
                                    <li>
                                        <button class="btn dropdown-item" @click="createNewFile">
                                            <font-awesome-icon icon="fa-solid fa-plus" class="me-2 mt-1" /> Create new
                                            file
                                        </button>
                                    </li>
                                    <li>
                                        <button class="btn dropdown-item" @click="uploadFiles">
                                            <font-awesome-icon icon="fa-solid fa-upload" class="me-2 mt-1" /> Upload
                                            files
                                        </button>
                                    </li>
                                </ul>
                            </div>


                            <button type="button"
                                :class="(httpChosen) ? 'btn-http-ssh btn-chosen bright' : 'btn-http-ssh'"
                                @click="setHttpChosen">HTTP</button>
                            <button type="button"
                                :class="(!httpChosen) ? 'btn-http-ssh btn-chosen me-2 bright' : 'btn-http-ssh me-2'"
                                @click="setSshChosen">SSH</button>
                            <input v-if="httpChosen" type="text" readonly v-model="repo.http" />
                            <input v-else type="text" readonly v-model="repo.ssh" />
                        </div>
                    </div>

                    <div v-if="repo.commitsOverview[repo.chosenBranch] !== undefined">
                        <CommitsOverview class="mt-3"
                            :latestCommit="repo.commitsOverview[repo.chosenBranch].latest_commit"
                            :numCommits="repo.commitsOverview[repo.chosenBranch].num_commits"
                            :branchName="repo.chosenBranch" />
                        <RepoContent :refName="repo.chosenBranch" :key="contentKey" :displayRoot="repo.displayRoot"
                            @folderClicked="folderClicked" :foldersPath="repo.foldersPath"
                            @returnToParent="returnToParent" :branch="repo.chosenBranch" />
                    </div>
                </div>


                <div class="w-25 ms-4">
                    <div class="d-flex flex-column">
                        <span class="bolder mt-1 bright">About</span>
                        <span v-if="repo.description" class="mt-3 muted">{{ repo.description }}</span>
                        <span v-else class="mt-3 muted"><i>No description provided</i></span>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="allowed == false">
            <NotFoundPage />
        </div>
    </div>
</template>

<script>

import RepositoryService from '@/services/RepositoryService';
import RepoContent from '@/components/repository/RepoContent.vue'
import RepoNavbar from './RepoNavbar.vue';
import NotFoundPage from '../util/NotFoundPage.vue';
import DeveloperService from '@/services/DeveloperService';
import CommitsOverview from './CommitsOverview.vue';
import WatchChoice from './WatchChoice.vue';
import TagService from '@/services/TagService';

export default {
    name: 'ViewRepo',

    components: {
        RepoContent,
        RepoNavbar,
        NotFoundPage,
        CommitsOverview,
        WatchChoice
    },

    mounted() {
        RepositoryService.get(this.$route.params.username, this.$route.params.repoName, localStorage.getItem("username")).then(res => {
            this.repo.name = res.data.name;
            this.repo.description = res.data.description;
            this.repo.accessModifier = res.data.access_modifier;
            this.repo.http = res.data.http;
            this.repo.ssh = res.data.ssh;
            this.repo.defaultBranch = res.data.default_branch;
            this.repo.commitsOverview = res.data.commits_overview;
            this.isStarred = res.data.star;
            this.repo.watch = res.data.watch;

            if (res.data.forked_from !== null && res.data.forked_from !== undefined) {
                this.repo.forkedFrom = {
                    ownerUsername: res.data.forked_from.owner_username,
                    repositoryName: res.data.forked_from.repository_name
                };
            } else {
                this.repo.forkedFrom = null;
            }

            this.repo.chosenBranch = res.data.default_branch;
            if (this.$route.query.chosen) {
                this.repo.chosenBranch = this.$route.query.chosen;
            }
            if (this.$route.query.path) {
                this.repo.foldersPath = this.$route.query.path + "/";
                this.repo.displayRoot = "false";
            }
            this.$router.replace({ 'query': null });

            for (let b of res.data.branches) {
                this.repo.branches.push({ 'name': b });
            }
            this.allowed = true
            this.filteredBranches = this.repo.branches;
            this.forceRerender();
        }).catch(err => {
            console.log(err);
            this.allowed = false;
        });

        RepositoryService.getOwner(this.$route.params.username).then(res => {
            this.owner.email = res.data.user.email;
            this.owner.firstName = res.data.user.first_name;
            this.owner.lastName = res.data.user.last_name;
        }).catch(err => {
            console.log(err);
        });


        DeveloperService.getUserAvatar(this.$route.params.username)
            .then(res => {
                this.owner.avatar = res.data
            })
            .catch(err => {
                console.log(err);
            });

        TagService.getTags(this.$route.params.username, this.$route.params.repoName).then((res) => {
            this.numTags = res.data.length
        })
            .catch(err => {
                console.log(err);
            });
    },

    data() {
        return {
            numTags: 0,
            repo: {
                name: '',
                description: '',
                accessModifier: '',
                defaultBranch: '',
                http: '',
                ssh: '',
                branches: [],
                chosenBranch: '',
                displayRoot: 'true',
                foldersPath: '',
                watch: {}
            },

            owner: {
                firstName: '',
                lastName: '',
                avatar: '',
                email: ''
            },

            httpChosen: true,
            contentKey: 1,
            allowed: 'not_set',
            isStarred: false,
            watchKey: 1,

            branchesSearchTerm: "",
            filteredBranches: []
        }
    },

    methods: {
        setHttpChosen() {
            this.httpChosen = true;
        },

        setSshChosen() {
            this.httpChosen = false;
        },

        forceRerender() {
            this.contentKey += 1;
            this.watchKey += 1;
        },

        filterBranches() {
            this.filteredBranches = this.repo.branches.filter(x => x.name.toLowerCase().includes(this.branchesSearchTerm.toLocaleLowerCase()));
        },

        isUsersRepo() {
            return localStorage.getItem("username") === this.$route.params.username;
        },

        selectedBranchChanged(branchName) {
            this.repo.chosenBranch = branchName;
            this.forceRerender();
        },

        folderClicked(data) {
            this.repo.foldersPath = this.repo.foldersPath.concat(data["name"] + "/")
            this.repo.displayRoot = "false";
            console.log(this.repo.foldersPath);
            this.forceRerender();
        },

        fork() {
            this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}/fork`)
        },

        returnToParent() {
            let folders = this.repo.foldersPath.split('/');
            folders.splice(-2);
            this.repo.foldersPath = folders.join('/') + '/';
            console.log(this.repo.foldersPath);
            if (this.repo.foldersPath === '/') {
                this.repo.displayRoot = "true";
            }
            this.forceRerender();
        },

        viewBranches() {
            this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}/branches`);
        },

        createNewFile() {
            this.$router.push(`/${this.$route.params.username}/${this.$route.params.repoName}/new/${this.repo.chosenBranch}`);
        },

        uploadFiles() {
            this.$router.push(`/${this.$route.params.username}/${this.$route.params.repoName}/upload/${this.repo.chosenBranch}`);
        },

        canAddFiles() {
            const role = localStorage.getItem(this.$route.params.repoName);
            return role === "Owner" || role === "Developer" || role === "Maintainer";
        },

        viewOriginalRepo() {
            let route = this.$router.resolve({ path: `/view/${this.repo.forkedFrom.ownerUsername}/${this.repo.forkedFrom.repositoryName}` });
            window.open(route.href, '_blank')
        },
        toggleStar() {
            this.isStarred = !this.isStarred;
            if (this.isStarred)
                RepositoryService.starr_it(localStorage.getItem('username'), this.repo.name, this.$route.params.username)
                    .then(res => {
                        console.log(res.data)
                    })
                    .catch(err => {
                        console.log(err);
                    });
            else
                RepositoryService.unstarr_it(localStorage.getItem('username'), this.repo.name, this.$route.params.username)
                    .then(res => {
                        console.log(res.data)
                    })
                    .catch(err => {
                        console.log(err);
                    });
        },
        viewTags() {
            this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}/tags`)
        }
    },

    computed: {
        numBranches() {
            return this.repo.branches.length;
        },

        branchesText() {
            return this.repo.branches.length > 1 ? "Branches" : "Branch";
        },

        tagsText() {
            return this.numTags != 1 ? 'Tags' : 'Tag'
        }
    }
}

</script>

<style scoped>
.bg {
    background-color: #22272d;
}

.btn-http-ssh {
    background: none;
    border: none;
    width: 50px;
    color: #c5d1df;
}

.avatar {
    height: 27px;
    border-radius: 50%;
}

.badge {
    margin-top: 14px;
    border: 2px solid #aeb6c0;
    color: #aeb6c0;
    background-color: #22272d;
}

.bright {
    color: #c5d1df;
}

.muted {
    color: #768491;
}

.repo-name {
    font-weight: 600;
    margin-top: 11px;
    font-size: large;
}

.btn-right {
    border: 1px solid #d6d9dd;
    height: 32px;
    width: 100px;
    margin-top: 25px;
    font-size: small;
}

input {
    min-width: 320px;
    height: 30px;
    margin-top: 10px;
    background-color: #22272d;
    border: 1px solid #7f8286;
    border-radius: 5px;
    font-size: small;
    padding-left: 5px;
    color: #c5d1df;
}

.bolder {
    font-weight: 600;
}

.btn-chosen {
    border-bottom: 2px solid #fe8c72;
    border-radius: 0%;
    color: #c5d1df;
}

.btn-chosen:hover {
    border-bottom: 2px solid #fe8c72;
}

.btn-gray {
    border-radius: 5px;
    border: none;
    background-color: #373e48;
    color: #c5d1df;
    height: 37px;
    min-width: 110px;
    margin-top: 10px;
    border-radius: 7px;
}

.search {
    height: 35px;
}

.btn-forked-from {
    background: none;
    border: none;
    color: #488ae7;
    text-decoration: underline;
}

.branch:hover, .add-file:hover, .btn-gray:hover {
    color: #c5d1df;
    background-color: #454e5a;
}

.branch {
    width: 145px;
}

.curr-branch-btn {
    margin-top: 3px;
}

.curr-branch-btn:hover {
    background-color: #434a54 !important;
}
</style>