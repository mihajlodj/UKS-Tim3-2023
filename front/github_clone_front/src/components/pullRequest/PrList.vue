<template>
    <div class="background is-fullheight min-vh-100">
        <RepoNavbar starting="pullRequests" />
        <div class="d-flex justify-content-center px-5">
            <div class="contain">
                <div class="d-flex justify-content-between mt-5">
                    <FilterBar />
                    <div class="d-flex justify-content-end">
                        <button type="button" class="btn-create py-2 px-3" @click="createPullRequest">New pull
                            request</button>
                    </div>
                </div>

                <div class="d-flex justify-content-between mt-3">
                    <div class="d-flex justify-content-start">

                    </div>

                    <div class="d-flex justify-content-end">

                    </div>
                </div>

                <div class="container" id="pulls-table">
                    <div class="row my-2">
                        <div class="col-1 check ms-2">
                            <input type="checkbox" />
                        </div>
                        <div class="col-5">
                            <label class="num-req">1 Open</label>
                        </div>
                        <div class="col criterium d-flex justify-content-center">
                            Author
                        </div>
                        <div class="col criterium d-flex justify-content-center">
                            Label
                        </div>
                        <div class="col criterium d-flex justify-content-center">
                            Milestones
                        </div>
                        <div class="col criterium d-flex justify-content-center">
                            Reviews
                        </div>
                        <div class="col criterium d-flex justify-content-center">
                            Assignee
                        </div>
                        <div class="col criterium d-flex justify-content-center">
                            Sort
                        </div>
                    </div>

                    <div v-for="pull in pulls" :key="pull.id" class="row my-1">
                        <hr />
                        <div class="col-1 check ms-2 mt-1">
                            <input type="checkbox" />
                        </div>

                        <div class="col-5">
                            <div class="d-flex justify-content-start">
                                <button type="button" class="btn-link"><h5 class="me-2 mt-1">{{ pull.title }}</h5></button>
                                <button v-for="lbl in pull.labels" :key="lbl" class="btn-label mx-1" type="button">{{ lbl }}</button>
                            </div>
                            <div class="d-flex justify-content-start mt-2">
                                <label class="pull-desc">
                                    #{{ pull.id }} opened on 2024-01-01 by 
                                    <button type="button" class="btn-link">{{ pull.author }}</button>
                                </label>
                            </div>
                        </div>

                        <div class="col"></div>
                        <div class="col"></div>
                        <div class="col"></div>
                        <div class="col"></div>
                        <div class="col criterium d-flex justify-content-center">
                            <img v-if="pull.assignee" :src="pull.assignee.icon" class="user-icon"/>
                        </div>
                        <div class="col"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import RepoNavbar from "@/components/repository/RepoNavbar.vue"
import FilterBar from "./FilterBar.vue";

export default {
    name: "PrList",
    components: {
        RepoNavbar,
        FilterBar
    },

    mounted() {
        this.pulls = [{
            title: "Moj request",
            status: "Open",
            author: "elenore55",
            timestamp: "",
            id: 1,
            labels: ["documentation", "feature"],
            assignee: {
                username: "elenore55",
                icon: "http://localhost:3000/avatar/c07feba0edeab310e51a1d754c81c0ef?size=512"
            },
            milestone: "Kontrolna tacka 1",
            reviews: []
        }, {
            title: "Moj request 2",
            status: "Open",
            author: "elenore55",
            timestamp: "",
            id: 1,
            labels: ["frontend", "feature"],
            assignee: {
                username: "elenore55",
                icon: "http://localhost:3000/avatar/c07feba0edeab310e51a1d754c81c0ef?size=512"
            },
            milestone: "Kontrolna tacka 1",
            reviews: []
        },
    ]
    },

    data() {
        return {
            pulls: [
                {
                    title: "",
                    status: "Open",
                    author: "",
                    timestamp: "",
                    id: -1,
                    labels: [],
                    assignee: {
                        username: "",
                        icon: ""
                    },
                    milestone: "",
                    reviews: []
                },
            ],

            openPulls: [],
            closedPulls: []
        }
    },

    methods: {
        createPullRequest() {

        }
    }
}
</script>

<style scoped>
.contain {
    width: 100%;
    max-width: 1500px;
}

.btn-create {
    color: #f4f8f4;
    background-color: #347d38;
    border-radius: 7px;
    border: none;
}

.background {
    background-color: #22272d;
}

.fa-code-pull-request,
.num-req, h5, hr {
    color: #adbbc8;
}

.criterium {
    color: #768491;
}

div.check {
    width: 40px;
}

#pulls-table {
    border: 1px solid #768491;
    width: 100%;
    border-radius: 7px;
}

.user-icon {
    width: 25px;
    height: 25px;
    border-radius: 50%;
}

.btn-label {
    padding: 0px 15px;
    border-radius: 16px;
    background-color: rgb(46, 27, 90);
    color: rgb(177, 154, 231);
    border: 1px solid rgb(177, 154, 231);
}

hr {
    margin-top: 5px;
}

.pull-desc {
    color: #5f6d7a;
    font-size: small;
}

.btn-link {
    background: none;
    border: none;
    text-decoration: none;
}

.pull-desc > .btn-link {
    color: #5f6d7a;
}

.btn-link:hover, .btn-link > h5:hover {
    color: #2671e2;
}

</style>