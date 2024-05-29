<template>
    <div>
        <table class="table">
            <tbody>
                <tr v-if="displayRoot == 'false' && content.length > 0">
                    <td style="background: none;">
                        <button type="button" class="btn" @click="returnToParent">
                            <div class="d-flex justify-content-start">
                                <font-awesome-icon icon="fa-regular fa-folder" class="me-2 mt-1" style="color: #c5d1df;" />
                                <span class="dots">.</span>
                                <span class="dots">.</span>
                            </div>

                        </button>
                    </td>
                </tr>
                <tr v-for="file in content" :key="file.name">
                    <td class="w-50" style="background: none;">
                        <button v-if="file.type == 'file'" type="button" class="btn" style="color: #c5d1df;" @click="fileClicked(file.name)">
                            <font-awesome-icon icon="fa-regular fa-file" class="me-2 mt-1" style="color: #c5d1df;" />
                            {{ file.name }}
                        </button>

                        <button v-else type="button" class="btn" style="color: #c5d1df;" @click="folderClicked(file.name)">
                            <font-awesome-icon icon="fa-regular fa-folder" class="me-2 mt-1" style="color: #c5d1df;" />
                            {{ file.name }}
                        </button>
                    </td>

                    <td style="background: none;">
                        <button type="button" class="btn-last-commit-msg" @click="displayLastCommit(file.lastCommitSHA)">
                            {{ file.lastCommitMessage }}
                        </button>
                    </td>

                    <td class="d-flex justify-content-end border-0" style="background: none;">
                        <span v-if="file.lastCommitTimestamp !== null && file.lastCommitTimestamp !== '' && file.lastCommitTimestamp !== undefined"
                            class="timestamp" style="color: #c5d1df;">
                            {{ howLongAgo(file.lastCommitTimestamp) }}
                        </span>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import RepositoryService from '@/services/RepositoryService';
import TimestampService from '@/services/TimestampService';

/* eslint-disable */
export default {
    name: "RepoContent",

    props: ['avatar', 'refName', 'displayRoot', 'foldersPath', 'branch'],

    mounted() {
        localStorage.removeItem("fileContent");
        if (this.displayRoot === "true") {
            RepositoryService.getRootContent(this.$route.params.username, this.$route.params.repoName, this.refName).then(res => {
                for (let obj of res.data) {
                    this.content.push({
                        "name": obj.name, "type": obj.type, "content": obj.content, "path": obj.path, "downloadURL": obj.download_url,
                        "htmlURL": obj.html_url, "lastCommitSHA": obj.last_commit_sha, "lastCommitMessage": obj.last_commit_message, "lastCommitTimestamp": obj.last_commit_timestamp
                    });
                }
                this.sortContent();
            }).catch(err => {
                console.log(err);
            });
        } else {
            RepositoryService.getFolderContent(this.$route.params.username, this.$route.params.repoName, this.branch, this.foldersPath.slice(0, -1)).then(res => {
                console.log(res);
                for (let obj of res.data) {
                    this.content.push({
                        "name": obj.name, "type": obj.type, "content": obj.content, "path": obj.path, "downloadURL": obj.download_url,
                        "htmlURL": obj.html_url, "lastCommitSHA": obj.last_commit_sha, "lastCommitMessage": obj.last_commit_message, "lastCommitTimestamp": obj.last_commit_timestamp
                    });
                }
                this.sortContent();
            }).catch(err => {
                console.log(err);
            });
        }
    },

    data() {
        return {
            content: [],
        }
    },

    methods: {
        folderClicked(name) {
            this.$emit('folderClicked', {
                'name': name
            });
        },

        sortContent() {
            this.content.sort((a, b) => {
                if (a.type < b.type) return -1;
                if (a.type > b.type) return 1;
                if (a.name < b.name) return -1;
                if (a.name > b.name) return 1;
                return 0;
            });
        },

        returnToParent() {
            this.$emit('returnToParent');
        },

        fileClicked(name) {
            this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}/blob/${this.branch}/${this.foldersPath}${name}`);
        },

        howLongAgo(timestamp) {
            let res = TimestampService.howLongAgo(timestamp);
            console.log(res);
            return res;
        },

        displayLastCommit(sha) {
            const username = this.$route.params.username;
            const repoName = this.$route.params.repoName;
            this.$router.push(`/view/${username}/${repoName}/commit/${sha}`);
        }
    }
}
</script>

<style scoped>
.table tr {
    border: 1px solid #4b5055;
    background: none;
}

td button {
    height: 32px;
    font-size: 14px;
}

td, tr, th {
    background-color: red;
}

.dots {
    font-weight: 700;
    margin-right: 1px;
    margin-top: -1px;
    color: #c5d1df;
}

.btn-last-commit-msg {
    border: none;
    background: none;
    color: #c5d1df;
}

.btn-last-commit-msg:hover {
    color: #549bf5;
    text-decoration: underline;
}

span.timestamp {
    font-size: small;
    margin-top: 7px;
}

</style>