<template>
    <div class="background is-fullheight min-vh-100">
        <RepoNavbar />
        <div class="mx-5 mt-4">
            <h3 class="bright">Comparing changes</h3>
            <h6 class="muted">Choose two branches to see what’s changed or to start a new pull request</h6>
        </div>
        <hr class="mx-5 muted">

        <div class="mx-5 px-4 d-flex justify-content-start align-items-center branches">
            <BranchChoice type="base" />
            <p class="mx-3">
                <font-awesome-icon icon="fa-solid fa-arrow-left-long" class="mt-4" />
            </p>
            <BranchChoice type="compare" />
        </div>

        <div class="mx-5 mt-3 d-flex justify-content-end">
            <button class="button px-3 py-2" type="button" @click="createPullRequest">Create pull request</button>
        </div>
    </div>
</template>

<script>
import RepoNavbar from "@/components/repository/RepoNavbar.vue"
import BranchChoice from "./BranchChoice.vue"
import PullRequestService from "@/services/PullRequestService"

export default {
    name: 'CreatePrPage',
    components: {
        RepoNavbar,
        BranchChoice,
    },

    methods: {
        createPullRequest() {
            PullRequestService.create(this.$route.params.username, this.$route.params.repoName, {
                "base": this.$route.params.dest, "compare": this.$route.params.src
            }).then(res => {
                console.log(res);
            }).catch(err => {
                console.log(err);
            });
        }
    }
}
</script>

<style scoped>
.background {
    background-color: #22272d;
}

.bright {
    color: #adbbc8;
}

.muted, .fa-arrow-left-long {
    color: #768491;
}

.branches {
    background-color: #2c333b;
    border: 1px solid #768491;
    border-radius: 7px;
}

.button {
    color: #f4f8f4;
    background-color: #347d38;
    border-radius: 7px;
    border: none;
}
</style>