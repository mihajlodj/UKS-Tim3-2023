<template>
    <div class="container my-4">
        <h3 class="mb-3">Danger Zone</h3>

        <div class="cell first d-flex justify-content-between">
            <div>
                <h6 class="bold">Change repository visibility</h6>
                <span>The repository is currently {{ accessModifier.toLowerCase() }}.</span>
            </div>

            <div>
                <button class="btn btn-outline-danger mt-1" data-bs-toggle="modal" data-bs-target="#changeVisibilityModal">
                    Change
                </button>
            </div>
        </div>
        <div class="cell d-flex justify-content-between">
            <div>
                <h6 class="bold">Transfer ownership</h6>
                <span>Transfer this repository to another user.</span>
            </div>

            <div>
                <button class="btn btn-outline-danger mt-1" @click="transferOwnership">Transfer ownership</button>
            </div>
        </div>
        <div class="cell last d-flex justify-content-between">
            <div>
                <h6 class="bold">Delete this repository</h6>
                <span>Once you delete a repository, there is no going back.</span>
            </div>

            <div>
                <button class="btn btn-outline-danger mt-1" data-bs-toggle="modal" data-bs-target="#deleteRepoModal">
                    Delete this repository
                </button>
            </div>
        </div>

        <!-- Modal -->
        <div class="modal fade" id="changeVisibilityModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Are you sure you want to change repository visibility?</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary btn-yes" @click="changeModifier">Yes</button>
                        <button type="button" class="btn btn-primary btn-no" data-bs-dismiss="modal">No</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal -->
        <div class="modal fade" id="deleteRepoModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Are you sure you want to delete this repository?</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary btn-yes" @click="deleteRepository">Yes</button>
                        <button type="button" class="btn btn-primary btn-no" data-bs-dismiss="modal">No</button>
                    </div>
                </div>
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
            RepositoryService.update(this.$route.params.username, { 'access_modifier': newModifier }, this.$route.params.repoName).then(_ => {
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
        },

        transferOwnership() {
            this.$router.push(`/view/${this.$route.params.username}/${this.$route.params.repoName}/transfer`)
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

.btn-yes,
.btn-no,
.btn-yes:hover,
.btn-no:hover {
    background-color: #f7f8fa;
    border: 1px solid #d0d7df;
    height: 40px;
    width: 70px;
    color: rgb(59, 58, 58);
}

h3, h6, span {
    color: #c5d1df
}
</style>