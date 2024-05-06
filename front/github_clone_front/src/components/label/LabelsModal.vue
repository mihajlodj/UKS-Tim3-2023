<template>
    <div class="contain p-2" :style="{ top: y + 'px', left: x + 'px', width: w + 'px' }" @click="preventClose">
        <h6 class="mt-1 bright small">Apply labels to this pull request</h6>
        <hr class="muted" />
        <input type="text" v-model="search" class="w-100 p-2 muted" placeholder="Filter lables" />
        <hr class="muted" />

        <!-- One label container -->
        <div class="container">
            <div class="row">
                <div class="col-md-1">
                    <svg viewBox="0 0 16 16" class="" aria-hidden="true" width="16" height="16" v-if="true">
                        <path
                            d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z">
                        </path>
                    </svg>
                </div>
                <div class="col-md-7">
                    <p class="muted small mt-1">Label name</p>
                </div>
                <div class="col-md-4 text-end">
                    <!-- Add button -->
                    <button class="button-color">
                        <svg viewBox="0 0 16 16" class="" aria-hidden="true" width="16" height="16">
                            <path
                                d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z">
                            </path>
                        </svg>
                    </button>

                    <!-- Remove button -->
                    <button class="button-color">
                        <svg viewBox="0 0 16 16" class="" aria-hidden="true" width="16" height="16">
                            <path
                                d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.749.749 0 0 1 1.275.326.749.749 0 0 1-.215.734L9.06 8l3.22 3.22a.749.749 0 0 1-.326 1.275.749.749 0 0 1-.734-.215L8 9.06l-3.22 3.22a.751.751 0 0 1-1.042-.018.751.751 0 0 1-.018-1.042L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06Z">
                            </path>
                        </svg>
                    </button>
                </div>
            </div>
            <hr class="muted" />
        </div>

        <div id="no-labels" v-if="true">
            <hr class="muted" />
            <label class="mb-1 muted">Nothing to show</label>
        </div>

    </div>
</template>

<script>
export default {
    name: "LabelsModal",
    props: ["x", "y", "w"],

    data() {
        return {
            search: ''
        }
    },

    methods: {
        close(e) {
            e.preventDefault();
            console.log(e.target.classList);
            if ("cover" in e.target.classList) {
                this.$emit('closeModal', {
                    name: 'labels'
                });
            }
        }
    }
}
</script>

<style scoped>
.contain {
    position: absolute;
    border-radius: 10px;
    z-index: 1;
    background-color: #2c333b;
    border: 1px solid #434c55;
}


.bright {
    color: #adbbc8;
}

.muted {
    color: #768491;
}

hr {
    margin: 15px 0px;
}

input {
    border-radius: 5px;
    background-color: #22272d;
    border: 1px solid #434c55;
}

.small {
    font-size: small;
}

.button-color {
    background-color: #2c333b;
    color: #adbbc8;
    border: none;
}

.button-color:hover {
    background-color: #434c55;
}
</style>