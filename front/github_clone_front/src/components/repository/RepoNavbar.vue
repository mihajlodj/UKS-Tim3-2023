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
            let username = this.$route.params.username;
            let repoName = this.$route.params.repoName;
            if (name === 'settings') {
                this.$router.push(`/settings/${username}/${repoName}`);
            } else if (name == 'code') {
                this.$router.push(`/view/${username}/${repoName}`);
            } else if (name == 'issues') {
                this.$router.push(`/view/${username}/${repoName}/issues`)
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