<template>
    <div class="container my-4">
        <h3 class="mb-3">Danger Zone</h3>

        <div class="cell first d-flex justify-content-between">
            <div>
                <h6 class="bold">Change repository visibility</h6>
                <span>The repository is currently {{ accessModifier.toLowerCase() }}.</span>
            </div>

            <div>
                <button class="btn btn-outline-danger mt-1" @click="changeModifier">Change</button>
            </div>
        </div>
        <div class="cell d-flex justify-content-between">
            <div>
                <h6 class="bold">Transfer ownership</h6>
                <span>Transfer this repository to another user.</span>
            </div>

            <div>
                <button class="btn btn-outline-danger mt-1">Transfer ownership</button>
            </div>
        </div>
        <div class="cell last d-flex justify-content-between">
            <div>
                <h6 class="bold">Delete this repository</h6>
                <span>Once you delete a repository, there is no going back.</span>
            </div>

            <div>
                <button class="btn btn-outline-danger mt-1" @click="deleteRepository">Delete this repository</button>
            </div>
        </div>
    </div>
</template>

<script>

import RepositoryService from '@/services/RepositoryService';

export default {
    /* eslint-disable */
    name: 'DangerZoneSettings',

    props: ['accessModifier'],

    methods: {
        changeModifier() {
            let newModifier = 'Public';
            if (this.accessModifier === 'Public') {
                newModifier = 'Private';
            }
            RepositoryService.update({'access_modifier': newModifier}, this.$route.params.repoName).then(_ => {
                location.reload();
            }).catch(err => {
                console.log(err);
            });
        },

        deleteRepository() {
            RepositoryService.deleteReposiory(this.$route.params.username, this.$route.params.repoName).then(_ => {
                console.log('DELETED');
            }).catch(err => {
                console.log(err);
            });
            this.$router.push('/main')
        }
    }
}

</script>

<style scoped>
.cell {
    border-top: 1px solid #a7a4a4;
    border-left: 2px solid #f8d0d2;
    border-right: 2px solid #f8d0d2;
    padding: 10px;
}

.first {
    border-top: 2px solid #f8d0d2;
    border-top-right-radius: 7px;
    border-top-left-radius: 7px;
}

.last {
    border-bottom: 2px solid #f8d0d2;
    border-bottom-right-radius: 7px;
    border-bottom-left-radius: 7px;
}

.bold {
    font-weight: 600;
}

.container {
    width: 50%;
    min-width: 700px;
    max-width: 850px;
}
</style>