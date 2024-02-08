<template lang="en">
    <div id="create-form">
        <div class="mb-3">
            <div class="d-flex flex-column">
                <label class="mb-1">Title</label>
                <input type="text" v-model="title" @input="validateMilestoneTitle" />
                <div class="d-flex justify-content-start">
                    <font-awesome-icon v-if="!isValidMilestoneTitle" icon="fa-solid fa-triangle-exclamation"
                        class="me-2 mt-1" />
                    <label v-if="!isValidMilestoneTitle" class="warn">Milestone title can only contain
                        alphanumerics, dashes ( - ) and underscores ( _ )
                    </label>
                </div>
            </div>
        </div>
        <div class="mb-2">
            <div class="d-flex flex-column">
                <label class="mb-1">Description</label>
                <textarea type="text" v-model="description" ></textarea>
            </div>
        </div>
        <div class="mb-2">
            <label for="due_date">Due date</label>
            <input id="due_date" class="form-control" type="date" data-date-format="YYYY-MM-DD " v-model="due_date" />
        </div>
        <div class="flex-container">
            <button type="button" class="btn btn-primary" @click="submit">Add</button>
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

    data() {
        return {
            milestone: 'Select milestone',
            title: '',
            isValidMilestoneTitle: true,
            description: '',
            due_date: '',
            repo: this.$route.params.repoName,
        }
    },
    methods: {
        submit() {
            MilestoneService.createMilestone(this.repo, {
                "title": this.title,
                "description": this.description,
                "deadline": this.due_date,
            }).then((res) => {
                console.log(res);
                toast("Milestone created", {
                    autoClose: 1000,
                    type: 'success',
                    position: toast.POSITION.BOTTOM_RIGHT
                });
                this.empty_fields();
            }).catch((err) => {
                console.log(err);
                toast("Issue created", {
                    autoClose: 1000,
                    type: 'success',
                    position: toast.POSITION.BOTTOM_RIGHT
                });
            });
            // createIssue({
            //     title: this.title,
            //     description: this.description,
            //     created: '',
            //     manager: localStorage.getItem("username"),
            //     tasks: [],
            //     events: [],
            //     milestone: undefined
            // }).then((res) => {
            //     console.log(res);
            //     toast("Issue created", {
            //         autoClose: 1000,
            //         type: 'success',
            //         position: toast.POSITION.BOTTOM_RIGHT
            //     });
            // }).catch((err) => {
            //     console.log(err);
            //     alert("Issue creation failed", {
            //         autoClose: 1000,
            //         type: 'error',
            //         position: toast.POSITION.BOTTOM_RIGHT
            //     });
            // });
        },
        validateMilestoneTitle() {
            const regexPattern = /^[a-zA-Z][\w-]*$/;
            this.isValidMilestoneTitle = (this.title !== "" && regexPattern.test(this.title));
        },
        empty_fields(){
            this.title = '';
            this.isValidMilestoneTitle = true;
            this.description = '';
            this.due_date = '';
        }        
    }
}
</script>
<style scoped></style>