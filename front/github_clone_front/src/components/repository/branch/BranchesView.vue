<template>
    <div>
        <RepoNavbar />

        <div class="container w-75 mt-4">
            <div class="d-flex justify-content-between">
                <h3>Branches</h3>
                <button type="button" class="btn btn-create">New branch</button>
            </div>

            <table class="table mt-3">
                <thead>
                    <tr>
                        <th scope="col" class="th-branch">Branch</th>
                        <th scope="col" class="th-updated">Updated</th>
                        <th scope="col" class="th-pull">Pull request</th>
                        <th scope="col" class="th-trash"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="b in branchData" :key="b.name">
                        <td>{{ b.name }}</td>
                        <td></td>
                        <td></td>
                        <td>
                            <button type="button" class="btn btn-trash" @click="deleteBranch">
                                <font-awesome-icon icon="fa-regular fa-trash-can" />
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import RepoNavbar from '@/components/repository/RepoNavbar.vue'
import BranchService from '@/services/BranchService'

export default {
    name: 'BranchesView',
    components: {
        RepoNavbar
    },

    mounted() {
        BranchService.getAllBranches(this.$route.params.username, this.$route.params.repoName).then(res => {
            for (let item of res.data) {
                this.branchData.push({
                    "name": item.name,
                    "updatedUsername": item.updated_username,
                    "updatedAvatar": item.updated_avatar,
                    "updatedTimestamp": item.updated_timestamp,
                    "prId": item.pr_id,
                    "prStatus": item.pr_status
                });
            }
            console.log(this.branchData);
        }).catch(err => {
            console.log(err);
        });
    },

    data() {
        return {
            selectedTab: 'all',
            branchData: []
        }
    },

    methods: {
        deleteBranch() {

        }
    }
}
</script>

<style scoped>

.th-branch, .th-updated, .th-pull, .th-trash {
    background-color: #f7f8fa;
    color: #656e77;
    font-weight: 600;
}

.btn-create, .btn-create:hover {
    color: white;
    background-color: #20883d;
    height: 90%;
}

.th-branch {
    width: 42%;
}

.th-updated {
    width: 25%
}

.btn-trash {
    padding: 0;
}
</style>