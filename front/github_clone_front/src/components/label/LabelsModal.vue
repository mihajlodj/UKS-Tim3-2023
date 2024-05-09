<template>
    <div class="contain p-2" :style="{ top: y + 'px', left: x + 'px', width: w + 'px' }" @click="preventClose">
        <h6 class="mt-1 bright small">Apply labels to this pull request</h6>
        <hr class="muted" />

        <!-- One label container -->
        <div class="container" v-for="(label, index) in labels" :key="index">
            <div class="row">
                <div class="col-md-1">
                    <svg viewBox="0 0 16 16" class="" aria-hidden="true" width="16" height="16" v-if="label.isSelected">
                        <path
                            d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z">
                        </path>
                    </svg>
                </div>
                <div class="col-md-7">
                    <p class="muted small mt-1">{{ label.name }}</p>
                </div>
                <div class="col-md-4 text-end">
                    <!-- Add button -->
                    <button class="button-color" @click="linkLabel(label.id)" :disabled="label.isSelected === true">
                        <svg viewBox="0 0 16 16" class="" aria-hidden="true" width="16" height="16">
                            <path
                                d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z">
                            </path>
                        </svg>
                    </button>

                    <!-- Remove button -->
                    <button class="button-color" @click="unlinkLabel(label.id)" :disabled="label.isSelected === false">
                        <svg viewBox="0 0 16 16" class="" aria-hidden="true" width="16" height="16">
                            <path
                                d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.749.749 0 0 1 1.275.326.749.749 0 0 1-.215.734L9.06 8l3.22 3.22a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L8 9.06l-3.22 3.22a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06Z">
                            </path>
                        </svg>
                    </button>
                </div>
            </div>
            <hr class="muted" />
        </div>

        <div id="no-labels" v-if="labels.length === 0">
            <hr class="muted" />
            <label class="mb-1 muted">Nothing to show</label>
        </div>

    </div>
</template>

<script>
import { toast } from 'vue3-toastify';
import LabelService from '@/services/LabelService';

