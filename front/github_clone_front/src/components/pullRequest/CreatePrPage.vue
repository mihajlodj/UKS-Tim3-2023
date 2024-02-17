<template>
    <div class="background is-fullheight min-vh-100">
        <RepoNavbar />
        <div class="mx-5 mt-4">
            <h3 class="bright">Comparing changes</h3>
            <h6 class="muted">Choose two branches to see what’s changed or to start a new pull request</h6>
        </div>
        <hr class="mx-5 muted">

        <div class="mx-5 px-4 d-flex justify-content-start align-items-center branches">
            <BranchChoice type="base" @updateBranch="updateBaseBranch" />
            <p class="mx-3">
                <font-awesome-icon icon="fa-solid fa-arrow-left-long" class="mt-4" />
            </p>
            <BranchChoice type="compare" @updateBranch="updateCompareBranch" />
        </div>

        <div class="d-flex justify-content-start">
            <div class="w-75">
                <div class="mx-5 mt-4">
                    <h5 class="bright">Add a title</h5>
                    <input type="text" v-model="title" class="w-100 p-2 title bright" />
                </div>

                <div class="mx-5 mt-3">
                    <h5 class="bright">Add a description</h5>
                    <textarea v-model="description" class="w-100 p-2 title bright"></textarea>
                </div>

                <div class="mx-5 mt-3 d-flex justify-content-end">
                    <button class="button px-3 py-2" type="button" @click="createPullRequest">Create pull request</button>
                </div>
            </div>

            <div>
                <div>
                    <p>Reviewers</p>
                    <button type="button" @click="requestReviewers">click</button>
                    <ReviewersModal v-if="showModal" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import RepoNavbar from "@/components/repository/RepoNavbar.vue"
import BranchChoice from "./BranchChoice.vue"
import PullRequestService from "@/services/PullRequestService"
import ReviewersModal from "@/components/pullRequest/modals/ReviewersModal.vue"

export default {
    name: 'CreatePrPage',
    components: {
        RepoNavbar,
        BranchChoice,
        ReviewersModal
    },

    mounted() {
        this.baseName = this.$route.params.dest;
        this.compareName = this.$route.params.src;
        this.title = this.compareName;
    },

    data() {
        return {
            baseName: "",
            compareName: "",
            title: "",
            description: "",
            showModal: false
        }
    },

    methods: {
        createPullRequest() {
            let data = {
                "base": this.baseName, "compare": this.compareName, "title": this.title, "description": this.description
            }
            PullRequestService.create(this.$route.params.username, this.$route.params.repoName, data).then(res => {
                this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}/pulls/${res.data.id}`);
            }).catch(err => {
                console.log(err);
            });
        },

        updateBaseBranch(data) {
            this.baseName = data.name;
        },

        updateCompareBranch(data) {
            this.compareName = data.name;
        },

        requestReviewers() {
            this.showModal = !this.showModal;
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

.muted,
.fa-arrow-left-long {
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

.title {
    background-color: #22272d;
    border: 1px solid #768491;
    border-radius: 5px;
}

textarea {
    min-height: 200px;
    resize: none;
}
</style>