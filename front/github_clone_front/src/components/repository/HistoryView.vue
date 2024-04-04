<template>
    <div class="bg is-fullheight min-vh-100">
        <RepoNavbar />
        <div class="d-flex justify-content-center">
            <div class="contain">
                <h3 class="mt-4">
                    Commits
                </h3>

                <hr />

                <div class="d-flex justify-content-between">
                    <div>
                        <button class="btn nav-link dropdown-toggle btn-branch-choice" type="button" id="navbarDropdown"
                            role="button" data-bs-toggle="dropdown" aria-expanded="false">
                            <font-awesome-icon icon="fa-solid fa-code-branch" class="me-2 mt-1" />
                            <span class="ms-1 me-2">{{ selectedBranch }}</span>
                        </button>
                        <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                            <li class="mx-2">
                                <input type="text" placeholder="Search branches" class="px-2 py-1" v-model="searchTerm"
                                    @input="searchTermChanged" />
                            </li>
                            <li v-for="b in filteredBranches" :key="b.name">
                                <button class="btn dropdown-item branch-name" @click="selectedBranchChanged(b.name)">
                                    {{ b.name }}
                                </button>
                            </li>
                        </ul>
                    </div>

                    <div class="d-flex justify-content-end">
                        <div>
                            <button class="btn nav-link dropdown-toggle btn-committer-choice" type="button"
                                id="navbarCommitterDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                                <span v-if="selectedCommitter === null">
                                    <font-awesome-icon icon="fa-solid fa-users" class="me-2 mt-1" />
                                    <span class="ms-1 me-2">All users</span>
                                </span>
                                <span v-else>
                                    <img :src="selectedCommitter.avatar" :alt="selectedCommitter.username[0]"/>
                                        {{ selectedCommitter.username }}
                                </span>
                            </button>
                            <ul class="dropdown-menu" aria-labelledby="navbarCommitterDropdown">
                                <li class="mx-2">
                                    <input type="text" placeholder="Find a user" class="px-2 py-1 mb-2"
                                        v-model="committerSearchTerm" @input="committerSearchTermChanged" />
                                </li>
                                <li v-for="c in filteredCommitters" :key="c.username">
                                    <button class="btn dropdown-item branch-name d-flex align-items-center"
                                        @click="selectedCommitterChanged(c)">
                                        <img :src="c.avatar" :alt="c.username[0]"/>
                                        {{ c.username }}
                                    </button>
                                </li>
                                <hr />
                                <li>
                                    <button class="btn-all-users d-flex justify-content-start align-items-center" type="button" @click="displayCommitsAllUsers">
                                        View commits for all users
                                    </button>
                                </li>
                            </ul>
                        </div>

                        <div>

                        </div>
                    </div>
                </div>

                <div class="d-flex justify-content-center w-100">
                    <CommitsTable :commits="commitsByCommitter" class="w-100" :ref="commitsTableRef" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import CommitsTable from '../commit/CommitsTable.vue';
import BranchService from '@/services/BranchService';
import RepoNavbar from './RepoNavbar.vue';

export default {
    name: "HistoryView",
    components: {
        CommitsTable,
        RepoNavbar
    },

    mounted() {
        this.selectedBranch = this.$route.params.branchName;

        BranchService.getAllBranches(this.$route.params.repoName).then(res => {
            this.branches = res.data;
            this.filteredBranches = res.data;
        }).catch(err => {
            console.log(err);
        });

        BranchService.getCommitters(this.$route.params.repoName, this.selectedBranch).then(res => {
            this.committers = res.data;
            this.filteredCommitters = res.data;
        }).catch(err => {
            console.log(err);
        });

        this.loadCommits();
    },

    data() {
        return {
            commits: [],
            commitsByCommitter: [],
            branches: [],
            filteredBranches: [],
            committers: [],
            filteredCommitters: [],
            selectedBranch: "",
            searchTerm: "",
            committerSearchTerm: "",
            selectedCommitter: null,
            commitsTableRef: 1
        }
    },

    methods: {
        loadCommits() {
            BranchService.getCommits(this.$route.params.repoName, this.selectedBranch).then(res => {
                this.commits = res.data;
                this.commitsByCommitter = res.data;
            }).catch(err => {
                console.log(err);
            });
        },

        selectedBranchChanged(branchName) {
            this.selectedBranch = branchName;
            this.loadCommits();
        },

        selectedCommitterChanged(committer) {
            this.selectedCommitter = committer;
            this.commitsByCommitter = this.commits.filter(c => c.author.username.toLowerCase().includes(committer.username.toLowerCase()));
            this.commitsTableRef++;
        },

        displayCommitsAllUsers() {
            this.selectedCommitter = null;
            this.commitsByCommitter = this.commits;
            this.commitsTableRef++;
        },

        searchTermChanged() {
            if (this.searchTerm === "") {
                this.filteredBranches = this.branches;
            } else {
                this.filteredBranches = this.branches.filter(b => b.name.toLowerCase().includes(this.searchTerm.toLowerCase()));
            }
        },

        committerSearchTermChanged() {
            if (this.committerSearchTerm === "") {
                this.filteredCommitters = this.committers;
            } else {
                this.filteredCommitters = this.committers.filter(c => c.username.toLowerCase().includes(this.committerSearchTerm.toLowerCase()));
            }
        }
    }
}
</script>

<style scoped>
.contain {
    width: 85%;
    max-width: 1400px;
}

.bg {
    background-color: #22272d;
}

h3,
hr {
    color: #c5d1df;
}

.btn-branch-choice,
.btn-branch-choice:hover,
.btn-committer-choice,
.btn-committer-choice:hover {
    color: #c5d1df;
    background-color: #373e48;
    border: 1px solid #b1bdca;
    padding: 5px 10px;
}



.dropdown-menu {
    background-color: #2c333b;
    border: 1px solid #646b72;
}

.branch-name {
    color: #c5d1df;
}

input {
    background-color: #22272d;
    color: #b1bdca;
    border: 1px solid #646b72;
    ;
    border-radius: 5px;
    min-width: 250px;
}

img {
    width: 25px;
    border-radius: 50%;
    margin-right: 5px;
}

.btn-all-users {
    color: #c5d1df;
    background: none;
    height: 37px;
    padding-left: 20px;
    border: none;
}

.btn-all-users:hover {
    color: #22272d ;
    background-color: #e1e7ee;
    width: 100%;
}
</style>