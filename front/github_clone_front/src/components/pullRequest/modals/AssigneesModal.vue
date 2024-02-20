<template>
    <div class="contain p-2" :style="{ top: y + 'px', left: x + 'px', width: w + 'px' }" @click="preventClose">
        <h6 class="mt-1 bright small">Assign up to 10 people on this pull request</h6>
        <hr class="muted" />
        <input type="text" v-model="search" class="w-100 p-2 muted" placeholder="Type or choose a user"/>
        <hr class="muted" />
        <label v-if="available.length === 0" class="mb-1 muted">Nothing to show</label>
        <div v-else class="hoverable">
            <button v-for="a in available" :key="a.username" class="btn-assignee w-100 d-flex justify-content-start p-2" @click="chooseAssignee(a)">
                <img class="avatar mt-1 me-1" :src="a.avatar"/>
                <label class="bright hoverable">{{ a.username }}</label>
            </button>
        </div>
    </div>
</template>

<script>
import PullRequestService from "@/services/PullRequestService"

export default {
    name: "AssigneesModal",
    props: ["x", "y", "w", "assignee"],

    mounted() {
        if (this.assignee) {
            this.chosenAssignee = this.assignee;
        }
        PullRequestService.getPossibleAssignees(this.$route.params.repoName).then(res => {
            this.available = res.data;
        }).catch(err => {
            console.log(err);
        });
    },

    data() {
        return {
            search: '',
            available: [],
            chosenAssignee: null
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
        },

        chooseAssignee(assignee) {
            this.$emit('chooseAssignee', assignee);
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

.avatar {
    height: 20px;
    border-radius: 50%;
}

.btn-assignee {
    border: none;
    background: none;
}

.hoverable:hover {
    cursor: pointer;
}
</style>