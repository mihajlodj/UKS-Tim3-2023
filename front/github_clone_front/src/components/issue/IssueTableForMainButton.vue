<template>
    <div style="margin-left:auto; margin-right:auto;">
        <div class="btn-group mb-2" style="text-align: left;" role="group" aria-label="Basic radio toggle button group">
            <input type="radio" @click="this.showOpen = true; this.showClosed = false;" class="btn-check"
                name="btnradio" id="btnradio1" autocomplete="off" :checked="this.showOpen">
            <label class="btn btn-outline-primary" for="btnradio1">Open issues</label>

            <input type="radio" @click="this.showOpen = false; this.showClosed = true;" class="btn-check"
                name="btnradio" id="btnradio2" autocomplete="off" :checked="this.showClosed">
            <label class="btn btn-outline-primary" for="btnradio2">Closed issues</label>

            <input type="radio" @click="this.showOpen = true; this.showClosed = true;" class="btn-check" name="btnradio"
                id="btnradio3" autocomplete="off" :checked="this.showOpen && this.showClosed">
            <label class="btn btn-outline-primary" for="btnradio3">All issues</label>
        </div>
        <div v-if="this.showOpen">
            <table class="" style="margin-left:auto; margin-right:auto; width: 100%;">
                <tr colspan="9">
                    <span font-size="28px" font-weight="bold" class="bright">Open issues: {{ this.filteredOpenIssues.length }}</span>
                    <hr>
                </tr>
                <tr colspan="9">
                    <IssueList :issueList="this.filteredOpenIssues" :isOpen="true" :milestones="this.milestones" :key="componentKey" />
                </tr>
            </table>

        </div>
        <div v-if="this.showClosed">
            <table class="" style="margin-left:auto; margin-right:auto; width: 100%;">
                <tr colspan="9">
                    <span font-size="28px" font-weight="bold" class="bright">Closed issues: {{ this.filteredClosedIssues.length }}</span>
                    <hr>
                </tr>
                <tr>
                    <IssueList :issueList="this.filteredClosedIssues" :isOpen="false" :milestones="this.milestones" :key="componentKey" />
                </tr>
            </table>

        </div>
    </div>
</template>
<script>
import IssueList from './IssueList.vue';
import MilestoneService from '@/services/MilestoneService';

export default {
    name: 'IssueTableForMainButton',
    components: {
        IssueList
    },
    props: ["issuesForDisplay"],
    watch: {
        issuesForDisplay(newVal) {
            this.issues = newVal;
            this.filteredOpenIssues = this.filterOpenIssues();
            this.filteredClosedIssues = this.filterClosedIssues();
            this.forceRerender();
        }
    },
    mounted() {
        this.issues = this.issuesForDisplay;
        this.filteredOpenIssues = this.filterOpenIssues();
        this.filteredClosedIssues = this.filterClosedIssues();

        MilestoneService.getAllMilestones(this.$route.params.username, this.$route.params.repoName).then(res => {
            this.milestones = res.data;
        }).catch(err => console.log(err));
    },
    data() {
        return {
            showOpen: true,
            showClosed: false,

            issues: [],
            filteredOpenIssues: [],
            filteredClosedIssues: [],
            milestones: [],
            componentKey: 0,
        }
    },
    methods: {
        filterOpenIssues() {
            return this.issues.filter((issue) => issue.open);
        },
        filterClosedIssues() {
            return this.issues.filter((issue) => !issue.open)
        },
        forceRerender() {
            this.componentKey += 1;
        }
    },
}
</script>
<style scoped>
thead th {
    background-color: #e9ecef;
}

button:hover {
    color: white;
}

button {
    color: white;
}

.bright {
    color: #ffffff;
}
</style>
