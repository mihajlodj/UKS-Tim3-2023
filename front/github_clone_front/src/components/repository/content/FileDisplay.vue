<template>
    <div>
        <TextFile v-if="kind === 'text'" @deleteFile="deleteFile" />
        <NonTextDisplay v-if="kind === 'non-text'" @deleteFile="deleteFile" />

        <div class="modal" ref="modal" id="commitModal" tabindex="-1">
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
                        <button type="button" class="btn btn-commit" data-bs-dismiss="modal" @click="finalizeDelete">Commit
                            changes</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import TextFile from './text/TextFile.vue';
import NonTextDisplay from './non-text/NonTextDisplay.vue';
import RepositoryService from '@/services/RepositoryService';
import { Modal } from "bootstrap";

export default {
    name: 'FileDisplay',
    components: {
        TextFile,
        NonTextDisplay
    },

    mounted() {
        this.modal = new Modal(this.$refs.modal);
        RepositoryService.getFile(this.$route.params.username, this.$route.params.repoName, this.$route.params.branchName, this.$route.params.path).then(res => {
            this.kind = res.data['is_text'] ? "text" : "non-text";
        }).catch(err => {
            console.log(err);
        })
    },

    data() {
        return {
            kind: "",
            commitMsg: "",
            additionalText: "",
            modal: ''
        }
    },

    methods: {
        deleteFile() {
            this.modal.show();
        },

        finalizeDelete() {
            let commitData = {
                'branch': this.$route.params.branchName,
                'message': this.commitMsg,
                'additional_text': this.additionalText
            }
            RepositoryService.deleteFile(this.$route.params.username, this.$route.params.repoName, this.$route.params.path, commitData).then(res => {
                console.log(res);
                this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}`);
            }).catch(err => {
                console.log(err);
            })
        }
    }
}
</script>

<style scoped>
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
