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

                        <div class="ms-3">
                            <VueDatePicker 
                                ref="datePicker"
                                range
                                v-model="date"
                                placeholder="All time"
                                :format="format"
                                @range-start="dateInputStarted"
                                @range-end="dateInputEnded"
                                @cleared="cleared"
                                @closed="closed"
                            ></VueDatePicker>
                        </div>
                    </div>
                </div>

                <div class="d-flex justify-content-center w-100">
                    <CommitsTable :commits="filteredCommits" class="w-100" :ref="commitsTableRef" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>

const format = (date) => {
    if (Array.isArray(date)) {
        const d1 = new Date(date[0]);
        const d2 = new Date(date[1]);

        const day1 = d1.getDate();
        const month1 = d1.getMonth() + 1;
        const year1 = d1.getFullYear();

        const day2 = d2.getDate();
        const month2 = d2.getMonth() + 1;
        const year2 = d2.getFullYear();

        return `${day1}/${month1}/${year1} - ${day2}/${month2}/${year2}`;
    }
    date = new Date(date);
    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();

    return `${day}/${month}/${year}`;
}

</script>

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

        BranchService.getAllBranches(this.$route.params.username, this.$route.params.repoName).then(res => {
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
            filteredCommits: [],
            branches: [],
            filteredBranches: [],
            committers: [],
            filteredCommitters: [],
            selectedBranch: "",
            searchTerm: "",
            committerSearchTerm: "",
            selectedCommitter: null,
            commitsTableRef: 1,
            date: null,
            startDate: null,
            endDate: null
        }
    },

    methods: {
        loadCommits() {
            BranchService.getCommits(this.$route.params.repoName, this.selectedBranch).then(res => {
                this.commits = res.data;
                this.filteredCommits = res.data;
            }).catch(err => {
                console.log(err);
            });
        },

        selectedBranchChanged(branchName) {
            this.selectedBranch = branchName;
            this.loadCommits();
            this.$refs.datePicker.clearValue();
            this.startDate = null;
            this.endDate = null;
            this.selectedCommitter = null;
        },

        selectedCommitterChanged(committer) {
            this.selectedCommitter = committer;
            this.filterCommits();
        },

        displayCommitsAllUsers() {
            this.selectedCommitter = null;
            this.filterCommits();
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
        },

        dateInputStarted(value) {
            this.startDate = value;
        },

        dateInputEnded(value) {
            this.endDate = value;
        },

        cleared() {
            this.startDate = null;
            this.endDate = null;
            this.filterCommits();
        },

        closed() {
            this.filterCommits();
        },

        filterCommits() {
            if (this.selectedCommitter !== null) {
                this.filteredCommits = this.commits.filter(c => c.author.username.toLowerCase().includes(this.selectedCommitter.username.toLowerCase()));
            } else {
                this.filteredCommits = this.commits;
            }

            if (this.startDate !== null && this.endDate !== null) {
                this.filteredCommits = this.filteredCommits.filter(c => {
                    const ts = new Date(c.timestamp);
                    return ts >= this.startDate && ts <= this.endDate;
                });
            } else if (this.startDate !== null) {
                this.filteredCommits = this.filteredCommits.filter(c => new Date(c.timestamp) >= this.startDate);
            } else if (this.endDate !== null) {
                this.filteredCommits = this.filteredCommits.filter(c => new Date(c.timestamp) <= this.endDate);
            }

            this.commitsTableRef++;
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

.dp__theme_light {
    --dp-background-color: #373e48;
    --dp-text-color: #fff;
    --dp-hover-color: #484848;
    --dp-hover-text-color: #c5d1df;
    --dp-hover-icon-color: #c5d1df;
    --dp-primary-color: #005cb2;
    --dp-primary-disabled-color: #61a8ea;
    --dp-primary-text-color: #c5d1df;
    --dp-secondary-color: #c5d1df;
    --dp-border-color: #b1bdca;
    --dp-menu-border-color: #2d2d2d;
    --dp-border-color-hover: #b1bdca;
    --dp-disabled-color: #737373;
    --dp-disabled-color-text: #d0d0d0;
    --dp-scroll-bar-background: #212121;
    --dp-scroll-bar-color: #484848;
    --dp-success-color: #00701a;
    --dp-success-color-disabled: #428f59;
    --dp-icon-color: #c5d1df;
}

.dp__instance_calendar {
    background-color: red;
}

:root {
    --dp-border-radius: 7px;
}
</style>