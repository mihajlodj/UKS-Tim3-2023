<template>
    <div class="bg is-fullheight min-vh-100">
        <div v-if="allowed && invitationInfo !== null">
            <RepoNavbar />

            <div class="d-flex justify-content-center w-100 mt-5">
                <div class="w-50">
                    <div class="d-flex justify-content-center">
                        <button class="img-avatar">
                            <img class="me-4" :src="invitationInfo.owner_avatar"/>
                        </button>
                        <button class="img-avatar">
                            <img class="ms-4" :src="invitationInfo.invited_user_avatar"/>
                        </button>
                    </div>

                    <h2 class="d-flex justify-content-center mt-4 mb-5">
                        <button class="owner-username">{{ invitationInfo.owner_username }}</button>&nbsp;
                        <span class=mt-1>invited you to collaborate</span>
                    </h2>

                    <div class="d-flex justify-content-center">
                        <button type="button" class="btn-accept me-1" @click="accept">Accept invitation</button>
                        <button type="button" class="btn-decline ms-1" @click="decline">Decline</button>
                    </div>
                </div>
            </div>
        </div>
        <NotFoundPage v-else />
    </div>
</template>

<script>
import RepoNavbar from './RepoNavbar.vue'
import NotFoundPage from '@/components/util/NotFoundPage.vue'
import RepositoryService from '@/services/RepositoryService';

export default {
    name: "CollaborationInvitation",
    components: {
        RepoNavbar,
        NotFoundPage
    },

    mounted() {
        RepositoryService.getInvitation(this.$route.params.username, this.$route.params.repoName, this.$route.params.invitedUsername).then(res => {
            this.invitationInfo = res.data;
            this.allowed = true;
        }).catch(err => {
            console.log(err);
        });
    },

    data() {
        return {
            allowed: false,
            invitationInfo: null
        }
    },

    methods: {
        accept() {
            RepositoryService.respondToInvitation(this.$route.params.username, this.$route.params.repoName, this.$route.params.invitedUsername, "accept").then(res => {
                console.log(res);
                this.$router.push(`/view/${this.invitationInfo.owner_username}/${this.$route.params.repoName}`);
            }).catch(err => {
                console.log(err);
            });
        },

        decline() {
            RepositoryService.respondToInvitation(this.$route.params.username, this.$route.params.repoName, this.$route.params.invitedUsername, "decline").then(res => {
                console.log(res);
                this.$router.push('/main');
            }).catch(err => {
                console.log(err);
            });
        }
    }
}
</script>

<style scoped>
.bg {
    background-color: #22272d;
}

h2 {
    color: #c5d1df;
}

.btn-accept {
    border: none;
    border-radius: 7px;
    color: #fff;
    background-color: #347d38;
    padding: 7px 17px;
}

.btn-decline {
    border: none;
    border-radius: 7px; 
    color: #bcc6d4;
    background-color: #373e48;
    padding: 7px 17px;
}

.owner-username {
    background: none;
    border: none;
    text-decoration: underline;
    color: #488be6;
    font-weight: 600;
}

img {
    height: 70px;
    border-radius: 50%;
}

.img-avatar {
    background: none;
    border: none;
}
</style>