<template>
    <div class="bg is-full-height min-vh-100">
        <RepoNavbar />
        <div class="w-100 d-flex justify-content-center">
            <div class="mt-4 contain">
                <h3>Commit</h3>
                <hr />
                <CommitBasicInfo v-if="commitLoaded" :commit="commit" />
                <ChangedFiles :diff="diff" :overall_additions="overall_additions" :overall_deletions="overall_deletions" />
            </div>
        </div>
    </div>
</template>

<script>
import ChangedFiles from "./ChangedFiles.vue"
import CommitService from "@/services/CommitService";
import RepoNavbar from "../repository/RepoNavbar.vue";
import CommitBasicInfo from './CommitBasicInfo.vue';

export default {
    name: "CommitDisplay",
    components: {
        ChangedFiles,
        RepoNavbar,
        CommitBasicInfo
    },

    mounted() {
        CommitService.get_diff(this.$route.params.repoName, this.$route.params.sha).then(res => {
            this.diff = res.data.diff;
            this.overall_additions = res.data.overall_additions;
            this.overall_deletions = res.data.overall_deletions;
        }).catch(err => {
            console.log(err);
        });

        CommitService.get_info(this.$route.params.repoName, this.$route.params.sha).then(res => {
            this.commit = res.data;
            this.commitLoaded = true;
        }).catch(err => {
            console.log(err);
        });
    },

    data() {
        return {
            diff: "",
            overall_additions: 0,
            overall_deletions: 0,
            commit: {},
            commitLoaded: false
        }
    }
}
</script>

<style scoped>
.bg {
    background-color: #22272d;
}

.contain {
    width: 85%;
    max-width: 1500px;
}

h3,
hr {
    color: #c5d1df;
}
</style>