<template>
    <div class="background is-fullheight min-vh-100">
        <span class="text">{{ path }}</span>
        <CodeHeader :numLines="lines.length" :size="file.size" :htmlUrl="file.html_url" :downloadUrl="file.download_url" />
        <CodeDisplay :lines="lines" />
    </div>
</template>

<script>
import RepositoryService from '@/services/RepositoryService';
import CodeDisplay from './CodeDisplay.vue';
import CodeHeader from './CodeHeader.vue';

export default {
    name: 'TextFile',
    components: {
        CodeDisplay,
        CodeHeader
    },

    mounted() {
        this.path = this.$route.params.path;
        RepositoryService.getFile(this.$route.params.username, this.$route.params.repoName, this.$route.params.branchName, this.$route.params.path).then(res => {
            this.file = {
                ...res.data
            };
            this.lines = res.data.content.split("\n");
            console.log(this.file.content);
            console.log(this.lines);
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

.text {
    color: white;
}
</style>