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
                    <span class="bright bold left-margin">{{ this.completedPercentage }}%</span>
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
import IssueService from '@/services/IssueService';

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
    --base-size-2: 0.125rem;
    --base-size-4: 0.25rem;
    --base-size-6: 0.375rem;
    --base-size-8: 0.5rem;
    --base-size-12: 0.75rem;
    --base-size-16: 1rem;
    --base-size-20: 1.25rem;
    --base-size-24: 1.5rem;
    --base-size-28: 1.75rem;
    --base-size-32: 2rem;
    --base-size-36: 2.25rem;
    --base-size-40: 2.5rem;
    --base-size-44: 2.75rem;
    --base-size-48: 3rem;
    --base-size-64: 4rem;
    --base-size-80: 5rem;
    --base-size-96: 6rem;
    --base-size-112: 7rem;
    --base-size-128: 8rem;
    --base-text-weight-light: 300;
    --base-text-weight-normal: 400;
    --base-text-weight-medium: 500;
    --base-text-weight-semibold: 600;
    --boxShadow-thin: inset 0 0 0 max(1px, 0.0625rem);
    --boxShadow-thick: inset 0 0 0 max(2px, 0.125rem);
    --boxShadow-thicker: inset 0 0 0 max(4px, 0.25rem);
    --borderWidth-thin: max(1px, 0.0625rem);
    --borderWidth-thick: max(2px, 0.125rem);
    --borderWidth-thicker: max(4px, 0.25rem);
    --borderRadius-small: 0.1875rem;
    --borderRadius-medium: 0.375rem;
    --borderRadius-large: 0.75rem;
    --borderRadius-full: 624.9375rem;
    --outline-focus-offset: -0.125rem;
    --outline-focus-width: 0.125rem;
    --breakpoint-xsmall: 20rem;
    --breakpoint-small: 34rem;
    --breakpoint-medium: 48rem;
    --breakpoint-large: 63.25rem;
    --breakpoint-xlarge: 80rem;
    --breakpoint-xxlarge: 87.5rem;
    --control-minTarget-fine: 1rem;
    --control-minTarget-coarse: 2.75rem;
    --control-xsmall-size: 1.5rem;
    --control-xsmall-lineBoxHeight: 1.25rem;
    --control-xsmall-paddingBlock: 0.125rem;
    --control-xsmall-paddingInline-condensed: 0.25rem;
    --control-xsmall-paddingInline-normal: 0.5rem;
    --control-xsmall-paddingInline-spacious: 0.75rem;
    --control-xsmall-gap: 0.25rem;
    --control-small-size: 1.75rem;
    --control-small-lineBoxHeight: 1.25rem;
    --control-small-paddingBlock: 0.25rem;
    --control-small-paddingInline-condensed: 0.5rem;
    --control-small-paddingInline-normal: 0.75rem;
    --control-small-gap: 0.25rem;
    --control-medium-size: 2rem;
    --control-medium-lineBoxHeight: 1.25rem;
    --control-medium-paddingBlock: 0.375rem;
    --control-medium-paddingInline-condensed: 0.5rem;
    --control-medium-paddingInline-normal: 0.75rem;
    --control-medium-paddingInline-spacious: 1rem;
    --control-medium-gap: 0.5rem;
    --control-large-size: 2.5rem;
    --control-large-lineBoxHeight: 1.25rem;
    --control-large-paddingBlock: 0.625rem;
    --control-large-paddingInline-normal: 0.75rem;
    --control-large-paddingInline-spacious: 1rem;
    --control-large-gap: 0.5rem;
    --control-xlarge-size: 3rem;
    --control-xlarge-lineBoxHeight: 1.25rem;
    --control-xlarge-paddingBlock: 0.875rem;
    --control-xlarge-paddingInline-normal: 0.75rem;
    --control-xlarge-paddingInline-spacious: 1rem;
    --control-xlarge-gap: 0.5rem;
    --controlStack-small-gap-condensed: 0.5rem;
    --controlStack-small-gap-spacious: 1rem;
    --controlStack-medium-gap-condensed: 0.5rem;
    --controlStack-medium-gap-spacious: 0.75rem;
    --controlStack-large-gap-auto: 0.5rem;
    --controlStack-large-gap-condensed: 0.5rem;
    --controlStack-large-gap-spacious: 0.75rem;
    --space-xxsmall: 0.125rem;
    --space-xsmall: 0.25rem;
    --space-small: 0.375rem;
    --space-medium: 0.5rem;
    --space-large: 0.75rem;
    --space-xlarge: 1rem;
    --spinner-strokeWidth-default: 0.125rem;
    --spinner-size-small: 1rem;
    --spinner-size-medium: 2rem;
    --spinner-size-large: 4rem;
    --stack-padding-condensed: 0.5rem;
    --stack-padding-normal: 1rem;
    --stack-padding-spacious: 1.5rem;
    --stack-gap-condensed: 0.5rem;
    --stack-gap-normal: 1rem;
    --stack-gap-spacious: 1.5rem;
    --overlay-width-xsmall: 12rem;
    --overlay-width-small: 20rem;
    --overlay-width-medium: 30rem;
    --overlay-width-large: 40rem;
    --overlay-width-xlarge: 60rem;
    --overlay-height-small: 16rem;
    --overlay-height-medium: 20rem;
    --overlay-height-large: 27rem;
    --overlay-height-xlarge: 37.5rem;
    --overlay-padding-normal: 1rem;
    --overlay-padding-condensed: 0.5rem;
    --overlay-paddingBlock-condensed: 0.25rem;
    --overlay-paddingBlock-normal: 0.75rem;
    --overlay-borderRadius: 0.375rem;
    --overlay-offset: 0.25rem;
    --text-codeInline-size: 0.9285em;
    --text-codeBlock-lineHeight: 1.5385;
    --text-codeBlock-size: 0.8125rem;
    --text-caption-lineHeight: 1.3333;
    --text-caption-size: 0.75rem;
    --text-body-lineHeight-small: 1.6666;
    --text-body-lineHeight-medium: 1.4285;
    --text-body-lineHeight-large: 1.5;
    --text-body-size-small: 0.75rem;
    --text-body-size-medium: 0.875rem;
    --text-body-size-large: 1rem;
    --text-subtitle-lineHeight: 1.6;
    --text-subtitle-size: 1.25rem;
    --text-title-lineHeight-small: 1.5;
    --text-title-lineHeight-medium: 1.6;
    --text-title-lineHeight-large: 1.5;
    --text-title-size-small: 1rem;
    --text-title-size-medium: 1.25rem;
    --text-title-size-large: 2rem;
    --text-display-lineHeight: 1.4;
    --text-display-size: 2.5rem;
    --text-display-lineBoxHeight: 1.4;
    --fontStack-monospace: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
    --fontStack-sansSerif: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
    --fontStack-system: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
    --text-codeInline-weight: var(--base-text-weight-normal);
    --text-codeBlock-weight: var(--base-text-weight-normal);
    --text-caption-weight: var(--base-text-weight-normal);
    --text-body-weight: var(--base-text-weight-normal);
    --text-subtitle-weight: var(--base-text-weight-normal);
    --text-title-weight-small: var(--base-text-weight-semibold);
    --text-title-weight-medium: var(--base-text-weight-semibold);
    --text-title-weight-large: var(--base-text-weight-semibold);
    --text-display-weight: var(--base-text-weight-medium);
    --text-codeInline-shorthand: var(--text-codeInline-weight) var(--text-codeInline-size) var(--fontStack-monospace);
    --text-codeBlock-shorthand: var(--text-codeBlock-weight) var(--text-codeBlock-size) / var(--text-codeBlock-lineHeight) var(--fontStack-monospace);
    --text-caption-shorthand: var(--text-caption-weight) var(--text-caption-size) / var(--text-caption-lineHeight) var(--fontStack-sansSerif);
    --text-body-shorthand-small: var(--text-body-weight) var(--text-body-size-small) / var(--text-body-lineHeight-small) var(--fontStack-sansSerif);
    --text-body-shorthand-medium: var(--text-body-weight) var(--text-body-size-medium) / var(--text-body-lineHeight-medium) var(--fontStack-sansSerif);
    --text-body-shorthand-large: var(--text-body-weight) var(--text-body-size-large) / var(--text-body-lineHeight-large) var(--fontStack-sansSerif);
    --text-subtitle-shorthand: var(--text-subtitle-weight) var(--text-subtitle-size) / var(--text-subtitle-lineHeight) var(--fontStack-sansSerif);
    --text-title-shorthand-small: var(--text-title-weight-small) var(--text-title-size-small) / var(--text-title-lineHeight-small) var(--fontStack-sansSerif);
    --text-title-shorthand-medium: var(--text-title-weight-medium) var(--text-title-size-medium) / var(--text-title-lineHeight-medium) var(--fontStack-sansSerif);
    --text-title-shorthand-large: var(--text-title-weight-large) var(--text-title-size-large) / var(--text-title-lineHeight-large) var(--fontStack-sansSerif);
    --text-display-shorthand: var(--text-display-weight) var(--text-display-size) / var(--text-display-lineHeight) var(--fontStack-sansSerif);
    --h00-size-mobile: 2.5rem;
    --h0-size-mobile: 2rem;
    --h1-size-mobile: 1.625rem;
    --h2-size-mobile: 1.375rem;
    --h3-size-mobile: 1.125rem;
    --h00-size: 3rem;
    --h0-size: 2.5rem;
    --h1-size: 2rem;
    --h2-size: 1.5rem;
    --h3-size: 1.25rem;
    --h4-size: 1rem;
    --h5-size: 0.875rem;
    --h6-size: 0.75rem;
    --body-font-size: 0.875rem;
    --font-size-small: 0.75rem;
    --Layout-pane-width: 220px;
    --Layout-content-width: 100%;
    --Layout-template-columns: 1fr var(--Layout-pane-width);
    --Layout-template-areas: "content pane";
    --Layout-column-gap: 16px;
    --Layout-row-gap: 16px;
    --Layout-outer-spacing-x: 0px;
    --Layout-outer-spacing-y: 0px;
    --Layout-inner-spacing-min: 0px;
    --Layout-inner-spacing-max: 0px;
    --actionListContent-paddingBlock: var(--control-medium-paddingBlock);
    --duration-fast: 80ms;
    --easing-easeInOut: cubic-bezier(0.65, 0, 0.35, 1);
    --button-outline-borderColor-active: #1f232826;
    --focus-outline: #0969da solid 2px;
    --topicTag-borderColor: #00000000;
    --highlight-neutral-bgColor: #d2992266;
    --page-header-bgColor: #0d1117;
    --diffBlob-addition-fgColor-text: #e6edf3;
    --diffBlob-addition-fgColor-num: #e6edf3;
    --diffBlob-addition-bgColor-num: #3fb9504d;
    --diffBlob-addition-bgColor-line: #2ea04326;
    --diffBlob-addition-bgColor-word: #2ea04366;
    --diffBlob-deletion-fgColor-text: #e6edf3;
    --diffBlob-deletion-fgColor-num: #e6edf3;
    --diffBlob-deletion-bgColor-num: #f851494d;
    --diffBlob-deletion-bgColor-line: #f8514926;
    --diffBlob-deletion-bgColor-word: #f8514966;
    --diffBlob-hunk-bgColor-num: #388bfd66;
    --diffBlob-expander-iconColor: #8d96a0;
    --codeMirror-fgColor: #e6edf3;
    --codeMirror-bgColor: #0d1117;
    --codeMirror-gutters-bgColor: #0d1117;
    --codeMirror-gutterMarker-fgColor-default: #0d1117;
    --codeMirror-gutterMarker-fgColor-muted: #8d96a0;
    --codeMirror-lineNumber-fgColor: #8d96a0;
    --codeMirror-cursor-fgColor: #e6edf3;
    --codeMirror-selection-bgColor: #388bfd66;
    --codeMirror-activeline-bgColor: #6e768166;
    --codeMirror-matchingBracket-fgColor: #e6edf3;
    --codeMirror-lines-bgColor: #0d1117;
    --codeMirror-syntax-fgColor-comment: #8b949e;
    --codeMirror-syntax-fgColor-constant: #79c0ff;
    --codeMirror-syntax-fgColor-entity: #d2a8ff;
    --codeMirror-syntax-fgColor-keyword: #ff7b72;
    --codeMirror-syntax-fgColor-storage: #ff7b72;
    --codeMirror-syntax-fgColor-string: #a5d6ff;
    --codeMirror-syntax-fgColor-support: #79c0ff;
    --codeMirror-syntax-fgColor-variable: #ffa657;
    --header-fgColor-default: #ffffffb3;
    --header-fgColor-logo: #f0f6fc;
    --header-bgColor: #161b22f2;
    --header-borderColor-divider: #8b949e;
    --headerSearch-bgColor: #0d1117;
    --headerSearch-borderColor: #30363d;
    --data-blue-color: #0576ff;
    --data-blue-color-muted: #001a47;
    --data-auburn-color: #a86f6b;
    --data-auburn-color-muted: #271817;
    --data-orange-color: #984b10;
    --data-orange-color-muted: #311708;
    --data-yellow-color: #895906;
    --data-yellow-color-muted: #2e1a00;
    --data-green-color: #2f6f37;
    --data-green-color-muted: #122117;
    --data-teal-color: #106c70;
    --data-teal-color-muted: #041f25;
    --data-purple-color: #975bf1;
    --data-purple-color-muted: #211047;
    --data-pink-color: #d34591;
    --data-pink-color-muted: #2d1524;
    --data-red-color: #eb3342;
    --data-red-color-muted: #3c0614;
    --data-gray-color: #576270;
    --data-gray-color-muted: #1c1c1c;
    --display-blue-bgColor-muted: #001a47;
    --display-blue-bgColor-emphasis: #0576ff;
    --display-blue-fgColor: #4da0ff;
    --display-blue-borderColor-muted: #002766;
    --display-blue-borderColor-emphasis: #0576ff;
    --display-green-bgColor-muted: #122117;
    --display-green-bgColor-emphasis: #388f3f;
    --display-green-fgColor: #41b445;
    --display-green-borderColor-muted: #182f1f;
    --display-green-borderColor-emphasis: #388f3f;
    --display-orange-bgColor-muted: #311708;
    --display-orange-bgColor-emphasis: #c46212;
    --display-orange-fgColor: #ed8326;
    --display-orange-borderColor-muted: #43200a;
    --display-orange-borderColor-emphasis: #c46212;
    --display-purple-bgColor-muted: #211047;
    --display-purple-bgColor-emphasis: #975bf1;
    --display-purple-fgColor: #b687f7;
    --display-purple-borderColor-muted: #31146b;
    --display-purple-borderColor-emphasis: #975bf1;
    --display-plum-bgColor-muted: #2a0e3f;
    --display-plum-bgColor-emphasis: #b643ef;
    --display-plum-fgColor: #d07ef7;
    --display-plum-borderColor-muted: #40125e;
    --display-plum-borderColor-emphasis: #b643ef;
    --display-red-bgColor-muted: #3c0614;
    --display-red-bgColor-emphasis: #eb3342;
    --display-red-fgColor: #f27d83;
    --display-red-borderColor-muted: #58091a;
    --display-red-borderColor-emphasis: #eb3342;
    --display-coral-bgColor-muted: #3c0614;
    --display-coral-bgColor-emphasis: #eb3342;
    --display-coral-fgColor: #f27d83;
    --display-coral-borderColor-muted: #58091a;
    --display-coral-borderColor-emphasis: #eb3342;
    --display-yellow-bgColor-muted: #2e1a00;
    --display-yellow-bgColor-emphasis: #aa7109;
    --display-yellow-fgColor: #d3910d;
    --display-yellow-borderColor-muted: #3d2401;
    --display-yellow-borderColor-emphasis: #aa7109;
    --display-gray-bgColor-muted: #1c1c1c;
    --display-gray-bgColor-emphasis: #6e7f96;
    --display-gray-fgColor: #92a1b5;
    --display-gray-borderColor-muted: #2a2b2d;
    --display-gray-borderColor-emphasis: #6e7f96;
    --display-auburn-bgColor-muted: #271817;
    --display-auburn-bgColor-emphasis: #a86f6b;
    --display-auburn-fgColor: #bf9592;
    --display-auburn-borderColor-muted: #3a2422;
    --display-auburn-borderColor-emphasis: #a86f6b;
    --display-brown-bgColor-muted: #241c14;
    --display-brown-bgColor-emphasis: #94774c;
    --display-brown-fgColor: #b69a6d;
    --display-brown-borderColor-muted: #342a1d;
    --display-brown-borderColor-emphasis: #94774c;
    --display-lemon-bgColor-muted: #291d00;
    --display-lemon-bgColor-emphasis: #977b0c;
    --display-lemon-fgColor: #ba9b12;
    --display-lemon-borderColor-muted: #372901;
    --display-lemon-borderColor-emphasis: #977b0c;
    --display-olive-bgColor-muted: #171e0b;
    --display-olive-bgColor-emphasis: #7a8321;
    --display-olive-fgColor: #a2a626;
    --display-olive-borderColor-muted: #252d10;
    --display-olive-borderColor-emphasis: #7a8321;
    --display-lime-bgColor-muted: #141f0f;
    --display-lime-bgColor-emphasis: #5f892f;
    --display-lime-fgColor: #7dae37;
    --display-lime-borderColor-muted: #1f3116;
    --display-lime-borderColor-emphasis: #5f892f;
    --display-pine-bgColor-muted: #082119;
    --display-pine-bgColor-emphasis: #18915e;
    --display-pine-fgColor: #1bb673;
    --display-pine-borderColor-muted: #0b3224;
    --display-pine-borderColor-emphasis: #18915e;
    --display-teal-bgColor-muted: #041f25;
    --display-teal-bgColor-emphasis: #158a8a;
    --display-teal-fgColor: #1cb0ab;
    --display-teal-borderColor-muted: #073036;
    --display-teal-borderColor-emphasis: #158a8a;
    --display-cyan-bgColor-muted: #001f29;
    --display-cyan-bgColor-emphasis: #0587b3;
    --display-cyan-fgColor: #07ace4;
    --display-cyan-borderColor-muted: #002e3d;
    --display-cyan-borderColor-emphasis: #0587b3;
    --display-indigo-bgColor-muted: #1b183f;
    --display-indigo-bgColor-emphasis: #7070e1;
    --display-indigo-fgColor: #9899ec;
    --display-indigo-borderColor-muted: #25215f;
    --display-indigo-borderColor-emphasis: #7070e1;
    --display-pink-bgColor-muted: #2d1524;
    --display-pink-bgColor-emphasis: #d34591;
    --display-pink-fgColor: #e57bb2;
    --display-pink-borderColor-muted: #451c35;
    --display-pink-borderColor-emphasis: #d34591;
    --avatar-bgColor: #ffffff1a;
    --avatar-borderColor: #ffffff26;
    --avatar-shadow: 0px 0px 0px 2px #0d1117;
    --avatarStack-fade-bgColor-default: #30363d;
    --avatarStack-fade-bgColor-muted: #21262d;
    --control-bgColor-rest: #21262d;
    --control-bgColor-hover: #292e36;
    --control-bgColor-active: #31363e;
    --control-bgColor-disabled: #21262db3;
    --control-bgColor-selected: #161b22;
    --control-fgColor-rest: #c9d1d9;
    --control-fgColor-placeholder: #484f58;
    --control-fgColor-disabled: #6e7681;
    --control-borderColor-rest: #30363d;
    --control-borderColor-emphasis: #666e79;
    --control-borderColor-disabled: #21262db3;
    --control-borderColor-selected: #f0f6fc;
    --control-borderColor-success: #238636;
    --control-borderColor-danger: #da3633;
    --control-borderColor-warning: #9e6a03;
    --control-iconColor-rest: #8d96a0;
    --control-transparent-bgColor-rest: #00000000;
    --control-transparent-bgColor-hover: #b1bac41f;
    --control-transparent-bgColor-active: #b1bac433;
    --control-transparent-bgColor-disabled: #21262db3;
    --control-transparent-bgColor-selected: #b1bac414;
    --control-transparent-borderColor-rest: #00000000;
    --control-transparent-borderColor-hover: #00000000;
    --control-transparent-borderColor-active: #00000000;
    --control-danger-fgColor-rest: #f85149;
    --control-danger-fgColor-hover: #ff7b72;
    --control-danger-bgColor-hover: #f851491a;
    --control-danger-bgColor-active: #f8514966;
    --control-checked-bgColor-rest: #1f6feb;
    --control-checked-bgColor-hover: #2a7aef;
    --control-checked-bgColor-active: #3685f3;
    --control-checked-bgColor-disabled: #6e7681;
    --control-checked-fgColor-rest: #ffffff;
    --control-checked-fgColor-disabled: #010409;
    --control-checked-borderColor-rest: #1f6feb;
    --control-checked-borderColor-hover: #2a7aef;
    --control-checked-borderColor-active: #3685f3;
    --control-checked-borderColor-disabled: #6e7681;
    --controlTrack-bgColor-rest: #21262d;
    --controlTrack-bgColor-hover: #292e36;
    --controlTrack-bgColor-active: #31363e;
    --controlTrack-bgColor-disabled: #6e7681;
    --controlTrack-fgColor-rest: #8d96a0;
    --controlTrack-fgColor-disabled: #ffffff;
    --controlTrack-borderColor-rest: #00000000;
    --controlTrack-borderColor-disabled: #6e7681;
    --controlKnob-bgColor-rest: #010409;
    --controlKnob-bgColor-disabled: #21262db3;
    --controlKnob-bgColor-checked: #ffffff;
    --controlKnob-borderColor-rest: #666e79;
    --controlKnob-borderColor-disabled: #21262db3;
    --controlKnob-borderColor-checked: #1f6feb;
    --counter-borderColor: #00000000;
    --button-default-fgColor-rest: #c9d1d9;
    --button-default-bgColor-rest: #21262d;
    --button-default-bgColor-hover: #292e36;
    --button-default-bgColor-active: #31363e;
    --button-default-bgColor-selected: #31363e;
    --button-default-bgColor-disabled: #21262db3;
    --button-default-borderColor-rest: #30363d;
    --button-default-borderColor-hover: #30363d;
    --button-default-borderColor-active: #30363d;
    --button-default-borderColor-disabled: #21262db3;
    --button-default-shadow-resting: 0px 0px 0px 0px #000000;
    --button-primary-fgColor-rest: #ffffff;
    --button-primary-fgColor-disabled: #ffffff66;
    --button-primary-iconColor-rest: #ffffff;
    --button-primary-bgColor-rest: #238636;
    --button-primary-bgColor-hover: #29903b;
    --button-primary-bgColor-active: #2e9a40;
    --button-primary-bgColor-disabled: #105823;
    --button-primary-borderColor-rest: #f0f6fc1a;
    --button-primary-borderColor-hover: #f0f6fc1a;
    --button-primary-borderColor-active: #f0f6fc1a;
    --button-primary-borderColor-disabled: #105823;
    --button-primary-shadow-selected: 0px 0px 0px 0px #000000;
    --button-invisible-fgColor-rest: #4493f8;
    --button-invisible-fgColor-hover: #58a6ff;
    --button-invisible-fgColor-disabled: #6e7681;
    --button-invisible-iconColor-rest: #8d96a0;
    --button-invisible-iconColor-hover: #e6edf3;
    --button-invisible-iconColor-disabled: #6e7681;
    --button-invisible-bgColor-rest: #00000000;
    --button-invisible-bgColor-hover: #b1bac41f;
    --button-invisible-bgColor-active: #b1bac433;
    --button-invisible-bgColor-disabled: #21262db3;
    --button-invisible-borderColor-rest: #00000000;
    --button-invisible-borderColor-hover: #00000000;
    --button-invisible-borderColor-disabled: #21262db3;
    --button-outline-fgColor-rest: #388bfd;
    --button-outline-fgColor-hover: #58a6ff;
    --button-outline-fgColor-active: #ffffff;
    --button-outline-fgColor-disabled: #4493f880;
    --button-outline-bgColor-rest: #f0f6fc;
    --button-outline-bgColor-hover: #30363d;
    --button-outline-bgColor-active: #0d419d;
    --button-outline-bgColor-disabled: #0d1117;
    --button-outline-borderColor-hover: #f0f6fc1a;
    --button-outline-borderColor-selected: #f0f6fc1a;
    --button-outline-shadow-selected: 0px 0px 0px 0px #000000;
    --button-danger-fgColor-rest: #f85149;
    --button-danger-fgColor-hover: #ffffff;
    --button-danger-fgColor-active: #ffffff;
    --button-danger-fgColor-disabled: #f8514980;
    --button-danger-iconColor-rest: #f85149;
    --button-danger-iconColor-hover: #ffffff;
    --button-danger-bgColor-rest: #21262d;
    --button-danger-bgColor-hover: #b62324;
    --button-danger-bgColor-active: #d03533;
    --button-danger-bgColor-disabled: #21262db3;
    --button-danger-borderColor-rest: #30363d;
    --button-danger-borderColor-hover: #f0f6fc1a;
    --button-danger-borderColor-active: #f0f6fc1a;
    --button-danger-shadow-selected: 0px 0px 0px 0px #000000;
    --button-inactive-fgColor: #8b949e;
    --button-inactive-bgColor: #21262d;
    --button-star-iconColor: #e3b341;
    --buttonCounter-default-bgColor-rest: #30363d;
    --buttonCounter-invisible-bgColor-rest: #30363d;
    --buttonCounter-primary-bgColor-rest: #04260f33;
    --buttonCounter-outline-bgColor-rest: #051d4d33;
    --buttonCounter-outline-bgColor-hover: #051d4d33;
    --buttonCounter-outline-bgColor-disabled: #1f6feb0d;
    --buttonCounter-outline-fgColor-rest: #388bfd;
    --buttonCounter-outline-fgColor-hover: #58a6ff;
    --buttonCounter-outline-fgColor-disabled: #4493f880;
    --buttonCounter-danger-bgColor-hover: #ffffff33;
    --buttonCounter-danger-bgColor-disabled: #da36330d;
    --buttonCounter-danger-bgColor-rest: #49020233;
    --buttonCounter-danger-fgColor-rest: #f85149;
    --buttonCounter-danger-fgColor-hover: #ffffff;
    --buttonCounter-danger-fgColor-disabled: #f8514980;
    --reactionButton-selected-bgColor-rest: #388bfd33;
    --reactionButton-selected-bgColor-hover: #3a8cfd5c;
    --reactionButton-selected-fgColor-rest: #4493f8;
    --reactionButton-selected-fgColor-hover: #79c0ff;
    --focus-outlineColor: #1f6feb;
    --menu-bgColor-active: #161b22;
    --overlay-bgColor: #161b22;
    --overlay-borderColor: #30363db3;
    --overlay-backdrop-bgColor: #161b2266;
    --selectMenu-borderColor: #484f58;
    --selectMenu-bgColor-active: #0c2d6b;
    --sideNav-bgColor-selected: #21262d;
    --skeletonLoader-bgColor: #161b22;
    --timelineBadge-bgColor: #21262d;
    --treeViewItem-leadingVisual-iconColor-rest: #8d96a0;
    --underlineNav-borderColor-active: #f78166;
    --underlineNav-borderColor-hover: #6e768166;
    --underlineNav-iconColor-rest: #8d96a0;
    --selection-bgColor: #1f6febb3;
    --card-bgColor: #161b22;
    --label-green-bgColor-rest: #122117;
    --label-green-bgColor-hover: #182f1f;
    --label-green-bgColor-active: #214529;
    --label-green-fgColor-rest: #41b445;
    --label-green-fgColor-hover: #46c144;
    --label-green-fgColor-active: #75d36f;
    --label-orange-bgColor-rest: #311708;
    --label-orange-bgColor-hover: #43200a;
    --label-orange-bgColor-active: #632f0d;
    --label-orange-fgColor-rest: #ed8326;
    --label-orange-fgColor-hover: #f1933b;
    --label-orange-fgColor-active: #f6b06a;
    --label-purple-bgColor-rest: #211047;
    --label-purple-bgColor-hover: #31146b;
    --label-purple-bgColor-active: #481a9e;
    --label-purple-fgColor-rest: #b687f7;
    --label-purple-fgColor-hover: #c398fb;
    --label-purple-fgColor-active: #d2affd;
    --label-red-bgColor-rest: #3c0614;
    --label-red-bgColor-hover: #58091a;
    --label-red-bgColor-active: #790c20;
    --label-red-fgColor-rest: #f27d83;
    --label-red-fgColor-hover: #f48b8d;
    --label-red-fgColor-active: #f7adab;
    --label-yellow-bgColor-rest: #2e1a00;
    --label-yellow-bgColor-hover: #3d2401;
    --label-yellow-bgColor-active: #5a3702;
    --label-yellow-fgColor-rest: #d3910d;
    --label-yellow-fgColor-hover: #df9e11;
    --label-yellow-fgColor-active: #edb431;
    --label-gray-bgColor-rest: #1c1c1c;
    --label-gray-bgColor-hover: #2a2b2d;
    --label-gray-bgColor-active: #393d41;
    --label-gray-fgColor-rest: #92a1b5;
    --label-gray-fgColor-hover: #9babbf;
    --label-gray-fgColor-active: #b3c0d1;
    --label-auburn-bgColor-rest: #271817;
    --label-auburn-bgColor-hover: #3a2422;
    --label-auburn-bgColor-active: #543331;
    --label-auburn-fgColor-rest: #bf9592;
    --label-auburn-fgColor-hover: #c6a19f;
    --label-auburn-fgColor-active: #d4b7b5;
    --label-brown-bgColor-rest: #241c14;
    --label-brown-bgColor-hover: #342a1d;
    --label-brown-bgColor-active: #483a28;
    --label-brown-fgColor-rest: #b69a6d;
    --label-brown-fgColor-hover: #bfa77d;
    --label-brown-fgColor-active: #cdbb98;
    --label-lemon-bgColor-rest: #291d00;
    --label-lemon-bgColor-hover: #372901;
    --label-lemon-bgColor-active: #4f3c02;
    --label-lemon-fgColor-rest: #ba9b12;
    --label-lemon-fgColor-hover: #c4a717;
    --label-lemon-fgColor-active: #d7bc1d;
    --label-olive-bgColor-rest: #171e0b;
    --label-olive-bgColor-hover: #252d10;
    --label-olive-bgColor-active: #374115;
    --label-olive-fgColor-rest: #a2a626;
    --label-olive-fgColor-hover: #b2af24;
    --label-olive-fgColor-active: #cbc025;
    --label-lime-bgColor-rest: #141f0f;
    --label-lime-bgColor-hover: #1f3116;
    --label-lime-bgColor-active: #2c441d;
    --label-lime-fgColor-rest: #7dae37;
    --label-lime-fgColor-hover: #89ba36;
    --label-lime-fgColor-active: #9fcc3e;
    --label-pine-bgColor-rest: #082119;
    --label-pine-bgColor-hover: #0b3224;
    --label-pine-bgColor-active: #0e4430;
    --label-pine-fgColor-rest: #1bb673;
    --label-pine-fgColor-hover: #1ac176;
    --label-pine-fgColor-active: #1bda81;
    --label-teal-bgColor-rest: #041f25;
    --label-teal-bgColor-hover: #073036;
    --label-teal-bgColor-active: #0a464d;
    --label-teal-fgColor-rest: #1cb0ab;
    --label-teal-fgColor-hover: #1fbdb2;
    --label-teal-fgColor-active: #24d6c4;
    --label-cyan-bgColor-rest: #001f29;
    --label-cyan-bgColor-hover: #002e3d;
    --label-cyan-bgColor-active: #014156;
    --label-cyan-fgColor-rest: #07ace4;
    --label-cyan-fgColor-hover: #09b7f1;
    --label-cyan-fgColor-active: #45cbf7;
    --label-indigo-bgColor-rest: #1b183f;
    --label-indigo-bgColor-hover: #25215f;
    --label-indigo-bgColor-active: #312c90;
    --label-indigo-fgColor-rest: #9899ec;
    --label-indigo-fgColor-hover: #a2a5f1;
    --label-indigo-fgColor-active: #b7baf6;
    --label-blue-bgColor-rest: #001a47;
    --label-blue-bgColor-hover: #002766;
    --label-blue-bgColor-active: #00378a;
    --label-blue-fgColor-rest: #4da0ff;
    --label-blue-fgColor-hover: #61adff;
    --label-blue-fgColor-active: #85c2ff;
    --label-plum-bgColor-rest: #2a0e3f;
    --label-plum-bgColor-hover: #40125e;
    --label-plum-bgColor-active: #5c1688;
    --label-plum-fgColor-rest: #d07ef7;
    --label-plum-fgColor-hover: #d889fa;
    --label-plum-fgColor-active: #e4a5fd;
    --label-pink-bgColor-rest: #2d1524;
    --label-pink-bgColor-hover: #451c35;
    --label-pink-bgColor-active: #65244a;
    --label-pink-fgColor-rest: #e57bb2;
    --label-pink-fgColor-hover: #ec8dbd;
    --label-pink-fgColor-active: #f4a9cd;
    --label-coral-bgColor-rest: #351008;
    --label-coral-bgColor-hover: #51180b;
    --label-coral-bgColor-active: #72220d;
    --label-coral-fgColor-rest: #f7794b;
    --label-coral-fgColor-hover: #fa8c61;
    --label-coral-fgColor-active: #fdaa86;
    --fgColor-default: #e6edf3;
    --fgColor-muted: #8d96a0;
    --fgColor-onEmphasis: #ffffff;
    --fgColor-white: #ffffff;
    --fgColor-black: #010409;
    --fgColor-disabled: #6e7681;
    --fgColor-link: #4493f8;
    --fgColor-neutral: #6e7681;
    --fgColor-accent: #4493f8;
    --fgColor-success: #3fb950;
    --fgColor-attention: #d29922;
    --fgColor-severe: #db6d28;
    --fgColor-danger: #f85149;
    --fgColor-open: #3fb950;
    --fgColor-closed: #f85149;
    --fgColor-done: #ab7df8;
    --fgColor-upsell: #ab7df8;
    --fgColor-sponsors: #db61a2;
    --bgColor-default: #0d1117;
    --bgColor-muted: #161b22;
    --bgColor-inset: #010409;
    --bgColor-emphasis: #6e7681;
    --bgColor-inverse: #ffffff;
    --bgColor-white: #ffffff;
    --bgColor-black: #010409;
    --bgColor-disabled: #21262db3;
    --bgColor-transparent: #00000000;
    --bgColor-neutral-muted: #6e768166;
    --bgColor-neutral-emphasis: #6e7681;
    --bgColor-accent-muted: #388bfd1a;
    --bgColor-accent-emphasis: #1f6feb;
    --bgColor-success-muted: #2ea04326;
    --bgColor-success-emphasis: #238636;
    --bgColor-attention-muted: #bb800926;
    --bgColor-attention-emphasis: #9e6a03;
    --bgColor-severe-muted: #db6d281a;
    --bgColor-severe-emphasis: #bd561d;
    --bgColor-danger-muted: #f851491a;
    --bgColor-danger-emphasis: #da3633;
    --bgColor-open-muted: #2ea0431a;
    --bgColor-open-emphasis: #238636;
    --bgColor-closed-muted: #f8514926;
    --bgColor-closed-emphasis: #da3633;
    --bgColor-done-muted: #ab7df826;
    --bgColor-done-emphasis: #8957e5;
    --bgColor-upsell-muted: #ab7df826;
    --bgColor-upsell-emphasis: #8957e5;
    --bgColor-sponsors-muted: #db61a21a;
    --bgColor-sponsors-emphasis: #bf4b8a;
    --borderColor-default: #30363d;
    --borderColor-muted: #30363db3;
    --borderColor-emphasis: #484f58;
    --borderColor-disabled: #21262db3;
    --borderColor-transparent: #00000000;
    --borderColor-neutral-muted: #6e768166;
    --borderColor-neutral-emphasis: #6e7681;
    --borderColor-accent-muted: #388bfd66;
    --borderColor-accent-emphasis: #1f6feb;
    --borderColor-success-muted: #2ea04366;
    --borderColor-success-emphasis: #238636;
    --borderColor-attention-muted: #bb800966;
    --borderColor-attention-emphasis: #9e6a03;
    --borderColor-severe-muted: #db6d2866;
    --borderColor-severe-emphasis: #bd561d;
    --borderColor-danger-muted: #f8514966;
    --borderColor-danger-emphasis: #da3633;
    --borderColor-open-muted: #2ea04366;
    --borderColor-open-emphasis: #238636;
    --borderColor-closed-muted: #f8514966;
    --borderColor-closed-emphasis: #da3633;
    --borderColor-done-muted: #ab7df866;
    --borderColor-done-emphasis: #8957e5;
    --borderColor-upsell-muted: #ab7df866;
    --borderColor-upsell-emphasis: #8957e5;
    --borderColor-sponsors-muted: #db61a266;
    --borderColor-sponsors-emphasis: #bf4b8a;
    --color-ansi-black: #484f58;
    --color-ansi-black-bright: #6e7681;
    --color-ansi-white: #b1bac4;
    --color-ansi-white-bright: #ffffff;
    --color-ansi-gray: #6e7681;
    --color-ansi-red: #ff7b72;
    --color-ansi-red-bright: #ffa198;
    --color-ansi-green: #3fb950;
    --color-ansi-green-bright: #56d364;
    --color-ansi-yellow: #d29922;
    --color-ansi-yellow-bright: #e3b341;
    --color-ansi-blue: #58a6ff;
    --color-ansi-blue-bright: #79c0ff;
    --color-ansi-magenta: #be8fff;
    --color-ansi-magenta-bright: #d2a8ff;
    --color-ansi-cyan: #39c5cf;
    --color-ansi-cyan-bright: #56d4dd;
    --color-prettylights-syntax-comment: #8b949e;
    --color-prettylights-syntax-constant: #79c0ff;
    --color-prettylights-syntax-constant-other-reference-link: #a5d6ff;
    --color-prettylights-syntax-entity: #d2a8ff;
    --color-prettylights-syntax-storage-modifier-import: #c9d1d9;
    --color-prettylights-syntax-entity-tag: #7ee787;
    --color-prettylights-syntax-keyword: #ff7b72;
    --color-prettylights-syntax-string: #a5d6ff;
    --color-prettylights-syntax-variable: #ffa657;
    --color-prettylights-syntax-brackethighlighter-unmatched: #f85149;
    --color-prettylights-syntax-brackethighlighter-angle: #8b949e;
    --color-prettylights-syntax-invalid-illegal-text: #f0f6fc;
    --color-prettylights-syntax-invalid-illegal-bg: #8e1519;
    --color-prettylights-syntax-carriage-return-text: #f0f6fc;
    --color-prettylights-syntax-carriage-return-bg: #b62324;
    --color-prettylights-syntax-string-regexp: #7ee787;
    --color-prettylights-syntax-markup-list: #f2cc60;
    --color-prettylights-syntax-markup-heading: #1f6feb;
    --color-prettylights-syntax-markup-italic: #c9d1d9;
    --color-prettylights-syntax-markup-bold: #c9d1d9;
    --color-prettylights-syntax-markup-deleted-text: #ffdcd7;
    --color-prettylights-syntax-markup-deleted-bg: #67060c;
    --color-prettylights-syntax-markup-inserted-text: #aff5b4;
    --color-prettylights-syntax-markup-inserted-bg: #033a16;
    --color-prettylights-syntax-markup-changed-text: #ffdfb6;
    --color-prettylights-syntax-markup-changed-bg: #5a1e02;
    --color-prettylights-syntax-markup-ignored-text: #c9d1d9;
    --color-prettylights-syntax-markup-ignored-bg: #1158c7;
    --color-prettylights-syntax-meta-diff-range: #d2a8ff;
    --color-prettylights-syntax-sublimelinter-gutter-mark: #484f58;
    --shadow-inset: inset 0px 1px 0px 0px #0104093d;
    --shadow-resting-xsmall: 0px 1px 0px 0px #010409cc;
    --shadow-resting-small: 0px 1px 0px 0px #01040966;
    --shadow-resting-medium: 0px 3px 6px 0px #010409cc;
    --shadow-floating-small: 0px 0px 0px 1px #30363d, 0px 6px 12px -3px #01040966, 0px 6px 18px 0px #01040966;
    --shadow-floating-medium: 0px 0px 0px 1px #30363d, 0px 8px 16px -4px #01040966, 0px 4px 32px -4px #01040966, 0px 24px 48px -12px #01040966, 0px 48px 96px -24px #01040966;
    --shadow-floating-large: 0px 0px 0px 1px #30363d, 0px 24px 48px 0px #010409;
    --shadow-floating-xlarge: 0px 0px 0px 1px #30363d, 0px 32px 64px 0px #010409;
    --shadow-floating-legacy: 0px 6px 12px -3px #01040966, 0px 6px 18px 0px #01040966;
    --outline-focus: #1f6feb solid 2px;
    color-scheme: dark;
    --color-workflow-card-bg: var(--bgColor-muted, var(--color-scale-gray-7));
    --color-workflow-card-header-shadow: rgba(27, 31, 35, 0.04);
    --color-bg-discussions-row-emoji-box: #57606a;
    --color-notifications-row-read-bg: var(--bgColor-default, var(--color-canvas-default));
    --color-notifications-row-bg: var(--bgColor-muted, var(--color-canvas-subtle));
    --color-calendar-halloween-graph-day-L1-bg: #631c03;
    --color-calendar-halloween-graph-day-L2-bg: #bd561d;
    --color-calendar-halloween-graph-day-L3-bg: #fa7a18;
    --color-calendar-halloween-graph-day-L4-bg: #fddf68;
    --color-calendar-winter-graph-day-L1-bg: #0A3069;
    --color-calendar-winter-graph-day-L2-bg: #0969DA;
    --color-calendar-winter-graph-day-L3-bg: #54AEFF;
    --color-calendar-winter-graph-day-L4-bg: #B6E3FF;
    --color-calendar-graph-day-bg: #161b22;
    --color-calendar-graph-day-border: rgba(27, 31, 35, 0.06);
    --color-calendar-graph-day-L1-bg: #0e4429;
    --color-calendar-graph-day-L2-bg: #006d32;
    --color-calendar-graph-day-L3-bg: #26a641;
    --color-calendar-graph-day-L4-bg: #39d353;
    --color-calendar-graph-day-L1-border: rgba(255, 255, 255, 0.05);
    --color-calendar-graph-day-L2-border: rgba(255, 255, 255, 0.05);
    --color-calendar-graph-day-L3-border: rgba(255, 255, 255, 0.05);
    --color-calendar-graph-day-L4-border: rgba(255, 255, 255, 0.05);
    --color-user-mention-fg: var(--fgColor-attention, var(--color-scale-yellow-0));
    --color-mktg-btn-shadow-outline: rgba(255, 255, 255, 0.25) 0 0 0 1px inset;
    --color-marketing-icon-primary: #79c0ff;
    --color-marketing-icon-secondary: #1f6feb;
    --color-project-header-bg: #0d1117;
    --color-project-sidebar-bg: #161b22;
    --color-project-gradient-in: #161b22;
    --color-project-gradient-out: rgba(22, 27, 34, 0);
    --color-diff-blob-selected-line-highlight-mix-blend-mode: screen;
    --color-text-white: var(--fgColor-white, var(--color-scale-white));
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
    --dialog-scrollgutter: 17px;
    word-wrap: break-word;
    box-sizing: border-box;
    align-items: center !important;
    display: flex !important;
    border-radius: 2em;
    font-size: var(--text-body-size-medium);
    font-weight: var(--base-text-weight-medium);
    line-height: var(--control-medium-lineBoxHeight);
    padding: 5px var(--control-medium-paddingInline-normal);
    text-align: center;
    white-space: nowrap;
    border: var(--borderWidth-thin) solid #0000;
    background-color: var(--bgColor-open-emphasis, var(--color-open-emphasis));
    color: var(--fgColor-onEmphasis);
    margin-right: var(--base-size-8);
}