export default {
    name: "LabelsModal",
    props: ["x", "y", "w", "selectedLabelsProp", "entityType", "entityId"],     // entityType: milestone, issue, pull_request; entityId is id of entytyType

    data() {
        return {
            username: this.$route.params.username,
            repo: this.$route.params.repoName,
            labels: [],
            selectedLabels: this.selectedLabelsProp,
        }
    },

    mounted() {
        this.loadLabels();
    },

    methods: {

        loadLabels() {
            this.labels = [];
            this.copySelectedLabels();
            this.getAllLabels();
        },

        getAllLabels() {
            LabelService.getAllLabels(this.username, this.repo)
                .then(res => {
                    for (let label of res.data) {
                        if (!this.labels.find(l => l.id === label.id)) {
                            label['isSelected'] = false;
                            this.labels.push(label);
                        }
                    }
                })
                .catch(err => {
                    console.log(err);
                    toast("Error occured while getting Labels!", {
                        autoClose: 1000,
                        type: 'error',
                        position: toast.POSITION.BOTTOM_RIGHT,
                        theme: toast.THEME.DARK
                    });
                });
        },

        copySelectedLabels() {
            for (let label of this.selectedLabels) {
                label['isSelected'] = true;
                this.labels.push(label);
            }
        },

        linkLabel(labelId) {
            if (this.entityType === "milestone") {
                LabelService.linkLabelAndMilestone(this.username, this.repo, labelId, this.entityId)
                    .then(res => {
                        console.log(res);
                        toast("Label added!", {
                            autoClose: 500,
                            type: 'success',
                            position: toast.POSITION.BOTTOM_RIGHT,
                            theme: toast.THEME.DARK
                        });
                        const label = this.labels.find(l => l.id === labelId);
                        label.isSelected = true;
                        this.selectedLabels.push(label);
                    })
                    .catch(err => {
                        console.log(err);
                        toast("Error occured while adding label!", {
                            autoClose: 1000,
                            type: 'error',
                            position: toast.POSITION.BOTTOM_RIGHT,
                            theme: toast.THEME.DARK
                        });
                    });
            }
            else if (this.entityType === "issue") {
                LabelService.linkLabelAndIssue(this.username, this.repo, labelId, this.entityId)
                    .then(res => {
                        console.log(res);
                        toast("Label added!", {
                            autoClose: 500,
                            type: 'success',
                            position: toast.POSITION.BOTTOM_RIGHT,
                            theme: toast.THEME.DARK
                        });
                        const label = this.labels.find(l => l.id === labelId);
                        label.isSelected = true;
                        this.selectedLabels.push(label);
                    })
                    .catch(err => {
                        console.log(err);
                        toast("Error occured while adding label!", {
                            autoClose: 1000,
                            type: 'error',
                            position: toast.POSITION.BOTTOM_RIGHT,
                            theme: toast.THEME.DARK
                        });
                    });
            }
            else if (this.entityType === "pull_request") {
                LabelService.linkLabelAndPullRequest(this.username, this.repo, labelId, this.entityId)
                    .then(res => {
                        console.log(res);
                        toast("Label added!", {
                            autoClose: 500,
                            type: 'success',
                            position: toast.POSITION.BOTTOM_RIGHT,
                            theme: toast.THEME.DARK
                        });
                        const label = this.labels.find(l => l.id === labelId);
                        label.isSelected = true;
                        this.selectedLabels.push(label);
                    })
                    .catch(err => {
                        console.log(err);
                        toast("Error occured while adding label!", {
                            autoClose: 1000,
                            type: 'error',
                            position: toast.POSITION.BOTTOM_RIGHT,
                            theme: toast.THEME.DARK
                        });
                    });
            }
            else {
                console.log("ERROR: entityType prop invalid!");
            }
        },

        async unlinkLabel(labelId) {
            if (this.entityType === "milestone") {
                console.log("TODO unlink milestone");
            }
            else if (this.entityType === "issue") {
                console.log("TODO unlink issue");
            }
            else if (this.entityType === "pull_request") {
                LabelService.unlinkLabelAndPullRequest(this.username, this.repo, labelId, this.entityId)
                    .then(res => {
                        console.log(res);
                        toast("Label removed!", {
                            autoClose: 500,
                            type: 'success',
                            position: toast.POSITION.BOTTOM_RIGHT,
                            theme: toast.THEME.DARK
                        });
                        const label = this.labels.find(l => l.id === labelId);
                        label.isSelected = false;
                        this.removeLabelFromSelectedLabels(labelId);
                    })
                    .catch(err => {
                        console.log(err);
                        toast("Error occured while removing label!", {
                            autoClose: 1000,
                            type: 'error',
                            position: toast.POSITION.BOTTOM_RIGHT,
                            theme: toast.THEME.DARK
                        });
                    });
            }
            else {
                console.log("ERROR: entityType prop invalid!");
            }
        },

        removeLabelFromSelectedLabels(id) {
            const index = this.selectedLabels.findIndex(item => item.id === id);
            if (index !== -1) {
                this.selectedLabels.splice(index, 1);
            }
        },

        close(e) {
            e.preventDefault();
            console.log(e.target.classList);
            if ("cover" in e.target.classList) {
                this.$emit('closeModal', {
                    name: 'labels'
                });
            }
        }
    }
}
</script>

<style scoped>
.contain {
    position: absolute;
    border-radius: 10px;
    z-index: 1;
    background-color: #2c333b;
    border: 1px solid #434c55;
}


.bright {
    color: #adbbc8;
}

.muted {
    color: #768491;
}

hr {
    margin: 15px 0px;
}

input {
    border-radius: 5px;
    background-color: #22272d;
    border: 1px solid #434c55;
}

.small {
    font-size: small;
}

.button-color {
    background-color: #2c333b;
    color: #adbbc8;
    border: none;
}

.button-color:hover {
    background-color: #434c55;
}
</style>