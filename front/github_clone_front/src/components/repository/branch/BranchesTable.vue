<template>
    <div>
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
                    <td>
                        <button type="button" class="btn-name px-2" @click="viewBranch(b.name)">
                            {{ b.name }}
                        </button>
                    </td>
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
                        <button type="button" class="btn-trash" @click="deleteBranch(b.name)">
                            <font-awesome-icon icon="fa-regular fa-trash-can" />
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import BranchService from '@/services/BranchService';
import TimestampService from '@/services/TimestampService';
import { toast } from 'vue3-toastify';

export default {
    name: 'BranchesTable',

    props: ['targetList'],

    methods: {
        viewBranch(name) {
            this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}?chosen=${name}`);
        },

        deleteBranch(name) {
            BranchService.deleteBranch(this.$route.params.repoName, name).then(res => {
                console.log(res)
                this.update(name);
                toast(`Branch ${name} has been deleted`, {
                    autoClose: 1000,
                    type: 'success',
                    position: toast.POSITION.BOTTOM_RIGHT
                });
            }).catch(err => {
                console.log(err);
            });
        },

        update(name) {
            this.$emit('branchDeleted', {
                "name": name
            });
        },

        howLongAgo(timestamp) {
            return TimestampService.howLongAgo(timestamp);
        }
    }
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

.btn-name {
    border: none;
    background-color: #def3fd;
    color: #0969da;
    border-radius: 7px;
    padding-bottom: 4px;
}

.btn-name:hover {
    text-decoration: underline;
}
</style>