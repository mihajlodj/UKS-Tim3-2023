<template>
    <div>
        <div v-if="!pull.mergeable" class="d-flex justify-content-start">
            <div class="warn d-flex justify-content-center mt-1">
                <font-awesome-icon icon="fa-solid fa-triangle-exclamation" class="mt-1"></font-awesome-icon>
            </div>
            <div class="ms-3">
                <h5 class="bright">This branch has conflicts that must be resolved</h5>
                <h5 class="bright">Conflicting files:</h5>
                <div class="d-flex flex-column">
                    <label v-for="file in pull.conflicting_files" :key="file" class="bright">{{ file }}</label>
                </div>

                <hr class="bright my-4" />
            </div>
        </div>

        <div v-else class="d-flex justify-content-start">
            <div class="success d-flex justify-content-center mt-1">
                <font-awesome-icon icon="fa-solid fa-check" class="mt-2"></font-awesome-icon>
            </div>
            <div class="ms-3">
                <h5 class="bright">This branch has no conflicts with the base branch</h5>
                <h6 class="muted">Merging can be performed automatically.</h6>
                <hr class="bright my-4" />
            </div>
        </div>

        <button class="merge my-2 py-2 px-3" :disabled="!pull.mergeable">
            Merge pull request
        </button>
    </div>
</template>

<script>
export default {
    name: "MergeInfo",
    props: ['pull'],
    methods: {
        merge() {
            this.$emit('merge');
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
.fa-triangle-exclamation, .fa-check {
    color: white;
    height: 30px;
}

.warn {
    border-radius: 50%;
    background-color: #626e7a;
    height: 45px;
    width: 45px;
}

.success {
    border-radius: 50%;
    background-color: #347d38;
    height: 45px;
    width: 45px;
}

button.merge {
    border-radius: 5px;
    background-color: #347d38;
    color: white;
    border: none;
}

button.merge:disabled {
    border-radius: 5px;
    background-color: #373e48;
    color: #768491;
    border: 1px solid #768491;
}

</style>