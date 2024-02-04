<template>
    <div class="background is-fullheight min-vh-100 ">
        <RepoNavbar />
        <PathDisplay />
        <div>
            <div class="editor">
                <CodeHeader :numLines="lines.length" :size="file.size" :name="file.name"
                    :downloadUrl="file.download_url" :content="file.content" />
                <CodeDisplay :lines="lines" />
            </div>
        </div>
    </div>
</template>

<script>
import RepositoryService from '@/services/RepositoryService';
import CodeDisplay from './CodeDisplay.vue';
import CodeHeader from './CodeHeader.vue';
import PathDisplay from './PathDisplay.vue';
import RepoNavbar from '../RepoNavbar.vue'

export default {
    name: 'TextFile',
    components: {
        CodeDisplay,
        CodeHeader,
        PathDisplay,
        RepoNavbar
    },

    mounted() {
        this.path = this.$route.params.path;
        RepositoryService.getFile(this.$route.params.username, this.$route.params.repoName, this.$route.params.branchName, this.$route.params.path).then(res => {
            this.file = {
                ...res.data
            };
            this.lines = res.data.content.split("\n");
        }).catch(err => {
            console.log(err);
        })
    },

    data() {
        return {
            path: '',
            file: {

            },
            lines: [],
        }
    },

    methods: {

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
</style>