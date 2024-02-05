<template>
    <div>
        <TextFile v-if="kind === 'text'" />
        <NonTextDisplay v-if="kind === 'non-text'" />
    </div>
</template>

<script>
import TextFile from './TextFile.vue';
import NonTextDisplay from './NonTextDisplay.vue';
import RepositoryService from '@/services/RepositoryService';

export default {
    name: 'FileDisplay',
    components: {
        TextFile,
        NonTextDisplay
    },

    mounted() {
        RepositoryService.getFile(this.$route.params.username, this.$route.params.repoName, this.$route.params.branchName, this.$route.params.path).then(res => {
            this.kind = res.data['is_text'] ? "text" : "non-text";
        }).catch(err => {
            console.log(err);
        })
    },

    data() {
        return {
            kind: ""
        }
    }
}
</script>
