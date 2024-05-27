<template>
    <div class="background is-fullheight min-vh-100">
        <RepoNavbar starting="pullRequests" />

        <LoadingPage v-if="!loaded" :key="loadingKey" />

        <div class="d-flex justify-content-between px-5 pt-4">
            <div v-if="!editingTitle" class="d-flex justify-content-start">
                <h2 class="bright me-2">{{ pull.title }}</h2>
                <h2 class="muted">#{{ pull.id }}</h2>
            </div>
            <div v-else class="w-100">
                <input type="text" v-model="newTitle" class="edit" />
            </div>

            <div class="d-flex justify-content-end">
                <button v-if="!editingTitle" type="button" class="btn-edit-title bright me-2"
                    @click="() => editingTitle = true">
                    Edit
                </button>
                <button v-else type="button" class="btn-save bright me-2" @click="updateTitle">
                    Save changes
                </button>
                <button type="button" class="btn-review bright"
                    v-if="reviewButtonVisible() && this.chosenTab !== 'files'" @click="addYourReview()">
                    Add your review
                </button>
                <button type="button" class="btn-review bright"
                    v-if="reviewButtonVisible() && this.chosenTab === 'files'" @click="reviewChanges()">
                    Review changes
                </button>
            </div>
        </div>

        <div class="px-5 mt-2 d-flex justify-content-start">
            <StatusPill :status="pull.status" />

            <div class="d-flex justify-content-start ms-3">
                <button class="bg-none muted" type="button">
                    {{ pull.author.username }}
                </button>
                <label class="muted">{{ getMergeMsg() }} {{ pull.commits.length }} commits into</label>
                <button type="button" class="btn-branch d-flex align-items-center" @click="viewBranch(pull.base)">{{
            pull.base }}</button>
                <label class="muted">from</label>
                <button type="button" class="btn-branch d-flex align-items-center" @click="viewBranch(pull.compare)">{{
            pull.compare }}</button>
            </div>
        </div>

        <div class="d-flex justify-content-start mt-4 px-5 w-100">
            <button type="button" :class="chosenTab === 'conversation' ? 'tab active' : 'tab'"
                @click="setActiveTab('conversation')">
                <font-awesome-icon icon="fa-regular fa-comments"></font-awesome-icon>
                Conversation
            </button>
            <button type="button" :class="chosenTab === 'commits' ? 'tab active' : 'tab'"
                @click="setActiveTab('commits')">
                <font-awesome-icon icon="fa-solid fa-code-commit"></font-awesome-icon>
                Commits
            </button>
            <button type="button" :class="chosenTab === 'files' ? 'tab active' : 'tab'" @click="setActiveTab('files')">
                <font-awesome-icon icon="fa-regular fa-file"></font-awesome-icon>
                Files changed
            </button>
        </div>

        <div class="px-5 pb-5 mt-2 w-100 d-flex justify-content-between">
            <div :class="chosenTab === 'conversation' ? 'w-75 pe-5' : 'w-100 pe-5'">
                <div v-if="chosenTab === 'conversation'">
                    <div>
                        <div v-if="pull.description" class="description w-100 mt-2">
                            <label class="bright">{{ pull.description }}</label>
                        </div>
                        Events - labels, milestones, assigning, reviewing, closing, opening
                    </div>

                    <hr class="bright" />

                    <div v-if="pull.status === 'Open'" class="mt-4 merge">
                        <MergeInfo :key="mergeDataKey" :pull="pull" @merge="merge" />
                    </div>

                    <CommentDisplay :username="this.$route.params.username" :repoName="this.$route.params.repoName"
                        :entityType="'pull_request'" :entityId="this.$route.params.id">
                    </CommentDisplay>

                    <div class="w-100 d-flex justify-content-end mt-2">
                        <button v-if="pull.status === 'Open' && canUpdatePull()" type="button"
                            class="btn-close-pr bright p-2" @click="close">
                            <img class="pr-icon me-1" src="../../assets/closed_pr_red.png" />
                            Close pull request
                        </button>
                        <button v-if="pull.status === 'Closed' && canUpdatePull()" type="button"
                            class="btn-close-pr bright p-2" @click="reopen">
                            Reopen pull request
                        </button>
                    </div>

                </div>

                <div v-if="chosenTab === 'commits'">
                    <CommitsTable :commits="pull.commits" :branch="pull.compare" />
                </div>

                <div v-if="chosenTab === 'files'">
                    <ReviewChanges v-if="this.reviewComponentVisible" @reviewAdded="this.reviewAddedHandle"></ReviewChanges>
                    <ChangedFiles :diff="pull.diff" :overall_additions="pull.overall_additions"
                        :overall_deletions="pull.overall_deletions" />
                </div>
            </div>

            <div v-if="chosenTab === 'conversation'" class="w-25">
                <AdditionalPrInfo :key="additionalInfoKey" :chosenMilestone="pull.milestone"
                    :chosenAssignee="pull.assignee" :chosenReviewers="pull.reviewers" :selectedLabels="pull.labels"
                    :prId="pull.id" :prAuthorUsername="pull.author.username" @updateAssignee="updateAssignee"
                    @updateMilestone="updateMilestone" @updateReviewers="updateReviewers" />
                <hr class="bright" />
                <div class="w-100 d-flex justify-content-end mt-3">
                    <button type="button" class="btn-save p-2 bright" @click="update">Save changes</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import RepoNavbar from '../repository/RepoNavbar.vue';
