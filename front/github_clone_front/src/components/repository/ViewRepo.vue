<template>
    <div>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container-fluid">
                <div class="collapse navbar-collapse">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item mx-2">
                            <button class="nav-link active">
                                <div class="d-flex justify-content-start">
                                    <font-awesome-icon icon="fa-solid fa-code" class="me-2 mt-1" />
                                    Code
                                </div>
                            </button>
                        </li>
                        <li class="nav-item mx-2">
                            <button class="nav-link">
                                <div class="d-flex justify-content-start">
                                    <font-awesome-icon icon="fa-regular fa-circle-dot" class="me-2 mt-1" />
                                    Issues
                                </div>
                            </button>
                        </li>
                        <li class="nav-item mx-2">
                            <button class="nav-link">
                                <div class="d-flex justify-content-start">
                                    <font-awesome-icon icon="fa-solid fa-code-pull-request" class="me-2 mt-1" />
                                    Pull requests
                                </div>
                            </button>
                        </li>
                        <li class="nav-item mx-2">
                            <button class="nav-link">
                                <div class="d-flex justify-content-start">
                                    <font-awesome-icon icon="fa-solid fa-gear" class="me-2 mt-1" />
                                    Settings
                                </div>
                            </button>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>

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

        <div class="d-flex justify-content-start mx-3">
            <div class="d-flex justify-content-between w-75">
                <div class="d-flex justify-content-start">
                    <button type="button" class="btn">
                        main
                    </button>
                    <button type="button" class="btn">
                        1 Branch
                    </button>
                </div>

                <div class="d-flex justify-content-end">
                    <button type="button" class="btn">Add file</button>
                    <button type="button" :class = "(httpChosen)?'btn btn-chosen':'btn'" @click="setHttpChosen">HTTP</button>
                    <button type="button" :class = "(!httpChosen)?'btn btn-chosen me-2':'btn me-2'" @click="setSshChosen">SSH</button>
                    <input v-if="httpChosen" type="text" readonly v-model="repo.http" />
                    <input v-else type="text" readonly v-model="repo.ssh" />
                </div>
            </div>

            <div class="w-25 ms-4">
                <div class="d-flex flex-column">
                    <span class="bolder">About</span>
                    <span>{{ repo.description }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import RepositoryService from '@/services/RepositoryService';

export default {
    name: 'ViewRepo',

    mounted() {
        RepositoryService.get(this.$route.params.username, this.$route.params.repoName).then(res => {
            this.repo.name = res.data.name;
            this.repo.description = res.data.description;
            this.repo.accessModifier = res.data.access_modifier;
        }).catch(err => {
            console.log(err);
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
                default_branch: '',
                http: 'http://localhost:3000',
                ssh: 'ssh-something'
            },

            owner: {
                firstName: '',
                lastName: '',
                avatar: '',
                email: ''
            },

            httpChosen: true
        }
    },

    methods: {
        setHttpChosen() {
            this.httpChosen = true;
        },

        setSshChosen() {
            this.httpChosen = false;
        }
    }
}

</script>

<style scoped>
.nav-link {
    color: black;
}

.active {
    border-bottom: 2px solid #fe8c72;
}

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
</style>