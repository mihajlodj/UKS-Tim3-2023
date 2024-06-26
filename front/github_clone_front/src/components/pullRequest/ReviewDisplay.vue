<template>
    <div v-if="this.reviews.length !== 0">
        <hr class="bright mt-4" />
        <div class="mt-4 reviews">Reviews</div>
        <section id="reviews" v-for="(review, index) in reviews" :key="index">
            <div class="review">
                <div class="review-header">
                    <div class="profile-image-container" v-if="review.reviewer">
                        <img :src="review.reviewer.avatar" alt="Current Avatar" class="profile-picture-main" />
                    </div>
                    <h3 class="review-author">{{ this.formatNameAndSurname(review.reviewer) }}</h3>
                    <span class="review-timestamp">{{ this.formatDate(review.timestamp) }}</span>
                </div>
                <p class="review-body">{{ review.comment }}</p>
                <div class="review-actions">
                    <div class="approved-icon" v-if="review.status === 'Approved'">
                        <svg viewBox="-1.7 0 20.4 20.4" class="" aria-hidden="true" width="20.4" height="20.4"
                            fill="#347d38">
                            <path
                                d="M16.417 10.283A7.917 7.917 0 1 1 8.5 2.366a7.916 7.916 0 0 1 7.917 7.917zm-4.105-4.498a.791.791 0 0 0-1.082.29l-3.828 6.63-1.733-2.08a.791.791 0 1 0-1.216 1.014l2.459 2.952a.792.792 0 0 0 .608.285.83.83 0 0 0 .068-.003.791.791 0 0 0 .618-.393L12.6 6.866a.791.791 0 0 0-.29-1.081z">
                            </path>
                        </svg>
                    </div>
                    <div class="comment-icon" v-if="review.status === 'General comment'">
                        <svg viewBox="0 0 32 32" class="" aria-hidden="true" width="20.4" height="20.4" fill="#FFC107">
                            <path
                                d="M326,257 C317.163,257 310,263.143 310,270.72 C310,276.969 314.877,282.232 321.542,283.889 L326,289.001 L330.459,283.889 C337.123,282.232 342,276.969 342,270.72 C342,263.143 334.837,257 326,257"
                                transform="translate(-310.000000, -257.000000)">
                            </path>
                        </svg>
                    </div>
                    <div class="request-changes-icon" v-if="review.status === 'Request changes'">
                        <svg viewBox="0 0 16 16" class="" aria-hidden="true" width="20.4" height="20.4" fill="#DC3545">
                            <path
                                d="M14.5 1h-13l-.5.5v10l.5.5H4v2.5l.854.354L7.707 12H14.5l.5-.5v-10l-.5-.5zM14 11H7.5l-.354.146L5 13.293V11.5l-.5-.5H2V2h12v9zm-4-1H6V8.979h4V10zM7.5 3h1v2h2v1h-2v2h-1V6h-2V5h2V3z">
                            </path>
                        </svg>
                    </div>
                </div>
            </div>
        </section>
        <hr class="bright mt-4" />
    </div>
</template>
<script>
import PullRequestService from '@/services/PullRequestService';
import DeveloperService from '@/services/DeveloperService';

import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';

export default {
    name: "ReviewDisplay",
    components: {

    },

    mounted() {
        this.loadReviews();
    },

    props: {
    },

    data() {
        return {
            username: this.$route.params.username,
            repoName: this.$route.params.repoName,
            pullRequestId: this.$route.params.id,

            reviews: [],
        }
    },

    methods: {
        loadReviews() {
            PullRequestService.getReviews(this.username, this.repoName, this.pullRequestId)
                .then(res => {
                    this.reviews = res.data;
                    for (let review of this.reviews) {

                        // Add developer for review
                        DeveloperService.getDeveloperBasicInfoFromId(review.reviewer_id)
                            .then(res => {
                                review['reviewer'] = res.data;

                                // Getting Developer avatar
                                DeveloperService.getUserAvatar(review.reviewer.username)
                                    .then(res => {
                                        // console.log(res);
                                        review.reviewer['avatar'] = res.data
                                    })
                                    .catch(err => {
                                        console.log(err);
                                    });
                            })
                            .catch(err => {
                                console.log(err);
                            });
                    }
                })
                .catch(err => {
                    console.log(err);
                });
        },

        formatNameAndSurname(reviewer) {
            return reviewer?.first_name + " " + reviewer?.last_name;
        },

        formatDate(date) {
            dayjs.extend(utc);
            // Parse the given date string using Day.js, considering it as UTC time
            const parsedDate = dayjs.utc(date);

            // Format the parsed date into the desired format
            return parsedDate.format('DD.MM.YYYY. HH:mm');
        },

    }
}
</script>
<style scoped>
.bright {
    color: #adbbc8;
}

#reviews {
    background-color: #22272d;
    margin-top: 20px;
}

.review {
    background-color: #444;
    border-radius: 5px;
    border: 2px solid #adbbc8;
    padding: 10px;
    margin-bottom: 15px;
}

.review-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 5px;
}

.reviews {
    color: #adbbc8;
    font-weight: bold;
    margin: 0;
    font-size: 35px;
}

.review-author {
    color: #adbbc8;
    font-weight: bold;
    margin: 0;
    flex-grow: 1;
    margin-left: 10px;
}

.review-timestamp {
    color: #aaa;
    font-size: 0.9em;
}

.review-body {
    color: #adbbc8;
    margin-bottom: 10px;
    margin-top: 15px;
    margin-left: 33px;
}

.review-actions {
    display: flex;
    justify-content: flex-end;
    /* margin-top: 25px; */
    margin-right: 5px;
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

.profile-image-container {
    display: flex;
    align-items: center;
    justify-content: center;
}

.profile-picture-main {
  width: 25px;
  height: 25px;
  border-radius: 50%; /* This makes the image circular */
  object-fit: cover; /* This ensures the image covers the entire 25x25 area */
}
</style>
