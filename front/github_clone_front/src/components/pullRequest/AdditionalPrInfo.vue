<template>
    <div>
        <div ref="reviewers">
            <button type="button" class="btn-gear d-flex justify-content-between align-items-center w-100"
                @click="openModal('reviewers')">
                <label class="muted">Reviewers</label>
                <font-awesome-icon icon="fa-solid fa-gear" class="muted" />
            </button>
            <label v-if="rev.length === 0" class="bright small">No reviewers</label>
            <div v-else>
                <div v-for="r in rev" :key="r.username" class="mt-1 d-flex justify-content-between">
                    <button type="button" class="btn-assignee w-100 d-flex justify-content-start">
                        <img class="avatar mt-1 me-1" :src="r.avatar"/>
                        <label class="bright hoverable">{{ r.username }}</label>
                    </button>
                    <button type="button" class="btn-remove">
                        <font-awesome-icon icon="fa-regular fa-circle-xmark" class="muted" @click="removeReviewer(r)" />
                    </button>
                </div>
            </div>
            <ReviewersModal v-if="showModal['reviewers']" :reviewers="rev" :x="modalX" :y="modalY" :w="modalW" @addReviewer="addReviewer" @closeModal="toggleModal('reviewers')" />
        </div>
        <hr class="muted" />

        <div ref="assignees">
            <button type="button" class="btn-gear d-flex justify-content-between align-items-center w-100"
                @click="openModal('assignees')">
                <label class="muted hoverable">Assignee</label>
                <font-awesome-icon icon="fa-solid fa-gear" class="muted" />
            </button>
            <label v-if="!assignee" class="bright small">No one</label>
            <div v-else class="mt-1 d-flex justify-content-between">
                <button type="button" class="btn-assignee w-100 d-flex justify-content-start">
                    <img class="avatar mt-1 me-1" :src="assignee.avatar"/>
                    <label class="bright hoverable">{{ assignee.username }}</label>
                </button>
                <button type="button" class="btn-remove">
                    <font-awesome-icon icon="fa-regular fa-circle-xmark" class="muted" @click="removeAssignee" />
                </button>
            </div>
            <AssigneesModal v-if="showModal['assignees']" :x="modalX" :y="modalY" :w="modalW" @chooseAssignee="chooseAssignee" @closeModal="toggleModal('assignees')" />
        </div>
        <hr class="muted" />

        <div ref="labels">
            <button type="button" class="btn-gear d-flex justify-content-between align-items-center w-100" @click="openModal('labels')">
                <label class="muted hoverable">Labels</label>
                <font-awesome-icon icon="fa-solid fa-gear" class="muted" />
            </button>
            <label v-if="labels.length == 0" class="bright small">None yet</label>
            <LabelsModal v-if="showModal['labels']" :x="modalX" :y="modalY" :w="modalW" @closeModal="toggleModal('labels')" />
        </div>
        <hr class="muted" />

        <div ref="milestone">
            <button type="button" class="btn-gear d-flex justify-content-between align-items-center w-100"
                @click="openModal('milestone')">
                <label class="muted hoverable">Milestone</label>
                <font-awesome-icon icon="fa-solid fa-gear" class="muted" />
            </button>
            <label v-if="milestone == null" class="bright small">No milestone</label>
            <div v-else class="mt-1 d-flex justify-content-between">
                <label class="bright">{{ milestone.title }}</label>
                <button type="button" class="btn-remove">
                    <font-awesome-icon icon="fa-regular fa-circle-xmark" class="muted" @click="removeMilestone" />
                </button>
            </div>
            <MilestoneModal v-if="showModal['milestone']" :key="milestoneKey" :x="modalX" :y="modalY" :w="modalW" :chosen="chosenMilestone" @closeModal="toggleModal('milestone')" @milestoneChosen="milestoneChosen" />
        </div>
    </div>
</template>

<script>
import ReviewersModal from "@/components/pullRequest/modals/ReviewersModal.vue"
import AssigneesModal from "@/components/pullRequest/modals/AssigneesModal.vue"
import LabelsModal from "@/components/label/LabelsModal.vue"
import MilestoneModal from "@/components/pullRequest/modals/MilestoneModal.vue"

export default {
    name: "AdditionalPrInfo",
    props: ["chosenMilestone", "chosenAssignee", "chosenReviewers"],
    components: {
        ReviewersModal,
        AssigneesModal,
        LabelsModal,
        MilestoneModal
    },
    mounted() {
        this.milestone = this.chosenMilestone;
        this.assignee = this.chosenAssignee;
        if (this.chosenReviewers !== undefined) {
            this.rev = this.chosenReviewers;
        }
    },
    data() {
        return {
            showModal: {
                "reviewers": false,
                "assignees": false,
                "labels": false,
                "milestone": false
            },
            modalX: 0,
            modalY: 0,
            modalW: 0,
            assignees: [],
            labels: [],
            milestone: null,
            milestoneKey: 1,
            assignee: null,
            rev: []
        }
    },

    methods: {
        toggleModal(name) {
            this.showModal[name] = !this.showModal[name];
            for (const key in this.showModal) {
                if (key !== name) {
                    this.showModal[key] = false;
                }
            }
        },

        openModal(refName) {
            this.toggleModal(refName);
            this.modalX = Math.trunc(this.$refs[refName].getBoundingClientRect().left + window.scrollX);
            this.modalY = Math.trunc(this.$refs[refName].getBoundingClientRect().top + window.scrollY) + 30;
            this.modalW = this.$refs[refName].offsetWidth;
        },

        milestoneChosen(data) {
            this.milestone = data;
            this.toggleModal("milestone");
            this.$emit('updateMilestone', this.milestone);
        },

        removeMilestone() {
            this.milestone = null;
            this.$emit('updateMilestone', this.milestone);
        },

        chooseAssignee(data) {
            this.assignee = data;
            this.toggleModal("assignees");
            this.$emit('updateAssignee', this.assignee);
        },

        removeAssignee() {
            this.assignee = null;
            this.$emit('updateAssignee', this.assignee);
        },

        removeReviewer(r) {
            this.rev = this.rev.filter(x => x.username !== r.username);
            this.$emit('updateReviewers', this.rev);
        },

        addReviewer(data) {
            this.rev.push(data);
            this.toggleModal("reviewers");
            this.$emit("updateReviewers", this.rev);
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

.btn-gear {
    background-color: #22272d;
    border: none;
    padding-left: 0px;
}

.hoverable:hover {
    cursor: pointer;
}

.small {
    font-size: small;
}

hr {
    z-index: 0;
}

.btn-remove {
    background: none;
    border: none;
}

.avatar {
    height: 20px;
    border-radius: 50%;
}

.btn-assignee {
    border: none;
    background: none;
}
</style>