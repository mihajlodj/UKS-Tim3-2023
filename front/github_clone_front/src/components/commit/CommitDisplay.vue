<template>
    <div>
        <ChangedFiles :diff="diff" :overall_additions="overall_additions" :overall_deletions="overall_deletions" />
    </div>
</template>

<script>
import ChangedFiles from "./ChangedFiles.vue"
import CommitService from "@/services/CommitService";

export default {
    name: "CommitDisplay",
    components: {
        ChangedFiles
    },

    mounted() {
        CommitService.get_diff(this.$route.params.repoName, this.$route.params.sha).then(res => {
            console.log(res.data);
            this.diff = res.data.diff;
            this.overall_additions = res.data.overall_additions;
            this.overall_deletions = res.data.overall_deletions;
        }).catch(err => {
            console.log(err);
        });
    },

    data() {
        return {
            diff: "",
            overall_additions: 0,
            overall_deletions: 0
        }
    }
}
</script>