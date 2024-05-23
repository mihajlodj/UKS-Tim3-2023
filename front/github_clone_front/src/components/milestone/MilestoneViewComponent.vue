<template>
    <div class="background is-fullheight min-vh-100">

        <RepoNavbar starting="milestones" />

        <!-- Milestone title -->
        <div class="d-flex justify-content-between px-5 pt-4 w-75">
            <div class="d-flex justify-content-start">
                <h2 class="bright me-2">{{ this.milestone.title }}</h2>
            </div>
            <!-- Milestone status -->
            <div style="margin-top: 6px;" class="pe-3">
                <!-- Open icon -->
                <div class="flex-shrink-0 mb-2 flex-self-start flex-md-self-center openbutton"
                    v-if="this.milestone.state === 'Open'">
                    <span title="Status: Open" data-view-component="true"
                        class="State State--open d-flex flex-items-center">
                        <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16"
                            data-view-component="true"
                            class="octicon octicon-issue-opened flex-items-center mr-1 margin-right margin-top white-fill">
                            <path d="M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z"></path>
                            <path d="M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0 6.5 6.5 0 0 0-13 0Z">
                            </path>
                        </svg>
                        <div class="bright">Open</div>
                    </span>
                </div>

                <!-- Closed icon -->
                <div class="flex-shrink-0 mb-2 flex-self-start flex-md-self-center closebutton" v-else>
                    <span title="Status: Open" data-view-component="true"
                        class="State State--open d-flex flex-items-center">
                        <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16"
                            data-view-component="true"
                            class="octicon octicon-issue-closed flex-items-center mr-1 margin-right margin-top white-fill">
                            <path
                                d="M11.28 6.78a.75.75 0 0 0-1.06-1.06L7.25 8.69 5.78 7.22a.75.75 0 0 0-1.06 1.06l2 2a.75.75 0 0 0 1.06 0l3.5-3.5Z">
                            </path>
                            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0Zm-1.5 0a6.5 6.5 0 1 0-13 0 6.5 6.5 0 0 0 13 0Z">
                            </path>
                        </svg>
                        <div class="bright">Closed</div>
                    </span>
                </div>
            </div>
        </div>

        <!-- Progress bar -->
        <div class="px-5 pb-1 mt-1">
            <div class="w-75 pe-5">
                <ProgressBar :value="this.completedPercentage" :showValue="false"
                    style="background-color: white; height: 20px;"></ProgressBar>
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
                    <span class="bright bold left-margin">{{ this.completedPercentage }}%</span>
                    <span class="bright">&nbsp;complete</span>
                </span>
            </div>
        </div>

        <div class="px-5 pb-5 mt-2 w-100 d-flex justify-content-between">
            <div class="w-75 pe-5">
                <hr class="bright" />
                <div class="w-100 mt-2">
                    <IssueTable :issues-for-display="this.issues"></IssueTable>
                </div>

                <hr class="bright" />

                <CommentDisplay :username="this.username" :repoName="this.repoName" :entityType="'milestone'"
                    :entityId="this.milestone_id">
                </CommentDisplay>

                <div class="mt-3">
                    <div class="w-100 d-flex justify-content-end mt-2">
                        <button v-if="this.milestone.state === 'Open'" type="button" class="btn btn-warning bright p-2"
                            @click="this.close()">
                            Close milestone
                        </button>
                        <button v-else type="button" class="btn btn-warning bright p-2" @click="this.reopen()">
                            Reopen milestone
                        </button>
                    </div>
                </div>

            </div>

            <div class="w-25">
                <AdditionalMilestoneInfo :selectedLabels="this.milestone.labels" :milestoneId="1" />
            </div>
        </div>
    </div>
</template>
<script>
import RepoNavbar from '@/components/repository/RepoNavbar.vue';
import CommentDisplay from '@/components/comment/CommentDisplay.vue';
import AdditionalMilestoneInfo from '@/components/milestone/AdditionalMilestoneInfo.vue';
import IssueTable from '@/components/issue/IssueTable.vue';

import MilestoneService from '@/services/MilestoneService';
import IssueService from '@/services/IssueService';

import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';
import { toast } from 'vue3-toastify';
import ProgressBar from 'primevue/progressbar';

