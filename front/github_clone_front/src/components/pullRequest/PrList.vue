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

                <div class="container mt-3" id="pulls-table">
                    <div class="row my-2">
                        <div class="col-1 check ms-2">
                            <input type="checkbox" />
                        </div>
                        <div class="col-5 d-flex justify-content-start">
                            <button type="button" class="btn-num-req me-2" @click="setOpenPullsChosen">
                                <label :class="openPullsChosen ? 'num-req-active' : 'num-req'">{{ openPulls.length }} Open</label>
                            </button>
                            <button type="button" class="btn-num-req" @click="setClosedPullsChosen">
                                <label :class="!openPullsChosen ? 'num-req-active' : 'num-req'">{{ closedPulls.length }} Closed</label>
                            </button>
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
                        <div class="col-1 check ms-2">
                            <input type="checkbox" />
                        </div>

                        <div class="col-5">
                            <div class="d-flex justify-content-start">
                                <img v-if="pull.status === 'Open'" alt="pr" src="../../assets/open_pr_green.png" class="img-pr mt-1 me-2" />
                                <img v-if="pull.status === 'Merged'" alt="pr" src="../../assets/merged_pr_purple.png" class="img-pr me-2" />
                                <img v-if="pull.status === 'Closed'" alt="pr" src="../../assets/closed_pr_red.png" class="img-pr me-2" />
                                <button type="button" class="btn-link">
                                    <h5 class="me-2">{{ pull.title }}</h5>
                                </button>
                                <button v-for="lbl in pull.labels" :key="lbl" class="btn-label mx-1" type="button">{{ lbl }}</button>
                            </div>
                            <div class="d-flex justify-content-start mt-1">
                                <label class="pull-desc">
                                    #{{ pull.id }} opened on {{ pull.timestamp.slice(0, 10) }} by
                                    <button type="button" class="btn-link">{{ pull.author }}</button>
                                </label>
                            </div>
                        </div>

                        <div class="col"></div>
                        <div class="col"></div>
                        <div class="col"></div>
                        <div class="col"></div>
                        <div class="col criterium d-flex justify-content-center align-items-top">
                            <button class="btn-img" type="button">
                                <img v-if="pull.assignee" :src="pull.assignee.avatar" class="user-icon" />
                            </button>
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
import PullRequestService from "@/services/PullRequestService"

export default {
    name: "PrList",
    components: {
        RepoNavbar,
        FilterBar
    },

    mounted() {
        PullRequestService.getAll(this.$route.params.repoName).then(res => {
            console.log(res.data);
            this.openPulls = res.data.filter(x => x.status === "Open");
            this.closedPulls = res.data.filter(x => x.status !== "Open");
            this.pulls = this.openPulls;
        }).catch(err => {
            console.log(err);
        });
    },

    data() {
        return {
            pulls: [],
            openPulls: [],
            closedPulls: [],
            openPullsChosen: true
        }
    },

    methods: {
        createPullRequest() {

        },

        setOpenPullsChosen() {
            this.pulls = this.openPulls;
            this.openPullsChosen = true;
        },

        setClosedPullsChosen() {
            this.pulls = this.closedPulls;
            this.openPullsChosen = false;
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

.img-pr {
    height: 18px;
}

.background {
    background-color: #22272d;
}

.fa-code-pull-request,
.num-req-active,
h5,
hr {
    color: #adbbc8;
}

.num-req {
    color: #768491;
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
    height: 26px;
}

hr {
    margin-top: 5px;
}

.pull-desc {
    color: #5f6d7a;
    font-size: small;
}

.btn-link,
.btn-img {
    background: none;
    border: none;
    text-decoration: none;
}

.btn-img {
    height: 25px;
}

.pull-desc>.btn-link {
    color: #5f6d7a;
}

.btn-link:hover,
.btn-link>h5:hover {
    color: #2671e2;
}

.btn-num-req {
    background: none;
    border: none;
}

.num-req:hover {
    cursor: pointer;
}
</style>