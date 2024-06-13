<template>
    <div class="mt-4 comments">Comments</div>
    <section id="comments" v-for="(comment, index) in comments" :key="index">
        <!-- Individual comment -->
        <div class="comment">
            <div class="comment-header">
                <div class="profile-image-container" v-if="comment.developer">
                    <img :src="comment.developer.avatar" alt="Current Avatar" class="profile-picture-main" />
                </div>
                <h3 class="comment-author">{{ this.formatNameAndSurname(comment.developer) }}</h3>
                <span class="comment-timestamp">{{ this.formatDate(comment.time) }}</span>
            </div>
            <p class="comment-body">{{ comment.content }}</p>
            <!-- Actions -->
            <div class="comment-actions">
                <div style="margin-right: auto;">
                    <EmojiReaction :reactor="this.username" :react="(reaction) => this.react(reaction, comment)"
                        :unreact="(reaction) => this.unreact(reaction, comment.id)"
                        :getReactions="() => this.getReactions(comment.id)" :dark="true" />
                </div>
                <button class="reply-button" @click="this.showReplySection(comment.id)">Reply</button>
                <button class="delete-button" @click="this.deleteComment(comment.id)">Delete</button>
            </div>



            <!-- Reply section -->
            <div class="mt-3" v-if="comment.replySectionVisible">
                <hr class="muted" />
                <h5 class="bright">Reply</h5>
                <textarea class="w-100 p-2 bright reply-textarea" v-model="newSubCommentContent"></textarea>
                <div class="w-100 d-flex justify-content-end mt-2">
                    <button type="button" class="btn-comment p-2" :disabled="newSubCommentContent == ''"
                        @click="sendReplyComment(comment.id)">Send reply</button>
                </div>
            </div>

            <div class="sub-comments" v-if="comment.sub_comments.length !== 0">
                <hr class="muted">
                <div class="sub-comment" v-for="(subComment, index) in comment.sub_comments" :key="index">
                    <div class="sub-comment-header">
                        <div class="profile-image-container" v-if="subComment.developer">
                            <img :src="subComment.developer.avatar" alt="Current Avatar" class="profile-picture-main" />
                        </div>
                        <h3 class="sub-comment-author">{{ this.formatNameAndSurname(subComment.developer) }}</h3>
                        <span class="sub-comment-timestamp">{{ this.formatDate(subComment.time) }}</span>
                    </div>
                    <p class="sub-comment-body">{{ subComment.content }}</p>
                    <!-- Sub-Comment Actions -->
                    <div class="sub-comment-actions">
                        <div style="margin-right: auto;">
                            <EmojiReaction :reactor="this.username"
                                :react="(reaction) => this.react(reaction, subComment)"
                                :unreact="(reaction) => this.unreact(reaction, subComment.id)"
                                :getReactions="() => this.getReactions(subComment.id)" :dark="true" />
                        </div>
                        <button class="sub-commentdelete-button"
                            @click="this.deleteComment(subComment.id)">Delete</button>
                    </div>
                </div>
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
import ReactionService from '@/services/ReactionService';
import { toast } from 'vue3-toastify';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';

import { EmojiReaction } from 'emoji-reaction';

