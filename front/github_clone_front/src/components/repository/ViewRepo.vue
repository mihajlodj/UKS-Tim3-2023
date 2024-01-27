<template>
    <div>
        <h1>Repo</h1>
    </div>
</template>

<script>

import RepositoryService from '@/services/RepositoryService';

export default {
    name: 'ViewRepo',

    mounted() {
        RepositoryService.get(this.$route.params.username, this.$route.params.repoName).then(res => {
            this.repo.name = res.data.name;
            this.repo.description = res.data.description;
            this.repo.accessModifier = res.data.access_modifier;
        }).catch(err => {
            console.log(err);
        });
    },

    data() {
        return {
            repo: {
                name: '',
                description: '',
                accessModifier: ''
            }
        }
    }
}

</script>

<style scoped>

</style>