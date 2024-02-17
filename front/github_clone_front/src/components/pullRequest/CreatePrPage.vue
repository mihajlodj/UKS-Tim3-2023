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

            <div class="w-25 me-5 mt-4">
                <div ref="reviewers">
                    <div class="d-flex justify-content-between">
                        <label class="muted">Reviewers</label>
                        <button type="button" class="btn-gear" @click="openModal('reviewers')">
                            <font-awesome-icon icon="fa-solid fa-gear" class="muted" />
                        </button>
                    </div>
                    <div>
                        <label v-if="reviews.length == 0" class="bright small">No reviews</label>
                    </div>
                    <ReviewersModal v-if="showModal['reviewers']" :x="modalX" :y="modalY" :w="modalW"
                        @closeModal="toggleModal('reviewers')" />
                </div>
                <hr class="muted" />

                <div ref="assignees">
                    <div class="">
                        <button type="button" class="btn-gear d-flex justify-content-between align-items-center w-100"
                            @click="openModal('assignees')">
                            <label class="muted hoverable">Asignees</label>
                            <font-awesome-icon icon="fa-solid fa-gear" class="muted" />
                        </button>
                    </div>
                    <div>
                        <label v-if="assignees.length == 0" class="bright small">No one</label>
                    </div>
                    <AssigneesModal v-if="showModal['assignees']" :x="modalX" :y="modalY" :w="modalW"
                        @closeModal="toggleModal('assignees')" />
                </div>
                <hr class="muted" />

                <div ref="labels">
                    <div>
                        <button type="button" class="btn-gear d-flex justify-content-between align-items-center w-100" @click="openModal('labels')">
                            <label class="muted hoverable">Labels</label>
                            <font-awesome-icon icon="fa-solid fa-gear" class="muted" />
                        </button>
                    </div>
                    <div>
                        <label v-if="labels.length == 0" class="bright small">None yet</label>
                    </div>
                    <LabelsModal v-if="showModal['labels']" :x="modalX" :y="modalY" :w="modalW"
                        @closeModal="toggleModal('labels')" />
                </div>
                <hr class="muted" />

                <div ref="milestone">
                    <div>
                        <button type="button" class="btn-gear d-flex justify-content-between align-items-center w-100" @click="openModal('milestone')">
                            <label class="muted hoverable">Milestone</label>
                            <font-awesome-icon icon="fa-solid fa-gear" class="muted" />
                        </button>
                    </div>
                    <div>
                        <label v-if="milestone == null" class="bright small">No milestone</label>
                    </div>
                    <MilestoneModal v-if="showModal['milestone']" :x="modalX" :y="modalY" :w="modalW"
                        @closeModal="toggleModal('milestone')" />
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
import AssigneesModal from "@/components/pullRequest/modals/AssigneesModal.vue"
import LabelsModal from "@/components/pullRequest/modals/LabelsModal.vue"
import MilestoneModal from "@/components/pullRequest/modals/MilestoneModal.vue"


export default {
    name: 'CreatePrPage',
    components: {
        RepoNavbar,
        BranchChoice,
        ReviewersModal,
        AssigneesModal,
        LabelsModal,
        MilestoneModal
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
            showModal: {
                "reviewers": false,
                "assignees": false,
                "labels": false,
                "milestone": false
            },
            modalX: 0,
            modalY: 0,
            modalW: 0,
            reviews: [],
            assignees: [],
            labels: [],
            milestone: null
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

        toggleModal(name) {
            this.showModal[name] = !this.showModal[name];
            for (const key in this.showModal) {
                if (key !== name) {
                    this.showModal[key] = false;
                }
            }
        },

        openModal(refName) {
            this.toggleModal(refName);
            console.log(`refName: ${refName}`);
            this.modalX = Math.trunc(this.$refs[refName].getBoundingClientRect().left + window.scrollX);
            this.modalY = Math.trunc(this.$refs[refName].getBoundingClientRect().top + window.scrollY) + 30;
            this.modalW = this.$refs[refName].offsetWidth;
            console.log(this.$refs[refName]);
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

.btn-gear {
    background-color: #22272d;
    border: none;
    padding-left: 0px;
}

.hoverable:hover {
    cursor: pointer;
}

.small {
    font-size: small;
}

hr {
    z-index: 0;
}
</style>