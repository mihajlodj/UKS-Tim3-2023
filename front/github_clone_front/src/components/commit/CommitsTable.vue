<template>
    <div>
        <div class="w-100 num-commits py-2 px-3">
            <h5 v-if="commits" class="bright">{{ commits.length }} commit(s) </h5>
        </div>
        <table>
            <thead>
                <tr>
                    <th scope="col" class="author">Author</th>
                    <th scope="col">SHA1</th>
                    <th scope="col">Message</th>
                    <th scope="col" class="date d-flex justify-content-end">Date</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="c in commits" :key="c.hash">
                    <td>
                        <div class="d-flex justify-content-start">
                            <img class="avatar me-1" :src="c.author.avatar" />
                            <label class="bright">{{ c.author.username }}</label>
                        </div>
                    </td>
                    <td>
                        <div class="d-flex justify-content-start">
                            <button type="button" class="btn-copy" @click="copySha(c.hash)">
                                <font-awesome-icon icon="fa-regular fa-copy"></font-awesome-icon>
                            </button>
                            <button type="button" class="btn-sha">
                                <label class="bright">{{ c.hash.slice(0, 7) }}</label>
                            </button>
                        </div>
                    </td>
                    <td>
                        <label>{{ c.message }}</label>
                    </td>
                    <td class="date">
                        <label>{{ c.timestamp }}</label>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import { toast } from 'vue3-toastify';

export default {
    name: "CommitsTable",
    props: ['commits'],
    data() {
        return {

        }
    },

    methods: {
        async copySha(sha) {
            try {
                await navigator.clipboard.writeText(sha);
                toast("Copied to clipboard", {
                    autoClose: 500,
                    type: 'info',
                    position: toast.POSITION.BOTTOM_RIGHT,
                    theme: toast.THEME.DARK
                });
            } catch ($e) {
                console.log('cannot copy')
            }
        }
    }
}

</script>

<style scoped>
div {
    color: white;
}

.bright {
    color: #adbbc8;
}

.muted {
    color: #768491;
}

.num-commits {
    background-color: #2c333b;
    border-top-right-radius: 7px;
    border-top-left-radius: 7px;
    border: 1px solid #6e7b88;
}

.date {
    width: 100px;
}

.avatar {
    width: 25px;
    height: 25px;
    border-radius: 50%;
}

th,
td {
    background-color: #1c2127;
    color: #adbbc8;
    font-weight: 600;
    border: 1px solid #6e7b88;
    padding: 5px 7px;
}

.btn-sha {
    border-top-right-radius: 5px;
    border-bottom-right-radius: 5px;
    background-color: #373e48;
    border: 1px solid #6e7b88;
}

.btn-copy {
    border-top-left-radius: 5px;
    border-bottom-left-radius: 5px;
    background-color: #373e48;
    border: 1px solid #6e7b88;
}

.fa-copy {
    color: #adbbc8;
}

.btn-sha label:hover {
    cursor: pointer;
}
</style>