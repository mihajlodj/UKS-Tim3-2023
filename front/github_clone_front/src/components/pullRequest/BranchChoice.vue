<template>
    <div class="contain py-2 px-3">
        <div class="d-flex justify-content-start">
            <button class="btn nav-link dropdown-toggle btn-gray" type="button" id="navbarDropdown" role="button"
                data-bs-toggle="dropdown" aria-expanded="false">
                <span class="muted">{{ type }}:</span> <span class="accent">{{ chosenBranch }}</span>
            </button>
            <ul class="dropdown-menu" id="branches-list" aria-labelledby="navbarDropdown">
                <li class="mx-2">
                    <input type="text" placeholder="Find a branch" class="px-2 py-1 mt-1" id="branches-search" />
                </li>
                <li>
                    <hr class="muted">
                </li>
                <li v-for="b in branches" :key="b.name">
                    <button class="btn dropdown-item" id="btn-name" @click="selectedBranchChanged(b.name)" style="color: #a5b2bf;">
                        {{ b.name }}
                    </button>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
import BranchService from '@/services/BranchService';

export default {
    name: 'BranchChoice',
    props: ['type'],

    mounted() {
        BranchService.getAllBranches(this.$route.params.username, this.$route.params.repoName).then(res => {
            this.branches = res.data;
            this.chosenBranch = res.data[0].name;
            this.selectedBranchChanged(this.chosenBranch);
        }).catch(err => {
            console.log(err);
        });
    },

    data() {
        return {
            dest: "",
            src: "",
            chosenBranch: "",
            branches: [],
        }
    },

    methods: {
        selectedBranchChanged(branchName) {
            this.chosenBranch = branchName;
            this.$emit('updateBranch', {
                name: this.chosenBranch
            });
        },
    }
}
</script>

<style scoped>
.muted {
    color: #a5b2bf;
}

.accent, .dropdown-toggle {
    color: #d9e6f1;
}

.contain {
    border: 1px solid #768491;
    border-radius: 5px;
    background-color: #373e48;
}

#branches-list {
    background-color: #2c333b;
    min-width: 350px;
    border: 1px solid #a5b2bf;
    border-radius: 7px;
}

#branches-search {
    width: 100%;
    color: #a5b2bf;
    background-color: #22272d;
    border: 1px solid #a5b2bf;
    border-radius: 5px;
}

#btn-name:hover {
    background-color: #38404b;
}
</style>