<template>
    <div>
        <div>
            <button type="button" class="btn me-2 dropdown-toggle" data-bs-toggle="dropdown"
                aria-expanded="false" id="btn-watch">
                <font-awesome-icon icon="fa-regular fa-eye" class="me-1" />
                Watch
            </button>
            <ul class="dropdown-menu" id="watch-choices" aria-labelledby="btn-watch" style="background-color: #2c333b; padding: 0px;">
                <li v-if="selectedWatchOption !== 'Custom'">
                    <button type="button" class="btn-drop-item" @click="selectedWatchOption = 'Participating'">
                        <span class="bright">Participating</span>
                    </button>
                </li>
                <li v-if="selectedWatchOption !== 'Custom'">
                    <button type="button" class="btn-drop-item" @click="selectedWatchOption = 'All'">
                        <span class="bright">All Activity</span>
                    </button>
                </li>
                <li v-if="selectedWatchOption !== 'Custom'">
                    <button type="button" class="btn-drop-item" @click="selectedWatchOption = 'Ignore'">
                        <span class="bright">Ignore</span>
                    </button>
                </li>
                <li v-if="selectedWatchOption !== 'Custom'">
                    <button type="button" class="btn-drop-item" @click="startCustomChoice">
                        <span class="bright">Custom</span>
                    </button>
                </li>

                <li v-if="selectedWatchOption === 'Custom'">
                    <div class="d-flex justify-content-start">
                        <button type="button" class="btn-drop-item" @click="cancelCustomChoice">
                            Back
                        </button>
                    </div>
                </li>
                <li v-if="selectedWatchOption === 'Custom'">
                    <button type="button" class="btn-drop-item">
                        <span class="bright">Issues</span>
                    </button>
                </li>
                <li v-if="selectedWatchOption === 'Custom'">
                    <button type="button" class="btn-drop-item">
                        <span class="bright">Pull requests</span>
                    </button>
                </li>
                <li v-if="selectedWatchOption === 'Custom'">
                    <button type="button" class="btn-drop-item">
                        <span class="bright">Releases</span>
                    </button>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
export default {
    name: "WatchChoice",
    props: [],

    data() {
        return {
            selectedWatchOption: "",
            selectedCustomWatchOptions: []
        }
    },

    methods: {
        startCustomChoice(event) {
            event.stopPropagation();
            this.selectedWatchOption = "Custom";
        },

        cancelCustomChoice(event) {
            event.stopPropagation();
            this.selectedWatchOption = "";
        }
    }
}
</script>

<style scoped>
#btn-watch {
    border: 1px solid #d6d9dd;
    background-color: #373e48;
    color: #a7b5c2;
    height: 32px;
    width: 100px;
    margin-top: 25px;
    font-size: small;
}

.btn-drop-item {
    background-color: #2c333b;
    width: 100%;
    text-align: left;
    padding: 15px 10px;
    border: 1px solid #a7b5c2;
}

.bright {
    color: #becad8;
}

.muted {
    color: #8d959e;
}
</style>