<template>
    <div class="contain">
        <div class="d-flex justify-content-start">
            <button class="btn nav-link dropdown-toggle btn-gray" type="button" id="navbarDropdown" role="button"
                data-bs-toggle="dropdown" aria-expanded="false">
                {{ type }}: {{ chosenBranch }}
            </button>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                <li class="mx-2">
                    <input type="text" placeholder="Search branches" class="px-1" />
                </li>
                <li v-for="b in branches" :key="b.name">
                    <button class="btn dropdown-item" @click="selectedBranchChanged(b.name)">
                        {{ b.name }}
                    </button>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    name: 'BranchChoice',
    props: ['type'],

    mounted() {
        if (this.type === "base") {
            this.chosenBranch = this.$route.params.dest;
        }
        else if (this.type === "compare") {
            this.chosenBranch = this.$route.params.src;
        }
    },

    data() {
        return {
            dest: "",
            src: "",
            chosenBranch: "",
            branches: [{name: "main"}, {name: "develop"}],
        }
    },

    methods: {
        selectedBranchChanged(branchName) {
            this.chosenBranch = branchName;
        },
    }
}
</script>