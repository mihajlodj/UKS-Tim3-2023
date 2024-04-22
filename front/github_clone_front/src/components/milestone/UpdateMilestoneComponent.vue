<template lang="en">
    <div id="create-form" >
        <div class="mb-3">
            <div class="d-flex flex-column">
                <label class="mb-1" style="color: beige">Title</label>
                <input type="text" v-model="title" @input="validateMilestoneTitle" />
                <div class="d-flex justify-content-start">
                    <font-awesome-icon v-if="!isValidMilestoneTitle" icon="fa-solid fa-triangle-exclamation"
                        class="me-2 mt-1" />
                    <label v-if="!isValidMilestoneTitle" class="warn" style="color: red;">Milestone title can only contain
                        alphanumerics, dashes ( - ) and underscores ( _ )
                    </label>
                </div>
            </div>
        </div>
        <div class="mb-2">
            <div class="d-flex flex-column">
                <label class="mb-1" style="color: beige">Description</label>
                <textarea type="text" v-model="description" ></textarea>
            </div>
        </div>
        
        <!-- State -->
        <button 
            class="btn btn-secondary dropdown-toggle mb-2" 
            type="button" 
            id="dropdownMenuButton" 
            data-bs-toggle="dropdown" 
            aria-haspopup="true" 
            aria-expanded="false">{{milestoneState}}</button>
        <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
            <a class="dropdown-item" @click="milestoneState = 'Open'">Open</a>
            <a class="dropdown-item" @click="milestoneState = 'Close'">Close</a>
        </div>

        <div class="mb-2">
            <label for="due_date" style="color: beige">Due date</label>
            <input id="due_date" class="form-control" type="date" data-date-format="YYYY-MM-DD " v-model="due_date" />
        </div>
        <div class="flex-container">
            <button type="button" class="btn btn-primary" @click="submit()">Edit</button>
        </div>
    </div>
    

</template>
<script>
import MilestoneService from '@/services/MilestoneService'
import { toast } from 'vue3-toastify';
export default {
    name: 'AddMilestoneComponent',
    components: {

    },
    props: ['selectedMilestone'],
    mounted() {
        this.milestone = this.selectedMilestone;
        this.setDataFromMilestone();
    },
    data() {
        return {
            milestone: null,
            title: '',
            oldTitle: '',
            isValidMilestoneTitle: true,
            description: '',
            due_date: '',
            milestoneState: '',
            repo: this.$route.params.repoName,
        }
    },
    methods: {
        submit() {
            let convertedState = true;
            if (this.milestoneState === "Open") {
                convertedState = true;
            }
            else {
                convertedState = false;
            }
            MilestoneService.editMilestone(this.$route.params.username, this.oldTitle, {
                "title": this.title,
                "description": this.description,
                "deadline": this.due_date,
                "repo_name": this.repo,
                "state": convertedState,
            }).then((res) => {
                console.log(res);
                toast("Milestone updated", {
                    autoClose: 1000,
                    type: 'success',
                    position: toast.POSITION.BOTTOM_RIGHT
                });
                this.notifyParrent();
            }).catch((err) => {
                console.log(err);
                toast("Error occured while editing milestone!", {
                        autoClose: 1000,
                        type: 'error',
                        position: toast.POSITION.BOTTOM_RIGHT
                    });
            });
        },
        validateMilestoneTitle() {
            const regexPattern = /^[a-zA-Z][\w-]*$/;
            this.isValidMilestoneTitle = (this.title !== "" && regexPattern.test(this.title));
        },
        empty_fields() {
            this.title = '';
            this.isValidMilestoneTitle = true;
            this.description = '';
            this.due_date = '';
        },
        setDataFromMilestone() {
            if (this.milestone != undefined) {
                this.oldTitle = this.milestone.title;
                this.title = this.milestone.title;
                this.description = this.milestone.description;
                this.due_date = this.milestone.due_date;
                this.milestoneState = this.milestone.state;
            }
        },
        notifyParrent() {
            this.$emit('milestoneUpdated');
        }
    }
}
</script>
<style scoped></style>