export default {
    name: "MilestoneViewComponent",
    props: [],
    components: {
        RepoNavbar,
        ProgressBar,
        CommentDisplay,
        AdditionalMilestoneInfo,
        IssueTable,
    },
    mounted() {
        this.loadMilestoneData();
        this.loadIssues();
    },
    data() {
        return {
            repoName: this.$route.params.repoName,
            username: this.$route.params.username,
            milestone_id: this.$route.params.milestone_id,
            milestone: Object,
            issues: [],
            numberOfOpenIssues: 0,
            numberOfClosedIssues: 0,
            completedPercentage: 0,
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

        loadIssues() {
            IssueService.getIssuesForMilestone(this.username, this.repoName, this.milestone_id)
                .then(res => {
                    this.issues = res.data;
                    this.calculateNumberOfIssues();
                    this.calculateCompletedPercentage();
                })
                .catch(err => console.log(err));
        },

        calculateNumberOfIssues() {
            const issueCounts = this.issues.reduce((counts, issue) => {
                if (issue.open) {
                    counts.open += 1;
                } else {
                    counts.closed += 1;
                }
                return counts;
            }, { open: 0, closed: 0 });
            this.numberOfOpenIssues = issueCounts.open;
            this.numberOfClosedIssues = issueCounts.closed;
        },

        calculateCompletedPercentage() {
            let totalNumberOfIssues = this.numberOfOpenIssues + this.numberOfClosedIssues;
            let percentage = (this.numberOfClosedIssues * 100) / totalNumberOfIssues;
            let wholePercentage = Math.floor(percentage);
            this.completedPercentage = wholePercentage;
        },

        close() {
            MilestoneService.closeMilestone(this.username, this.repoName, this.milestone_id)
                .then(res => {
                    console.log(res);
                    toast("Milestone closed!", {
                        autoClose: 500,
                        type: 'success',
                        position: toast.POSITION.BOTTOM_RIGHT,
                        theme: toast.THEME.DARK
                    });
                    this.loadMilestoneData();
                })
                .catch(err => {
                    console.log(err);
                    toast("Milestone closure failed.", {
                        autoClose: 1000,
                        type: 'error',
                        position: toast.POSITION.BOTTOM_RIGHT,
                        theme: toast.THEME.DARK
                    });
                });
        },

        reopen() {
            MilestoneService.reOpenMilestone(this.username, this.repoName, this.milestone_id)
                .then(res => {
                    console.log(res);
                    toast("Milestone reopened!", {
                        autoClose: 500,
                        type: 'success',
                        position: toast.POSITION.BOTTOM_RIGHT,
                        theme: toast.THEME.DARK
                    });
                    this.loadMilestoneData();
                })
                .catch(err => {
                    console.log(err);
                    toast("Milestone reopening failed.", {
                        autoClose: 1000,
                        type: 'error',
                        position: toast.POSITION.BOTTOM_RIGHT,
                        theme: toast.THEME.DARK
                    });
                });
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

.margin-right {
    margin-right: 10px;
}

.margin-top {
    margin-top: 2px;
}

.background-color {
    background-color: #ffffff;
}

.white-fill {
    fill: white;
}

.openbutton {
    -webkit-text-size-adjust: 100%;

    color-scheme: dark;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
    word-wrap: break-word;
    box-sizing: border-box;
    align-items: center !important;
    display: flex !important;
    border-radius: 2em;
    text-align: center;
    white-space: nowrap;

    --text-body-size-medium: 0.875rem;
    font-size: var(--text-body-size-medium);

    --base-text-weight-medium: 500;
    font-weight: var(--base-text-weight-medium);

    --control-medium-lineBoxHeight: 1.25rem;
    line-height: var(--control-medium-lineBoxHeight);

    --control-medium-paddingInline-normal: 0.75rem;
    padding: 5px var(--control-medium-paddingInline-normal);

    --borderWidth-thin: max(1px, 0.0625rem);
    border: var(--borderWidth-thin) solid #0000;

    --bgColor-open-emphasis: #238636;
    background-color: var(--bgColor-open-emphasis);

    --fgColor-onEmphasis: #ffffff;
    color: var(--fgColor-onEmphasis);

    --base-size-8: 0.5rem;
    margin-right: var(--base-size-8);
}

.closebutton {
    -webkit-text-size-adjust: 100%;

    color-scheme: dark;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
    word-wrap: break-word;
    box-sizing: border-box;
    align-items: center !important;
    display: flex !important;
    border-radius: 2em;
    text-align: center;
    white-space: nowrap;

    --text-body-size-medium: 0.875rem;
    font-size: var(--text-body-size-medium);

    --base-text-weight-medium: 500;
    font-weight: var(--base-text-weight-medium);

    --control-medium-lineBoxHeight: 1.25rem;
    line-height: var(--control-medium-lineBoxHeight);

    --control-medium-paddingInline-normal: 0.75rem;
    padding: 5px var(--control-medium-paddingInline-normal);

    --borderWidth-thin: max(1px, 0.0625rem);
    border: var(--borderWidth-thin) solid #0000;

    --bgColor-open-emphasis: #238636;
    background-color: plum;

    --fgColor-onEmphasis: #ffffff;
    color: var(--fgColor-onEmphasis);

    --base-size-8: 0.5rem;
    margin-right: var(--base-size-8);
}
</style>