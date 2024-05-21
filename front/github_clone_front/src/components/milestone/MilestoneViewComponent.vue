<template>
    <div class="background is-fullheight min-vh-100">

        <RepoNavbar starting="milestones" />

        <!-- Milestone title -->
        <div class="d-flex justify-content-between px-5 pt-4">
            <div class="d-flex justify-content-start">
                <h2 class="bright me-2">{{ this.milestone.title }}</h2>
            </div>
        </div>

        <!-- Progress bar -->
        <div class="d-flex justify-content-between px-5 pt-1">
            <div class="d-flex justify-content-start">
                <div class="bright me-2">Progress bar component</div>
            </div>
        </div>

        <!-- Due date and completion percent -->
        <div class="d-flex justify-content-between px-5 pt-1">
            <div class="d-flex justify-content-start">
                <!-- Due date display -->
                <span>
                    <div class="bright me-2" v-if="this.milestone.due_date">
                        <span class="bright me-2">Due date</span>
                        <span class="bright me-2">{{ this.formatDate(this.milestone.due_date) }}</span>
                    </div>
                    <div class="bright me-2" v-else>No due date</div>
                </span>

                <!-- Completion percent -->
                <span>
                    <span class="bright bold left-margin">83%</span>
                    <span class="bright">&nbsp;complete</span>
                </span>
            </div>
        </div>

        <div class="px-5 pb-5 mt-2 w-100 d-flex justify-content-between">
            <div class="w-75 pe-5">
                <div class="description w-100 mt-2">
                    <label class="bright">Issues component</label>
                </div>

                <hr class="bright" />

                <div class="description w-100 mt-2">
                    <label class="bright">Comments component</label>
                </div>
                <!-- <CommentDisplay :username="this.$route.params.ownerUsername" :repoName="this.$route.params.repoName"
                    :entityType="'issue'" :entityId="this.$route.params.issue_id">
                </CommentDisplay> -->
            </div>

            <div class="w-25">
                <!-- <AdditionalIssueInfo :key="additionalInfoKey" :chosenMilestone="this.issue.milestone"
                    :chosenAssignee="this.issue.manager" :selectedLabels="issue.labels" :issueId="issue.id"
                    @updateAssignee="updateManagers" @updateMilestone="updateMilestone" /> -->
            </div>
        </div>
    </div>
</template>
<script>
import RepoNavbar from '@/components/repository/RepoNavbar.vue';
import MilestoneService from '@/services/MilestoneService';

import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';

export default {
    name: "MilestoneViewComponent",
    props: [],
    components: {
        RepoNavbar,
    },
    mounted() {
        this.loadMilestoneData();
    },
    data() {
        return {
            repoName: this.$route.params.repoName,
            username: this.$route.params.username,
            milestone_id: this.$route.params.milestone_id,
            milestone: Object,
        }
    },

    methods: {
        loadMilestoneData() {
            MilestoneService.getOneMilestone(this.username, this.repoName, this.milestone_id)
            .then(res => {
                this.milestone = res.data;
            })
            .catch(err => console.log(err));
        },

        formatDate(date) {
            dayjs.extend(utc);
            // Parse the given date string using Day.js, considering it as UTC time
            const parsedDate = dayjs.utc(date);

            // Format the parsed date into the desired format
            return parsedDate.format('DD.MM.YYYY.');
        },

    }
}
</script>
<style scoped>
.btn-save {
    width: 120px;
    background-color: #373e48;
    border: 1px solid #768491;
    border-radius: 5px;
}

.background {
    background-color: #22272d;
}

.bg-none {
    background: none;
    border: none;
    height: 15px;
    font-weight: 600;
}

textarea {
    min-height: 150px;
    resize: none;
    background-color: #22272d;
    border: 1px solid #768491;
    border-radius: 7px;
}

.btn-close {
    width: 120px;
    background-color: #373e48;
    border: 1px solid #768491;
    border-radius: 5px;
}

.btn-comment {
    background-color: #347d38;
    border-radius: 5px;
    border: none;
    color: white;
}

.muted {
    color: #768491;
}

.bright {
    color: #ffffff;
}

.description {
    min-height: 100px;
    background: none;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #0298db;
}

.bold {
    font-weight: bold;
}

.left-margin {
    margin-left: 2rem;
}
</style>