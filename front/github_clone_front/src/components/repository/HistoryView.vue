<template>
    <div>
        <h1>
            Commits
        </h1>
        <div>
            <CommitsTable />
        </div>
    </div>
</template>

<script>
import CommitsTable from '../commit/CommitsTable.vue';

export default {
    name: "HistoryView",
    components: {
        CommitsTable
    },

    mounted() {
        // Fetch commits on branch
    },

    data() {
        return {

        }
    }
}
</script>

<style scoped>

</style>