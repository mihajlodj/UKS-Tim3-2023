<template>
    <div class="bg min-vh-100 is-fullheight">
        <RepoNavbar />

        <div class="container w-75 mt-4">
            <div class="d-flex justify-content-between">
                <h3 class="bright">Branches</h3>
                <button type="button" class="btn btn-create" data-bs-toggle="modal" data-bs-target="#exampleModal">
                    New branch
                </button>
            </div>

            <ul class="nav-tabs2 mt-3">
                <li class="nav-item2">
                    <button :class="activeAll ? 'nav-link2 active-link' : 'nav-link2'" id="tab-all" @click="setActiveAll">All</button>
                </li>
                <li class="nav-item2">
                    <button :class="!activeAll ? 'nav-link2 active-link' : 'nav-link2'" id="tab-yours" @click="setActiveYours">Yours</button>
                </li>
            </ul>

            <BranchesTable :targetList="targetList" @branchDeleted="branchDeleted" />
        </div>

        <div class="modal" id="exampleModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content" style="background-color: #2c333b;">
                    <div class="modal-header">
                        <h5 class="modal-title bright">Create a branch</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="container">
                            <div class="d-flex flex-column">
                                <label class="mb-1 bright">New branch name</label>
                                <input type="text" v-model="newBranchName" @input="validateBranchName" style="background-color: #1c2127; height: 35px; border-radius: 5px; padding-left: 7px;" />
                                <div class="d-flex justify-content-start">
                                    <font-awesome-icon v-if="!isValidBranchName" icon="fa-solid fa-triangle-exclamation"
                                        class="me-2 mt-1" />
                                    <label v-if="!isValidBranchName" class="warn">Branch name can only contain
                                        alphanumerics, dashes ( - ) and underscores ( _ )
                                    </label>
                                </div>
                            </div>
                            <div v-if="eligible.length > 0">
                                <label class="mt-3 mb-1 bright">Source</label>
                                <button class="btn nav-link dropdown-toggle btn-gray" type="button" id="navbarDropdown"
                                    role="button" data-bs-toggle="dropdown" aria-expanded="false"  style="background-color: #c5d1df;">
                                    <font-awesome-icon icon="fa-solid fa-code-branch" class="me-2 mt-1" /> {{ chosenSource
                                    }}
                                </button>
                                <ul class="dropdown-menu" aria-labelledby="navbarDropdown" style="background-color: #c5d1df;">
                                    <li v-for="b in eligible" :key="b.name">
                                        <button class="btn dropdown-item" @click="changeChosenSource(b.name)" style="background-color: #c5d1df;">
                                            {{ b.name }}
                                        </button>
                                    </li>
                                </ul>
                            </div>
                            <div v-else>
                                Cannot create a branch from an empty branch
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-gray" @click="cancelBranchInput"
                            data-bs-dismiss="modal"  style="background-color: #c5d1df;">Cancel</button>
                        <button type="button" class="btn btn-create" @click="createBranch" data-bs-dismiss="modal" :disabled="eligible.length === 0">
                            Create new branch
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import RepoNavbar from '@/components/repository/RepoNavbar.vue'
import BranchService from '@/services/BranchService'
import BranchesTable from './BranchesTable.vue'
import { toast } from 'vue3-toastify';

