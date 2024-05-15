<template>
    <div class="bg min-vh-100 is-fullheight">
        <NavBar />

        <hr class="bright" />

        <div class="d-flex justify-content-center">
            <div class="contain">
                <h3 class="bright mt-3 mb-4">Notifications</h3>

                <div v-for="notif in notifications" :key="notif.id">
                    <NotificationDisplay :id="notif.id" :isRead="notif.is_read" :message="notif.message" :timestamp="notif.timestamp"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import NotificationService from "@/services/NotificationService"
import NotificationDisplay from "./NotificationDisplay.vue"
import NavBar from "../util/MainPageUtil/Nav-bar.vue"

export default {
    name: "NotificationsList",
    components: {
        NotificationDisplay,
        NavBar
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

.bg {
    background-color: #22272d; 
}
.bright {
    color: #c5d1df;
}
.contain {
    width: 70%;
    max-width: 1500px;
}
hr {
    margin: 0;
}

</style>