<template>
    <div>
        <table class="table mt-3">
            <tbody>
                <tr v-for="file in content" :key="file.name">
                    <td>
                        <button type="button" class="btn">
                            <font-awesome-icon v-if="file.type == 'file'" icon="fa-regular fa-file" class="me-2 mt-1" />
                            <font-awesome-icon v-else icon="fa-regular fa-folder" class="me-2 mt-1" />
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

    props: ['avatar', 'refName'],

    mounted() {
        RepositoryService.getRootContent(this.$route.params.username, this.$route.params.repoName, this.refName).then(res => {
            for (let obj of res.data) {
                this.content.push({
                    "name": obj.name, "type": obj.type, "content": obj.content, "path": obj.path, "downloadURL": obj.download_url,
                    "htmlURL": obj.html_url, "lastCommitSHA": obj.last_commit_sha
                });
            }
        }).catch(err => {
            console.log(err);
        })
    },

    data() {
        return {
            content: [],
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
</style>