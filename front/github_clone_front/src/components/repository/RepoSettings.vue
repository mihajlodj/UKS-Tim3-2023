<template>
    <div>
        <RepoNavbar starting="settings" />
        <GeneralSettings :key="generalKey" :name="repo.name" :description="repo.description" :branches="repo.branches"
            :branchName="repo.defaultBranch" />
    </div>
</template>

<script>
import RepoNavbar from './RepoNavbar.vue';
import GeneralSettings from './GeneralSettings.vue'
import RepositoryService from '@/services/RepositoryService';

// access, transfer ownership, delete


export default {
    name: 'RepoSettings',
    components: {
        RepoNavbar,
        GeneralSettings
    },

    mounted() {
        RepositoryService.get(this.$route.params.username, this.$route.params.repoName).then(res => {
            this.repo.name = res.data.name;
            this.repo.description = res.data.description;
            this.repo.accessModifier = res.data.access_modifier;
            this.repo.defaultBranch = res.data.default_branch;
            for (let b of res.data.branches) {
                this.repo.branches.push({ 'name': b });
            }
            console.log(this.repo.branches);
            this.forceRerender();
        }).catch(err => {
            console.log(err);
        });
    },

    data() {
        return {
            repo: {
                name: '',
                description: '',
                accessModifier: '',
                defaultBranch: '',
                branches: [],
            },

            generalKey: 1
        }
    },

    methods: {
        forceRerender() {
            this.generalKey += 1;
        },
    }
}

</script>

<style scoped></style>