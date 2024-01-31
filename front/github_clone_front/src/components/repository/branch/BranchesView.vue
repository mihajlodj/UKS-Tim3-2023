<template>
    <div>
        <RepoNavbar />

        <div class="container w-75 mt-4">
            <div class="d-flex justify-content-between">
                <h3>Branches</h3>
                <button type="button" class="btn btn-create">New branch</button>
            </div>

            <ul class="nav nav-tabs mt-3">
                <li class="nav-item">
                    <button :class="activeAll ? 'nav-link active' : 'nav-link'" @click="setActiveAll">All</button>
                </li>
                <li class="nav-item">
                    <button :class="!activeAll ? 'nav-link active' : 'nav-link'" @click="setActiveYours">Yours</button>
                </li>
            </ul>

            <table class="table mt-2">
                <thead>
                    <tr>
                        <th scope="col" class="th-branch">Branch</th>
                        <th scope="col" class="th-updated">Updated</th>
                        <th scope="col" class="th-pull">Pull request</th>
                        <th scope="col" class="th-trash"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="b in targetList" :key="b.name">
                        <td>{{ b.name }}</td>
                        <td>
                            <div v-if="b.updatedAvatar !== undefined">
                                <button type="button" class="btn-avatar me-2">
                                    <img :src="b.updatedAvatar" alt="avatar" class="updated-avatar" />
                                </button>
                                <span class="how-long">{{ howLongAgo(b.updatedTimestamp) }}</span>
                            </div>
                        </td>
                        <td>
                            <button v-if="b.prStatus !== undefined" type="button" class="btn-pr">
                                <img v-if="b.prStatus == 'Closed'" alt="pr" src="../../../assets/closed_pr_red.png"
                                    class="img-pr mb-1" />
                                <img v-if="b.prStatus == 'Open'" alt="pr" src="../../../assets/open_pr_green.png"
                                    class="img-pr mb-1" />
                                <img v-if="b.prStatus == 'Merged'" alt="pr" src="../../../assets/merged_pr_purple.png"
                                    class="img-pr mb-1" />
                                <span>#{{ b.prId }}</span>
                            </button>
                        </td>
                        <td>
                            <button type="button" class="btn-trash" @click="deleteBranch">
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
                    "prStatus": item.pr_status,
                    "createdBy": item.created_by
                });
            }
            this.createdByUser = this.branchData.filter(item => item.createdBy === this.$route.params.username);
            this.targetList = this.branchData;
            console.log(this.branchData);
        }).catch(err => {
            console.log(err);
        });
    },

    data() {
        return {
            selectedTab: 'all',
            branchData: [],
            createdByUser: [],
            activeAll: true,
            targetList: []
        }
    },

    methods: {
        deleteBranch() {

        },

        setActiveAll() {
            this.activeAll = true;
            this.targetList = this.branchData;
        },

        setActiveYours() {
            this.activeAll = false;
            this.targetList = this.createdByUser;
        },

        howLongAgo(timestamp) {
            const currentDate = new Date();
            const previousDate = new Date(timestamp);
            const seconds = Math.floor((currentDate - previousDate) / 1000);
            let interval = Math.floor(seconds / 31536000);

            if (interval >= 1) {
                return interval + " year" + (interval === 1 ? "" : "s") + " ago";
            }
            interval = Math.floor(seconds / 2592000);
            if (interval >= 1) {
                return interval + " month" + (interval === 1 ? "" : "s") + " ago";
            }
            interval = Math.floor(seconds / 86400);
            if (interval >= 1) {
                return interval + " day" + (interval === 1 ? "" : "s") + " ago";
            }
            interval = Math.floor(seconds / 3600);
            if (interval >= 1) {
                return interval + " hour" + (interval === 1 ? "" : "s") + " ago";
            }
            interval = Math.floor(seconds / 60);
            if (interval >= 1) {
                return interval + " minute" + (interval === 1 ? "" : "s") + " ago";
            }
            return Math.floor(seconds) + " second" + (Math.floor(seconds) === 1 ? "" : "s") + " ago";
        }
    },
}
</script>

<style scoped>
.th-branch,
.th-updated,
.th-pull,
.th-trash {
    background-color: #f7f8fa;
    color: #656e77;
    font-weight: 600;
}

.btn-create,
.btn-create:hover {
    color: white;
    background-color: #20883d;
    height: 90%;
}

.th-branch {
    width: 42%;
}

.th-updated {
    width: 30%
}

.th-pull {
    width: 22%;
}

.btn-trash {
    padding: 2px 10px;
    background: none;
    border: none;
}

.btn-trash:hover {
    background-color: #f7f8fa;
}

.updated-avatar {
    height: 25px;
    border-radius: 50%;
}

.btn-avatar {
    padding: 0%;
    border: none;
    background: none;
}

.how-long {
    font-size: small;
}

.img-pr {
    height: 12px;
    margin-right: 7px;
}

.btn-pr {
    background: none;
    border: 1px solid #656e77;
    color: black;
    padding: 0px 10px;
    margin: 4px 2px;
    border-radius: 16px;
    font-size: small;
    color: #656e77;
}

table {
    border: 1px solid #d6dce3;
}

.nav-link,
.nav-link:hover {
    color: black;
}
</style>