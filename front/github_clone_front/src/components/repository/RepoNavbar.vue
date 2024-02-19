<template>
    <div>
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <div class="container-fluid">
                <div class="collapse navbar-collapse">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item mx-2">
                            <button :class="(activeLink=='code') ? 'nav-link active' : 'nav-link'" @click="setActiveLink('code')">
                                <div class="d-flex justify-content-start">
                                    <font-awesome-icon icon="fa-solid fa-code" class="me-2 mt-1" />
                                    Code
                                </div>
                            </button>
                        </li>
                        <li class="nav-item mx-2">
                            <button :class="(activeLink=='issues') ? 'nav-link active' : 'nav-link'" @click="setActiveLink('issues')">
                                <div class="d-flex justify-content-start">
                                    <font-awesome-icon icon="fa-regular fa-circle-dot" class="me-2 mt-1" />
                                    Issues
                                </div>
                            </button>
                        </li>
                        <li class="nav-item mx-2">
                            <button :class="(activeLink=='milestones') ? 'nav-link active' : 'nav-link'" @click="setActiveLink('milestones')">
                                <div class="d-flex justify-content-start">
                                    <svg viewBox="0 0 16 16" class="svg mt-1 me-2" aria-hidden="true" width="16" height="16"><path d="M7.75 0a.75.75 0 0 1 .75.75V3h3.634c.414 0 .814.147 1.13.414l2.07 1.75a1.75 1.75 0 0 1 0 2.672l-2.07 1.75a1.75 1.75 0 0 1-1.13.414H8.5v5.25a.75.75 0 0 1-1.5 0V10H2.75A1.75 1.75 0 0 1 1 8.25v-3.5C1 3.784 1.784 3 2.75 3H7V.75A.75.75 0 0 1 7.75 0Zm4.384 8.5a.25.25 0 0 0 .161-.06l2.07-1.75a.248.248 0 0 0 0-.38l-2.07-1.75a.25.25 0 0 0-.161-.06H2.75a.25.25 0 0 0-.25.25v3.5c0 .138.112.25.25.25h9.384Z"></path></svg>
                                    Milestones
                                </div>
                            </button>
                        </li>
                        <li class="nav-item mx-2">
                            <button :class="(activeLink=='pullRequests') ? 'nav-link active' : 'nav-link'" @click="setActiveLink('pullRequests')">
                                <div class="d-flex justify-content-start">
                                    <font-awesome-icon icon="fa-solid fa-code-pull-request" class="me-2 mt-1" />
                                    Pull requests
                                </div>
                            </button>
                        </li>
                        <li class="nav-item mx-2">
                            <button :class="(activeLink=='settings') ? 'nav-link active' : 'nav-link'" @click="setActiveLink('settings')">
                                <div class="d-flex justify-content-start">
                                    <font-awesome-icon icon="fa-solid fa-gear" class="me-2 mt-1" />
                                    Settings
                                </div>
                            </button>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </div>
</template>

<script>

export default {
    name: 'RepoNavbar',

    props: ['starting'],

    mounted() {
        if (this.starting) {
            this.activeLink = this.starting;
        }
    },

    data() {
        return {
            activeLink: 'code',
        }
    },

    methods: {
        setActiveLink(name) {
            this.activeLink = name;
            console.log(this.activeLink);
            let username = this.$route.params.username;
            let repoName = this.$route.params.repoName;
            if (name === 'settings') {
                this.$router.push(`/settings/${username}/${repoName}`);
            } else if (name == 'code') {
                this.$router.push(`/view/${username}/${repoName}`);
            } else if (name == 'milestones') {
                this.$router.push(`/view/${username}/${repoName}/milestones`);
            } else if (name == 'pullRequests') {
                this.$router.push(`/view/${username}/${repoName}/pulls`);
            }
        }
    }
}

</script>

<style scoped>
.nav-link {
    color: black;
}

.active {
    border-bottom: 2px solid #fe8c72;
}
</style>