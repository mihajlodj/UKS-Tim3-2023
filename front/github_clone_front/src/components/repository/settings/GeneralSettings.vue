<template>
    <div class="mt-4">
        <div class="container">
            <h3>General</h3>
            <hr>

            <div class="d-flex flex-column mb-3">
                <label class="bold mb-2">Repository name</label>
                <input type="text" class="repo-name ps-2" v-model="newName" @input="validate" />
                <div class="d-flex justify-content-start">
                    <font-awesome-icon v-if="!isValidName" icon="fa-solid fa-triangle-exclamation" class="me-2 mt-1" />
                    <label v-if="!isValidName" class="w-50 warn">Name must not be empty and can only contain alphanumerics,
                        dashes ( - ) and underscores ( _ )</label>
                </div>
            </div>

            <div class="d-flex flex-column">
                <label class="bold mb-2">Description <span class="sub smaller">(optional)</span></label>
                <input type="text" class="w-100 ps-2" v-model="newDescription" />
            </div>
            <div class="d-flex justify-content-end">
                <button type="button" class="btn btn-save mt-3 me-2" @click="saveGeneralData"
                    :disabled="newName == oldName && newDescription == oldDescription || !isValidName">Save changes</button>
                <button type="button" class="btn btn-cancel mt-3" @click="cancelGeneralData"
                    :disabled="newName == oldName && newDescription == oldDescription">Cancel</button>
            </div>


            <h3 class="mt-4">Default branch</h3>
            <hr>
            <div class="d-flex justify-content-start">
                <select class="form-select" v-model="selectedBranch" style="background-color: #2c333b;">
                    <option v-for="b in repoBranches" :key="b.name">{{ b.name }}</option>
                </select>
            </div>

            <div class="d-flex justify-content-end mt-2">
                <button type="button" class="btn btn-save mt-3 me-2" @click="saveBranchData"
                    :disabled="selectedBranch == oldBranchName">Save changes</button>
                <button type="button" class="btn btn-cancel mt-3" @click="cancelBranchData"
                    :disabled="selectedBranch == oldBranchName">Cancel</button>
            </div>
        </div>
    </div>
</template>

<script>
import RepositoryService from '@/services/RepositoryService'
import { toast } from 'vue3-toastify';

export default {
    name: 'GeneralSettings',

    props: ['name', 'description', 'branchName', 'branches'],

    mounted() {
        this.oldName = this.name;
        this.newName = this.name;
        this.oldBranchName = this.branchName;
        this.oldDescription = this.description;
        this.newDescription = this.description;
        this.repoBranches = this.branches;
        this.selectedBranch = this.branchName;
    },

    data() {
        return {
            isValidName: true,
            oldName: '',
            newName: '',
            oldBranchName: '',
            oldDescription: '',
            newDescription: '',
            repoBranches: [],
            selectedBranch: ''
        }
    },

    methods: {
        validate() {
            const regexPattern = /^[a-zA-Z][\w-]*$/;
            this.isValidName = (this.newName !== "" && regexPattern.test(this.newName));
        },

        cancelBranchData() {
            this.selectedBranch = this.oldBranchName;
        },

        saveBranchData() {
            let changedName = this.selectedBranch;

            RepositoryService.update(this.$route.params.username, { "default_branch_name": changedName }, this.oldName).then(res => {
                console.log(res.data);
                this.oldBranchName = changedName;
                toast("Changes saved!", {
                    autoClose: 500,
                    type: 'success',
                    position: toast.POSITION.BOTTOM_RIGHT
                });
            }).catch(err => {
                console.log(err);
            });
        },

        cancelGeneralData() {
            this.newName = this.oldName;
            this.newDescription = this.oldDescription;
        },

        saveGeneralData() {
            RepositoryService.update(this.$route.params.username, {
                "description": this.newDescription,
                "name": this.newName
            }, this.oldName).then(res => {
                let repoName = res.data.name;
                let username = this.$route.params.username;
                this.oldDescription = this.newDescription;
                this.oldName = this.newName;
                this.$router.push(`/settings/${username}/${repoName}`);
                toast("Changes saved!", {
                    autoClose: 500,
                    type: 'success',
                    position: toast.POSITION.BOTTOM_RIGHT
                });
            }).catch(err => {
                console.log(err);
            });
        }
    }
}

</script>

<style scoped>
.repo-name {
    width: 50%;
    min-width: 250px;
    max-width: 350px;
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

input, select {
    border-radius: 5px;
    border: 1px solid #787c80;
    color: #c5d1df;
    background-color: #2c333b;
    height: 40px;
}

.sub {
    color: #88929d;
}

.bold {
    font-weight: 600;
}

.repo-name {
    width: 50%;
    min-width: 250px;
    max-width: 350px;
}

.smaller {
    font-size: small;
    color: #656e77;
}

.branch-name,
select {
    width: 50%;
}

.btn-save,
.btn-save:hover,
.btn-save:disabled {
    background-color: #20883d;
    color: white;
    height: 40px;
}


.btn-cancel,
.btn-cancel:hover,
.btn-cancel:disabled {
    background-color: #f7f8fa;
    border: 1px solid #d0d7df;
    height: 40px;
}

.fa-pen,
.fa-arrow-right-arrow-left {
    height: 15px;
    padding-bottom: 4px;
    margin-left: 7px;
}

select {
    height: 32px;
    margin-top: 8px;
    padding-top: 2px;
    background-color: #f7f8fa;
}

.container {
    width: 50%;
    min-width: 700px;
    max-width: 850px;
}

h3, label {
    color: #c5d1df
}

hr {
    color: #b9c3cf;
}
</style>