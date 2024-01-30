<template>
    <div>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container-fluid">
                <div class="collapse navbar-collapse">
                    <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                        <li class="nav-item mx-2">
                            <button :class="(activeLink=='overview') ? 'nav-link active' : 'nav-link'" @click="setActiveLink('overview')">
                                <div class="d-flex justify-content-start">
                                    <i class="bi bi-book"></i>
                                    &nbsp; 
                                    Overview
                                </div>
                            </button>
                        </li>
                        <li class="nav-item mx-2">
                            <button :class="(activeLink=='repositories') ? 'nav-link active' : 'nav-link'" @click="setActiveLink('repositories')">
                                <div class="d-flex justify-content-start">
                                    <i class="bi bi-journal-bookmark"></i>
                                    &nbsp; 
                                    Repositories
                                </div>
                            </button>
                        </li>
                        <li class="nav-item mx-2">
                            <button :class="(activeLink=='projects') ? 'nav-link active' : 'nav-link'" @click="setActiveLink('projects')">
                                <div class="d-flex justify-content-start">
                                    <i class="bi bi-window-sidebar"></i>
                                    &nbsp;
                                    Projects
                                </div>
                            </button>
                        </li>
                        <li class="nav-item mx-2">
                            <button :class="(activeLink=='stars') ? 'nav-link active' : 'nav-link'" @click="setActiveLink('stars')">
                                <div class="d-flex justify-content-start">
                                    <i class="bi bi-star"></i>
                                    &nbsp;
                                    Stars
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
    name: 'ProfileNavBarExtension',

    props: ['starting'],

    mounted() {
        if (this.starting) {
            this.activeLink = this.starting;
        }
    },

    data() {
        return {
            activeLink: 'overview',
        }
    },

    methods: {
        setActiveLink(name) {
            this.activeLink = name;
            // let username = this.$route.params.username;
            // let repoName = this.$route.params.repoName;
            if (name === 'stars') {
                // this.$router.push(`/settings/${username}/${repoName}`);
            } else if (name == 'overview') {
                // this.$router.push(`/view/${username}/${repoName}`);
            }
        }
    }
}

</script>

<style scoped>
.nav-link {
    color: white;
}

.active {
    border-bottom: 2px solid #fe8c72;
}

</style>