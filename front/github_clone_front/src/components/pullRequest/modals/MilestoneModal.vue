<template>
    <div class="contain p-2" :style="{ top: y + 'px', left: x + 'px', width: w + 'px' }" @click="preventClose">
        <h6 class="mt-1 bright small">Set milestone</h6>
        <hr class="muted" />
        <input type="text" v-model="search" class="w-100 p-2 muted" placeholder="Filter milestones" @input="filterMilestones" />
        <hr class="muted" />
        <ul class="nav nav-tabs mb-2">
            <li class="nav-item">
                <button :class="activeOpen ? 'tab active small' : 'tab small'" @click="setActiveOpen">Open</button>
            </li>
            <li class="nav-item">
                <button :class="!activeOpen ? 'tab active small' : 'tab small'" @click="setActiveClosed">Closed</button>
            </li>
        </ul>
        <label v-if="milestones.length == 0" class="mb-1 muted">Nothing to show</label>
        <div v-else class="d-flex flex-column">
            <div v-for="m in milestones" :key="m.id" class="hoverable">
                <button type="button" class="btn-milestone d-flex flex-column" @click="milestoneChosen(m.id, m.title)">
                    <label class="bright hoverable">{{ m.title }}</label>
                    <label class="muted small hoverable">Due date: {{ m.due_date }}</label>
                </button>
                <hr class="muted narrow" />
            </div>
        </div>
    </div>
</template>

<script>
import MilestoneService from "@/services/MilestoneService"

export default {
    name: "MilestoneModal",
    props: ["chosen", "x", "y", "w"],

    mounted() {
        MilestoneService.getAllMilestones(this.$route.params.username, this.$route.params.repoName).then(res => {
            this.openMilestones = res.data.filter(item => item.state === "Open");
            this.closedMilestones = res.data.filter(item => item.state === "Closed");
            this.milestones = this.openMilestones;
        }).catch(err => {
            console.log(err);
        });
        if (this.chosen) {
            this.chosenMilestone = this.chosen;
        }
    },

    data() {
        return {
            search: '',
            milestones: [],
            filtered: [],
            openMilestones: [],
            closedMilestones: [],
            chosenMilestone: { id: -1, title: "" },
            activeOpen: true
        }
    },

    methods: {
        close(e) {
            e.preventDefault();
            console.log(e.target.classList);
            if ("cover" in e.target.classList) {
                this.$emit('closeModal', {
                    name: 'milestone'
                });
            }
        },

        milestoneChosen(id, title) {
            this.chosenMilestone = { id, title };
            this.$emit('milestoneChosen', this.chosenMilestone);
        },

        setActiveOpen() {
            this.activeOpen = true;
            this.milestones = this.openMilestones;
        },

        setActiveClosed() {
            this.activeOpen = false;
            this.milestones = this.closedMilestones;
        },

        filterMilestones() {
            if (this.activeOpen) {
                if (this.search === "") this.milestones = this.openMilestones;
                else this.milestones = this.openMilestones.filter(x => x.title.toLowerCase().includes(this.search.toLowerCase()));
            } else {
                if (this.search === "") this.milestones = this.closedMilestones;
                else this.milestones = this.closedMilestones.filter(x => x.title.toLowerCase().includes(this.search.toLowerCase()));
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

hr.narrow {
    margin: 5px 0px;
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

.btn-milestone {
    text-align: left;
    background-color: #2c333b;
    width: 100%;
    border: none;
}

.hoverable:hover {
    cursor: pointer;
}

.btn-milestone:hover {
    background-color: #39424d;
}

.nav-item {
    background-color: #2c333b;
}

.tab.active {
    padding: 7px 12px;
    background-color: #2c333b;
    border: 1px solid #768491;
    border-top-right-radius: 5px;
    border-top-left-radius: 5px;
    color: #adbbc8;
}

.tab {
    padding: 7px 12px;
    background-color: #2c333b;
    border: none;
    border-top-right-radius: 5px;
    border-top-left-radius: 5px;
    color: #768491;
}
</style>