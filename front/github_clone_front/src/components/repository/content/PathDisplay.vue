<template>
    <div class="d-flex justify-content-center">
        <div class="contain">
            <span>
                <span @click="repoClicked" class="repo">{{ repoName }}</span>
                <span class="text">/</span>
                <span v-for="(d, index) in directories" :key="d">
                    <span v-if="d" class="dir" @click="navigateToDir(index)">{{ d }}</span>
                    <span v-if="d" class="text">/</span>
                </span>
                <span class="text">{{ fileName }}</span>
            </span>
        </div>
    </div>
</template>

<script>
export default {
    name: 'PathDisplay',

    mounted() {
        this.getDirectories();
    },

    data() {
        return {
            repoName: this.$route.params.repoName,
            path: this.$route.params.path,
            fileName: '',
            directories: [],
            branch: this.$route.params.branchName
        }
    },

    methods: {
        getDirectories() {
            this.directories = this.path.split("/");
            this.fileName = this.directories.pop();
        },

        repoClicked() {
            this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}?chosen=${this.branch}`);
        },

        navigateToDir(index) {
            let result = this.directories.slice(0, index + 1);
            console.log(result);
            console.log(result.join("/"));
            let path = result.join("/");
            this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}?chosen=${this.branch}&path=${path}`);
        }
    }
}

</script>

<style scoped>
.dir {
    color: #559af5;
}

.dir:hover {
    cursor: pointer;
}

.repo {
    color: #559af5;
    font-weight: 600;
}

.repo:hover {
    cursor: pointer;
}

.text {
    color: #adbbc8;
    margin: 0px 5px;
}

.contain {
    width: 80%;
    padding: 25px 10px;
    background-color: #22272d;
}
</style>