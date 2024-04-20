<template>
    <div class="bg is-fullheight min-vh-100 w-100">
        <RepoNavbar starting="settings"/>
        <div class="d-flex justify-content-center mt-5">
            <div class="contain">
                <h3>
                    Transfer repository: {{ $route.params.username }}/{{ $route.params.repoName }}
                </h3>
                <h6 class="muted">Transfer this repository to another user</h6>

                <hr class="muted"/>

                <h6 class="bright bold">
                    New owner
                </h6>

                <div v-if="selectedCollaborator === null" class="d-flex justify-content-center my-3">
                    <input type="text" class="bright" name="search" placeholder="Search by username or email" 
                        v-model="searchTerm" @input="searchTermChanged" />
                </div>

                <div v-else>
                    <div class="d-flex justify-content-between collab-display p-2">
                        <div class="d-flex justify-content-start">
                            <img class="collab-avatar" :src="selectedCollaborator.avatar" />
                            <span class="bright ms-2 mt-1">{{ selectedCollaborator.username }}</span>
                        </div>

                        <button type="button" class="btn-remove-collab" @click="removeCollaboratorToTransfer">
                            <font-awesome-icon icon="fa-solid fa-xmark"></font-awesome-icon>
                        </button>
                    </div>
                </div>

                <div v-if="filteredCollaborators.length > 0 && selectedCollaborator == null" class="collabs-list">
                    <div v-for="(dev, i) in filteredCollaborators" :key="dev.username">
                        <button type="button" class="btn-select-dev w-100" @click="selectCollaborator(i)">
                            <div class="d-flex justify-content-start">
                                <img class="collab-avatar mt-1" :src="dev.avatar" />
                                <div class="d-flex flex-column ms-2 mt-2">
                                    <span class="collab-username d-flex justify-content-start">{{ dev.username }}</span>
                                </div>
                            </div>
                        </button>
                    </div>
                </div>

                <hr class="muted"/>
                <h6 class="bright bold">
                    Type {{ $route.params.username }}/{{ $route.params.repoName }} to confirm.
                </h6>
                <input v-model="confirmation" class="bright" />
                <div class="w-100 d-flex justify-content-end">
                    <button type="button" class="btn-transfer mt-3" :disabled="!canTransfer()">I understand, I transfer this repository.</button>
                </div>
            </div> 
        </div>
    </div>
</template>

<script>
import RepoNavbar from '../RepoNavbar.vue';
import RepositoryService from '@/services/RepositoryService';

export default {
    name: "TransferOwnership",
    components: {
        RepoNavbar
    },

    mounted() {
        RepositoryService.getCollaborators(this.$route.params.username, this.$route.params.repoName).then(res => {
            this.collaborators = res.data;
            console.log(res.data);
            this.filteredCollaborators = [];
        }).catch(err => {
            console.log(err);
        });
    },

    data() {
        return {
            confirmation: "",
            collaborators: [],
            filteredCollaborators: [],
            selectedCollaborator: null,
            searchTerm: ""
        }
    },

    methods: {
        transfer() {
            if (this.canTransfer()) {
                console.log("transfer");
            }
        },

        searchTermChanged() {
            if (this.searchTerm !== "" && this.searchTerm !== null) {
                let term = this.searchTerm.toLowerCase();
                this.filteredCollaborators = this.collaborators.filter(dev =>
                    dev.username.toLowerCase().includes(term) || dev.email.toLowerCase().includes(term)
                );
            } else {
                this.filteredCollaborators = [];
            }
        },

        selectCollaborator(i) {
            this.selectedCollaborator = this.filteredCollaborators[i];
        },

        removeCollaboratorToTransfer() {
            this.selectedCollaborator = null;
            this.searchTerm = "";
            this.searchTermChanged();
        },

        canTransfer() {
            return this.selectedCollaborator !== null && this.confirmation === `${this.$route.params.username}/${this.$route.params.repoName}`;
        }
    }
}
</script>

<style scoped>
.bg {
    background-color: #22272d;
}

h3 {
    color: #c5d1df;
    font-weight: 600;
}

.contain {
    width: 50%;
    min-width: 700px;
    max-width: 850px;
}

.muted {
    color: #7f909f
}

.bright {
    color: #c5d1df;
}

.bold {
    font-weight: 600;
}

input {
    width: 100%;
    height: 35px;
    border-radius: 7px;
    border: 1px solid #7f909f;
    padding-left: 3px;
    background-color: #22272d;
    margin-top: 3px;
}

.btn-transfer {
    color: #d6514b;
    background-color: #373e48;
    border: 1px solid #7f909f;
    border-radius: 7px;
    padding: 5px 17px;
}

.btn-transfer:hover {
    background-color: #ac3731;
    color: #c5d1df;
    cursor: pointer;
}

img {
    height: 35px;
    border-radius: 50%;
}

.btn-select-dev {
    background-color: #2c333b;
    border: none;
    padding: 10px 15px;
    color: #c5d1df;
}

.btn-select-dev:hover {
    background-color: #3d4854;
}

.btn-remove-collab {
    background: none;
    color: #488ae7;
    font-weight: 550;
    border: none;
}

.collab-display {
    background-color: #253141;
    border: 1px solid #2c4a72;
    border-radius: 7px;
}
</style>