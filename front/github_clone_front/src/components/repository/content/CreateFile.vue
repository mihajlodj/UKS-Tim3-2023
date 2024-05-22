<template>
    <div class="background is-fullheight min-vh-100">
        <RepoNavbar />

        <LoadingPage v-if="!loaded" />

        <PathDisplay :creating="true" ref="pathDisplay" />
        <EditingHeader />
        <TextFileEdit />
        <div class="d-flex justify-content-center">
            <div class="d-flex justify-content-end mt-2 commit-cancel">
                <button type="button" class="btn-cancel" @click="cancel">Cancel changes</button>
                <button type="button" class="btn-commit" data-bs-toggle="modal" data-bs-target="#commitModal">
                    Commit changes...
                </button>
            </div>
        </div>

        <div class="modal" id="commitModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Commit changes</h5>
                    </div>
                    <div class="modal-body">
                        <div class="d-flex flex-column">
                            <label class="mb-1">Commit message</label>
                            <input type="text" v-model="commitMsg" />
                        </div>

                        <div class="d-flex flex-column mt-3">
                            <label class="mb-1">Extended description</label>
                            <textarea placeholder="Add an optional extended description"
                                v-model="additionalText"></textarea>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-cancel" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-commit" data-bs-dismiss="modal" @click="commitChanges">
                            Commit changes
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import RepoNavbar from '../RepoNavbar.vue';
import PathDisplay from './PathDisplay.vue';
import EditingHeader from './text/EditingHeader.vue';
import TextFileEdit from './text/TextFileEdit.vue';
import RepositoryService from '@/services/RepositoryService';
import LoadingPage from '@/components/util/LoadingPage.vue';

export default {
    name: 'CreateFile',

    components: {
        RepoNavbar,
        PathDisplay,
        EditingHeader,
        TextFileEdit,
        LoadingPage
    },

    data() {
        return {
            content: "",
            commitMsg: "",
            additionalText: "",
            loaded: true
        }
    },

    methods: {
        cancel() {
            this.reset();
            this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}`);
        },

        commitChanges() {
            this.loaded = false;
            this.content = localStorage.getItem("newContent");
            let data = {
                "message": this.commitMsg,
                "branch": this.$route.params.branchName,
                "content": this.content,
                "additional_text": this.additionalText
            }
            let path = this.$refs.pathDisplay.getFullPath();
            RepositoryService.createFile(this.$route.params.username, this.$route.params.repoName, path, data).then(res => {
                console.log(res);
                this.reset();
                this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}`);
                this.loaded = true;
            }).catch(err => {
                console.log(err);
                this.loaded = true;
            });
        },

        reset() {
            this.content = "";
            this.commitMsg = "";
            this.additionalText = "";
            localStorage.removeItem("newContent");
        }
    }
}
</script>

<style scoped>
.background {
    background-color: #22272d;
}

.commit-cancel {
    width: 80%;
}

.btn-commit,
.btn-commit:hover {
    background-color: #347d38;
    color: white;
    border-radius: 5px;
    padding: 7px 15px;
    border: none;
}

.btn-cancel,
.btn-cancel:hover {
    background-color: #373e48;
    color: white;
    border-radius: 5px;
    padding: 7px 15px;
    margin-right: 5px;
    border: none;
}

textarea {
    resize: none;
    background-color: #1c2127;
    color: #adbbc8;
    height: 150px;
    border: 1px solid #adbbc8;
    border-radius: 5px;
    padding: 10px;
}

input {
    background-color: #1c2127;
    color: #adbbc8;
    border: 1px solid #adbbc8;
    border-radius: 5px;
    padding: 3px 10px;
}

.modal-content {
    background-color: #2c333b;
    color: #adbbc8;
    border: 1px solid #adbbc8;
}
</style>
