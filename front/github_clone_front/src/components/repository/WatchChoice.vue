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
                    <button type="button" class="btn-drop-item d-flex justify-content-start" @click="selectedWatchOption = 'Participating'">
                        <div style="width: 27px">
                            <font-awesome-icon v-if="selectedWatchOption === 'Participating'" icon="fa-solid fa-check" />
                        </div>
                        <div class="d-flex flex-column">
                            <span class="bright">Participating</span>
                            <span class="muted">Only receive notifications from this repository when participating.</span>
                        </div>
                    </button>
                </li>
                <li v-if="selectedWatchOption !== 'Custom'">
                    <button type="button" class="btn-drop-item d-flex justify-content-start" @click="selectedWatchOption = 'All'">
                        <div style="width: 20px">
                            <font-awesome-icon v-if="selectedWatchOption === 'All'" icon="fa-solid fa-check" />
                        </div>
                        <div class="d-flex flex-column">        
                            <span class="bright">All Activity</span>
                            <span class="muted">Notified of all notifications on this repository.</span>
                        </div>
                    </button>
                </li>
                <li v-if="selectedWatchOption !== 'Custom'">
                    <button type="button" class="btn-drop-item d-flex justify-content-start" @click="selectedWatchOption = 'Ignore'">
                        <div style="width: 20px">
                            <font-awesome-icon v-if="selectedWatchOption === 'Ignore'" icon="fa-solid fa-check" />
                        </div>
                        <div class="d-flex flex-column">
                            <span class="bright">Ignore</span>
                            <span class="muted">Never be notified.</span>
                        </div>
                    </button>
                </li>
                <li v-if="selectedWatchOption !== 'Custom'">
                    <button type="button" class="btn-drop-item d-flex justify-content-start" @click="startCustomChoice">
                        <div style="width: 27px">
                            <font-awesome-icon v-if="selectedWatchOption === 'Custom'" icon="fa-solid fa-check" />
                        </div>
                        <div class="d-flex flex-column">
                            <span class="bright">Custom</span>
                            <span class="muted">Select events you want to be notified of in addition to participating.</span>
                        </div>
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
                    <div class="btn-drop-item d-flex justify-content-start">
                        <input type="checkbox" class="me-2 mt-1" />
                        <span class="bright">Issues</span>
                    </div>
                </li>
                <li v-if="selectedWatchOption === 'Custom'">
                    <div class="btn-drop-item d-flex justify-content-start">
                        <input type="checkbox" class="me-2 mt-1" />
                        <span class="bright">Pull requests</span>
                    </div>
                </li>
                <li v-if="selectedWatchOption === 'Custom'">
                    <div class="btn-drop-item d-flex justify-content-start">
                        <input type="checkbox" class="me-2 mt-1" />
                        <span class="bright">Releases</span>
                    </div>
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
            selectedWatchOption: "Participating",  // TODO: fetch from backend
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
    padding: 10px 10px;
    border: 1px solid #a7b5c2;
    max-width: 300px;
}

.btn-drop-item:hover {
    background-color: #3d4450;
}

.bright {
    color: #c5d1df;
    font-weight: 600;
}

.muted {
    color: #8d959e;
    font-size: small;
}

.fa-check {
    color: #c5d1df;
    height: 15px;
    margin-top: 5px;
}
</style>