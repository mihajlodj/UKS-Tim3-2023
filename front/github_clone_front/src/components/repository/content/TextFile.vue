<template>
    <div v-if="allowed" class="background is-fullheight min-vh-100 ">
        <RepoNavbar />
        <PathDisplay :editing="editing" :key="pathKey" @updateFileName="updateFileName" />

        <div>
            <div class="editor">
                <CodeHeader v-if="!editing" :numLines="lines.length" :size="file.size" :name="file.name" :downloadUrl="file.download_url"
                    :content="file.content" @editFile="editFile" />

                <EditingHeader v-else />
                <CodeDisplay v-if="!editing" />
                <TextFileEdit v-else />

                <div class="d-flex justify-content-center">
                    <div v-if="editing" class="d-flex justify-content-end mt-2 commit-cancel">
                        <button type="button" class="btn-cancel" @click="cancelEdit">Cancel changes</button>
                        <button type="button" class="btn-commit">Commit changes...</button>
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
            this.lines = res.data.content.split("\n");
            localStorage.setItem('lines', this.lines);
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
            newFileName: ''
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

        cancelEdit() {
            this.editing = false;
            this.pathKey += 1;
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

.btn-commit {
    background-color: #347d38;
    color: white;
    border-radius: 5px;
    padding: 7px 15px;
    border: none;
}

.btn-cancel {
    background-color: #373e48;
    color: white;
    border-radius: 5px;
    padding: 7px 15px;
    margin-right: 5px;
    border: none;
}
</style>