<template>
    <div>
        <div>
            <button type="button" class="btn me-2 dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false" id="btn-watch">
                <font-awesome-icon icon="fa-regular fa-eye" class="me-1" />
                {{ buttonText }}
            </button>
            <ul class="dropdown-menu" id="watch-choices" aria-labelledby="btn-watch" style="background-color: #2c333b; padding: 0px;">
                <li v-if="!showCustomOptions">
                    <button type="button" class="btn-drop-item d-flex justify-content-start" @click="selectRegularOption('Participating')">
                        <div style="width: 27px">
                            <font-awesome-icon v-if="selectedWatchOption === 'Participating'" icon="fa-solid fa-check" />
                        </div>
                        <div class="d-flex flex-column">
                            <span class="bright">Participating</span>
                            <span class="muted">Only receive notifications from this repository when participating.</span>
                        </div>
                    </button>
                </li>
                <li v-if="!showCustomOptions">
                    <button type="button" class="btn-drop-item d-flex justify-content-start" @click="selectRegularOption('All')">
                        <div style="width: 20px">
                            <font-awesome-icon v-if="selectedWatchOption === 'All'" icon="fa-solid fa-check" />
                        </div>
                        <div class="d-flex flex-column">        
                            <span class="bright">All Activity</span>
                            <span class="muted">Notified of all notifications on this repository.</span>
                        </div>
                    </button>
                </li>
                <li v-if="!showCustomOptions">
                    <button type="button" class="btn-drop-item d-flex justify-content-start" @click="selectRegularOption('Ignore')">
                        <div style="width: 20px">
                            <font-awesome-icon v-if="selectedWatchOption === 'Ignore'" icon="fa-solid fa-check" />
                        </div>
                        <div class="d-flex flex-column">
                            <span class="bright">Ignore</span>
                            <span class="muted">Never be notified.</span>
                        </div>
                    </button>
                </li>
                <li v-if="!showCustomOptions">
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

                <li v-if="showCustomOptions">
                    <div class="d-flex justify-content-start">
                        <button type="button" class="btn-drop-item d-flex justify-content-start" @click="cancelCustomChoice">
                            <div style="width: 27px">
                            <font-awesome-icon icon="fa-solid fa-arrow-left-long" class="me-2" />
                        </div>
                            <div class="d-flex flex-column">
                                <span class="bright">Custom</span>
                                <span class="muted">Select events you want to be notified of in addition to participating</span>
                            </div>
                        </button>
                    </div>
                </li>
                <li v-if="showCustomOptions">
                    <div class="btn-drop-item d-flex justify-content-start">
                        <input type="checkbox" v-model="issuesSelected" @change="inputChanged" class="me-2" />
                        <span class="bright">Issues</span>
                    </div>
                </li>
                <li v-if="showCustomOptions">
                    <div class="btn-drop-item d-flex justify-content-start">
                        <input type="checkbox" v-model="pullsSelected" @change="inputChanged" class="me-2" />
                        <span class="bright">Pull requests</span>
                    </div>
                </li>
                <li v-if="showCustomOptions">
                    <div class="btn-drop-item d-flex justify-content-start">
                        <input type="checkbox" v-model="releasesSelected" @change="inputChanged" class="me-2" />
                        <span class="bright">Releases</span>
                    </div>
                </li>
                <li v-if="showCustomOptions">
                    <div class="d-flex justify-content-end p-2">
                        <button type="button" class="btn-cancel me-2" @click="cancelCustomSelection">
                            Cancel
                        </button>
                        <button type="button" class="btn-apply" @click="applyCustomSelection" :disabled="!issuesSelected && !pullsSelected && !releasesSelected">
                            Apply
                        </button>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
import RepositoryService from "@/services/RepositoryService"

export default {
    name: "WatchChoice",
    props: ["watchInfo"],

    mounted() {
        if (this.watchInfo) {
            this.selectedWatchOption = this.watchInfo.option;
            this.issuesSelected = this.watchInfo.issue_events;
            this.pullsSelected = this.watchInfo.pull_events;
            this.releasesSelected = this.watchInfo.release_events;
            if (this.selectedWatchOption === "Participating" && (this.issuesSelected || this.pullsSelected || this.releasesSelected)) {
                this.selectedWatchOption = "Custom";
            }
            if (this.issuesSelected) this.selectedCustomWatchOptions.push("Issues");
            if (this.pullsSelected) this.selectedCustomWatchOptions.push("Pulls");
            if (this.releasesSelected) this.selectedCustomWatchOptions.push("Releases");

            if (this.selectedWatchOption !== "Participating") {
                this.buttonText = "Unwatch";
            }
        }
    },

    data() {
        return {
            selectedWatchOption: "Participating",  // TODO: fetch from backend
            selectedCustomWatchOptions: [],
            issuesSelected: false,
            pullsSelected: false,
            releasesSelected: false,
            showCustomOptions: false,
            payload: {},
            buttonText: "Watch"
        }
    },

    methods: {
        startCustomChoice(event) {
            event.stopPropagation();
            this.selectedWatchOption = "Custom";
            this.showCustomOptions = true;
        },

        cancelCustomChoice(event) {
            event.stopPropagation();
            this.showCustomOptions = false;
            if (!this.issuesSelected && !this.pullsSelected && !this.releasesSelected) {
                this.selectedWatchOption = "Participating";
            }
            this.updatePayload();
        },

        inputChanged() {
            this.selectedCustomWatchOptions = [];
            if (this.issuesSelected) {
                this.selectedCustomWatchOptions.push('Issues');
            }
            if (this.pullsSelected) {
                this.selectedCustomWatchOptions.push('Pulls');
            }
            if (this.releasesSelected) {
                this.selectedCustomWatchOptions.push('Releases');
            }
            this.updatePayload();
        },

        selectRegularOption(option) {
            this.selectedWatchOption = option;
            this.issuesSelected = false;
            this.pullsSelected = false;
            this.releasesSelected = false;
            this.updatePayload();
            this.updateWatchPreferences();
        },

        updatePayload() {
            let option = this.selectedWatchOption;
            if (this.selectedWatchOption === "Custom") {
                option = "Participating";
            }
            this.payload = {
                "option": option,
                "issue_events": this.issuesSelected,
                "pull_events": this.pullsSelected,
                "release_events": this.releasesSelected
            };
        },

        applyCustomSelection() {
            this.updatePayload();
            this.updateWatchPreferences();
        },

        cancelCustomSelection() {
            this.issuesSelected = false;
            this.pullsSelected = false;
            this.releasesSelected = false;
            this.updatePayload();
        },

        updateWatchPreferences() {
            RepositoryService.saveWatchPreferences(this.$route.params.username, this.$route.params.repoName, this.payload)
            .then(res => {
                console.log(res);
                if (this.selectedWatchOption === "Participating") {
                    this.buttonText = "Watch";
                } else {
                    this.buttonText = "Unwatch";
                }
            }).catch(err => {
                console.log(err);
            });
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
    min-width: 100px;
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

.fa-check, .fa-arrow-left-long {
    color: #c5d1df;
    height: 15px;
    margin-top: 5px;
}

.btn-cancel {
    background-color: #363e47;
    color: #acbac7;
    border: 1px solid #8f9ba5;
    border-radius: 7px;
    padding: 5px 15px;
    font-size: small;
}

.btn-apply {
    background-color: #347c39;
    color: white;
    border: 1px solid #8f9ba5;
    border-radius: 7px;
    padding: 5px 15px;
    font-size: small;
}

.btn-apply:disabled {
    background-color: #2f7033;
    color: #8f9ba5;
}
</style>