export default {
    name: "CommentDisplay",
    components: {
        EmojiReaction,
    },

    mounted() {
        this.loadComments();
    },

    props: {
        username: String,
        repoName: String,
        entityType: String,     // issue, milestone, pull_request
        entityId: String,
    },

    data() {
        return {
            newCommentContent: "",
            newSubCommentContent: "",
            comments: [],
        }
    },

    methods: {
        loadComments() {
            CommentService?.getAllComments(this.username, this.repoName, this.entityType, this.entityId)
                .then(res => {
                    console.log(res.data);
                    this.comments = res.data;
                    for (let comment of this.comments) {
                        // Add aditional info for comment
                        comment['replySectionVisible'] = false;

                        // Add developer for comment
                        DeveloperService.getDeveloperBasicInfoFromId(comment.developer_id)
                            .then(res => {
                                comment['developer'] = res.data;

                                // Getting Developer avatar
                                DeveloperService.getUserAvatar(comment.developer.username)
                                    .then(res => {
                                        comment.developer['avatar'] = res.data;
                                    })
                                    .catch(err => {
                                        console.log(err);
                                    });
                            })
                            .catch(err => {
                                console.log(err);
                            });

                        // Add developer for sub comments
                        for (let subComment of comment.sub_comments) {
                            DeveloperService.getDeveloperBasicInfoFromId(subComment.developer_id)
                                .then(res => {
                                    subComment['developer'] = res.data;

                                    // Getting Developer avatar
                                    DeveloperService.getUserAvatar(subComment.developer.username)
                                        .then(res => {
                                            subComment.developer['avatar'] = res.data;
                                        })
                                        .catch(err => {
                                            console.log(err);
                                        });
                                })
                                .catch(err => {
                                    console.log(err);
                                });
                        }
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
                "type_for": this.entityType,
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

        showReplySection(commentId) {
            let comment = this.comments.find(c => c.id === commentId);
            let oldValue = comment.replySectionVisible;
            if (oldValue === true) {
                comment.replySectionVisible = false;
            }
            else {
                comment.replySectionVisible = true;
            }

        },

        sendReplyComment(parentId) {
            if (this.newSubCommentContent === "") {
                return;
            }

            let data = {
                "content": this.newSubCommentContent,
                "parent": parentId,
                "type_for": this.entityType,
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
                    this.emptyReplyCommentsForm();
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

        emptyReplyCommentsForm() {
            this.newSubCommentContent = '';
        },

        react(reaction, reactTo) {
            let data = {
                'code': reaction,
                'comment_id': reactTo.id,
            }
            return ReactionService.createNewReaction(this.username, this.repoName, data)
                .then(res => { console.log(res); })
                .catch(err => { console.log(err); });
        },

        unreact(reaction, reactTo) {
            // console.log("UNREACTTTTTTTT");
            console.log(reaction);
            console.log(reactTo);
            // return ReactionService.deleteReaction(this.username, this.repoName, reactTo);
        },

        async getReactions(reactTo) {
            return ReactionService.getReactionsForComment(this.username, this.repoName, reactTo)
                .then((records) => {
                    if (!Array.isArray(records.data)) {
                        return [];
                    }
                    else {
                        return records.data.reduce((acc, curr) => {
                            const { code, developer_id } = curr;
                            const existingReaction = acc.find(reaction => reaction.reaction === code);

                            if (existingReaction) {
                                // If reaction exists, add reactor if not already present
                                if (!existingReaction.reactors.includes(developer_id)) {
                                    existingReaction.reactors.push(developer_id);
                                }
                            } else {
                                // If reaction does not exist, create new reaction
                                acc.push({
                                    reaction: code,
                                    reactors: [developer_id]
                                });
                            }

                            return acc;
                        }, []);
                    }
                },
                );
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
    flex-grow: 1;
    margin-left: 10px;
}

.comment-timestamp {
    color: #aaa;
    font-size: 0.9em;
}

.comment-body {
    color: #adbbc8;
    margin-bottom: 10px;
    margin-top: 15px;
    margin-left: 33px;
}

.comment-actions {
    display: flex;
    justify-content: flex-end;
    margin-top: 45px
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

/* Dark theme styles for sub-comments */

.sub-comments {
    color: #adbbc8;
    margin: 0;
}

.sub-comment {
    background-color: #444;
    border-radius: 5px;
    border: 2px solid #adbbc8;
    padding: 10px;
    margin-bottom: 15px;
    margin-left: 5em;
}

.sub-comment-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 5px;
}

.sub-comment-author {
    color: #adbbc8;
    /* font-weight: bold; */
    margin: 0;
    flex-grow: 1;
    margin-left: 10px;
}

.sub-comment-timestamp {
    color: #aaa;
    font-size: 0.9em;
}

.sub-comment-body {
    color: #adbbc8;
    margin-bottom: 10px;
    margin-top: 10px;
    margin-left: 33px;
}

.sub-comment-actions {
    display: flex;
    justify-content: flex-end;
}

.sub-commentdelete-button {
    background-color: #333;
    color: #adbbc8;
    border: none;
    border-radius: 3px;
    padding: 5px 10px;
    margin-left: 5px;
    cursor: pointer;
}

.sub-commentdelete-button:hover {
    background-color: #555;
}

.reply-textarea {
    background-color: #555;
}

.profile-image-container {
    display: flex;
    align-items: center;
    justify-content: center;
}

.profile-picture-main {
    width: 25px;
    height: 25px;
    border-radius: 50%;
    /* This makes the image circular */
    object-fit: cover;
    /* This ensures the image covers the entire 25x25 area */
}
</style>