.closebutton {
    -webkit-text-size-adjust: 100%;
    --base-size-2: 0.125rem;
    --base-size-4: 0.25rem;
    --base-size-6: 0.375rem;
    --base-size-8: 0.5rem;
    --base-size-12: 0.75rem;
    --base-size-16: 1rem;
    --base-size-20: 1.25rem;
    --base-size-24: 1.5rem;
    --base-size-28: 1.75rem;
    --base-size-32: 2rem;
    --base-size-36: 2.25rem;
    --base-size-40: 2.5rem;
    --base-size-44: 2.75rem;
    --base-size-48: 3rem;
    --base-size-64: 4rem;
    --base-size-80: 5rem;
    --base-size-96: 6rem;
    --base-size-112: 7rem;
    --base-size-128: 8rem;
    --base-text-weight-light: 300;
    --base-text-weight-normal: 400;
    --base-text-weight-medium: 500;
    --base-text-weight-semibold: 600;
    --boxShadow-thin: inset 0 0 0 max(1px, 0.0625rem);
    --boxShadow-thick: inset 0 0 0 max(2px, 0.125rem);
    --boxShadow-thicker: inset 0 0 0 max(4px, 0.25rem);
    --borderWidth-thin: max(1px, 0.0625rem);
    --borderWidth-thick: max(2px, 0.125rem);
    --borderWidth-thicker: max(4px, 0.25rem);
    --borderRadius-small: 0.1875rem;
    --borderRadius-medium: 0.375rem;
    --borderRadius-large: 0.75rem;
    --borderRadius-full: 624.9375rem;
    --outline-focus-offset: -0.125rem;
    --outline-focus-width: 0.125rem;
    --breakpoint-xsmall: 20rem;
    --breakpoint-small: 34rem;
    --breakpoint-medium: 48rem;
    --breakpoint-large: 63.25rem;
    --breakpoint-xlarge: 80rem;
    --breakpoint-xxlarge: 87.5rem;
    --control-minTarget-fine: 1rem;
    --control-minTarget-coarse: 2.75rem;
    --control-xsmall-size: 1.5rem;
    --control-xsmall-lineBoxHeight: 1.25rem;
    --control-xsmall-paddingBlock: 0.125rem;
    --control-xsmall-paddingInline-condensed: 0.25rem;
    --control-xsmall-paddingInline-normal: 0.5rem;
    --control-xsmall-paddingInline-spacious: 0.75rem;
    --control-xsmall-gap: 0.25rem;
    --control-small-size: 1.75rem;
    --control-small-lineBoxHeight: 1.25rem;
    --control-small-paddingBlock: 0.25rem;
    --control-small-paddingInline-condensed: 0.5rem;
    --control-small-paddingInline-normal: 0.75rem;
    --control-small-gap: 0.25rem;
    --control-medium-size: 2rem;
    --control-medium-lineBoxHeight: 1.25rem;
    --control-medium-paddingBlock: 0.375rem;
    --control-medium-paddingInline-condensed: 0.5rem;
    --control-medium-paddingInline-normal: 0.75rem;
    --control-medium-paddingInline-spacious: 1rem;
    --control-medium-gap: 0.5rem;
    --control-large-size: 2.5rem;
    --control-large-lineBoxHeight: 1.25rem;
    --control-large-paddingBlock: 0.625rem;
    --control-large-paddingInline-normal: 0.75rem;
    --control-large-paddingInline-spacious: 1rem;
    --control-large-gap: 0.5rem;
    --control-xlarge-size: 3rem;
    --control-xlarge-lineBoxHeight: 1.25rem;
    --control-xlarge-paddingBlock: 0.875rem;
    --control-xlarge-paddingInline-normal: 0.75rem;
    --control-xlarge-paddingInline-spacious: 1rem;
    --control-xlarge-gap: 0.5rem;
    --controlStack-small-gap-condensed: 0.5rem;
    --controlStack-small-gap-spacious: 1rem;
    --controlStack-medium-gap-condensed: 0.5rem;
    --controlStack-medium-gap-spacious: 0.75rem;
    --controlStack-large-gap-auto: 0.5rem;
    --controlStack-large-gap-condensed: 0.5rem;
    --controlStack-large-gap-spacious: 0.75rem;
    --space-xxsmall: 0.125rem;
    --space-xsmall: 0.25rem;
    --space-small: 0.375rem;
    --space-medium: 0.5rem;
    --space-large: 0.75rem;
    --space-xlarge: 1rem;
    --spinner-strokeWidth-default: 0.125rem;
    --spinner-size-small: 1rem;
    --spinner-size-medium: 2rem;
    --spinner-size-large: 4rem;
    --stack-padding-condensed: 0.5rem;
    --stack-padding-normal: 1rem;
    --stack-padding-spacious: 1.5rem;
    --stack-gap-condensed: 0.5rem;
    --stack-gap-normal: 1rem;
    --stack-gap-spacious: 1.5rem;
    --overlay-width-xsmall: 12rem;
    --overlay-width-small: 20rem;
    --overlay-width-medium: 30rem;
    --overlay-width-large: 40rem;
    --overlay-width-xlarge: 60rem;
    --overlay-height-small: 16rem;
    --overlay-height-medium: 20rem;
    --overlay-height-large: 27rem;
    --overlay-height-xlarge: 37.5rem;
    --overlay-padding-normal: 1rem;
    --overlay-padding-condensed: 0.5rem;
    --overlay-paddingBlock-condensed: 0.25rem;
    --overlay-paddingBlock-normal: 0.75rem;
    --overlay-borderRadius: 0.375rem;
    --overlay-offset: 0.25rem;
    --text-codeInline-size: 0.9285em;
    --text-codeBlock-lineHeight: 1.5385;
    --text-codeBlock-size: 0.8125rem;
    --text-caption-lineHeight: 1.3333;
    --text-caption-size: 0.75rem;
    --text-body-lineHeight-small: 1.6666;
    --text-body-lineHeight-medium: 1.4285;
    --text-body-lineHeight-large: 1.5;
    --text-body-size-small: 0.75rem;
    --text-body-size-medium: 0.875rem;
    --text-body-size-large: 1rem;
    --text-subtitle-lineHeight: 1.6;
    --text-subtitle-size: 1.25rem;
    --text-title-lineHeight-small: 1.5;
    --text-title-lineHeight-medium: 1.6;
    --text-title-lineHeight-large: 1.5;
    --text-title-size-small: 1rem;
    --text-title-size-medium: 1.25rem;
    --text-title-size-large: 2rem;
    --text-display-lineHeight: 1.4;
    --text-display-size: 2.5rem;
    --text-display-lineBoxHeight: 1.4;
    --fontStack-monospace: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas, Liberation Mono, monospace;
    --fontStack-sansSerif: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
    --fontStack-system: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
    --text-codeInline-weight: var(--base-text-weight-normal);
    --text-codeBlock-weight: var(--base-text-weight-normal);
    --text-caption-weight: var(--base-text-weight-normal);
    --text-body-weight: var(--base-text-weight-normal);
    --text-subtitle-weight: var(--base-text-weight-normal);
    --text-title-weight-small: var(--base-text-weight-semibold);
    --text-title-weight-medium: var(--base-text-weight-semibold);
    --text-title-weight-large: var(--base-text-weight-semibold);
    --text-display-weight: var(--base-text-weight-medium);
    --text-codeInline-shorthand: var(--text-codeInline-weight) var(--text-codeInline-size) var(--fontStack-monospace);
    --text-codeBlock-shorthand: var(--text-codeBlock-weight) var(--text-codeBlock-size) / var(--text-codeBlock-lineHeight) var(--fontStack-monospace);
    --text-caption-shorthand: var(--text-caption-weight) var(--text-caption-size) / var(--text-caption-lineHeight) var(--fontStack-sansSerif);
    --text-body-shorthand-small: var(--text-body-weight) var(--text-body-size-small) / var(--text-body-lineHeight-small) var(--fontStack-sansSerif);
    --text-body-shorthand-medium: var(--text-body-weight) var(--text-body-size-medium) / var(--text-body-lineHeight-medium) var(--fontStack-sansSerif);
    --text-body-shorthand-large: var(--text-body-weight) var(--text-body-size-large) / var(--text-body-lineHeight-large) var(--fontStack-sansSerif);
    --text-subtitle-shorthand: var(--text-subtitle-weight) var(--text-subtitle-size) / var(--text-subtitle-lineHeight) var(--fontStack-sansSerif);
    --text-title-shorthand-small: var(--text-title-weight-small) var(--text-title-size-small) / var(--text-title-lineHeight-small) var(--fontStack-sansSerif);
    --text-title-shorthand-medium: var(--text-title-weight-medium) var(--text-title-size-medium) / var(--text-title-lineHeight-medium) var(--fontStack-sansSerif);
    --text-title-shorthand-large: var(--text-title-weight-large) var(--text-title-size-large) / var(--text-title-lineHeight-large) var(--fontStack-sansSerif);
    --text-display-shorthand: var(--text-display-weight) var(--text-display-size) / var(--text-display-lineHeight) var(--fontStack-sansSerif);
    --h00-size-mobile: 2.5rem;
    --h0-size-mobile: 2rem;
    --h1-size-mobile: 1.625rem;
    --h2-size-mobile: 1.375rem;
    --h3-size-mobile: 1.125rem;
    --h00-size: 3rem;
    --h0-size: 2.5rem;
    --h1-size: 2rem;
    --h2-size: 1.5rem;
    --h3-size: 1.25rem;
    --h4-size: 1rem;
    --h5-size: 0.875rem;
    --h6-size: 0.75rem;
    --body-font-size: 0.875rem;
    --font-size-small: 0.75rem;
    --Layout-pane-width: 220px;
    --Layout-content-width: 100%;
    --Layout-template-columns: 1fr var(--Layout-pane-width);
    --Layout-template-areas: "content pane";
    --Layout-column-gap: 16px;
    --Layout-row-gap: 16px;
    --Layout-outer-spacing-x: 0px;
    --Layout-outer-spacing-y: 0px;
    --Layout-inner-spacing-min: 0px;
    --Layout-inner-spacing-max: 0px;
    --actionListContent-paddingBlock: var(--control-medium-paddingBlock);
    --duration-fast: 80ms;
    --easing-easeInOut: cubic-bezier(0.65, 0, 0.35, 1);
    --button-outline-borderColor-active: #1f232826;
    --focus-outline: #0969da solid 2px;
    --topicTag-borderColor: #00000000;
    --highlight-neutral-bgColor: #d2992266;
    --page-header-bgColor: #0d1117;
    --diffBlob-addition-fgColor-text: #e6edf3;
    --diffBlob-addition-fgColor-num: #e6edf3;
    --diffBlob-addition-bgColor-num: #3fb9504d;
    --diffBlob-addition-bgColor-line: #2ea04326;
    --diffBlob-addition-bgColor-word: #2ea04366;
    --diffBlob-deletion-fgColor-text: #e6edf3;
    --diffBlob-deletion-fgColor-num: #e6edf3;
    --diffBlob-deletion-bgColor-num: #f851494d;
    --diffBlob-deletion-bgColor-line: #f8514926;
    --diffBlob-deletion-bgColor-word: #f8514966;
    --diffBlob-hunk-bgColor-num: #388bfd66;
    --diffBlob-expander-iconColor: #8d96a0;
    --codeMirror-fgColor: #e6edf3;
    --codeMirror-bgColor: #0d1117;
    --codeMirror-gutters-bgColor: #0d1117;
    --codeMirror-gutterMarker-fgColor-default: #0d1117;
    --codeMirror-gutterMarker-fgColor-muted: #8d96a0;
    --codeMirror-lineNumber-fgColor: #8d96a0;
    --codeMirror-cursor-fgColor: #e6edf3;
    --codeMirror-selection-bgColor: #388bfd66;
    --codeMirror-activeline-bgColor: #6e768166;
    --codeMirror-matchingBracket-fgColor: #e6edf3;
    --codeMirror-lines-bgColor: #0d1117;
    --codeMirror-syntax-fgColor-comment: #8b949e;
    --codeMirror-syntax-fgColor-constant: #79c0ff;
    --codeMirror-syntax-fgColor-entity: #d2a8ff;
    --codeMirror-syntax-fgColor-keyword: #ff7b72;
    --codeMirror-syntax-fgColor-storage: #ff7b72;
    --codeMirror-syntax-fgColor-string: #a5d6ff;
    --codeMirror-syntax-fgColor-support: #79c0ff;
    --codeMirror-syntax-fgColor-variable: #ffa657;
    --header-fgColor-default: #ffffffb3;
    --header-fgColor-logo: #f0f6fc;
    --header-bgColor: #161b22f2;
    --header-borderColor-divider: #8b949e;
    --headerSearch-bgColor: #0d1117;
    --headerSearch-borderColor: #30363d;
    --data-blue-color: #0576ff;
    --data-blue-color-muted: #001a47;
    --data-auburn-color: #a86f6b;
    --data-auburn-color-muted: #271817;
    --data-orange-color: #984b10;
    --data-orange-color-muted: #311708;
    --data-yellow-color: #895906;
    --data-yellow-color-muted: #2e1a00;
    --data-green-color: #2f6f37;
    --data-green-color-muted: #122117;
    --data-teal-color: #106c70;
    --data-teal-color-muted: #041f25;
    --data-purple-color: #975bf1;
    --data-purple-color-muted: #211047;
    --data-pink-color: #d34591;
    --data-pink-color-muted: #2d1524;
    --data-red-color: #eb3342;
    --data-red-color-muted: #3c0614;
    --data-gray-color: #576270;
    --data-gray-color-muted: #1c1c1c;
    --display-blue-bgColor-muted: #001a47;
    --display-blue-bgColor-emphasis: #0576ff;
    --display-blue-fgColor: #4da0ff;
    --display-blue-borderColor-muted: #002766;
    --display-blue-borderColor-emphasis: #0576ff;
    --display-green-bgColor-muted: #122117;
    --display-green-bgColor-emphasis: #388f3f;
    --display-green-fgColor: #41b445;
    --display-green-borderColor-muted: #182f1f;
    --display-green-borderColor-emphasis: #388f3f;
    --display-orange-bgColor-muted: #311708;
    --display-orange-bgColor-emphasis: #c46212;
    --display-orange-fgColor: #ed8326;
    --display-orange-borderColor-muted: #43200a;
    --display-orange-borderColor-emphasis: #c46212;
    --display-purple-bgColor-muted: #211047;
    --display-purple-bgColor-emphasis: #975bf1;
    --display-purple-fgColor: #b687f7;
    --display-purple-borderColor-muted: #31146b;
    --display-purple-borderColor-emphasis: #975bf1;
    --display-plum-bgColor-muted: #2a0e3f;
    --display-plum-bgColor-emphasis: #b643ef;
    --display-plum-fgColor: #d07ef7;
    --display-plum-borderColor-muted: #40125e;
    --display-plum-borderColor-emphasis: #b643ef;
    --display-red-bgColor-muted: #3c0614;
    --display-red-bgColor-emphasis: #eb3342;
    --display-red-fgColor: #f27d83;
    --display-red-borderColor-muted: #58091a;
    --display-red-borderColor-emphasis: #eb3342;
    --display-coral-bgColor-muted: #3c0614;
    --display-coral-bgColor-emphasis: #eb3342;
    --display-coral-fgColor: #f27d83;
    --display-coral-borderColor-muted: #58091a;
    --display-coral-borderColor-emphasis: #eb3342;
    --display-yellow-bgColor-muted: #2e1a00;
    --display-yellow-bgColor-emphasis: #aa7109;
    --display-yellow-fgColor: #d3910d;
    --display-yellow-borderColor-muted: #3d2401;
    --display-yellow-borderColor-emphasis: #aa7109;
    --display-gray-bgColor-muted: #1c1c1c;
    --display-gray-bgColor-emphasis: #6e7f96;
    --display-gray-fgColor: #92a1b5;
    --display-gray-borderColor-muted: #2a2b2d;
    --display-gray-borderColor-emphasis: #6e7f96;
    --display-auburn-bgColor-muted: #271817;
    --display-auburn-bgColor-emphasis: #a86f6b;
    --display-auburn-fgColor: #bf9592;
    --display-auburn-borderColor-muted: #3a2422;
    --display-auburn-borderColor-emphasis: #a86f6b;
    --display-brown-bgColor-muted: #241c14;
    --display-brown-bgColor-emphasis: #94774c;
    --display-brown-fgColor: #b69a6d;
    --display-brown-borderColor-muted: #342a1d;
    --display-brown-borderColor-emphasis: #94774c;
    --display-lemon-bgColor-muted: #291d00;
    --display-lemon-bgColor-emphasis: #977b0c;
    --display-lemon-fgColor: #ba9b12;
    --display-lemon-borderColor-muted: #372901;
    --display-lemon-borderColor-emphasis: #977b0c;
    --display-olive-bgColor-muted: #171e0b;
    --display-olive-bgColor-emphasis: #7a8321;
    --display-olive-fgColor: #a2a626;
    --display-olive-borderColor-muted: #252d10;
    --display-olive-borderColor-emphasis: #7a8321;
    --display-lime-bgColor-muted: #141f0f;
    --display-lime-bgColor-emphasis: #5f892f;
    --display-lime-fgColor: #7dae37;
    --display-lime-borderColor-muted: #1f3116;
    --display-lime-borderColor-emphasis: #5f892f;
    --display-pine-bgColor-muted: #082119;
    --display-pine-bgColor-emphasis: #18915e;
    --display-pine-fgColor: #1bb673;
    --display-pine-borderColor-muted: #0b3224;
    --display-pine-borderColor-emphasis: #18915e;
    --display-teal-bgColor-muted: #041f25;
    --display-teal-bgColor-emphasis: #158a8a;
    --display-teal-fgColor: #1cb0ab;
    --display-teal-borderColor-muted: #073036;
    --display-teal-borderColor-emphasis: #158a8a;
    --display-cyan-bgColor-muted: #001f29;
    --display-cyan-bgColor-emphasis: #0587b3;
    --display-cyan-fgColor: #07ace4;
    --display-cyan-borderColor-muted: #002e3d;
    --display-cyan-borderColor-emphasis: #0587b3;
    --display-indigo-bgColor-muted: #1b183f;
    --display-indigo-bgColor-emphasis: #7070e1;
    --display-indigo-fgColor: #9899ec;
    --display-indigo-borderColor-muted: #25215f;
    --display-indigo-borderColor-emphasis: #7070e1;
    --display-pink-bgColor-muted: #2d1524;
    --display-pink-bgColor-emphasis: #d34591;
    --display-pink-fgColor: #e57bb2;
    --display-pink-borderColor-muted: #451c35;
    --display-pink-borderColor-emphasis: #d34591;
    --avatar-bgColor: #ffffff1a;
    --avatar-borderColor: #ffffff26;
    --avatar-shadow: 0px 0px 0px 2px #0d1117;
    --avatarStack-fade-bgColor-default: #30363d;
    --avatarStack-fade-bgColor-muted: #21262d;
    --control-bgColor-rest: #21262d;
    --control-bgColor-hover: #292e36;
    --control-bgColor-active: #31363e;
    --control-bgColor-disabled: #21262db3;
    --control-bgColor-selected: #161b22;
    --control-fgColor-rest: #c9d1d9;
    --control-fgColor-placeholder: #484f58;
    --control-fgColor-disabled: #6e7681;
    --control-borderColor-rest: #30363d;
    --control-borderColor-emphasis: #666e79;
    --control-borderColor-disabled: #21262db3;
    --control-borderColor-selected: #f0f6fc;
    --control-borderColor-success: #238636;
    --control-borderColor-danger: #da3633;
    --control-borderColor-warning: #9e6a03;
    --control-iconColor-rest: #8d96a0;
    --control-transparent-bgColor-rest: #00000000;
    --control-transparent-bgColor-hover: #b1bac41f;
    --control-transparent-bgColor-active: #b1bac433;
    --control-transparent-bgColor-disabled: #21262db3;
    --control-transparent-bgColor-selected: #b1bac414;
    --control-transparent-borderColor-rest: #00000000;
    --control-transparent-borderColor-hover: #00000000;
    --control-transparent-borderColor-active: #00000000;
    --control-danger-fgColor-rest: #f85149;
    --control-danger-fgColor-hover: #ff7b72;
    --control-danger-bgColor-hover: #f851491a;
    --control-danger-bgColor-active: #f8514966;
    --control-checked-bgColor-rest: #1f6feb;
    --control-checked-bgColor-hover: #2a7aef;
    --control-checked-bgColor-active: #3685f3;
    --control-checked-bgColor-disabled: #6e7681;
    --control-checked-fgColor-rest: #ffffff;
    --control-checked-fgColor-disabled: #010409;
    --control-checked-borderColor-rest: #1f6feb;
    --control-checked-borderColor-hover: #2a7aef;
    --control-checked-borderColor-active: #3685f3;
    --control-checked-borderColor-disabled: #6e7681;
    --controlTrack-bgColor-rest: #21262d;
    --controlTrack-bgColor-hover: #292e36;
    --controlTrack-bgColor-active: #31363e;
    --controlTrack-bgColor-disabled: #6e7681;
    --controlTrack-fgColor-rest: #8d96a0;
    --controlTrack-fgColor-disabled: #ffffff;
    --controlTrack-borderColor-rest: #00000000;
    --controlTrack-borderColor-disabled: #6e7681;
    --controlKnob-bgColor-rest: #010409;
    --controlKnob-bgColor-disabled: #21262db3;
    --controlKnob-bgColor-checked: #ffffff;
    --controlKnob-borderColor-rest: #666e79;
    --controlKnob-borderColor-disabled: #21262db3;
    --controlKnob-borderColor-checked: #1f6feb;
    --counter-borderColor: #00000000;
    --button-default-fgColor-rest: #c9d1d9;
    --button-default-bgColor-rest: #21262d;
    --button-default-bgColor-hover: #292e36;
    --button-default-bgColor-active: #31363e;
    --button-default-bgColor-selected: #31363e;
    --button-default-bgColor-disabled: #21262db3;
    --button-default-borderColor-rest: #30363d;
    --button-default-borderColor-hover: #30363d;
    --button-default-borderColor-active: #30363d;
    --button-default-borderColor-disabled: #21262db3;
    --button-default-shadow-resting: 0px 0px 0px 0px #000000;
    --button-primary-fgColor-rest: #ffffff;
    --button-primary-fgColor-disabled: #ffffff66;
    --button-primary-iconColor-rest: #ffffff;
    --button-primary-bgColor-rest: #238636;
    --button-primary-bgColor-hover: #29903b;
    --button-primary-bgColor-active: #2e9a40;
    --button-primary-bgColor-disabled: #105823;
    --button-primary-borderColor-rest: #f0f6fc1a;
    --button-primary-borderColor-hover: #f0f6fc1a;
    --button-primary-borderColor-active: #f0f6fc1a;
    --button-primary-borderColor-disabled: #105823;
    --button-primary-shadow-selected: 0px 0px 0px 0px #000000;
    --button-invisible-fgColor-rest: #4493f8;
    --button-invisible-fgColor-hover: #58a6ff;
    --button-invisible-fgColor-disabled: #6e7681;
    --button-invisible-iconColor-rest: #8d96a0;
    --button-invisible-iconColor-hover: #e6edf3;
    --button-invisible-iconColor-disabled: #6e7681;
    --button-invisible-bgColor-rest: #00000000;
    --button-invisible-bgColor-hover: #b1bac41f;
    --button-invisible-bgColor-active: #b1bac433;
    --button-invisible-bgColor-disabled: #21262db3;
    --button-invisible-borderColor-rest: #00000000;
    --button-invisible-borderColor-hover: #00000000;
    --button-invisible-borderColor-disabled: #21262db3;
    --button-outline-fgColor-rest: #388bfd;
    --button-outline-fgColor-hover: #58a6ff;
    --button-outline-fgColor-active: #ffffff;
    --button-outline-fgColor-disabled: #4493f880;
    --button-outline-bgColor-rest: #f0f6fc;
    --button-outline-bgColor-hover: #30363d;
    --button-outline-bgColor-active: #0d419d;
    --button-outline-bgColor-disabled: #0d1117;
    --button-outline-borderColor-hover: #f0f6fc1a;
    --button-outline-borderColor-selected: #f0f6fc1a;
    --button-outline-shadow-selected: 0px 0px 0px 0px #000000;
    --button-danger-fgColor-rest: #f85149;
    --button-danger-fgColor-hover: #ffffff;
    --button-danger-fgColor-active: #ffffff;
    --button-danger-fgColor-disabled: #f8514980;
    --button-danger-iconColor-rest: #f85149;
    --button-danger-iconColor-hover: #ffffff;
    --button-danger-bgColor-rest: #21262d;
    --button-danger-bgColor-hover: #b62324;
    --button-danger-bgColor-active: #d03533;
    --button-danger-bgColor-disabled: #21262db3;
    --button-danger-borderColor-rest: #30363d;
    --button-danger-borderColor-hover: #f0f6fc1a;
    --button-danger-borderColor-active: #f0f6fc1a;
    --button-danger-shadow-selected: 0px 0px 0px 0px #000000;
    --button-inactive-fgColor: #8b949e;
    --button-inactive-bgColor: #21262d;
    --button-star-iconColor: #e3b341;
    --buttonCounter-default-bgColor-rest: #30363d;
    --buttonCounter-invisible-bgColor-rest: #30363d;
    --buttonCounter-primary-bgColor-rest: #04260f33;
    --buttonCounter-outline-bgColor-rest: #051d4d33;
    --buttonCounter-outline-bgColor-hover: #051d4d33;
    --buttonCounter-outline-bgColor-disabled: #1f6feb0d;
    --buttonCounter-outline-fgColor-rest: #388bfd;
    --buttonCounter-outline-fgColor-hover: #58a6ff;
    --buttonCounter-outline-fgColor-disabled: #4493f880;
    --buttonCounter-danger-bgColor-hover: #ffffff33;
    --buttonCounter-danger-bgColor-disabled: #da36330d;
    --buttonCounter-danger-bgColor-rest: #49020233;
    --buttonCounter-danger-fgColor-rest: #f85149;
    --buttonCounter-danger-fgColor-hover: #ffffff;
    --buttonCounter-danger-fgColor-disabled: #f8514980;
    --reactionButton-selected-bgColor-rest: #388bfd33;
    --reactionButton-selected-bgColor-hover: #3a8cfd5c;
    --reactionButton-selected-fgColor-rest: #4493f8;
    --reactionButton-selected-fgColor-hover: #79c0ff;
    --focus-outlineColor: #1f6feb;
    --menu-bgColor-active: #161b22;
    --overlay-bgColor: #161b22;
    --overlay-borderColor: #30363db3;
    --overlay-backdrop-bgColor: #161b2266;
    --selectMenu-borderColor: #484f58;
    --selectMenu-bgColor-active: #0c2d6b;
    --sideNav-bgColor-selected: #21262d;
    --skeletonLoader-bgColor: #161b22;
    --timelineBadge-bgColor: #21262d;
    --treeViewItem-leadingVisual-iconColor-rest: #8d96a0;
    --underlineNav-borderColor-active: #f78166;
    --underlineNav-borderColor-hover: #6e768166;
    --underlineNav-iconColor-rest: #8d96a0;
    --selection-bgColor: #1f6febb3;
    --card-bgColor: #161b22;
    --label-green-bgColor-rest: #122117;
    --label-green-bgColor-hover: #182f1f;
    --label-green-bgColor-active: #214529;
    --label-green-fgColor-rest: #41b445;
    --label-green-fgColor-hover: #46c144;
    --label-green-fgColor-active: #75d36f;
    --label-orange-bgColor-rest: #311708;
    --label-orange-bgColor-hover: #43200a;
    --label-orange-bgColor-active: #632f0d;
    --label-orange-fgColor-rest: #ed8326;
    --label-orange-fgColor-hover: #f1933b;
    --label-orange-fgColor-active: #f6b06a;
    --label-purple-bgColor-rest: #211047;
    --label-purple-bgColor-hover: #31146b;
    --label-purple-bgColor-active: #481a9e;
    --label-purple-fgColor-rest: #b687f7;
    --label-purple-fgColor-hover: #c398fb;
    --label-purple-fgColor-active: #d2affd;
    --label-red-bgColor-rest: #3c0614;
    --label-red-bgColor-hover: #58091a;
    --label-red-bgColor-active: #790c20;
    --label-red-fgColor-rest: #f27d83;
    --label-red-fgColor-hover: #f48b8d;
    --label-red-fgColor-active: #f7adab;
    --label-yellow-bgColor-rest: #2e1a00;
    --label-yellow-bgColor-hover: #3d2401;
    --label-yellow-bgColor-active: #5a3702;
    --label-yellow-fgColor-rest: #d3910d;
    --label-yellow-fgColor-hover: #df9e11;
    --label-yellow-fgColor-active: #edb431;
    --label-gray-bgColor-rest: #1c1c1c;
    --label-gray-bgColor-hover: #2a2b2d;
    --label-gray-bgColor-active: #393d41;
    --label-gray-fgColor-rest: #92a1b5;
    --label-gray-fgColor-hover: #9babbf;
    --label-gray-fgColor-active: #b3c0d1;
    --label-auburn-bgColor-rest: #271817;
    --label-auburn-bgColor-hover: #3a2422;
    --label-auburn-bgColor-active: #543331;
    --label-auburn-fgColor-rest: #bf9592;
    --label-auburn-fgColor-hover: #c6a19f;
    --label-auburn-fgColor-active: #d4b7b5;
    --label-brown-bgColor-rest: #241c14;
    --label-brown-bgColor-hover: #342a1d;
    --label-brown-bgColor-active: #483a28;
    --label-brown-fgColor-rest: #b69a6d;
    --label-brown-fgColor-hover: #bfa77d;
    --label-brown-fgColor-active: #cdbb98;
    --label-lemon-bgColor-rest: #291d00;
    --label-lemon-bgColor-hover: #372901;
    --label-lemon-bgColor-active: #4f3c02;
    --label-lemon-fgColor-rest: #ba9b12;
    --label-lemon-fgColor-hover: #c4a717;
    --label-lemon-fgColor-active: #d7bc1d;
    --label-olive-bgColor-rest: #171e0b;
    --label-olive-bgColor-hover: #252d10;
    --label-olive-bgColor-active: #374115;
    --label-olive-fgColor-rest: #a2a626;
    --label-olive-fgColor-hover: #b2af24;
    --label-olive-fgColor-active: #cbc025;
    --label-lime-bgColor-rest: #141f0f;
    --label-lime-bgColor-hover: #1f3116;
    --label-lime-bgColor-active: #2c441d;
    --label-lime-fgColor-rest: #7dae37;
    --label-lime-fgColor-hover: #89ba36;
    --label-lime-fgColor-active: #9fcc3e;
    --label-pine-bgColor-rest: #082119;
    --label-pine-bgColor-hover: #0b3224;
    --label-pine-bgColor-active: #0e4430;
    --label-pine-fgColor-rest: #1bb673;
    --label-pine-fgColor-hover: #1ac176;
    --label-pine-fgColor-active: #1bda81;
    --label-teal-bgColor-rest: #041f25;
    --label-teal-bgColor-hover: #073036;
    --label-teal-bgColor-active: #0a464d;
    --label-teal-fgColor-rest: #1cb0ab;
    --label-teal-fgColor-hover: #1fbdb2;
    --label-teal-fgColor-active: #24d6c4;
    --label-cyan-bgColor-rest: #001f29;
    --label-cyan-bgColor-hover: #002e3d;
    --label-cyan-bgColor-active: #014156;
    --label-cyan-fgColor-rest: #07ace4;
    --label-cyan-fgColor-hover: #09b7f1;
    --label-cyan-fgColor-active: #45cbf7;
    --label-indigo-bgColor-rest: #1b183f;
    --label-indigo-bgColor-hover: #25215f;
    --label-indigo-bgColor-active: #312c90;
    --label-indigo-fgColor-rest: #9899ec;
    --label-indigo-fgColor-hover: #a2a5f1;
    --label-indigo-fgColor-active: #b7baf6;
    --label-blue-bgColor-rest: #001a47;
    --label-blue-bgColor-hover: #002766;
    --label-blue-bgColor-active: #00378a;
    --label-blue-fgColor-rest: #4da0ff;
    --label-blue-fgColor-hover: #61adff;
    --label-blue-fgColor-active: #85c2ff;
    --label-plum-bgColor-rest: #2a0e3f;
    --label-plum-bgColor-hover: #40125e;
    --label-plum-bgColor-active: #5c1688;
    --label-plum-fgColor-rest: #d07ef7;
    --label-plum-fgColor-hover: #d889fa;
    --label-plum-fgColor-active: #e4a5fd;
    --label-pink-bgColor-rest: #2d1524;
    --label-pink-bgColor-hover: #451c35;
    --label-pink-bgColor-active: #65244a;
    --label-pink-fgColor-rest: #e57bb2;
    --label-pink-fgColor-hover: #ec8dbd;
    --label-pink-fgColor-active: #f4a9cd;
    --label-coral-bgColor-rest: #351008;
    --label-coral-bgColor-hover: #51180b;
    --label-coral-bgColor-active: #72220d;
    --label-coral-fgColor-rest: #f7794b;
    --label-coral-fgColor-hover: #fa8c61;
    --label-coral-fgColor-active: #fdaa86;
    --fgColor-default: #e6edf3;
    --fgColor-muted: #8d96a0;
    --fgColor-onEmphasis: #ffffff;
    --fgColor-white: #ffffff;
    --fgColor-black: #010409;
    --fgColor-disabled: #6e7681;
    --fgColor-link: #4493f8;
    --fgColor-neutral: #6e7681;
    --fgColor-accent: #4493f8;
    --fgColor-success: #3fb950;
    --fgColor-attention: #d29922;
    --fgColor-severe: #db6d28;
    --fgColor-danger: #f85149;
    --fgColor-open: #3fb950;
    --fgColor-closed: #f85149;
    --fgColor-done: #ab7df8;
    --fgColor-upsell: #ab7df8;
    --fgColor-sponsors: #db61a2;
    --bgColor-default: #0d1117;
    --bgColor-muted: #161b22;
    --bgColor-inset: #010409;
    --bgColor-emphasis: #6e7681;
    --bgColor-inverse: #ffffff;
    --bgColor-white: #ffffff;
    --bgColor-black: #010409;
    --bgColor-disabled: #21262db3;
    --bgColor-transparent: #00000000;
    --bgColor-neutral-muted: #6e768166;
    --bgColor-neutral-emphasis: #6e7681;
    --bgColor-accent-muted: #388bfd1a;
    --bgColor-accent-emphasis: #1f6feb;
    --bgColor-success-muted: #2ea04326;
    --bgColor-success-emphasis: #238636;
    --bgColor-attention-muted: #bb800926;
    --bgColor-attention-emphasis: #9e6a03;
    --bgColor-severe-muted: #db6d281a;
    --bgColor-severe-emphasis: #bd561d;
    --bgColor-danger-muted: #f851491a;
    --bgColor-danger-emphasis: #da3633;
    --bgColor-open-muted: #2ea0431a;
    --bgColor-open-emphasis: #238636;
    --bgColor-closed-muted: #f8514926;
    --bgColor-closed-emphasis: #da3633;
    --bgColor-done-muted: #ab7df826;
    --bgColor-done-emphasis: #8957e5;
    --bgColor-upsell-muted: #ab7df826;
    --bgColor-upsell-emphasis: #8957e5;
    --bgColor-sponsors-muted: #db61a21a;
    --bgColor-sponsors-emphasis: #bf4b8a;
    --borderColor-default: #30363d;
    --borderColor-muted: #30363db3;
    --borderColor-emphasis: #484f58;
    --borderColor-disabled: #21262db3;
    --borderColor-transparent: #00000000;
    --borderColor-neutral-muted: #6e768166;
    --borderColor-neutral-emphasis: #6e7681;
    --borderColor-accent-muted: #388bfd66;
    --borderColor-accent-emphasis: #1f6feb;
    --borderColor-success-muted: #2ea04366;
    --borderColor-success-emphasis: #238636;
    --borderColor-attention-muted: #bb800966;
    --borderColor-attention-emphasis: #9e6a03;
    --borderColor-severe-muted: #db6d2866;
    --borderColor-severe-emphasis: #bd561d;
    --borderColor-danger-muted: #f8514966;
    --borderColor-danger-emphasis: #da3633;
    --borderColor-open-muted: #2ea04366;
    --borderColor-open-emphasis: #238636;
    --borderColor-closed-muted: #f8514966;
    --borderColor-closed-emphasis: #da3633;
    --borderColor-done-muted: #ab7df866;
    --borderColor-done-emphasis: #8957e5;
    --borderColor-upsell-muted: #ab7df866;
    --borderColor-upsell-emphasis: #8957e5;
    --borderColor-sponsors-muted: #db61a266;
    --borderColor-sponsors-emphasis: #bf4b8a;
    --color-ansi-black: #484f58;
    --color-ansi-black-bright: #6e7681;
    --color-ansi-white: #b1bac4;
    --color-ansi-white-bright: #ffffff;
    --color-ansi-gray: #6e7681;
    --color-ansi-red: #ff7b72;
    --color-ansi-red-bright: #ffa198;
    --color-ansi-green: #3fb950;
    --color-ansi-green-bright: #56d364;
    --color-ansi-yellow: #d29922;
    --color-ansi-yellow-bright: #e3b341;
    --color-ansi-blue: #58a6ff;
    --color-ansi-blue-bright: #79c0ff;
    --color-ansi-magenta: #be8fff;
    --color-ansi-magenta-bright: #d2a8ff;
    --color-ansi-cyan: #39c5cf;
    --color-ansi-cyan-bright: #56d4dd;
    --color-prettylights-syntax-comment: #8b949e;
    --color-prettylights-syntax-constant: #79c0ff;
    --color-prettylights-syntax-constant-other-reference-link: #a5d6ff;
    --color-prettylights-syntax-entity: #d2a8ff;
    --color-prettylights-syntax-storage-modifier-import: #c9d1d9;
    --color-prettylights-syntax-entity-tag: #7ee787;
    --color-prettylights-syntax-keyword: #ff7b72;
    --color-prettylights-syntax-string: #a5d6ff;
    --color-prettylights-syntax-variable: #ffa657;
    --color-prettylights-syntax-brackethighlighter-unmatched: #f85149;
    --color-prettylights-syntax-brackethighlighter-angle: #8b949e;
    --color-prettylights-syntax-invalid-illegal-text: #f0f6fc;
    --color-prettylights-syntax-invalid-illegal-bg: #8e1519;
    --color-prettylights-syntax-carriage-return-text: #f0f6fc;
    --color-prettylights-syntax-carriage-return-bg: #b62324;
    --color-prettylights-syntax-string-regexp: #7ee787;
    --color-prettylights-syntax-markup-list: #f2cc60;
    --color-prettylights-syntax-markup-heading: #1f6feb;
    --color-prettylights-syntax-markup-italic: #c9d1d9;
    --color-prettylights-syntax-markup-bold: #c9d1d9;
    --color-prettylights-syntax-markup-deleted-text: #ffdcd7;
    --color-prettylights-syntax-markup-deleted-bg: #67060c;
    --color-prettylights-syntax-markup-inserted-text: #aff5b4;
    --color-prettylights-syntax-markup-inserted-bg: #033a16;
    --color-prettylights-syntax-markup-changed-text: #ffdfb6;
    --color-prettylights-syntax-markup-changed-bg: #5a1e02;
    --color-prettylights-syntax-markup-ignored-text: #c9d1d9;
    --color-prettylights-syntax-markup-ignored-bg: #1158c7;
    --color-prettylights-syntax-meta-diff-range: #d2a8ff;
    --color-prettylights-syntax-sublimelinter-gutter-mark: #484f58;
    --shadow-inset: inset 0px 1px 0px 0px #0104093d;
    --shadow-resting-xsmall: 0px 1px 0px 0px #010409cc;
    --shadow-resting-small: 0px 1px 0px 0px #01040966;
    --shadow-resting-medium: 0px 3px 6px 0px #010409cc;
    --shadow-floating-small: 0px 0px 0px 1px #30363d, 0px 6px 12px -3px #01040966, 0px 6px 18px 0px #01040966;
    --shadow-floating-medium: 0px 0px 0px 1px #30363d, 0px 8px 16px -4px #01040966, 0px 4px 32px -4px #01040966, 0px 24px 48px -12px #01040966, 0px 48px 96px -24px #01040966;
    --shadow-floating-large: 0px 0px 0px 1px #30363d, 0px 24px 48px 0px #010409;
    --shadow-floating-xlarge: 0px 0px 0px 1px #30363d, 0px 32px 64px 0px #010409;
    --shadow-floating-legacy: 0px 6px 12px -3px #01040966, 0px 6px 18px 0px #01040966;
    --outline-focus: #1f6feb solid 2px;
    color-scheme: dark;
    --color-workflow-card-bg: var(--bgColor-muted, var(--color-scale-gray-7));
    --color-workflow-card-header-shadow: rgba(27, 31, 35, 0.04);
    --color-bg-discussions-row-emoji-box: #57606a;
    --color-notifications-row-read-bg: var(--bgColor-default, var(--color-canvas-default));
    --color-notifications-row-bg: var(--bgColor-muted, var(--color-canvas-subtle));
    --color-calendar-halloween-graph-day-L1-bg: #631c03;
    --color-calendar-halloween-graph-day-L2-bg: #bd561d;
    --color-calendar-halloween-graph-day-L3-bg: #fa7a18;
    --color-calendar-halloween-graph-day-L4-bg: #fddf68;
    --color-calendar-winter-graph-day-L1-bg: #0A3069;
    --color-calendar-winter-graph-day-L2-bg: #0969DA;
    --color-calendar-winter-graph-day-L3-bg: #54AEFF;
    --color-calendar-winter-graph-day-L4-bg: #B6E3FF;
    --color-calendar-graph-day-bg: #161b22;
    --color-calendar-graph-day-border: rgba(27, 31, 35, 0.06);
    --color-calendar-graph-day-L1-bg: #0e4429;
    --color-calendar-graph-day-L2-bg: #006d32;
    --color-calendar-graph-day-L3-bg: #26a641;
    --color-calendar-graph-day-L4-bg: #39d353;
    --color-calendar-graph-day-L1-border: rgba(255, 255, 255, 0.05);
    --color-calendar-graph-day-L2-border: rgba(255, 255, 255, 0.05);
    --color-calendar-graph-day-L3-border: rgba(255, 255, 255, 0.05);
    --color-calendar-graph-day-L4-border: rgba(255, 255, 255, 0.05);
    --color-user-mention-fg: var(--fgColor-attention, var(--color-scale-yellow-0));
    --color-mktg-btn-shadow-outline: rgba(255, 255, 255, 0.25) 0 0 0 1px inset;
    --color-marketing-icon-primary: #79c0ff;
    --color-marketing-icon-secondary: #1f6feb;
    --color-project-header-bg: #0d1117;
    --color-project-sidebar-bg: #161b22;
    --color-project-gradient-in: #161b22;
    --color-project-gradient-out: rgba(22, 27, 34, 0);
    --color-diff-blob-selected-line-highlight-mix-blend-mode: screen;
    --color-text-white: var(--fgColor-white, var(--color-scale-white));
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
    --dialog-scrollgutter: 17px;
    word-wrap: break-word;
    box-sizing: border-box;
    align-items: center !important;
    display: flex !important;
    border-radius: 2em;
    font-size: var(--text-body-size-medium);
    font-weight: var(--base-text-weight-medium);
    line-height: var(--control-medium-lineBoxHeight);
    padding: 5px var(--control-medium-paddingInline-normal);
    text-align: center;
    white-space: nowrap;
    border: var(--borderWidth-thin) solid #0000;
    background-color: plum;
    color: var(--fgColor-onEmphasis);
    margin-right: var(--base-size-8);
}
</style>