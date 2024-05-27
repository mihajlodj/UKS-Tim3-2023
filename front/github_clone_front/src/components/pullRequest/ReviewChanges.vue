<template>
    <div class="mt-1 mb-4 w-100">
        <h5 class="bright">Add a review</h5>
        <textarea v-model="commentContent" class="w-100 p-2 bright"></textarea>
        <div class="typeofreview">
            <div class="d-flex flex-column gap-2 bright">
                <div class="outer-div">
                    <input class="" type="radio" value="General comment" v-model="this.selectedOption">
                    <span class="inner-span">
                        <label class="label">Comment</label>
                        <span>Submit general feedback without explicit approval.</span>
                    </span>
                </div>

                <div class="outer-div">
                    <input class="" type="radio" value="Approved" v-model="this.selectedOption">
                    <span class="inner-span">
                        <label class="label">Approve</label>
                        <span>Submit feedback and approve merging these
                            changes.</span>
                    </span>
                </div>

                <div class="outer-div">
                    <input class="" type="radio" value="Request changes" v-model="this.selectedOption">
                    <span class="inner-span">
                        <label class="label">Request changes</label>
                        <span>Submit feedback that must be addressed
                            before merging.</span>
                    </span>
                </div>
            </div>
        </div>
        <div class="w-100 mt-3">
            <button type="button" class="btn-comment p-2" :disabled="commentContent == ''"
                @click="submitReview()">Submit review</button>
        </div>
        <hr class="bright">
    </div>
</template>
<script>
import PullRequestService from '@/services/PullRequestService';
import { toast } from 'vue3-toastify';

export default {
    name: "ReviewChanges",
    components: {

    },

    mounted() {

    },

    props: {

    },

    data() {
        return {
            commentContent: '',
            selectedOption: 'General comment',
            username: this.$route.params.username,
            repoName: this.$route.params.repoName,
            pullRequestId: this.$route.params.id,
        }
    },

    methods: {
        submitReview() {
            let data = {
                "reviewer": localStorage.getItem('username'),
                "comment": this.commentContent,
                "status": this.selectedOption,
            }
            PullRequestService.addReview(this.username, this.repoName, this.pullRequestId, data)
                .then(res => {
                    console.log(res);
                    toast("Review sucessfully added!", {
                        autoClose: 500,
                        type: 'success',
                        position: toast.POSITION.BOTTOM_RIGHT,
                        theme: toast.THEME.DARK
                    });
                    this.clearForm();
                    this.notifyParent();
                })
                .catch(err => {
                    console.log(err);
                    toast("Error occured while adding review!", {
                        autoClose: 1000,
                        type: 'error',
                        position: toast.POSITION.BOTTOM_RIGHT,
                        theme: toast.THEME.DARK
                    });
                });
        },

        clearForm() {
            this.commentContent = '';
            this.selectedOption = 'General comment';
        },

        notifyParent() {
            this.$emit('reviewAdded');
        },
    }
}
</script>
<style scoped>
.background {
    background-color: #22272d;
}

.bright {
    color: #adbbc8;
}

.description {
    min-height: 100px;
    background: none;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #0298db;
}

.muted {
    color: #768491;
}


input.edit {
    width: 75%;
    height: 40px;
    border-radius: 5px;
    background-color: #1c2127;
    color: #adbbc8;
    border: 1px solid #768491;
}

.pr-icon {
    height: 17px;
}

.btn-edit-title,
.btn-review {
    height: 40px;
    width: 70px;
    background-color: #373e48;
    border: 1px solid #768491;
    border-radius: 5px;
}

.btn-close-pr {
    background-color: #373e48;
    border-radius: 5px;
    border: 1px solid #768491;
}

.btn-comment {
    background-color: #347d38;
    border-radius: 5px;
    border: none;
    color: white;
}

.btn-comment:disabled {
    background-color: #315f3a;
    color: #adbbc8;
}

.tab {
    background: none;
    border: 1px solid #adbbc8;
    min-width: 140px;
    color: #768491;
    border-top-right-radius: 5px;
    border-top-left-radius: 5px;
    height: 40px;
}

.tab.active {
    color: #adbbc8;
    border-bottom: none;
}

.tab:hover {
    color: #adbbc8;
}

.bg-none {
    background: none;
    border: none;
    height: 15px;
    font-weight: 600;
}

.btn-branch {
    height: 25px;
    border: none;
    background-color: #253141;
    color: #549bf5;
    margin: 0px 3px;
    padding: 1px 5px;
    border-radius: 5px;
}

div.merge {
    border: 1px solid #768491;
    border-radius: 7px;
    padding: 10px 15px;
}

textarea {
    min-height: 150px;
    resize: none;
    background-color: #22272d;
    border: 1px solid #768491;
    border-radius: 7px;
}

.btn-save {
    width: 120px;
    background-color: #373e48;
    border: 1px solid #768491;
    border-radius: 5px;
}


/************ Styles for radio buttons ************/

/* Style for the outer div */
.outer-div {
    display: flex;
    /* Use flexbox */
    align-items: center;
    /* Vertically align items */
}

/* Style for the input */
.outer-div input[type="radio"] {
    margin-right: 10px;
    /* Adjust margin as needed */
}

/* Style for the inner span */
.inner-span {
    display: flex;
    /* Use flexbox */
    flex-direction: column;
    /* Stack elements vertically */
}

/* Style for the label */
.inner-span .label {
    margin-top: 15px;
    font-weight: bold;
    /* Example styling */
}

/* Style for the span inside inner span */
.inner-span span {
    margin-top: 5px;
    /* Add space between label and span */
}
</style>
