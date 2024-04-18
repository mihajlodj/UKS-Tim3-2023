<template>
    <div class="mt-4 container">
        <h3>Manage access</h3>

        <div v-if="!collaboratorsExist" class="no-collaborators d-flex flex-column mt-3">
            <div class="d-flex justify-content-center align-items-center h-31 mt-4">
                <font-awesome-icon icon="fa-solid fa-user-lock"></font-awesome-icon>
            </div>

            <div class="d-flex justify-content-center align-items-center h-31">
                <h4>You haven't invited any collaborators yet</h4>
            </div>

            <div class="d-flex justify-content-center align-items-center h-31 mb-4" data-bs-toggle="modal"
                data-bs-target="#add-people-modal">
                <button type="button" class="btn-add-people">
                    Add people
                </button>
            </div>
        </div>

        <div v-else>
            <div class="d-flex justify-content-end" data-bs-toggle="modal" data-bs-target="#add-people-modal">
                <button type="button" class="btn-add-people mb-1">Add people</button>
            </div>
            <div class="d-flex justify-content-between p-3" style="border: 1px solid #72808d;">
                <input v-model="existingCollaboratorsSearchTerm" placeholder="Find a collaborator..."
                    @input="existingCollaboratorsSearchTermChanged" />

                <div class="d-flex justify-content-start ms-4 me-1">
                    <button class="btn nav-link dropdown-toggle" type="button" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false" style="color: #717f8c;">
                        <span>Type</span>
                    </button>
                    <ul class="dropdown-menu" id="collab-type-list" aria-labelledby="navbarDropdown" style="background-color: #2c333b">
                        <li>
                            <button class="dropdown-item" @click="displayAll" style="color: #a5b2bf;">All</button>
                        </li>
                        <li>
                            <button class="dropdown-item" @click="displayCollaborators"
                                style="color: #a5b2bf;">Collaborators</button>
                        </li>
                        <li>
                            <button class="dropdown-item" @click="displayPending" style="color: #a5b2bf;">Pending
                                invitations</button>
                        </li>
                    </ul>
                </div>
            </div>

            <div>
                <div v-for="collaborator in filteredExistingCollaborators" :key="collaborator.username">
                    <CollaboratorDisplay :collaborator="collaborator" @remove="deleteExistingCollaborator" />
                </div>
            </div>
        </div>

        <div class="modal fade" id="add-people-modal" tabindex="-1" aria-labelledby="add-people-modal-lbl"
            aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="d-flex justify-content-center">
                            <font-awesome-icon icon="fa-solid fa-book-bookmark"></font-awesome-icon>
                        </div>

                        <div class="d-flex justify-content-center my-3">
                            <h5>
                                Add a collaborator to <span class="repo-name">{{ $route.params.repoName }}</span>
                            </h5>
                        </div>

                        <div v-if="selectedCollaborator === null" class="d-flex justify-content-center my-3">
                            <input type="text" name="search" placeholder="Search by username or email"
                                v-model="searchTerm" @input="searchTermChanged" />
                        </div>

                        <div v-else>
                            <div class="d-flex justify-content-between collab-display p-2">
                                <div class="d-flex justify-content-start">
                                    <img class="collab-avatar" :src="selectedCollaborator.avatar" />
                                    <span class="selected-collab-username ms-2">{{ selectedCollaborator.username }}</span>
                                </div>

                                <button type="button" class="btn-remove-collab" @click="removeCollaborator">
                                    <font-awesome-icon icon="fa-solid fa-xmark"></font-awesome-icon>
                                </button>
                            </div>

                            <div class="d-flex justify-content-start mt-3">
                                <button class="btn nav-link dropdown-toggle btn-gray" type="button" id="roleChoice" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                    <span class="me-1 mb-1">{{ chosenRole }}</span>
                                </button>
                                <ul class="dropdown-menu" id="branches-list" aria-labelledby="roleChoice" style="background-color: #2c333b">
                                    <li>
                                        <button class="btn dropdown-item" @click="selectedRoleChanged('Readonly')" style="color: #a5b2bf;">
                                            Readonly
                                        </button>
                                    </li>
                                    <li>
                                        <button class="btn dropdown-item" @click="selectedRoleChanged('Developer')" style="color: #a5b2bf;">
                                            Developer
                                        </button>
                                    </li>
                                    <li>
                                        <button class="btn dropdown-item" @click="selectedRoleChanged('Maintainer')" style="color: #a5b2bf;">
                                            Maintainer
                                        </button>
                                    </li>
                                </ul>
                            </div>
                        </div>

                        <div v-if="filteredDevelopers.length > 0" class="collabs-list">
                            <div v-for="(dev, i) in filteredDevelopers" :key="dev.username">
                                <button type="button" class="btn-select-dev w-100" @click="selectCollaborator(i)">
                                    <div class="d-flex justify-content-start">
                                        <img class="collab-avatar mt-1" :src="dev.avatar" />
                                        <div class="d-flex flex-column ms-2">
                                            <span class="collab-username d-flex justify-content-start">{{ dev.username
                                                }}</span>
                                            <span class="invite-collab-text">Invite collaborator</span>
                                        </div>
                                    </div>
                                </button>
                            </div>
                        </div>

                        <div class="d-flex justify-content-center mt-4 mb-2">
                            <button type="button" class="btn-invite" :disabled="selectedCollaborator === null"
                                data-bs-dismiss="modal" @click="inviteCollaborator">
                                Invite
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import DeveloperService from '@/services/DeveloperService';
import RepositoryService from '@/services/RepositoryService';
import CollaboratorDisplay from '../CollaboratorDisplay.vue'

