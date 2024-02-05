<template>
    <div class="d-flex justify-content-center center">
        <div class="contain">
            <div class="d-flex justify-content-between">
                <div class="d-flex justify-content-start">
                    <button type="button" :class="activeTab === 'code' ? 'header-btn active mx-2' : 'header-btn mx-2'"
                        @click="setActiveTab('code')">Code</button>
                    <button type="button" :class="activeTab === 'blame' ? 'header-btn active' : 'header-btn'"
                        @click="setActiveTab('blame')">Blame</button>
                    <div v-if="numLines" class="d-flex align-items-center ms-5">
                        <span class="text sm">{{ numLines }} lines</span>
                    </div>
                    <div v-if="size" class="d-flex align-items-center ms-3">
                        <span class="text sm">{{ fileSize }}</span>
                    </div>
                </div>

                <div class="d-flex justify-content-end">
                    <a class="header-btn me-1" :href="downloadUrl">Raw</a>
                    <button type="button" class="header-btn me-1 px-3" @click="downloadFile">
                        <font-awesome-icon icon="fa-solid fa-download" />
                    </button>
                    <button type="button" class="header-btn me-1 px-3" @click="editFile">
                        <font-awesome-icon icon="fa-solid fa-pen" />
                    </button>
                    <button type="button" class="header-btn me-1 px-3" @click="deleteFile">
                        <font-awesome-icon icon="fa-regular fa-trash-can" />
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'CodeDisplay',

    props: ['numLines', 'size', 'name', 'downloadUrl', 'content'],

    data() {
        return {
            activeTab: 'code',
        }
    },

    methods: {
        setActiveTab(name) {
            this.activeTab = name;
        },

        editFile() {
            this.$emit('editFile', {});
        },

        deleteFile() {
            this.$emit('deleteFile', {});
        },

        async downloadFile() {
            try {
                const blob = new Blob([this.content]);
                const link = document.createElement('a');
                link.href = window.URL.createObjectURL(blob);
                link.download = this.name;
                link.click();
            } catch (error) {
                console.error('Error downloading file', error);
            }
        },
    },

    computed: {
        fileSize() {
            if (this.size < 1024) {
                return `${this.size.toString()} B`
            } else if (this.size < 1024 * 1024) {
                let s = Math.floor(this.size / 1024);
                return `${s.toString()} KB`
            } else if (this.size < 1024 * 1024 * 1024) {
                let s = Math.floor(this.size / (1024 * 1024));
                return `${s.toString()} MB`
            } else {
                let s = Math.floor(this.size / (1024 * 1024 * 1024));
                return `${s.toString()} GB`
            }
        }
    }
}
</script>

<style scoped>
.text {
    color: #adbbc8;
    ;
}

.center {
    background-color: #22272d;
}

.header-btn {
    color: #adbbc8;
    background-color: #323941;
    border: none;
    border-radius: 5px;
    padding: 5px 10px;
    text-decoration: none;
}

.active {
    color: #adbbc8;
    border: 1px solid #adbbc8;
    background-color: #22272d;
}

.contain {
    width: 80%;
    background-color: #2c333b;
    padding: 15px 5px;
    border-right: 1px solid #adbbc8;
    border-left: 1px solid #adbbc8;
    border-top: 1px solid #adbbc8;
    border-top-right-radius: 7px;
    border-top-left-radius: 7px;
}

.sm {
    font-size: small;
}

.fa-download {
    color: #adbbc8;
}
</style>