import AdditionalPrInfo from './AdditionalPrInfo.vue';
import MergeInfo from './MergeInfo.vue'
import CommitsTable from '../commit/CommitsTable.vue'
import StatusPill from './StatusPill.vue';
import PullRequestService from '@/services/PullRequestService'
import ChangedFiles from "../commit/ChangedFiles.vue"
import { toast } from 'vue3-toastify';
import CommentDisplay from '@/components/comment/CommentDisplay.vue'
import LoadingPage from '@/components/util/LoadingPage.vue'
import ReviewChanges from '@/components/pullRequest/ReviewChanges.vue'

export default {
    name: "PrDisplay",
    components: {
        RepoNavbar,
        AdditionalPrInfo,
        MergeInfo,
        CommitsTable,
        StatusPill,
        ChangedFiles,
        CommentDisplay,
        LoadingPage,
        ReviewChanges
    },

    mounted() {
        this.logedInUserUsername = localStorage.getItem('username');
        PullRequestService.getOne(this.$route.params.username, this.$route.params.repoName, this.$route.params.id).then(res => {
            console.log(res.data);
            this.pull = res.data;
            this.mergeDataKey += 1;
            this.additionalInfoKey += 1;
            this.newTitle = this.pull.title;
            this.loaded = true;
        }).catch(err => {
            console.log(err);
        });
    },

    data() {
        return {
            milestone: null,
            pull: {
                title: "",
                id: -1,
                status: "Open",
                author: { username: "" },
                base: "",
                compare: "",
                commits: [],
                milestone: { id: -1, title: "" },
                labels: [],
                assignee: { username: "", avatar: "" },
                reviewers: [],
                files_changed: [],
                mergeable: false,
                conflicting_files: []
            },
            mergeDataKey: 1,
            chosenTab: "conversation",
            additionalInfoKey: 1,
            newTitle: "",
            editingTitle: false,
            loadingKey: 1,
            loaded: false,
            logedInUserUsername: '',
            reviewComponentVisible: false,
        }
    },

    methods: {
        viewBranch(name) {
            this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}?chosen=${name}`);
        },

        updateMilestone(data) {
            this.pull.milestone = data;
        },

        updateAssignee(data) {
            this.pull.assignee = data;
        },

        updateReviewers(data) {
            this.pull.reviewers = data;
        },

        canUpdatePull() {
            const role = localStorage.getItem(this.$route.params.repoName);
            return role === "Owner" || role === "Developer" || role === "Maintainer";
        },

        getMergeMsg() {
            if (this.pull.status === "Merged") return "merged";
            return "wants to merge"
        },

        setActiveTab(value) {
            this.chosenTab = value;
        },

        update() {
            let data = {};
            if (this.pull.milestone) data['milestone_id'] = this.pull.milestone.id;
            if (this.pull.assignee) data['assignee_username'] = this.pull.assignee.username;
            if (this.pull.reviewers.length > 0) data['reviewers'] = this.pull.reviewers;
            PullRequestService.update(this.$route.params.username, this.$route.params.repoName, this.$route.params.id, data).then(res => {
                console.log(res);
                toast("Changes saved!", {
                    autoClose: 500,
                    type: 'success',
                    position: toast.POSITION.BOTTOM_RIGHT,
                    theme: toast.THEME.DARK
                });
            }).catch(err => {
                console.log(err);
            });
        },

        updateTitle() {
            if (this.newTitle.trim() !== "") {
                this.editingTitle = false;
                let data = { "title": this.newTitle };
                PullRequestService.updateTitle(this.$route.params.username, this.$route.params.repoName, this.$route.params.id, data).then(res => {
                    this.pull.title = res.data;
                }).catch(err => {
                    console.log(err);
                    toast("Unable to update!", {
                        autoClose: 500,
                        type: 'error',
                        position: toast.POSITION.BOTTOM_RIGHT,
                        theme: toast.THEME.DARK
                    });
                });
            }
        },

        close() {
            PullRequestService.close(this.$route.params.username, this.$route.params.repoName, this.$route.params.id).then(res => {
                this.pull.status = res.data;
            }).catch(err => {
                console.log(err);
            });
        },

        reopen() {
            PullRequestService.reopen(this.$route.params.username, this.$route.params.repoName, this.$route.params.id).then(res => {
                this.pull.status = res.data;
            }).catch(err => {
                console.log(err);
            });
        },

        merge() {
            this.loaded = false;
            this.loadingKey++;
            PullRequestService.merge(this.$route.params.username, this.$route.params.repoName, this.$route.params.id).then(res => {
                console.log(res);
                this.pull.status = "Merged";
                toast("Pull request merged!", {
                    autoClose: 500,
                    type: 'success',
                    position: toast.POSITION.BOTTOM_RIGHT,
                    theme: toast.THEME.DARK
                });
                this.loaded = true;
            }).catch(err => {
                console.log(err);
                this.loaded = true;
            });
        },

        reviewButtonVisible() {
            return this.pull.reviewers.some(r => r.username === this.logedInUserUsername);
        },

        addYourReview() {
            this.chosenTab = "files";
        },

        reviewChanges() {
            this.reviewComponentVisible = !this.reviewComponentVisible;
        },

        reviewAddedHandle() {
            this.chosenTab = "conversation";
            // TODO: reload reviews for this PR
        },

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

.description {
    min-height: 100px;
    background: none;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #0298db;
}

.muted {
    color: #768491;
}


input.edit {
    width: 75%;
    height: 40px;
    border-radius: 5px;
    background-color: #1c2127;
    color: #adbbc8;
    border: 1px solid #768491;
}

.pr-icon {
    height: 17px;
}

.btn-edit-title {
    height: 40px;
    width: 70px;
    background-color: #373e48;
    border: 1px solid #768491;
    border-radius: 5px;
}

.btn-review {
    height: 40px;
    width: 130px;
    background-color: #373e48;
    border: 1px solid #768491;
    border-radius: 5px;
}

.btn-close-pr {
    background-color: #373e48;
    border-radius: 5px;
    border: 1px solid #768491;
}

.btn-comment {
    background-color: #347d38;
    border-radius: 5px;
    border: none;
    color: white;
}

.btn-comment:disabled {
    background-color: #315f3a;
    color: #adbbc8;
}

.tab {
    background: none;
    border: 1px solid #adbbc8;
    min-width: 140px;
    color: #768491;
    border-top-right-radius: 5px;
    border-top-left-radius: 5px;
    height: 40px;
}

.tab.active {
    color: #adbbc8;
    border-bottom: none;
}

.tab:hover {
    color: #adbbc8;
}

.bg-none {
    background: none;
    border: none;
    height: 15px;
    font-weight: 600;
}

.btn-branch {
    height: 25px;
    border: none;
    background-color: #253141;
    color: #549bf5;
    margin: 0px 3px;
    padding: 1px 5px;
    border-radius: 5px;
}

div.merge {
    border: 1px solid #768491;
    border-radius: 7px;
    padding: 10px 15px;
}

textarea {
    min-height: 150px;
    resize: none;
    background-color: #22272d;
    border: 1px solid #768491;
    border-radius: 7px;
}

.btn-save {
    width: 120px;
    background-color: #373e48;
    border: 1px solid #768491;
    border-radius: 5px;
}

/* Dark theme styles for comments */
#comments {
    background-color: #22272d;
    margin-top: 20px;
}

.comment {
    background-color: #444;
    border-radius: 5px;
    border: 2px solid #adbbc8;
    padding: 10px;
    margin-bottom: 15px;
}

.comment-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 5px;
}

.comments {
    color: #adbbc8;
    font-weight: bold;
    margin: 0;
    font-size: 35px;
}

.comment-author {
    color: #adbbc8;
    font-weight: bold;
    margin: 0;
}

.comment-timestamp {
    color: #aaa;
    font-size: 0.9em;
}

.comment-body {
    color: #adbbc8;
    margin-bottom: 10px;
}

.comment-actions {
    display: flex;
    justify-content: flex-end;
}

.reply-button,
.delete-button {
    background-color: #333;
    color: #adbbc8;
    border: none;
    border-radius: 3px;
    padding: 5px 10px;
    margin-left: 5px;
    cursor: pointer;
}

.reply-button:hover,
.delete-button:hover {
    background-color: #555;
}

.loading-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
}

.spinner {
    border: 15px solid #f3f3f3;
    border-radius: 50%;
    border-top: 15px solid #488be6;
    width: 120px;
    height: 120px;
    animation: spin 2s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}
</style>