<template>
    <div>
        <div ref="reviewers">
            <button type="button" class="btn-gear d-flex justify-content-between align-items-center w-100"
                @click="openModal('reviewers')">
                <label class="muted">Reviewers</label>
                <font-awesome-icon icon="fa-solid fa-gear" class="muted" />
            </button>
            <label v-if="reviews.length == 0" class="bright small">No reviews</label>
            <ReviewersModal v-if="showModal['reviewers']" :x="modalX" :y="modalY" :w="modalW" @closeModal="toggleModal('reviewers')" />
        </div>
        <hr class="muted" />

        <div ref="assignees">
            <button type="button" class="btn-gear d-flex justify-content-between align-items-center w-100"
                @click="openModal('assignees')">
                <label class="muted hoverable">Asignees</label>
                <font-awesome-icon icon="fa-solid fa-gear" class="muted" />
            </button>
            <label v-if="assignees.length == 0" class="bright small">No one</label>
            <AssigneesModal v-if="showModal['assignees']" :x="modalX" :y="modalY" :w="modalW" @closeModal="toggleModal('assignees')" />
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
            <MilestoneModal v-if="showModal['milestone']" :x="modalX" :y="modalY" :w="modalW" @closeModal="toggleModal('milestone')" @milestoneChosen="milestoneChosen" />
        </div>
    </div>
</template>

<script>
import ReviewersModal from "@/components/pullRequest/modals/ReviewersModal.vue"
import AssigneesModal from "@/components/pullRequest/modals/AssigneesModal.vue"
import LabelsModal from "@/components/pullRequest/modals/LabelsModal.vue"
import MilestoneModal from "@/components/pullRequest/modals/MilestoneModal.vue"

export default {
    name: "AdditionalPrInfo",
    components: {
        ReviewersModal,
        AssigneesModal,
        LabelsModal,
        MilestoneModal
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
            reviews: [],
            assignees: [],
            labels: [],
            milestone: null
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
</style>