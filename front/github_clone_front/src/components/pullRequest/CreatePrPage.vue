<template>
    <div>
        <RepoNavbar />
        <div class="p-3">
            <h3>Compare changes</h3>
            <h6>Choose two branches to see what’s changed or to start a new pull request</h6>
        </div>
        <hr>

        <div class="p-3 d-flex justify-content-start">
            <BranchChoice type="base" />
            <p class="mx-3">arrow</p>
            <BranchChoice type="compare" />
        </div>

        <div class="p-3">Number of commits, number of files changed, number of contributors</div>
    </div>
</template>

<script>
import RepoNavbar from "@/components/repository/RepoNavbar.vue"
import BranchChoice from "./BranchChoice.vue"

export default {
    name: 'CreatePrPage',
    components: {
        RepoNavbar,
        BranchChoice
    }
}
</script>