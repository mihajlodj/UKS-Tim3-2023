<template>
    <div>
        <div class="mb-3">
            <InputField id="1" type="text" placeholder="Title" :value="this.title" name="issuetitle" min="4" @update="typeTitle"/>
        </div>
        <div class="mb-2">
            <InputField id="2" type="text" placeholder="Description" :value="this.description" name="issueDescription" min="0" @update="typeDescription"/>
        </div>
        <div>
            <button 
                class="btn btn-secondary dropdown-toggle mb-2" 
                type="button" 
                id="dropdownMenuButton" 
                data-bs-toggle="dropdown" 
                aria-haspopup="true" 
                aria-expanded="false">{{milestone ? milestone.title : 'Select milestone'}}</button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <a class="dropdown-item" v-for="(item, index) in this.milestones" :key="index" @click="setMilestone(item)">{{item.title}}</a>
            </div> 
        </div>
       
        <div class="flex-container">
            <button type="button" class="btn btn-primary"  @click="submit">Add
            </button>
        </div>
    </div>
</template>
<script>
import InputField from '@/components/util/InputField.vue'
import IssueService from '@/services/IssueService';
import { toast } from 'vue3-toastify';
export default {
    name: 'AddIssueComponent',
    components: {
        InputField,
    },
    props: ['milestones'],
    mounted() {
    },

    data() {
        return {
            milestoneId: null,
            milestone: null,
            title: '',
            description: '',
            created: '',
            repo: this.$route.params.repoName
        }
    },
    methods: {
        submit() {
            let newIssue = {
                title: this.title,
                description: this.description,
                // created: Date.now(), // add date string
                creator: localStorage.getItem("username"),
                managers: [],
                open: true,
                milestone: this.milestoneId,
                project: this.repo
            }
            console.log('Created issue');
            console.log(newIssue)
            IssueService.createIssue(newIssue).then((res) => {
                console.log(res);
                location.reload();
                toast("Issue created", {
                    autoClose: 1000,
                    type: 'success',
                    position: toast.POSITION.BOTTOM_RIGHT
                });
            }).catch((err) => {
                console.log(err);
                toast("Issue creation failed", {
                    autoClose: 1000,
                    type: 'error',
                    position: toast.POSITION.BOTTOM_RIGHT
                });
            });
        },
        typeTitle(obj) {
            this.title = obj.val;
        },
        typeDescription(obj) {
            this.description = obj.val;
        },
        setMilestone(item) {
            this.milestoneId = item.id;
            this.milestone = item;
        }
    }
}
</script>
<style scoped></style>