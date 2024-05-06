<template>
    <div class="mt-4 comments">Comments</div>
    <section id="comments" v-for="(comment, index) in comments" :key="index">
        <!-- Individual comment -->
        <div class="comment">
            <div class="comment-header">
                <h3 class="comment-author">{{ this.formatNameAndSurname(comment.developer) }}</h3>
                <span class="comment-timestamp">{{ this.formatDate(comment.time) }}</span>
            </div>
            <p class="comment-body">{{ comment.content }}</p>
            <!-- Actions -->
            <div class="comment-actions">
                <button class="reply-button">Reply</button>
                <button class="delete-button" @click="this.deleteComment(comment.id)">Delete</button>
            </div>
        </div>
    </section>


    <div class="mt-3">
        <h5 class="bright">Add a comment</h5>
        <textarea v-model="newCommentContent" class="w-100 p-2 bright"></textarea>
        <div class="w-100 d-flex justify-content-end mt-2">
            <button type="button" class="btn-comment p-2" :disabled="newCommentContent == ''"
                @click="sendComment()">Comment</button>
        </div>
    </div>

</template>

<script>
import CommentService from '@/services/CommentService'
import DeveloperService from '@/services/DeveloperService';
import { toast } from 'vue3-toastify';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';


export default {
    name: "CommentDisplay",
    components: {
        
    },

    mounted() {
        this.loadComments();
    },

    props: {
        username: String,
        repoName: String,
        entityType: String,     // issue, milestone, pull_request
        entityId: Int32Array,
    },

    data() {
        return {
            newCommentContent: "",
            comments: [],
        }
    },

    methods: {
        loadComments() {
            CommentService.getAllCommentsForPullRequest(this.username, this.repoName, this.entityId)
            .then(res => {
                console.log(res.data);
                this.comments = res.data;
                for (let comment of this.comments) {
                    DeveloperService.getUserBasicInfoFromId(comment.developer_id)
                    .then(res => {
                        comment['developer'] = res.data;
                    })
                    .catch(err => {
                        console.log(err);
                    });
                }
                console.log(this.comments);
            })
            .catch(err => {
                console.log(err);
            });
        },

        formatNameAndSurname(developer) {
            return developer?.first_name + " " + developer?.last_name;
        },

        formatDate(date) {
            dayjs.extend(utc);
            // Parse the given date string using Day.js, considering it as UTC time
            const parsedDate = dayjs.utc(date);

            // Format the parsed date into the desired format
            return parsedDate.format('DD.MM.YYYY. HH:mm');
        },

        sendComment() {
            if (this.newCommentContent === "") {
                return;
            }

            let data = {
                "content": this.newCommentContent,
                "parent": null,
                "type_for": "pull_request",
                "type_id": this.entityId,
            };

            CommentService.createNewComment(this.username, this.repoName, data)
                .then(res => {
                    console.log(res);
                    toast("Comment added.", {
                        autoClose: 500,
                        type: 'success',
                        position: toast.POSITION.BOTTOM_RIGHT,
                        theme: toast.THEME.DARK
                    });
                    this.emptyCommentsForm();
                    this.loadComments();
                })
                .catch(err => {
                    console.log(err);
                    toast("Error occured while adding comment.", {
                        autoClose: 1000,
                        type: 'error',
                        position: toast.POSITION.BOTTOM_RIGHT,
                        theme: toast.THEME.DARK
                    });
                });
        },

        emptyCommentsForm() {
            this.newCommentContent = '';
        },

        deleteComment(commentId) {
            CommentService.deleteComment(this.username, this.repoName, commentId)
            .then(res => {
                console.log(res);
                toast("Comment deleted.", {
                    autoClose: 500,
                    type: 'success',
                    position: toast.POSITION.BOTTOM_RIGHT,
                    theme: toast.THEME.DARK
                });
                this.loadComments();
            })
            .catch(err => {
                console.log(err);
                toast("Error occured while deleting comment!", {
                    autoClose: 1000,
                    type: 'error',
                    position: toast.POSITION.BOTTOM_RIGHT,
                    theme: toast.THEME.DARK
                });
            });
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

/* Dark theme styles for comments */
#comments {
    background-color: #22272d;
    margin-top: 20px;
}

.comment {
    background-color: #444;
    border-radius: 5px;
    border: 2px solid #adbbc8;
    padding: 10px;
    margin-bottom: 15px;
}

.comment-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 5px;
}

.comments {
    color: #adbbc8;
    font-weight: bold;
    margin: 0;
    font-size: 35px;
}

.comment-author {
    color: #adbbc8;
    font-weight: bold;
    margin: 0;
}

.comment-timestamp {
    color: #aaa;
    font-size: 0.9em;
}

.comment-body {
    color: #adbbc8;
    margin-bottom: 10px;
}

.comment-actions {
    display: flex;
    justify-content: flex-end;
}

.reply-button,
.delete-button {
    background-color: #333;
    color: #adbbc8;
    border: none;
    border-radius: 3px;
    padding: 5px 10px;
    margin-left: 5px;
    cursor: pointer;
}

.reply-button:hover,
.delete-button:hover {
    background-color: #555;
}

</style>
