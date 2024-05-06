<template>
    <div>
        <RepoNavbar starting="milestones" />
    </div>

    <!-- Modal add -->
    <div class="modal fade" id="exampleModalAdd" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
        aria-hidden="true">
        <div class="modal-dialog" role="document" style="background-color: #24292e; border: 2px solid;">
            <div class="modal-content" style="background-color: #24292e;">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel" style="color: beige">Create new label</h5>
                    <button type="button" id="addModalCloseId" class="btn-close" data-bs-dismiss="modal"
                        aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <AddLabelComponent @labelAdded="labelAdded" />
                </div>
            </div>
        </div>
    </div>

    <div style="background-color: #24292e; height: 100vh;">
        <div class="container w-75 pt-4" style="background-color: #24292e;">
            <div class="d-flex justify-content-between">
                <h3 style="color: beige;">Labels</h3>
                <button v-if="canModifyLabels()" type="button" data-bs-toggle="modal" data-bs-target="#exampleModalAdd"
                    class="btn btn-create">
                    Create new label
                </button>
            </div>
        </div>
        <div style="background-color: #24292e;">
            <table class="tg mt-5"
                style="margin-left:auto;margin-right:auto; border-radius: 10px; background-color: #24292e;">
                <thead style="background-color: #24292e;">
                    <tr style="background-color: #24292e;">
                        <th class="tg-lboi" style="background-color: #24292e; color: beige;">Name</th>
                        <th class="tg-lboi" style="background-color: #24292e; color: beige;">Description</th>
                        <th class="tg-lboi" style="background-color: #24292e;"></th>
                        <th class="tg-lboi" style="background-color: #24292e;"></th>
                    </tr>
                </thead>
                <tbody style="background-color: #24292e;">
                    <tr v-for="(item, index) in this.labels" :key="index">
                        <td class="tg-c7q8">{{ item.name }}</td>
                        <td class="tg-c7q8">{{ item.description }}</td>
                        <td class="tg-c7q8">
                            <button v-if="canModifyLabels()" type="button" class="btn btn-primary"
                                data-bs-toggle="modal" data-bs-target="#exampleModalUpdate"
                                @click="setSelectedLabel(item)">Edit
                            </button>
                        </td>
                        <td class="tg-c7q8">
                            <button v-if="canModifyLabels()" type="button" class="btn btn-danger"
                                @click="deleteMilestone(item.title)">Delete
                            </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

</template>
<script>
import { toast } from 'vue3-toastify';
import RepoNavbar from '@/components/repository/RepoNavbar.vue';
import AddLabelComponent from '@/components/label/AddLabelComponent.vue';
import LabelService from '@/services/LabelService';

export default {
    name: 'ListLabelsComponent',
    components: {
        RepoNavbar,
        AddLabelComponent
    },
    mounted() {
        this.getAllLabelsForRepo();
    },
    data() {
        return {
            username: this.$route.params.username,
            repo: this.$route.params.repoName,
            labels: [],
            selectedLabel: null,
        }
    },
    methods: {

        getAllLabelsForRepo() {
            LabelService.getAllLabels(this.username, this.repo)
                .then(res => {
                    console.log(res.data);
                    this.labels = res.data;
                })
                .catch(err => {
                    console.log(err);
                    toast("Error occured while getting Labels!", {
                        autoClose: 1000,
                        type: 'error',
                        position: toast.POSITION.BOTTOM_RIGHT,
                        theme: toast.THEME.DARK
                    });
                })
        },

        setSelectedLabel(label) {
            this.selectedLabel = label;
        },

        labelAdded() {
            this.closeAddModal();
            this.getAllLabelsForRepo();
        },

        closeAddModal() {
            document.getElementById('addModalCloseId').click();
        },

        canModifyLabels() {
            const role = localStorage.getItem(this.$route.params.repoName);
            return role === "Owner" || role === "Developer" || role === "Maintainer";
        },

    }
}

</script>
<style scoped>
.tg {
    border-collapse: collapse;
    border-color: #bbb;
    border-spacing: 0;
    border-radius: 10px;
}

.tg td {
    border-color: #bbb;
    border-style: solid;
    border-bottom: 0px;
    color: beige;
    font-family: Arial, sans-serif;
    font-size: 14px;
    overflow: hidden;
    padding: 10px 5px;
    word-break: normal;
}

.tg th {
    border-color: #bbb;
    border-style: solid;
    border-bottom: 0px;
    color: #493F3F;
    font-family: Arial, sans-serif;
    font-size: 14px;
    font-weight: normal;
    overflow: hidden;
    padding: 10px 5px;
    word-break: normal;
}

.tg .tg-cly1 {
    text-align: center;
    vertical-align: middle
}

.tg .tg-lboi {
    /* border-color: inherit; */
    text-align: center;
    vertical-align: middle
}

.tg .tg-c7q8 {
    text-align: center;
    vertical-align: middle;
    padding: 3em;
}

.btn-create,
.btn-create:hover {
    color: white;
    background-color: #20883d;
    height: 90%;
}

.dark-color {
    background-color: #24292e;
}
</style>
