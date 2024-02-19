<template>
    <div class="background is-fullheight min-vh-100">
        <RepoNavbar starting="pullRequests" />
        <div class="d-flex justify-content-between px-5 pt-4">
            <div class="d-flex justify-content-start">
                <h2 class="bright me-2">{{ pull.title }}</h2>
                <h2 class="muted">#{{ pull.id }}</h2>
            </div>

            <div class="d-flex justify-content-end">
                <button type="button" class="btn-edit-title bright me-2">
                    Edit
                </button>

                <button type="button" class="btn-review bright">
                    Review
                </button>
            </div>
        </div>

        <div class="px-5 mt-2 d-flex justify-content-start">
            <div v-if="pull.status === 'Open'" class="status-pill open">
                <label>{{ pull.status }}</label>
            </div>
            <div v-if="pull.status === 'Closed'" class="status-pill closed">
                <label>{{ pull.status }}</label>
            </div>
            <div v-if="pull.status === 'Merged'" class="status-pill merged">
                <label>{{ pull.status }}</label>
            </div>

            <div class="d-flex justify-content-start ms-3">
                <button class="bg-none muted" type="button">
                    {{ pull.author.username }}
                </button>
                <label class="muted">{{ getMergeMsg() }} {{ pull.commits.length }} commits into</label>
                <button type="button" class="btn-branch d-flex align-items-center">{{ pull.base }}</button> <label
                    class="muted">from</label>
                <button type="button" class="btn-branch d-flex align-items-center">{{ pull.compare }}</button>
            </div>
        </div>

        <div class="px-5 w-100 d-flex justify-content-start my-3">
            <button type="button" @click="setActiveTab('conversation')">Conversation</button>
            <button type="button" @click="setActiveTab('commits')">Commits</button>
            <button type="button" @click="setActiveTab('files')">Files changes</button>
        </div>

        <div class="px-5 pb-5 mt-2 w-100 d-flex justify-content-between">
            <div class="w-75 pe-5">
                <div v-if="chosenTab === 'conversation'">
                    <div>
                        Events - labele, milestone, assigning, reviewing, closing, opening
                    </div>

                    <div>
                        Comments
                    </div>

                    <hr class="bright" />

                    <div class="mt-4 merge">
                        <MergeInfo :pull="pull" />
                    </div>

                    <div class="mt-3">
                        <h5 class="bright">Add a comment</h5>
                        <textarea v-model="newComment" class="w-100 p-2 bright"></textarea>
                        <div class="w-100 d-flex justify-content-end">
                            <button type="button">Close pull request</button>
                            <button type="button">Comment</button>
                        </div>
                    </div>
                </div>

                <div v-if="chosenTab === 'commits'">
                    <CommitsTable :commits="pull.commits" />
                </div>

                <div v-if="chosenTab === 'files'">

                </div>
            </div>

            <div class="w-25">
                <AdditionalPrInfo />
            </div>
        </div>
    </div>
</template>

<script>
import RepoNavbar from '../repository/RepoNavbar.vue';
import AdditionalPrInfo from './AdditionalPrInfo.vue';
import MergeInfo from './MergeInfo.vue'
import CommitsTable from '../commit/CommitsTable.vue'

export default {
    name: "PrDisplay",
    components: {
        RepoNavbar,
        AdditionalPrInfo,
        MergeInfo,
        CommitsTable
    },

    data() {
        return {
            milestone: null,
            pull: {
                title: "Dev",
                id: 1,
                status: "Open",
                author: {
                    username: "elenore55"
                },
                base: "main",
                compare: "develop",
                commits: [{
                    hash: "fweurh3iurhqlieurhoi3u434534fsdfa",
                    message: "Ovo je moja commit poruka this isd asdkn vanfdv dsvufdnbvld vkbkv dsvlkabdfn v v;snbv dsfkvbdf vkndhbgvkd fkabdf vn",
                    timestamp: "2024-02-01",
                    author: {
                        username: "elenore55",
                        avatar: "http://localhost:3000/avatar/7bc306a1860b7f9fa06cbb9a27161a49"
                    }
                }],
                milestone: {
                    id: 1,
                    title: "Kontrolna tacka"
                },
                labels: ["feature", "backend"],
                assignee: {
                    username: "elenore55",
                    avatar: ""
                },
                reviewers: [],
                files_changed: [],
                can_be_merged: false,
                review_requested: true,
                conflicting_files: ["README.md", "main.js"]
            },
            chosenTab: "conversation",
            newComment: ""
        }
    },

    methods: {
        updateMilestone(data) {
            this.milestone = data;
        },

        getMergeMsg() {
            if (this.pull.status === "Merged") {
                return "merged";
            }
            return "wants to merge"
        },

        setActiveTab(value) {
            this.chosenTab = value;
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

.muted {
    color: #768491;
}

.btn-edit-title,
.btn-review {
    height: 35px;
    width: 70px;
    background-color: #373e48;
    border: 1px solid #768491;
    border-radius: 5px;
}

.bg-none {
    background: none;
    border: none;
    height: 15px;
    font-weight: 600;
}

.status-pill {
    font-size: large;
    padding: 3px 12px;
    border-radius: 8px;
    font-weight: 600;
    color: white;
}

.open {
    background-color: #347d38;
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
</style>