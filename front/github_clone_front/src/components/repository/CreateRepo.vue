<template>
    <div>
        <div class="container w-50 py-5">
            <h3 class="mb-3">Create a new repository</h3>
            <h6 class="sub">A repository contains all project files, including the revision history</h6>
            <hr>
            <h6><i>Required fields are marked with an asterisk (*)</i></h6>
            <hr>

            <div class="d-flex flex-column mb-3">
                <label class="bold mb-2">Repository name *</label>
                <input type="text" class="repo-name" v-model="name" @input="validate" />
                <div class="d-flex justify-content-start">
                    <font-awesome-icon v-if="!isValidName" icon="fa-solid fa-triangle-exclamation" class="me-2 mt-1" />
                    <label v-if="!isValidName" class="w-50 warn">Name must not be empty and can only contain alphanumerics,
                        dashes ( - ) and underscores ( _ )</label>
                </div>
            </div>

            <div class="d-flex flex-column">
                <label class="bold mb-2">Dafault branch name <span class="sub smaller">(optional)</span></label>
                <input type="text" class="w-50 mb-3" v-model="defaultBranchName" @input="validateBranchName" />
                <div class="d-flex justify-content-start">
                    <font-awesome-icon v-if="!isValidBranchName" icon="fa-solid fa-triangle-exclamation" class="me-2 mt-1" />
                    <label v-if="!isValidBranchName" class="w-50 warn">Branch name can only contain alphanumerics,
                        dashes ( - ) and underscores ( _ )</label>
                </div>
            </div>

            <div class="d-flex flex-column">
                <label class="bold mb-2">Description <span class="sub smaller">(optional)</span></label>
                <input type="text" class="w-100" v-model="description" />
            </div>

            <hr>
            <div class="d-flex justify-content-start">
                <input class="form-check-input mt-3" type="radio" name="access-modifier" id="public-radio"
                    @input="publicChecked" checked>
                <font-awesome-icon icon="fa-solid fa-book-bookmark" class="ms-4 me-3 mt-2" />
                <div class="d-flex flex-column">
                    <span class="bold">Public</span>
                    <span class="smaller">Anyone on the internet can see this repository. You choose who can commit.</span>
                </div>
            </div>
            <div class="d-flex justify-content-start mt-3">
                <input class="form-check-input mt-3" type="radio" name="access-modifier" id="private-radio"
                    @input="privateChecked">
                <font-awesome-icon icon="fa-solid fa-lock" class="ms-4 me-3 mt-2" />
                <div class="d-flex flex-column">
                    <span class="bold">Private</span>
                    <span class="smaller">You choose who can see and commit to this repository.</span>
                </div>
            </div>

            <hr>
            <div class="d-flex justify-content-start">
                <font-awesome-icon icon="fa-solid fa-circle-info" class="me-2" style="margin-top: 6px; color: #7a8188" />
                <p class="sub">You are creating a {{ modifier }} repository in your personal account.</p>
            </div>

            <hr>
            <div class="d-flex justify-content-end">
                <button class="btn" @click="submit">Create repository</button>
            </div>
        </div>
    </div>
</template>

<script>
import RepositoryService from '@/services/RepositoryService';
import { toast } from 'vue3-toastify';

export default {
    name: 'CreateRepo',

    data() {
        return {
            name: '',
            description: '',
            isPublic: true,
            defaultBranchName: '',
            isValidName: true,
            isValidBranchName: true
        }
    },

    methods: {
        publicChecked() {
            this.isPublic = true;
        },

        privateChecked() {
            this.isPublic = false;
        },

        validate() {
            const regexPattern = /^[a-zA-Z][\w-]*$/;
            this.isValidName = (this.name !== "" && regexPattern.test(this.name));
        },

        validateBranchName() {
            const regexPattern = /^[a-zA-Z][\w-]*$/;
            this.isValidBranchName = (this.defaultBranchName === "" || regexPattern.test(this.defaultBranchName));
        },

        submit() {
            this.validate();
            this.validateBranchName();
            /* eslint-disable */
            if (this.isValidName && this.isValidBranchName) {
                const mod = this.isPublic ? 'Public' : 'Private';
                RepositoryService.create({
                    name: this.name,
                    description: this.description,
                    default_branch_name: this.defaultBranchName,
                    access_modifier: mod
                }).then(_res => {
                    this.resetFields();
                    toast("Repository created!", {
                        autoClose: 1000,
                        type: 'success',
                        position: toast.POSITION.BOTTOM_RIGHT
                    });
                }).catch(err => {
                    console.log(err.response.data.name[0]);
                    if (err.response.data.name[0] === "This field must be unique.") {
                        toast("Repository name already exists!", {
                            autoClose: 1000,
                            type: 'error',
                            position: toast.POSITION.BOTTOM_RIGHT
                        });
                    } else {
                        toast("Something went wrong!", {
                            autoClose: 1000,
                            type: 'error',
                            position: toast.POSITION.BOTTOM_RIGHT
                        });
                    }
                })
            }
        },

        resetFields() {
            this.name = '';
            this.defaultBranchName = '';
            this.description = '';
            this.isValidName = true;
        }
    },

    computed: {
        modifier() {
            return this.isPublic ? 'public' : 'private';
        }
    }
}

</script>

<style scoped>
button {
    background-color: #20883d;
    color: white;
    font-size: large;
}

button:hover {
    background-color: #20883d;
    color: white;
}

.container {
    max-width: 900px;
}

h3 {
    font-weight: 600;
}

.sub {
    color: #656e77;
}

.bold {
    font-weight: 600;
    font-size: large;
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

.fa-book-bookmark,
.fa-lock {
    height: 25px;
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
</style>