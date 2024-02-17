<template>
    <div class="contain p-2" :style="{ top: y + 'px', left: x + 'px', width: w + 'px' }" @click="preventClose">
        <h6 class="mt-1 bright small">Set milestone</h6>
        <hr class="muted" />
        <input type="text" v-model="search" class="w-100 p-2 muted" placeholder="Filter milestones"/>
        <hr class="muted" />
        <label class="mb-1 muted">Nothing to show</label>
    </div>
</template>

<script>
export default {
    name: "MilestoneModal",
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
            if("cover" in e.target.classList){
                this.$emit('closeModal', {
                    name: 'assignees'
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
</style>