<template>
    <div style="margin-left:auto; margin-right:auto;" class="mt-3">
        <h1>{{ issue.title }} <span color="grey">#{{ issue.id }}</span></h1>
    </div>
    <div style="margin-left:auto; margin-right:auto;" class="mt-1" v-if="issue.opened">
        <h5 color="grey"><span class="badge badge-success">Opened</span> <b>{{ this.creator.username }}</b> opened this
            issue {{ howLongAgo(this.issue.created) }}</h5>
    </div>
    <div style="margin-left:auto; margin-right:auto;" class="mt-1" v-else>
        <h5><span class="badge badge-danger">ClosedOpened</span> <b>{{ this.creator.username }}</b> opened this issue {{
            howLongAgo(this.issue.created) }}</h5>
    </div>
    <hr>
    <div class="flex-container">
        <div class="flex-items">
            <img :src="this.creator.avatar" class="rounded-circle" style="width: 30px;" alt="Avatar" />
        </div>
        <div class="flex-items">
            <textarea disabled placeholder="No description provided">{{ this.issue.description }}</textarea>
        </div>
        <div class="flex-items">
            <div>
                Managers:
                <div v-if="this.issue.managers == []">
                    No one: <button type="submit" class="btn btn-link">Assign yourself</button>
                </div>
                <div v-else>
                    <button class="btn btn-link" v-for="(manager, index) in this.issue.managers.slice(0, 3)" :key="index">{{ manager.username }}</button>
                </div>
            </div>
            <hr>
            <div>
                Labels:
                <div v-if="this.issue.tags == []">
                    None yet
                </div>
                <div v-else>
                    <button class="btn btn-link" v-for="(tag,index) in this.issue.tags.slice(0, 3)" :key="index">{{ tag.name }}</button>
                </div>
            </div>
            <div>
                Milestones:
                <div v-if="this.issue.milestone == []">
                    None yet
                </div>
                <div v-else>
                    <button class="btn btn-link" v-for="(milestone, index) in this.issue.milestones" :key="index">{{ milestone.title }}</button>
                </div>
            </div>
        </div>
    </div>
    <hr>
    <div class="flex-container" v-for="(comment, index) in this.issue.comments" :key="index">
        <div class="flex-items">
            <img :src="this.comment.caused_by.avatar" class="rounded-circle" style="width: 30px;" alt="Avatar" />
        </div>
        <div class="flex-items">
            <textarea disabled placeholder="Could not be loaded">{{ comment.content }}</textarea>
        </div>
    </div>
    <hr>
    <h3>Add a comment</h3>
    <div class="flex-container">
        <div class="flex-items">
            <img :src="this.loggedUser.avatar" class="rounded-circle" style="width: 30px;" alt="Avatar" />
        </div>
        <div class="flex-items">
            <textarea placeholder="Add your comment here">{{ this.newComment.content }}</textarea>
        </div>
    </div>
    <div>
        <button type="submit" class="btn btn-danger">Close</button>
        <button type="submit" class="btn btn-succcess">Comment</button>
    </div>
</template>

<script>
import RepoNavbar from '@/components/repository/RepoNavbar.vue'
import IssueService from '@/services/IssueService';
import DeveloperService from '@/services/DeveloperService';
import { toast } from 'vue3-toastify';
export default {
    name: 'IssueViewComponent',
    components: {
        RepoNavbar
    },
    mounted() {
        IssueService.getIssue(this.$route.params.issue_id).then((res) => {
            this.issue = res.data;
            console.log(this.issue);
            DeveloperService.getUserBasicInfo(this.issue.creator).then((res2) => {
/* this might be subject of change. issue.creator might be just username. or whole object.
 * if it is object, then this backend call is unecessary 
*/              this.creator = res2.data;
            });
        }).catch(err => { console.log(err); });
    },
    data() {
        return {
            issue: undefined,
            creator: undefined,
            loggedUser: undefined,
            newComment: {
                content: '',
                parent: undefined
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
        }
    }
}
</script>

<style scoped>
.tg td {
    border-bottom: 0px;
    color: #594F4F;
    font-family: Arial, sans-serif;
    font-size: 14px;
    overflow: hidden;
    padding: 10px 5px;
    word-break: normal;
}

.tg th {
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
    border-color: inherit;
    text-align: center;
    vertical-align: middle
}

.tg .tg-c7q8 {
    text-align: center;
    vertical-align: middle
}

.flex-container {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    justify-content: center;
    align-items: flex-start;
    align-content: normal;
}

.flex-items:nth-child(1) {
    display: block;
    flex-grow: 0;
    flex-shrink: 1;
    flex-basis: auto;
    align-self: auto;
    order: 0;
}

.flex-items:nth-child(2) {
    display: block;
    flex-grow: 0;
    flex-shrink: 1;
    flex-basis: auto;
    align-self: auto;
    order: 0;
}
</style>