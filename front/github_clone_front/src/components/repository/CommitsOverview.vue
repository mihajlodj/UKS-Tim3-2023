<template>
    <div class="d-flex justify-content-between contain">
        <div class="d-flex justify-content-start align-items-center">
            <button type="button" class="btn-author d-flex align-items-center">
                <img :src="latestCommit.author.avatar" />
                <span class="author-username">{{ latestCommit.author.username }}</span>
            </button>
            <button type="button" class="btn-msg" @click="viewCommit">
                <span>{{ latestCommit.message }}</span>
            </button>
        </div>

        <div class="d-flex justify-content-end align-items-center">
            <button type="button" class="btn-sha" @click="viewCommit">
                <span>
                    {{ latestCommit.sha.slice(0, 7) }}
                </span>
            </button>

            <span class="timestamp">
                {{ howLongAgo(latestCommit.timestamp) }}
            </span>

            <button type="button" class="btn-commits" @click="viewAllCommits">
                <span>
                    <font-awesome-icon icon="fa-solid fa-clock-rotate-left"></font-awesome-icon>
                </span>
                <span class="num-commits">
                    {{ numCommits }} commits
                </span>
            </button>
        </div>
    </div>
</template>

<script>
import TimestampService from '@/services/TimestampService';

export default {
    name: 'CommitsOverview',
    props: ['latestCommit', 'numCommits', 'branchName'],

    methods: {
        viewAuthorProfile() {

        },

        viewCommit() {
            const username = this.$route.params.username;
            const repoName = this.$route.params.repoName;
            this.$router.push(`/view/${username}/${repoName}/commit/${this.latestCommit.sha}`);
        },

        viewAllCommits() {
            const username = this.$route.params.username;
            const repoName = this.$route.params.repoName;
            this.$router.push(`/view/${username}/${repoName}/commits/${this.branchName}`);
        },

        howLongAgo(timestamp) {
            return TimestampService.howLongAgo(timestamp);
        }
    }
}

</script>

<style scoped>
img {
    width: 25px;
    border-radius: 50%;
    margin: 3px;
}

.contain {
    background-color: #2c333b;
    padding: 10px 15px;
    border: 1px solid #343b42;
    border-top-left-radius: 15px;
    border-top-right-radius: 15px;
}

button {
    background: none;
    border: none;
}

.author-username {
    margin-left: 5px;
    font-weight: 600;
    color: #c5d1df;
}

.btn-msg,
.btn-sha,
.timestamp {
    color: #8392a0;
    margin-left: 10px;
}

.btn-msg:hover,
.btn-sha:hover {
    color: #549bf7;
    text-decoration: underline;
}

.btn-commits {
    margin-left: 20px;
    padding: 5px 10px;
    border-radius: 5px;
}

.btn-commits:hover {
    background-color: #38414d;
}

.num-commits {
    color: #c5d1df;
}

.fa-clock-rotate-left {
    color: #717f8c;
    margin-right: 5px;
}
</style>