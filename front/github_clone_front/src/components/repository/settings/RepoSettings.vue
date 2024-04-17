<template>
    <div class="bg min-vh-100 is-fullheight pb-3">
        <div v-if="allowed == true">
            <RepoNavbar starting="settings" />
            <GeneralSettings :key="generalKey" :name="repo.name" :description="repo.description" :branches="repo.branches"
                :branchName="repo.defaultBranch" />
            <CollaboratorsSettings />
            <DangerZoneSettings :accessModifier="repo.accessModifier" />
        </div>

        <div v-if="allowed == false">
            <NotFoundPage />
        </div>
    </div>
</template>

<script>
import RepoNavbar from '../RepoNavbar.vue';
import GeneralSettings from './GeneralSettings.vue'
import CollaboratorsSettings from './CollaboratorsSettings.vue';
import DangerZoneSettings from './DangerZoneSettings.vue';
import RepositoryService from '@/services/RepositoryService';
import NotFoundPage from '../../util/NotFoundPage.vue';

// transfer ownership


export default {
    name: 'RepoSettings',
    components: {
        RepoNavbar,
        GeneralSettings,
        CollaboratorsSettings,
        DangerZoneSettings,
        NotFoundPage
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
            this.allowed = true;
            this.forceRerender();
        }).catch(err => {
            console.log(err);
            this.allowed = false;
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

            generalKey: 1,
            allowed: 'not_set'
        }
    },

    methods: {
        forceRerender() {
            this.generalKey += 1;
        },
    }
}

</script>

<style scoped>
.bg {
    background-color: #22272d;
}

</style>