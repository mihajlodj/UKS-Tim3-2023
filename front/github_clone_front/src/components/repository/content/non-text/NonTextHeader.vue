<template>
    <div class="d-flex justify-content-center center">
        <div class="contain d-flex justify-content-between">
            <div class="d-flex justify-content-start">
                <div v-if="size" class="d-flex align-items-center ms-3">
                    <span class="text sm">{{ fileSize }}</span>
                </div>
            </div>

            <div class="d-flex justify-content-end">
                <a :href="download_url" class="header-btn me-1 px-3">
                    <font-awesome-icon icon="fa-solid fa-download" />
                </a>
                <button type="button" class="header-btn me-1 px-3" @click="deleteFile">
                    <font-awesome-icon icon="fa-regular fa-trash-can" />
                </button>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'NonTextHeader',

    props: ['size', 'download_url'],

    methods: {
        deleteFile() {
            this.$emit('deleteFile', {});
        }
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
</style>