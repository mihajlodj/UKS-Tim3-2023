<template>
    <div class="bg is-fullheight min-vh-100">
        <RepoNavbar />

        <div class="container w-50 py-5">
            <h3 class="mb-2 bright">Create a new fork</h3>
            <h6 class="sub">A <i>fork</i> is a copy of a repository. Forking a repository allows you to freely experiment with changes without affecting the original project.</h6>
            <hr>
            <h6 class="bright"><i>Required fields are marked with an asterisk (*)</i></h6>
            <hr>

            <div class="d-flex flex-column mb-3">
                <label class="bold mb-2 bright">Repository name *</label>
                <input type="text" class="repo-name" v-model="name" @input="validate" />
                <div class="d-flex justify-content-start">
                    <font-awesome-icon v-if="!isValidName" icon="fa-solid fa-triangle-exclamation" class="me-2 mt-1" />
                    <label v-if="!isValidName" class="w-50 warn">Name must not be empty and can only contain alphanumerics,
                        dashes ( - ) and underscores ( _ )</label>
                </div>
            </div>

            <p class="bright">By default, forks are named the same as their upstream repository. You can customize the name to distinguish it further.</p>

            <div class="d-flex flex-column">
                <label class="bold mb-2 bright">Description <span class="sub smaller">(optional)</span></label>
                <input type="text" class="w-100" v-model="description" />
            </div>

            <hr/>

            <div class="d-flex justify-content-start info">
                <font-awesome-icon icon="fa-solid fa-circle-info" class="me-2 mt-1" style="color: #7a8188" />
                <p class="sub info">You are creating a fork in your personal account.</p>
            </div>

            <hr>
            <div class="d-flex justify-content-end">
                <button class="btn" @click="submit">Create fork</button>
            </div>
        </div>
    </div>
</template>

<script>
/* eslint-disable */
import RepositoryService from '@/services/RepositoryService';
import { toast } from 'vue3-toastify';
import RepoNavbar from './RepoNavbar.vue';

export default {
    name: 'ForkRepo',
    components: {
        RepoNavbar
    },

    data() {
        return {
            name: this.$route.params.repoName,
            description: '',
            isValidName: true
        }
    },

    methods: {
        validate() {
            const regexPattern = /^[a-zA-Z][\w-]*$/;
            this.isValidName = (this.name !== "" && regexPattern.test(this.name));
        },

        submit() {
            this.validate();
            /* eslint-disable */
            if (this.isValidName) {

                RepositoryService.fork(this.$route.params.username, this.$route.params.repoName, {
                    name: this.name,
                    description: this.description 
                }).then(res => {
                    console.log(res);
                    this.$router.push(`/view/${localStorage.username}/${this.name}`);
                }).catch(err => {
                    console.log(err);
                    if (err.response.data.name[0] === "Repository with this name already exists for this owner.") {
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
                });
            }
        },

        resetFields() {
            this.name = '';
            this.description = '';
            this.isValidName = true;
        }
    }
}

</script>

<style scoped>
.bg {
    background-color: #22272d;
}

button {
    background-color: #347d38;
    color: white;
}

button:hover {
    background-color: #347d38;
    color: white;
}

.container {
    max-width: 900px;
}

h3 {
    font-weight: 600;
}

.bright {
    color: #c5d1df;
}

.sub {
    color: #828d98;
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

.info {
    margin-top: 0;
    margin-bottom: 0;
}

hr {
    color: #a6b3c1;
}

input {
    background-color: #22272d;
    border: 1px solid #656c74;
    border-radius: 7px;
    color: #c5d1df;
    height: 35px;
    padding-left: 10px;
}
</style>