export default {
    name: "CollaboratorsSettings",
    components: {
        CollaboratorDisplay
    },

    mounted() {
        DeveloperService.getDevelopers(this.$route.params.repoName).then(res => {
            this.developers = res.data.filter(dev => dev.avatar !== null);
        }).catch(err => {
            console.log(err);
        });

        RepositoryService.getCollaborators(this.$route.params.username, this.$route.params.repoName).then(res => {
            this.existingCollaborators = res.data;
            this.filteredExistingCollaborators = res.data;
            this.collaboratorsExist = this.existingCollaborators.length > 0;
        }).catch(err => {
            console.log(err);
        })
    },

    data() {
        return {
            developers: [],
            filteredDevelopers: [],
            selectedCollaborator: null,
            searchTerm: "",
            existingCollaborators: [],
            filteredExistingCollaborators: [],
            collaboratorsExist: false,
            existingCollaboratorsSearchTerm: "",
            chosenType: "all",
            chosenRole: "Developer"
        }
    },

    methods: {
        searchTermChanged() {
            if (this.searchTerm !== "" && this.searchTerm !== null) {
                let term = this.searchTerm.toLowerCase();
                this.filteredDevelopers = this.developers.filter(dev =>
                    dev.username.toLowerCase().includes(term) || dev.email.toLowerCase().includes(term)
                );
            } else {
                this.filteredDevelopers = [];
            }
        },

        selectCollaborator(i) {
            this.selectedCollaborator = this.filteredDevelopers[i];
            this.filteredDevelopers = [];
            this.searchTerm = "";
        },

        removeCollaborator() {
            this.selectedCollaborator = null;
        },

        inviteCollaborator() {
            if (this.selectedCollaborator !== null) {
                RepositoryService.inviteCollaborator(this.$route.params.repoName, this.selectedCollaborator.username).then(res => {
                    this.existingCollaborators.push(res.data);
                    this.filteredExistingCollaborators = this.existingCollaborators;

                    this.developers = this.developers.filter(x => x.username !== this.selectedCollaborator.username);
                    this.filteredDevelopers = [];

                    this.existingCollaboratorsSearchTerm = "";
                    this.searchTerm = "";
                    this.selectedCollaborator = null;
                    this.collaboratorsExist = true;
                }).catch(err => {
                    console.log(err);
                });
            }
        },

        deleteExistingCollaborator(username) {
            RepositoryService.removeCollaborator(this.$route.params.username, this.$route.params.repoName, username).then(res => {
                console.log(res);
                this.existingCollaborators = this.existingCollaborators.filter(x => x.username !== username);
                this.filteredExistingCollaborators = this.filteredExistingCollaborators.filter(x => x.username !== username);
                DeveloperService.getDevelopers(this.$route.params.repoName).then(res => {
                    this.developers = res.data.filter(dev => dev.avatar !== null);
                }).catch(err => {
                    console.log(err);
                });
                if (this.existingCollaborators.length == 0) {
                    this.collaboratorsExist = false;
                }
            }).catch(err => {
                console.log(err);
            });
        },

        selectedRoleChanged(role) {
            this.chosenRole = role;
        },

        existingCollaboratorsSearchTermChanged() {
            if (this.existingCollaboratorsSearchTerm !== "" && this.existingCollaboratorsSearchTerm !== null) {
                if (this.existingCollaboratorsSearchTerm === "filter:collaborators") {
                    this.filteredExistingCollaborators = this.existingCollaborators.filter(dev => dev.role !== "Pending");
                } else if (this.existingCollaboratorsSearchTerm == "filter:pending_invitations") {
                    this.filteredExistingCollaborators = this.existingCollaborators.filter(dev => dev.role === "Pending");
                } else {
                    let term = this.existingCollaboratorsSearchTerm.toLowerCase();
                    this.filteredExistingCollaborators = this.existingCollaborators.filter(dev => dev.username.toLowerCase().includes(term));
                }
            } else {
                this.filteredExistingCollaborators = this.existingCollaborators;
            }
        },

        displayAll() {
            this.existingCollaboratorsSearchTerm = "";
            this.filteredExistingCollaborators = this.existingCollaborators;
        },

        displayCollaborators() {
            this.existingCollaboratorsSearchTerm = "filter:collaborators";
            this.filteredExistingCollaborators = this.existingCollaborators.filter(dev => dev.role !== "Pending");
        },

        displayPending() {
            this.existingCollaboratorsSearchTerm = "filter:pending_invitations";
            this.filteredExistingCollaborators = this.existingCollaborators.filter(dev => dev.role === "Pending");
        }
    }
}
</script>

