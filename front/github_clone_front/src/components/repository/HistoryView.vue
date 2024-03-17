<template>
    <div>
        <h1>
            Commits
        </h1>
        <div>
            <CommitsTable :commits="commits" />
        </div>
    </div>
</template>

<script>
import CommitsTable from '../commit/CommitsTable.vue';
import BranchService from '@/services/BranchService';

export default {
    name: "HistoryView",
    components: {
        CommitsTable
    },

    mounted() {
        BranchService.getCommits(this.$route.params.repoName, this.$route.params.branchName).then(res => {
            this.commits = res.data;
        }).catch(err => {
            console.log(err);
        });
    },

    data() {
        return {
            commits: []
        }
    }
}
</script>

<style scoped>

</style>