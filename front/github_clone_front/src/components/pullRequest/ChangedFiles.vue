<template>
    <div>
        <ChangedFileView v-for="obj in diff" :key="obj.file_path" :file="obj" />
    </div>
</template>

<script>
import ChangedFileView from './ChangedFileView.vue';

export default {
    name: "ChangedFiles",
    props: ["diff"],
    components: {
        ChangedFileView,
    }
}
</script>