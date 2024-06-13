<template>
    <div class="mb-3">
        <div class="msg px-3 py-2">
            <h4 class="msg" v-html="formattedMessage"></h4>
            <div class="ms-1 pt-2 d-flex justify-content-start">
                <font-awesome-icon icon="fa-solid fa-code-branch" class="me-1"></font-awesome-icon>
                <button type="button" class="btn-branch" @click="goToBranch">
                    <h6>{{ commit.branch }}</h6>
                </button>
            </div>
        </div>
        <div class="d-flex align-items-center py-2 ps-2 author">
            <img :src="commit.author.avatar"/>
            <span class="username mx-1">{{ commit.author.username }}</span>
            <span class="timestamp">committed {{ howLongAgo() }}</span>
        </div>
    </div>
</template>

<script>
import TimestampService from '@/services/TimestampService';

export default {
    name: 'CommitBasicInfo',
    props: ['commit'],

    methods: {
        howLongAgo() {
            return TimestampService.howLongAgo(this.commit.timestamp);
        },

        goToBranch() {
            this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}?chosen=${this.commit.branch}`);
        }
    },

    computed: {
        formattedMessage() {
            const username = this.$route.params.username;
            const repoName = this.$route.params.repoName;

            return this.commit.message.replace(/#(\d+)/g, (match, issueId) => {
                return `<a href="/view/${username}/${repoName}/issues/${issueId}">${match}</a>`;
            });
        }
    }
}
</script>

<style scoped>
h4, h6 {
    color: #c5d1df;
}

.fa-code-branch {
    color: #8a949e;
    margin-top: 2px;
}

div.msg {
    background-color: #2c333b;
    border: 1px solid #969ea8;
    border-top-left-radius: 7px;
    border-top-right-radius: 7px;
}

h4.msg {
    font-weight: 600;
}

img {
    width: 20px;
    border-radius: 50%;
}

.username {
    font-weight: 550;
}

.username, .timestamp {
    color: #c5d1df;
}

.author {
    border: 1px solid #969ea8;
    border-bottom-left-radius: 7px;
    border-bottom-right-radius: 7px;
}

.btn-branch {
    border: none;
    background: none;
}

.btn-branch>h6:hover {
    text-decoration: underline;
}

a {
    color: #0366d6;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

</style>