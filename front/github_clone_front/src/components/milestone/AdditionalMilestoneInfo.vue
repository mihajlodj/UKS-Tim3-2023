<template>
    <div ref="labels">
        <button type="button" class="btn-gear d-flex justify-content-between align-items-center w-100"
            @click="openModal('labels')">
            <label class="muted hoverable">Labels</label>
            <font-awesome-icon icon="fa-solid fa-gear" class="muted" />
        </button>
        <label v-if="this.selectedLabels?.length == 0" class="bright small">None yet</label>
        <LabelsModal v-if="showModal['labels']" :x="modalX" :y="modalY" :w="modalW" :selectedLabelsProp="this.selectedLabels"
            :entityType="'milestone'" :entityId="milestoneId" @closeModal="toggleModal('labels')" />
    </div>
</template>
<script>
import LabelsModal from "@/components/label/LabelsModal.vue";

export default {
    name: "AdditionalMilestoneInfo",
    props: ["selectedLabels", "milestoneId"],

    components: {
        LabelsModal,
    },
    mounted() {
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