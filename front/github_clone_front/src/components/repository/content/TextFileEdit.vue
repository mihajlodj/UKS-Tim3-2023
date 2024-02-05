<template>
    <div class="d-flex justify-content-center">
        <textarea v-model="newContent" @change="updateContent"></textarea>
    </div>
</template>

<script>

export default {
    name: 'TextFileEdit',

    mounted() {
        this.oldContent = localStorage.getItem('fileContent');
        this.newContent = localStorage.getItem('fileContent');
    },

    data() {
        return {
            oldContent: "",
            newContent: ""
        }
    },

    methods: {
        updateContent() {
            localStorage.setItem('newContent', this.newContent);
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