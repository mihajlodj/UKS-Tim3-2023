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
                                <input type="text" placeholder="Search branches" class="px-2 py-1" v-model="searchTerm" @input="searchTermChanged"/>
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

                        </div>

                        <div>

                        </div>
                    </div>
                </div>

                <div class="d-flex justify-content-center w-100">
                    <CommitsTable :commits="commits" class="w-100" />
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
        })
        this.loadCommits();
    },

    data() {
        return {
            commits: [],
            branches: [],
            filteredBranches: [],
            selectedBranch: "",
            searchTerm: ""
        }
    },

    methods: {
        loadCommits() {
            BranchService.getCommits(this.$route.params.repoName, this.selectedBranch).then(res => {
                this.commits = res.data;
            }).catch(err => {
                console.log(err);
            });
        },

        selectedBranchChanged(branchName) {
            this.selectedBranch = branchName;
            this.loadCommits();
        },

        searchTermChanged() {
            if (this.searchTerm === "") {
                this.filteredBranches = this.branches;
            } else {
                this.filteredBranches = this.branches.filter(b => b.name.toLowerCase().includes(this.searchTerm.toLowerCase()));
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

.btn-branch-choice, .btn-branch-choice:hover {
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
    border: 1px solid #646b72;;
    border-radius: 5px;
    min-width: 250px;
}
</style>