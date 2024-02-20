<template>
    <div>
        <div class="header d-flex justify-content-start mt-3 px-3 py-2">
            <button v-if="!collapsed" type="button" class="btn-collapse" @click="switchCollapse">
                <font-awesome-icon icon="fa-solid fa-angle-down"></font-awesome-icon>
            </button>
            <button v-else type="button" class="btn-collapse" @click="switchCollapse">
                <font-awesome-icon icon="fa-solid fa-angle-right"></font-awesome-icon>
            </button>

            <label class="bright ms-2">{{ file.additions + file.deletions }}</label>
            <button type="button" class="btn-file-name ms-3">{{ file.file_path }}</button>
        </div>

        <div v-if="!collapsed" class="content">
            <div v-if="!file.content || file.content.length === 0" class="binary p-2">
                <label class="muted">Binary file not shown</label>
            </div>
            <div v-else>
                <div v-for="line in file.content" :key="line">
                    <label v-if="line.startsWith('+')" class="green-line px-2">{{ line }}</label>
                    <label v-else-if="line.startsWith('-')" class="red-line px-2">{{ line }}</label>
                    <label v-else-if="!line.startsWith('\\ No newline at end of file')" class="regular-line px-2">{{ line }}</label>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "ChangedFileView",
    props: ["file"],
    data() {
        return {
            collapsed: false
        }
    },

    mounted() {
        console.log(this.file.content);
    },

    methods: {
        switchCollapse() {
            this.collapsed = !this.collapsed;
        }
    }
}
</script>

<style scoped>

.bright {
    color: #adbbc8;
}

.muted {
    color: #768491;
}
.header {
    background-color: #2c333b;
    border-top-left-radius: 7px;
    border-top-right-radius: 7px;
    border: 1px solid #768491;
}

.binary {
    background: none;
    border: 1px solid #768491;
    border-bottom-left-radius: 7px;
    border-bottom-right-radius: 7px;
}

.green-line {
    background-color: #324f3b;
    color: #adbbc8;
    width: 100%;
}

.red-line {
    background-color: #5c3435;
    color: #adbbc8;
    width: 100%;
}

.regular-line {
    color: #adbbc8;
}

.content {
    border: 1px solid #768491;
}

.btn-collapse, .btn-file-name {
    border: none;
    background: none;
    color: #adbbc8;
}

.btn-collapse:hover, .btn-file-name:hover {
    border: none;
    background: none;
    color: #03a9f4;
}
</style>