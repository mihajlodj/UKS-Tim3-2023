<template>
    <div>
        <div v-for="notif in notifications" :key="notif.id">
            <NotificationDisplay :id="notif.id" :isRead="notif.is_read" :message="notif.message" :timestamp="notif.timestamp"/>
        </div>
    </div>
</template>

<script>
import NotificationService from "@/services/NotificationService"
import NotificationDisplay from "./NotificationDisplay.vue"

export default {
    name: "NotificationsList",
    components: {
        NotificationDisplay
    },
    data() {
        return {
            notifications: []
        }
    },
    mounted() {
        NotificationService.get().then(res => {
            this.notifications = res.data;
        }).catch(err => {
            console.log(err);
        });
    }
}
</script>

<style scoped>
</style>