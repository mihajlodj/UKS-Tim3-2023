<template>
    <div class="d-flex justify-content-center">
        <textarea v-model="newContent"></textarea>
    </div>
</template>

<script>
// import RepositoryService from '@/services/RepositoryService';

export default {
    name: 'TextFileEdit',

    mounted() {
        this.oldContent = localStorage.getItem('fileContent');
        this.newContent = localStorage.getItem('fileContent');
    },

    data() {
        return {
            oldContent: "",
            newContent: "",
            oldName: "",
            newName: ""
        }
    }
}
</script>

<style scoped>

textarea {
    width: 80%;
    min-height: 300px;
    resize: none;
    background-color: #22272d;
    color: #adbbc8;
    padding: 10px;
}

</style>