<style scoped>
.no-collaborators {
    height: 250px;
    width: 100%;
    border: 1px solid #7f848b;
    border-radius: 10px;
}

.container {
    width: 50%;
    min-width: 700px;
    max-width: 850px;
}

.btn-add-people,
.btn-invite {
    background-color: #347d38;
    color: #fff;
    border-radius: 7px;
    border: none;
    padding: 5px 17px;
    height: 40px;
}

.btn-add-people:hover,
.btn-invite:hover {
    background-color: #3a843d;
}

.btn-invite {
    min-width: 100px;
}

.btn-invite:disabled {
    background-color: #385f3a;
    color: #919aac;
    border: 1px solid #919aac;
}

.fa-user-lock {
    height: 40px;
    color: #1f84f5;
}

.fa-book-bookmark {
    height: 40px;
    color: #798088;
}

.h-31 {
    height: 31%;
}

h3,
h4,
h5 {
    color: #c5d1df;
}

.repo-name {
    font-weight: 600;
}

input {
    width: 100%;
    border: 1px solid #7f848b;
    color: #b7c2cd;
    border-radius: 7px;
    background-color: #2c333b;
    padding: 5px 7px;
}

.modal-content {
    background-color: #22272d;
}

.collab-avatar {
    height: 27px;
    border-radius: 50%;
}

.btn-select-dev {
    background-color: #2c333b;
    border: none;
    padding: 10px 15px;
}

.btn-select-dev:hover {
    background-color: #3d4854;
}

.collab-username {
    color: #c5d1de;
    font-weight: 550;
    font-size: 13px;
}

.invite-collab-text {
    color: #7f868e;
    font-size: 12px;
}

.btn-remove-collab {
    background: none;
    color: #488ae7;
    font-weight: 550;
    border: none;
}

.selected-collab-username {
    color: #488ae7;
    font-weight: 600;
}

.collab-display {
    background-color: #253141;
    border: 1px solid #2c4a72;
    border-radius: 7px;
}

button.dropdown-item:hover {
    background-color: #414957 !important;
}

#roleChoice {
    color: #c5d1de;
    border: 1px solid #c5d1de;
    border-radius: 7px;
    min-width: 140px;
    padding: 7px 20px;
}
</style>