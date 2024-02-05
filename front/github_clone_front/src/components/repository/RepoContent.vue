<template>
    <div>
        <table class="table mt-3">
            <tbody>
                <tr v-if="displayRoot == 'false' && content.length > 0">
                    <td>
                        <button type="button" class="btn" @click="returnToParent">
                            <div class="d-flex justify-content-start">
                                <font-awesome-icon icon="fa-regular fa-folder" class="me-2 mt-1" />
                                <span class="dots">.</span>
                                <span class="dots">.</span>
                            </div>

                        </button>
                    </td>
                </tr>
                <tr v-for="file in content" :key="file.name">
                    <td>
                        <button v-if="file.type == 'file'" type="button" class="btn" @click="fileClicked(file.name)">
                            <font-awesome-icon icon="fa-regular fa-file" class="me-2 mt-1" />
                            {{ file.name }}
                        </button>

                        <button v-else type="button" class="btn" @click="folderClicked(file.name)">
                            <font-awesome-icon icon="fa-regular fa-folder" class="me-2 mt-1" />
                            {{ file.name }}
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import RepositoryService from '@/services/RepositoryService';
/* eslint-disable */
export default {
    name: "RepoContent",

    props: ['avatar', 'refName', 'displayRoot', 'foldersPath', 'branch'],

    mounted() {
        if (this.displayRoot === "true") {
            RepositoryService.getRootContent(this.$route.params.username, this.$route.params.repoName, this.refName).then(res => {
                for (let obj of res.data) {
                    this.content.push({
                        "name": obj.name, "type": obj.type, "content": obj.content, "path": obj.path, "downloadURL": obj.download_url,
                        "htmlURL": obj.html_url, "lastCommitSHA": obj.last_commit_sha
                    });
                }
            }).catch(err => {
                console.log(err);
            });
        } else {
            RepositoryService.getFolderContent(this.$route.params.username, this.$route.params.repoName, this.branch, this.foldersPath.slice(0, -1)).then(res => {
                console.log(res);
                for (let obj of res.data) {
                    this.content.push({
                        "name": obj.name, "type": obj.type, "content": obj.content, "path": obj.path, "downloadURL": obj.download_url,
                        "htmlURL": obj.html_url, "lastCommitSHA": obj.last_commit_sha
                    });
                }
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

        returnToParent() {
            this.$emit('returnToParent');
        },

        fileClicked(name) {
            this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}/blob/${this.branch}/${this.foldersPath}${name}`);
        }
    }
}
</script>

<style scoped>
.table tr {
    border: 1px solid #d6d9dd;
}

td button {
    height: 32px;
    font-size: 14px;
}

.dots {
    font-weight: 700;
    margin-right: 1px;
    margin-top: -1px;
}
</style>