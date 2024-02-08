<template lang="en">
    <div id="create-form">
        <div class="mb-3">
            <InputField id="1" type="text" placeholder="Title" :value="title" name="issuetitle" min="4"/>
        </div>
        <div class="mb-2">
            <InputField id="2" type="text" placeholder="Description" :value="description" name="issueDescription" min="0"/>
        </div>
        <div class="mb-2">
            <label for="startDate">Due date</label>
            <input id="startDate" class="form-control" type="date" />
        </div>
        <div class="flex-container">
            <button type="button" class="btn btn-primary"  @click="submit">Add</button>
        </div>
    </div>
    

</template>
<script>
import InputField from '@/components/util/InputField.vue'
// import createIssue from '@/services/IssueService';
// import { toast } from 'vue3-toastify';
export default {
    name: 'AddMilestoneComponent',
    components: {
        InputField,
    },

    data() {
        return {
            milestone: 'Select milestone',
            title: '',
            description: '',
            created: '',
            repo: undefined
        }
    },
    methods: {
        submit() {
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
        }
    }
}
</script>
<style scoped></style>