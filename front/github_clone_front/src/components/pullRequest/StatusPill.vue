<template>
    <div>
        <div v-if="status === 'Open'" class="status-pill open">
            <img class="pr-icon me-1 mb-1" src="../../assets/open_pr_white.png" />
            <label>{{ status }}</label>
        </div>
        <div v-if="status === 'Closed'" class="status-pill closed">
            <img class="pr-icon me-1 mb-1" src="../../assets/closed_pr_white.png" />
            <label>{{ status }}</label>
        </div>
        <div v-if="status === 'Merged'" class="status-pill merged">
            <img class="pr-icon me-1 mb-1" src="../../assets/merged_pr_white.png" />
            <label>{{ status }}</label>
        </div>
    </div>
</template>

<script>
export default {
    name: "StatusPill",
    props: ['status']
}
</script>

<style scoped>
.status-pill {
    font-size: large;
    padding: 3px 12px;
    border-radius: 8px;
    font-weight: 600;
    color: white;
}

.open {
    background-color: #347d38;
}

.closed {
    background-color: #ca3c38;
}

.merged {
    background-color: #8256d1
}

.pr-icon {
    height: 17px;
}
</style>