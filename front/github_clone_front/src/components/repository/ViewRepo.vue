<template>
    <div>
        <div v-if="allowed == true">
            <RepoNavbar starting="code" />

            <div class="d-flex justify-content-between w-100">
                <div class="d-flex justify-content-start ms-4 mt-3">
                    <button type="button" class="btn">
                        <img class="avatar" :src="owner.avatar" alt="User avatar" />
                    </button>
                    <span class="me-3 repo-name">{{ repo.name }}</span>
                    <span class="badge rounded-pill h-50 pb-3">{{ repo.accessModifier }}</span>
                </div>

                <div class="d-flex justify-content-end me-4">
                    <button type="button" class="btn btn-right me-2">
                        <font-awesome-icon icon="fa-regular fa-eye" class="me-1" />
                        Watch
                    </button>
                    <button type="button" class="btn btn-right me-2">
                        <font-awesome-icon icon="fa-solid fa-code-fork" class="me-1" />
                        Fork
                    </button>
                    <button type="button" class="btn btn-right">
                        <font-awesome-icon icon="fa-regular fa-star" class="me-1" />
                        Star
                    </button>
                </div>
            </div>

            <hr class="mx-4">

            <div class="d-flex justify-content-start mx-4">
                <div class="w-75">
                    <div class="d-flex justify-content-between">
                        <div class="d-flex justify-content-start">
                            <button class="btn nav-link dropdown-toggle btn-gray" type="button" id="navbarDropdown"
                                role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                <font-awesome-icon icon="fa-solid fa-code-branch" class="me-2 mt-1" /> {{ repo.chosenBranch }}
                            </button>
                            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                                <li class="mx-2">
                                    <input type="text" placeholder="Search branches" class="px-1" />
                                </li>
                                <li v-for="b in repo.branches" :key="b.name">
                                    <button class="btn dropdown-item" @click="selectedBranchChanged(b.name)">
                                        {{ b.name }}
                                    </button>
                                </li>
                            </ul>
                            <button type="button" class="btn btn-gray ms-2" @click="viewBranches">
                                <font-awesome-icon icon="fa-solid fa-code-branch" class="me-2 mt-1" /> {{ numBranches }} {{ branchesText }}
                            </button>
                        </div>

                        <div class="d-flex justify-content-end">

                            <button class="btn nav-link dropdown-toggle btn-gray me-2" type="button" role="button"
                                data-bs-toggle="dropdown" aria-expanded="false">
                                Add file
                            </button>
                            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                                <li>
                                    <button class="btn dropdown-item">
                                        <font-awesome-icon icon="fa-solid fa-plus" class="me-2 mt-1" /> Create new file
                                    </button>
                                </li>
                                <li>
                                    <button class="btn dropdown-item">
                                        <font-awesome-icon icon="fa-solid fa-upload" class="me-2 mt-1" /> Upload files
                                    </button>
                                </li>
                            </ul>


                            <button type="button" :class="(httpChosen) ? 'btn btn-chosen' : 'btn'"
                                @click="setHttpChosen">HTTP</button>
                            <button type="button" :class="(!httpChosen) ? 'btn btn-chosen me-2' : 'btn me-2'"
                                @click="setSshChosen">SSH</button>
                            <input v-if="httpChosen" type="text" readonly v-model="repo.http" />
                            <input v-else type="text" readonly v-model="repo.ssh" />
                        </div>
                    </div>

                    <div>
                        <RepoContent :refName="repo.chosenBranch" :key="contentKey" :displayRoot="repo.displayRoot"
                            @folderClicked="folderClicked" :foldersPath="repo.foldersPath" @returnToParent="returnToParent"
                            :branch="repo.chosenBranch" />
                    </div>
                </div>


                <div class="w-25 ms-4">
                    <div class="d-flex flex-column">
                        <span class="bolder mt-1">About</span>
                        <span v-if="repo.description" class="mt-3">{{ repo.description }}</span>
                        <span v-else class="mt-3"><i>No description provided</i></span>
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

export default {
    name: 'ViewRepo',

    components: {
        RepoContent,
        RepoNavbar,
        NotFoundPage
    },

    mounted() {
        RepositoryService.get(this.$route.params.username, this.$route.params.repoName).then(res => {
            this.repo.name = res.data.name;
            this.repo.description = res.data.description;
            this.repo.accessModifier = res.data.access_modifier;
            this.repo.http = res.data.http;
            this.repo.ssh = res.data.ssh;
            this.repo.defaultBranch = res.data.default_branch;

            this.repo.chosenBranch = res.data.default_branch;
            if (this.$route.query.chosen) {
                this.repo.chosenBranch = this.$route.query.chosen;
            }

            for (let b of res.data.branches) {
                this.repo.branches.push({ 'name': b });
            }
            this.allowed = true
            this.forceRerender();
        }).catch(err => {
            console.log(err);
            this.allowed = false;
        });

        RepositoryService.getOwner(this.$route.params.username).then(res => {
            this.owner.email = res.data.user.email;
            this.owner.firstName = res.data.user.first_name;
            this.owner.lastName = res.data.user.last_name;
            this.owner.avatar = res.data.avatar;
        }).catch(err => {
            console.log(err);
        })
    },

    data() {
        return {
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
                foldersPath: ''
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
        },

        selectedBranchChanged(branchName) {
            this.repo.chosenBranch = branchName;
            this.forceRerender();
        },

        folderClicked(data) {
            this.repo.foldersPath = this.repo.foldersPath.concat(data["name"] + "/")
            this.repo.displayRoot = "false";
            this.forceRerender();
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
        }
    },

    computed: {
        numBranches() {
            return this.repo.branches.length;
        },

        branchesText() {
            return this.repo.branches.length > 1 ? "Branches" : "Branch";
        }
    }
}

</script>

<style scoped>
.avatar {
    height: 27px;
    border-radius: 50%;
}

.badge {
    margin-top: 13px;
    border: 2px solid #dce1e6;
    color: #9ea2a7;
    background-color: white;
}

.repo-name {
    font-weight: 600;
    margin-top: 11px;
    font-size: large;
}

.btn-right {
    border: 1px solid #d6d9dd;
    background-color: #f7f8fa;
    color: #4d5256;
    height: 32px;
    width: 100px;
    margin-top: 25px;
    font-size: small;
}

input {
    min-width: 320px;
    height: 30px;
    margin-top: 10px;
    background-color: #f7f8fa;
    border: 1px solid #adafb1;
    border-radius: 5px;
    font-size: small;
}

.bolder {
    font-weight: 600;
}

.btn-chosen {
    border-bottom: 2px solid #fe8c72;
    border-radius: 0%;
}

.btn-chosen:hover {
    border-bottom: 2px solid #fe8c72;
}

.btn-gray,
.btn-gray:hover {
    border: 1px solid #d6d9dd;
    background-color: #f7f8fa;
    color: #353636;
    height: 37px;
    min-width: 120px;
    max-width: 200px;
    margin-top: 10px;
}

.search {
    height: 35px;
}
</style>