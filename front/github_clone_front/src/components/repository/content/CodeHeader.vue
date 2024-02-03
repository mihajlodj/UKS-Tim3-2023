<template>
    <div class="d-flex justify-content-center center">
        <div class="contain">
            <div class="d-flex justify-content-start">
                <button type="button" :class="activeTab==='code' ? 'header-btn active mx-2' : 'header-btn mx-2'" @click="setActiveTab('code')">Code</button>
                <button type="button" :class="activeTab==='blame' ? 'header-btn active' : 'header-btn'" @click="setActiveTab('blame')">Blame</button>
                <div v-if="numLines" class="d-flex align-items-center ms-5">
                    <span class="text sm">{{ numLines }} lines</span>
                </div>
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

    props: ['numLines', 'size', 'htmlUrl', 'downloadUrl'],

    data() {
        return {
            activeTab: 'code',
        }
    },

    methods: {
        setActiveTab(name) {
            this.activeTab = name;
        }
    },

    computed: {
        fileSize() {
            if (this.size < 1024) {
                return `${this.size.toString()} B`
            } else if (this.size < 1024 * 1024) {
                let s = this.size / 1024;
                return `${s.toString()} KB`
            } else if (this.size < 1024 * 1024 * 1024) {
                let s = this.size / (1024 * 1024);
                return `${s.toString()} MB`
            } else {
                let s = this.size / (1024 * 1024 * 1024);
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
}

.sm {
    font-size: small;
}
</style>