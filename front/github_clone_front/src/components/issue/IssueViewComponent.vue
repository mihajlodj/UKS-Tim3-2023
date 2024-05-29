<template>
    <div class="background is-fullheight min-vh-100">
        <RepoNavbar starting="issues" />
    <div class="d-flex justify-content-between px-5 pt-4">
        <div class="d-flex justify-content-start">
            <h2 class="bright me-2">{{ this.issue.title }}</h2>
            <h2 class="muted">#{{ this.issue.id }}</h2>
        </div>
    </div>

    <div class="px-5 mt-2 d-flex justify-content-start">

        <div class="d-flex justify-content-start ms-3">
            <button class="bg-none muted" type="button">
                {{ this.issue.creator.username}}
            </button>
            <label class="muted">opened this issue {{ howLongAgo(this.issue.created) }}</label>
        </div>
    </div>

    <div class="px-5 pb-5 mt-2 w-100 d-flex justify-content-between">
        <div class="w-75 pe-5">
            <div>
                <div>
                    <div class="description w-100 mt-2">
                        <label class="bright">{{ this.issue.description ? this.issue.description : '--No description provided' }}</label>
                    </div>
                </div>
                <hr class="bright" />
            </div>

            <CommentDisplay 
                :username="this.$route.params.username" 
                :repoName="this.$route.params.repoName"
                :entityType="'issue'"
                :entityId="this.$route.params.issue_id"
                >
            </CommentDisplay>

            <div class="mt-3">
                <div class="w-100 d-flex justify-content-end mt-2">
                    <button v-if="this.issue.open === true" type="button" class="btn btn-warning bright p-2" @click="this.close()">
                        Close issue
                    </button>
                    <button v-else type="button" class="btn btn-warning bright p-2" @click="this.reopen()">
                        Reopen issue
                    </button>
                </div>
            </div>
        </div>
       
        
        
        <div class="w-25">
            <AdditionalIssueInfo :key="additionalInfoKey" :chosenMilestone="this.issue.milestone" 
                :chosenAssignees="this.issue.manager" :selectedLabels="issue.labels" :issueId="issue.id"
                :owner="this.owner" :repoName="this.repoName"
                @addAssignee="addAssignee" @removeAssignee="removeAssignee" @updateMilestone="updateMilestone" />
            <hr class="bright"/>
            <div class="w-100 d-flex justify-content-end mt-3">
                <button type="button" class="btn-save p-2 bright" @click="update">Save changes</button>
            </div>
        </div>

        
    
    </div>
</div>
</template>

<script>
import RepoNavbar from '@/components/repository/RepoNavbar.vue';
import IssueService from '@/services/IssueService';
import AdditionalIssueInfo from './AdditionalIssueInfo.vue';
// import DeveloperService from '@/services/DeveloperService';
import { toast } from 'vue3-toastify';
import CommentDisplay from '@/components/comment/CommentDisplay.vue'

export default {
    name: 'IssueViewComponent',
    components: {
        RepoNavbar,
        AdditionalIssueInfo,
        CommentDisplay,
    },
    mounted() {
        console.log('Params: ', this.$route.params)
        this.owner = this.$route.params.ownerUsername;
        this.repoName = this.$route.params.repoName;
        IssueService.getIssue(this.$route.params.issue_id).then((res) => {
            this.issue = res.data;
            console.log(this.issue);
            this.additionalInfoKey += 1;
//             DeveloperService.getUserBasicInfo(this.issue.creator).then((res2) => {
// /* this might be subject of change. issue.creator might be just username. or whole object.
//  * if it is object, then this backend call is unecessary 
// */              this.creator = res2.data;
//             });
        }).catch(err => { console.log('Error:',err); });
    },
    data() {
        return {
            owner: '',
            repoName: '',
            issue: {
                id: 0,
                title: 'title',
                description: 'descriptionnn',
                created: 'dd/mm/yyyy',
                milestone: null,
                creator: {
                    username: 'korisnik1',
                    avatar: 'dasfas'
                },
                labels: [],
                manager: []
            },
            additionalInfoKey: 1,
            newMilestoneId: null,
            toastSuccess: {
                autoClose: 1000,
                type: 'success',
                position: toast.POSITION.BOTTOM_RIGHT
            },
            toastFailed: {
                autoClose: 1000,
                type: 'error',
                position: toast.POSITION.BOTTOM_RIGHT
            }
        }
    },
    methods: {
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
        },
        close() {
            IssueService.closeIssue(this.$route.params.repoName, this.issue.id).then((res) => {
                console.log(res);
                toast("Issue closed", this.toastSuccess);
                let ownerUsername = this.$route.params.username;
                let repoName = this.$route.params.repoName;
                this.$router.push('/view/' + ownerUsername + '/' + repoName + '/issues');
            }).catch((err) => {
                console.log(err);
                toast("Issue closure failed", this.toastFailed);
            });
        },
        reopen() {
            IssueService.reopenIssue(this.$route.params.repoName, this.issue.id).then((res) => {
                console.log(res);
                toast("Issue reopened", this.toastSuccess);
                let ownerUsername = this.$route.params.username;
                let repoName = this.$route.params.repoName;
                this.$router.push('/view/' + ownerUsername + '/' + repoName + '/issues');
            }).catch((err) => {
                console.log(err);
                toast("Issue reopening failed", this.toastFailed);
            });
        },
        addAssignee(data) {
            this.issue.manager.push(data);
            let body = {
                'manager': data,
                'issue_id': this.issue.id
            }
            IssueService.assignManager(this.$route.params.repoName, this.$route.params.ownerUsername, body).then((res) => {
                res.statusText;
                toast(`${data} assigned to the issue.`, this.toastSuccess);
            }).catch((err) => {
                console.log(err);
                toast('Assigning user failed', this.toastFailed);
            });
        },
        removeAssignee(data) {
            let remainingManagers = []
            this.issue.manager.forEach((e) => {
                if (data === e) {
                    console.log('');
                } else {
                    remainingManagers.push(e);
                }
            });
            this.issue.manager = remainingManagers;
            let body = {
                'manager': data,
                'issue_id': this.issue.id
            }
            IssueService.unassignManager(this.$route.params.repoName, this.$route.params.ownerUsername, body).then((res) => {
                res.statusText;
                toast(`${data} unassigned from the issue.`, this.toastSuccess);
            }).catch((err) => {
                console.log(err);
                toast('Unassigning user failed', this.toastFailed);
            });
        },
        updateMilestone(data) {
            this.issue.milestone = data;
            if (data == null) {
                this.newMilestoneId = null;
            } else {
                this.newMilestoneId = data.id;
            }
        },
        update() {
            let updatedIssue = {
                id: this.issue.id,
                title: this.issue.title,
                description: this.issue.description,
                // created: Date.now(), // add date string
                creator: this.issue.creator,
                open: this.issue.open,
                milestone: this.newMilestoneId,
                project: this.$route.params.repoName
            };
            console.log(updatedIssue);
            IssueService.updateIssue(updatedIssue)
            .then((res) => {
                console.log(res);
                toast("Issue updated", this.toastSuccess);
                location.reload();
            }).catch((err) => {
                console.log(err);
                toast("Issue update failed", this.toastFailed);
            });
        }
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
</style>