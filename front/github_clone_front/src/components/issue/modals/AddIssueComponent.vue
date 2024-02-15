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
                aria-expanded="false">{{milestone}}</button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <a class="dropdown-item" v-for="(item, index) in this.milestones" :key="index" @click="this.milestone = item.name">{{item.name}}</a>
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
        this.milestone = 'Select milestone';
    },

    data() {
        return {
            milestone: '',
            title: '',
            description: '',
            created: '',
            repo: this.$route.params.repoName
        }
    },
    methods: {
        submit() {
            IssueService.createIssue({
                title: this.title,
                description: this.description,
                // created: Date.now(), // add date string
                manager: localStorage.getItem("username"),
                open: true,
                milestone: this.milestone === 'Select milestone' ? '' : this.milestone,
                project: this.$route.params.repoName
            }).then((res) => {
                console.log(res);
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
        }
    }
}
</script>
<style scoped></style>