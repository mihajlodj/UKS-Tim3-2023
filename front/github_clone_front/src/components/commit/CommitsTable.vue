<template>
    <div>
        <div class="w-100 num-commits py-2 px-3 mt-2">
            <h5 v-if="commits" class="bright">{{ commits.length }} commit(s) </h5>
        </div>
        <table class="w-100">
            <thead>
                <tr>
                    <th scope="col" class="author">Author</th>
                    <th scope="col" class="sha">SHA1</th>
                    <th scope="col" class="message">Message</th>
                    <th scope="col" class="date">Date</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="c in commits" :key="c.hash">
                    <td>
                        <div class="d-flex justify-content-start" style="cursor: pointer;" @click="$router.push(`/profile/${c.author.username}`)">
                            <img class="avatar me-1" :src="c.author.avatar" />
                            <label class="bright">{{ c.author.username }}</label>
                        </div>
                    </td>
                    <td>
                        <div class="d-flex justify-content-start">
                            <button type="button" class="btn-copy" @click="copySha(c.hash)">
                                <font-awesome-icon icon="fa-regular fa-copy"></font-awesome-icon>
                            </button>
                            <button type="button" class="btn-sha" @click="displayCommit(c.hash)">
                                <label class="bright">{{ c.hash.slice(0, 7) }}</label>
                            </button>
                        </div>
                    </td>
                    <td>
                        <label class="msg" v-html="formattedMessage(c.message)"></label>
                    </td>
                    <td class="date">
                        <label>{{ formatDate(c.timestamp) }}</label>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import { toast } from 'vue3-toastify';

export default {
    name: "CommitsTable",
    props: ['commits', 'branch'],
    data() {
        return {

        }
    },

    methods: {
        async copySha(sha) {
            try {
                await navigator.clipboard.writeText(sha);
                toast("Copied to clipboard", {
                    autoClose: 500,
                    type: 'info',
                    position: toast.POSITION.BOTTOM_RIGHT,
                    theme: toast.THEME.DARK
                });
            } catch ($e) {
                console.log('cannot copy')
            }
        },

        formatDate(dateStr) {
            const date = new Date(dateStr);
            date.setHours(date.getHours() + 2);
            const newTimestamp = date.toISOString();
            let arr = newTimestamp.split("T");
            return `${arr[0]} ${arr[1].slice(0, 5)}`
        },

        displayCommit(sha) {
            this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}/${this.branch}/commit/${sha}`);
        },

        formattedMessage(message) {
            const username = this.$route.params.username;
            const repoName = this.$route.params.repoName;

            return message.replace(/#(\d+)/g, (match, issueId) => {
                return `<a href="/view/${username}/${repoName}/issues/${issueId}">${match}</a>`;
            });
        }
    }
}

</script>

<style scoped>
div {
    color: white;
}

.bright {
    color: #adbbc8;
}

.muted {
    color: #768491;
}

.num-commits {
    background-color: #2c333b;
    border-top-right-radius: 7px;
    border-top-left-radius: 7px;
    border: 1px solid #6e7b88;
}

.date {
    width: 120px;
}

.sha {
    width: 100px;
}

td.date {
    font-size: small;
}

.avatar {
    width: 25px;
    height: 25px;
    border-radius: 50%;
}

th,
td {
    background-color: #1c2127;
    color: #adbbc8;
    font-weight: 600;
    border: 1px solid #6e7b88;
    padding: 5px 7px;
}

td {
    font-weight: 500;
}

.msg {
    font-size: 14px;
}

.btn-sha {
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    background-color: #373e48;
    border: 1px solid #6e7b88;
    min-width: 70px;
}

.btn-copy {
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
    background-color: #373e48;
    border: 1px solid #6e7b88;
}

.fa-copy {
    color: #adbbc8;
}

.btn-sha label:hover {
    cursor: pointer;
}

a {
    color: #0366d6;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}
</style>