export default {
    name: 'BranchesView',
    components: {
        RepoNavbar,
        BranchesTable
    },

    mounted() {
        BranchService.getAllBranches(this.$route.params.username, this.$route.params.repoName).then(res => {
            for (let item of res.data) {
                this.branchData.push({
                    "name": item.name,
                    "updatedUsername": item.updated_username,
                    "updatedAvatar": item.updated_avatar,
                    "updatedTimestamp": item.updated_timestamp,
                    "prId": item.pr_id,
                    "prStatus": item.pr_status,
                    "createdBy": item.created_by
                });
            }
            this.eligible = this.branchData.filter(x => x.updatedUsername !== undefined);
            if (this.eligible.length > 0) {
                this.chosenSource = this.eligible[0].name;
            }
            this.createdByUser = this.branchData.filter(item => item.createdBy === this.$route.params.username);
            this.targetList = this.branchData;
        }).catch(err => {
            console.log(err);
        });
    },

    data() {
        return {
            selectedTab: 'all',
            branchData: [],
            createdByUser: [],
            activeAll: true,
            targetList: [],
            chosenSource: '',
            newBranchName: '',
            isValidBranchName: true,
            eligible: []
        }
    },

    methods: {
        setActiveAll() {
            this.activeAll = true;
            this.targetList = this.branchData;
        },

        setActiveYours() {
            this.activeAll = false;
            this.targetList = this.createdByUser;
        },

        changeChosenSource(name) {
            this.chosenSource = name;
        },

        validateBranchName() {
            const regexPattern = /^[a-zA-Z][\w-]*$/;
            this.isValidBranchName = (this.newBranchName !== "" && regexPattern.test(this.newBranchName));
        },

        cancelBranchInput() {
            this.newBranchName = "";
            this.isValidBranchName = true;
        },

        branchDeleted(data) {
            const branchName = data.name;
            this.targetList = this.targetList.filter(item => item.name !== branchName);
            this.branchData = this.branchData.filter(item => item.name !== branchName);
            this.createdByUser = this.createdByUser.filter(item => item.name !== branchName);
            this.eligible = this.eligible.filter(item => item.name !== branchName);
        },

        /* eslint-disable */
        createBranch() {
            BranchService.createBranch(this.$route.params.username, localStorage.getItem("username"), this.$route.params.repoName, {
                "name": this.newBranchName,
                "parent": this.chosenSource
            }).then(_res => {
                let chosenSourceObj = this.eligible.find(x => x.name === this.chosenSource);
                
                let newBranch = {
                    "name": this.newBranchName,
                    "createdBy": this.$route.params.username,
                    "updatedUsername": chosenSourceObj.updatedUsername,
                    "updatedAvatar": chosenSourceObj.updatedAvatar,
                    "updatedTimestamp": chosenSourceObj.updatedTimestamp
                }
                this.branchData.push(newBranch);
                this.createdByUser.push(newBranch);
                this.eligible.push(newBranch);
                this.newBranchName = "";
                this.isValidBranchName = true;
                this.chosenSource = this.eligible[0].name;
                
            }).catch(err => {
                console.log(err);
                if (err.response.data.detail === "duplicate branch name") {
                    toast("Branch already exists!", {
                        autoClose: 1000,
                        type: 'error',
                        position: toast.POSITION.BOTTOM_RIGHT
                    });
                }
                else {
                    toast("Unable to create branch!", {
                        autoClose: 1000,
                        type: 'error',
                        position: toast.POSITION.BOTTOM_RIGHT
                    });
                }

            })
        }
    },
}
</script>

<style scoped>
.bg {
    background-color: #22272d;
}

.btn-create,
.btn-create:hover {
    color: white;
    background-color: #20883d;
    height: 90%;
}

.active-link {
    border-top: 1px solid #82878d !important;
    border-left: 1px solid #82878d !important;
    border-right: 1px solid #82878d !important;
}

.btn-gray,
.btn-gray:hover {
    border: 1px solid #d6d9dd;
    background-color: #f7f8fa;
    color: #353636;
    height: 37px;
    min-width: 120px;
    max-width: 200px;
}

.warn {
    font-size: smaller;
    color: #d32d36;
    font-weight: 600;
    max-width: 350px;
}

.fa-triangle-exclamation {
    color: #d32d36;
    height: 15px;
}

.bright {
    color: #c5d1df;
}

.nav-tabs2 {
  list-style-type: none;
  padding: 0;
  margin: 0;
  display: flex;
  border-bottom: 1px solid #82878d;
  margin-top: 1rem;
}

.nav-link2 {
  background: none;
  border: none;
  padding: 0.5rem 1rem;
  cursor: pointer;
  text-decoration: none;
  color: #c5d1df;
  border: 1px solid transparent;
  border-radius: 0.25rem 0.25rem 0 0;
}

</style>