<template>
    <div class="w-100 contain d-flex justify-content-center">
        <div class="message d-flex justify-content-between" @mouseover="markAsRead">
            <div>
                <font-awesome-icon v-if="!isRead" icon="fa-solid fa-circle"></font-awesome-icon>
                <h4>{{ message }}</h4>
            </div>
            
            <h6>{{ timestamp }}</h6>
        </div>
    </div>
</template>

<script>
import NotificationService from "@/services/NotificationService"

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
            if (this.isReadModifiable) {
                NotificationService.markAsRead(this.id).then(res => {
                    console.log(res);
                    this.isReadModifiable = false;
                }).catch(err => {
                    console.log(err);
                });
            }
        }
    }
}
</script>

<style scoped>
.message {
    width: 60%;
}
</style>