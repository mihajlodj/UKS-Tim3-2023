<template>
    <div class="w-100 contain d-flex justify-content-center my-2">
        <div class="message d-flex justify-content-between" @mouseover="markAsRead">
            <div class="h-100 d-flex align-items-center">
                <font-awesome-icon v-if="!isReadModifiable" icon="fa-solid fa-circle" class="ms-3"></font-awesome-icon>
                <div v-else class="fill"></div>
                <h4 class="bright ms-3">{{ message }}</h4>
            </div>
            
            <h6 class="muted mt-2 me-2">{{ howLongAgo() }}</h6>
        </div>
    </div>
</template>

<script>
import NotificationService from "@/services/NotificationService"
import TimestampService from "@/services/TimestampService";

export default {
    name: "NotificationDisplay",
    props: ["message", "timestamp", "isRead", "id"],

    mounted() {
        this.isReadModifiable = this.isRead;
    },

    data() {
        return {
            isReadModifiable: false
        }
    },

    methods: {
        markAsRead() {
            if (!this.isReadModifiable) {
                NotificationService.markAsRead(this.id).then(res => {
                    console.log(res);
                    this.isReadModifiable = true;
                }).catch(err => {
                    console.log(err);
                });
            }
        },

        howLongAgo() {
            return TimestampService.howLongAgo(this.timestamp);
        }
    }
}
</script>

<style scoped>
.message {
    width: 100%;
    min-height: 120px;
    border: 1px solid #8a98a1;
    border-radius: 10px;
}
.bright {
    color: #c5d1df;
}
.muted {
    color: #8a98a1;
}
.fa-circle {
    height: 15px;
    color: #488be6;
}
.message:hover {
    border: 2px solid #b5b8bb;
    transform: scale(1.02);
}
.fill {
    width: 31px;
}
</style>