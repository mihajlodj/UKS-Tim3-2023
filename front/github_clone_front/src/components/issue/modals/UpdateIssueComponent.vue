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
            aria-expanded="false">{{this.milestone ? this.milestone.title : 'None selected'}}</button>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                <a class="dropdown-item" v-for="(item, index) in this.allMilestones" :key="index" @click="modifyMilestone(item)">{{item.title}}</a>
            </div>
        </div>
        <div class="flex-container">
            <button type="button" class="btn btn-primary"  @click="submit">Update
            </button>
        </div>
    </div>
</template>
<script>
import InputField from '@/components/util/InputField.vue';
export default {
    props: ['title', 'description', 'id', 'milestone', 'allMilestones'],
    components: {
        InputField
    },
    data() {
        return {
            receivedMilestone: this.milestone,
            milestoneId: null
        }
    },
    methods: {
        submit() {
            this.$emit('updateIssue');
        },
        modifyMilestone(item) {
            this.receivedMilestone = item.id;
            this.$emit('propModified', this.receivedMilestone);
        },
        typeTitle(obj) {
            this.$emit('updateTitle', obj.val)
        },
        typeDescription(obj) {
            this.$emit('updateDescription', obj.val)
        },
        setMilestone(item) {
            this.milestoneId = item.id;
        }
    }
}
</script>
<style scoped>
    
</style>