<template>
    <div v-if="allowed" class="background is-fullheight min-vh-100">
        <RepoNavbar />
        <div class="editor">
            <PathDisplay :editing="editing" :key="pathKey" ref="pathDisplay" @updateFileName="updateFileName" />
        </div>
        <div>
            <div class="editor">
                <CodeHeader v-if="!editing" :numLines="lines.length" :size="file.size" :name="file.name"
                    :downloadUrl="file.download_url" :content="file.content" @editFile="editFile" @deleteFile="deleteFile" />

                <EditingHeader v-else />
                <CodeDisplay v-if="!editing" :key="codeDisplayKey" />
                <TextFileEdit v-else />

                <div class="d-flex justify-content-center">
                    <div v-if="editing" class="d-flex justify-content-end mt-2 commit-cancel">
                        <button type="button" class="btn-cancel" @click="cancelEdit">Cancel changes</button>
                        <button type="button" class="btn-commit" data-bs-toggle="modal" data-bs-target="#commitModal">Commit
                            changes...</button>
                    </div>
                </div>
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
                        <button type="button" class="btn btn-commit" data-bs-dismiss="modal" @click="commitChanges">Commit
                            changes</button>
                    </div>
                </div>
            </div>
        </div>

    </div>
    <div v-else>
        <NotFoundPage />
    </div>
</template>

<script>
import RepositoryService from '@/services/RepositoryService';
import CodeDisplay from './CodeDisplay.vue';
import CodeHeader from './CodeHeader.vue';
import PathDisplay from './PathDisplay.vue';
import RepoNavbar from '../RepoNavbar.vue'
import NotFoundPage from '@/components/util/NotFoundPage.vue';
import TextFileEdit from './TextFileEdit.vue';
import EditingHeader from './EditingHeader.vue';

export default {
    name: 'TextFile',
    components: {
        CodeDisplay,
        CodeHeader,
        PathDisplay,
        RepoNavbar,
        NotFoundPage,
        TextFileEdit,
        EditingHeader
    },

    mounted() {
        this.path = this.$route.params.path;
        RepositoryService.getFile(this.$route.params.username, this.$route.params.repoName, this.$route.params.branchName, this.$route.params.path).then(res => {
            this.file = {
                ...res.data
            };
            localStorage.setItem('fileContent', res.data.content);
            this.codeDisplayKey += 1;
            this.newFileName = this.file.name;
        }).catch(err => {
            console.log(err);
            this.allowed = false;
        })
    },

    data() {
        return {
            path: '',
            file: {

            },
            lines: [],
            allowed: true,
            editing: false,
            pathKey: 1,
            codeDisplayKey: 1,
            newFileName: '',
            commitMsg: '',
            additionalText: ''
        }
    },

    methods: {
        editFile() {
            this.editing = true;
            this.pathKey += 1;
        },

        updateFileName(data) {
            this.newFileName = data.fileName;
        },

        deleteFile() {
            this.$emit('deleteFile', {});
        },

        cancelEdit() {
            this.editing = false;
            this.pathKey += 1;
        },

        commitChanges() {
            let commitData = {
                'branch': this.$route.params.branchName,
                'content': localStorage.getItem('newContent'),
                'from_path': this.$route.params.path,
                'message': this.commitMsg,
                'additional_text': this.additionalText
            }
            let newPath = this.formNewPath();
            RepositoryService.editFile(this.$route.params.username, this.$route.params.repoName, newPath, commitData).then(res => {
                console.log(res);
                this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}/blob/${this.$route.params.branchName}/${newPath}`);
                localStorage.setItem('fileContent', localStorage.getItem('newContent'));
                localStorage.removeItem('newContent');
                this.codeDisplayKey += 1;
                // this.pathKey += 1;
                console.log(this.newFileName);
                this.$refs.pathDisplay.updatePath(this.newFileName);
            }).catch(err => {
                console.log(err);
            });
            this.cancelEdit();
            this.commitMsg = "";
            this.additionalText = "";
        },

        formNewPath() {
            let dirs = this.$route.params.path.split("/");
            dirs.pop()
            if (dirs.length == 0) return this.newFileName;
            return `${dirs.join("/")}/${this.newFileName}`
        }
    }
}
</script>

<style scoped>
.background {
    background-color: #22272d;
}

.editor {
    max-width: 1250px;
}

.commit-cancel {
    width: 80%;
}

.btn-commit, .btn-commit:hover {
    background-color: #347d38;
    color: white;
    border-radius: 5px;
    padding: 7px 15px;
    border: none;
}

.btn-cancel, .btn-cancel:hover {
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