<template>
    <div class="d-flex justify-content-center center">
        <div class="contain">
            <div class="d-flex justify-content-between">
                <div class="d-flex justify-content-start">
                    <button type="button" :class="activeTab === 'edit' ? 'header-btn active mx-2' : 'header-btn mx-2'" @click="setActiveTab('edit')">
                        Edit
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

export default {
    name: 'EditingHeader',

    data() {
        return {
            activeTab: 'edit',
        }
    },

    methods: {
        setActiveTab(name) {
            this.activeTab = name;
        }
    },
}
</script>

<style scoped>

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
</style>