<template>
    <div class="d-flex justify-content-center center">
        <div class="contain">
            <div class="d-flex justify-content-start">
                <div v-if="size" class="d-flex align-items-center ms-3">
                    <span class="text sm">{{ fileSize }}</span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'CodeDisplay',

    props: ['size'],

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