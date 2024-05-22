<template>
    <div class="background is-fullheight min-vh-100">
        <RepoNavbar />

        <LoadingPage v-if="!loaded" />

        <PathDisplay />

        <DropZone class="drop-area" @files-dropped="addFiles" #default="{ dropZoneActive }">
            <label for="file-input">
                <div class="d-flex justify-content-center">
                    <span v-if="dropZoneActive">
                        <div class="d-flex justify-content-center mb-3">
                            <font-awesome-icon icon="fa-regular fa-file" class="me-2 mt-1" />
                        </div>
                        <span>Drop to upload your files</span>
                    </span>
                    <span v-else>
                        <div class="d-flex justify-content-center mb-3">
                            <font-awesome-icon icon="fa-regular fa-file" class="me-2 mt-1" />
                        </div>
                        <span>Drag files here to add them to your repository</span>
                        <span class="smaller mt-2 d-flex justify-content-center">
                            Or &nbsp; <strong>choose your files</strong>
                        </span>
                    </span>
                </div>
                <input type="file" id="file-input" multiple @change="onInputChange" />
            </label>
            <ul class="image-list" v-show="files.length">
                <FilePreview v-for="file of files" :key="file.id" :file="file" tag="li" @remove="removeFile" />
            </ul>
        </DropZone>

        <div class="d-flex justify-content-center">
            <div class="commit-changes d-flex flex-column">
                <h3>Commit changes</h3>
                <input v-model="commitMsg" type="text" placeholder="Add files via upload" />
                <textarea v-model="additionalText" placeholder="Add an optional extended description"></textarea>
            </div>
        </div>
        <div class="d-flex justify-content-center">
            <div class="d-flex justify-content-start commit-cancel mb-5" style="width: 80%; max-width: 1200px;">
                <button @click="uploadSelectedFiles(files)" class="btn-commit me-2">Commit changes</button>
                <button type="button" class="btn-cancel" @click="cancel">Cancel</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import DropZone from './DropZone.vue';
import FilePreview from './FilePreview.vue'
import useFileList from '@/services/FileList'
import RepoNavbar from '../../RepoNavbar.vue';
import PathDisplay from '../PathDisplay.vue';
import LoadingPage from '@/components/util/LoadingPage.vue';

const { files, addFiles, removeFile } = useFileList()

function onInputChange(e) {
    addFiles(e.target.files)
    e.target.value = null
}

</script>

<script>
import FileUploader from '@/services/FileUploader';

export default {
    data() {
        return {
            commitMsg: "",
            additionalText: "",
            loaded: true
        }
    },

    methods: {
        uploadSelectedFiles(files) {
            this.loaded = false;
            let data = {
                "branch": this.$route.params.branchName,
                "message": this.commitMsg,
                "additional_text": this.additionalText
            };
            try {
                FileUploader.uploadFiles(files, this.$route.params.username, this.$route.params.repoName, data).then(res => {
                    console.log(res);
                    this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}`);
                    this.loaded = true;
                }).catch(err => {
                    console.log(err);
                    this.loaded = true;
                });
            }
            catch (e) {
                console.log(e);
                this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}`);
                this.loaded = true;
            }
        },

        cancel() {
            this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}`);
        }
    }
}
</script>

<style scoped>
.background {
    background-color: #22272d;
}

h3 {
    color: #adbbc8;
    margin-bottom: 20px;
}

.commit-changes {
    width: 80%;
    max-width: 1200px;
    border: 1px solid #adbbc8;
    padding: 20px;
    margin: 10px;
    border-radius: 5px;
}

input,
textarea {
    background-color: #1c2127;
    color: #adbbc8;
    margin-bottom: 7px;
    padding: 7px;
    resize: none;
    border: 1px solid #adbbc8;
    border-radius: 5px;
}

.drop-area {
    width: 80%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 50px;
    background: #22272d;
    color: #adbbc8;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
    border: 1px solid #adbbc8;
    border-radius: 5px;
    transition: .2s ease;

    &[data-active=true] {
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        border: 3px dashed #adbbc8;
    }
}

strong {
    color: #539af3;
    font-weight: 550;
}

strong:hover {
    text-decoration: underline;
}

label {
    font-size: 30px;
    cursor: pointer;
    display: block;
}

span {
    display: block;
}

input[type=file]:not(:focus-visible) {
    position: absolute !important;
    width: 1px !important;
    height: 1px !important;
    padding: 0 !important;
    margin: -1px !important;
    overflow: hidden !important;
    clip: rect(0, 0, 0, 0) !important;
    white-space: nowrap !important;
    border: 0 !important;
}

.smaller {
    font-size: 16px;
}

.image-list {
    display: flex;
    list-style: none;
    flex-wrap: wrap;
    padding: 0;
}

.upload-button {
    display: block;
    appearance: none;
    border: 0;
    border-radius: 50px;
    padding: 0.75rem 3rem;
    margin: 1rem auto;
    font-size: 1.25rem;
    font-weight: bold;
    background: #369;
    color: #fff;
    text-transform: uppercase;
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
</style>