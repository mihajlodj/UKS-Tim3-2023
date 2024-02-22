<template>
    <div class="w-100">
        <div class="d-flex justify-content-start mt-1">
            <label class="num-changes">{{ diff.length }} changed files</label>
            <label>&nbsp; with &nbsp;</label>
            <label class="num-add">{{ overall_additions }} additions</label>
            <label>&nbsp; and &nbsp;</label>
            <label class="num-del">{{ overall_deletions }} deletions</label>
        </div>
        <div class="d-flex justify-content-between">
            <div class="list d-flex flex-column mt-3">
                <div v-for="file in diff" :key="file.file_path" class="d-flex justify-content-start">
                    <button  class="btn-file bright p-1 w-100 d-flex justify-content-between me-3" @click="scrollToElement(file.file_path)">
                        {{ file.file_path }}
                        <font-awesome-icon v-if="file.mode === 'add'" icon="fa-solid fa-circle-plus" class="mt-1"></font-awesome-icon>
                        <font-awesome-icon v-else-if="file.mode === 'delete'" icon="fa-solid fa-circle-minus" class="mt-1"></font-awesome-icon>
                        <font-awesome-icon v-else icon="fa-solid fa-circle-stop" class="mt-1"></font-awesome-icon>
                    </button>
                </div>
            </div>

            <div class="files">
                <div v-for="obj in diff" :key="obj.file_path" :ref="obj.file_path">
                    <ChangedFileView :file="obj" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import ChangedFileView from './ChangedFileView.vue';

export default {
    name: "ChangedFiles",
    props: ["diff", "overall_additions", "overall_deletions"],
    components: {
        ChangedFileView,
    },

    methods: {
        scrollToElement(path) {
            const [el] = this.$refs[path];
            if (el) {
                el.scrollIntoView({ behavior: "smooth" });
            }
        }
    }
}
</script>

<style scoped>
.list {
    width: 25%;
}

.bright {
    color: #adbbc8;
}
.files {
    width: 75%;
}

label {
    color: #768491;
    font-weight: 600;
}

.num-changes, .fa-circle-stop {
    color: #c69026;
}

.num-add, .fa-circle-plus {
    color: #347d38;
}

.num-del, .fa-circle-minus {
    color: #ca3c38;
}

.btn-file {
    background: none;
    border: none;
    border-radius: 5px;
}

.btn-file:hover {
    background-color: #3c4550;
    border: none;
    border-radius: 5px;
}

</style>