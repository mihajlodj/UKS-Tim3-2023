<template>
  <div class="slide-profile-menu" :class="{ 'slide-in': isProfileOpen }">
    <div class="basic-info">
      <img :src="currentAvatar" alt="Current Avatar" class="profile-picture-main" />
      &nbsp;
      <label>{{this.username}}</label>
    </div>
    <a href="#"><i class="bi bi-emoji-smile"></i>&nbsp;&nbsp;Set status</a>
    <a href="/profile"><i class="bi bi-person"></i>&nbsp;&nbsp;Your profile</a>
    <a href="#"><i class="bi bi-person-plus"></i>&nbsp;&nbsp;Add account</a>
    <a href="#"><i class="bi bi-journal-bookmark"></i>&nbsp;&nbsp;Your repositories</a>
    <a href="#"><i class="bi bi-file-bar-graph"></i>&nbsp;&nbsp;Your projects</a>
    <a href="#"><i class="bi bi-buildings"></i>&nbsp;&nbsp;Your organizations</a>
    <a href="#"><i class="bi bi-globe"></i>&nbsp;&nbsp;Your enterprises</a>
    <a href="#"><i class="bi bi-star"></i>&nbsp;&nbsp;Your stars</a>
    <a href="#"><i class="bi bi-heart"></i>&nbsp;&nbsp;Your sponsors</a>
    <a href="#"><i class="bi bi-file-code"></i>&nbsp;&nbsp;Your gits</a>
    <a href="#"><i class="bi bi-upload"></i>&nbsp;&nbsp;Upgrade</a>
    <a href="#"><i class="bi bi-globe2"></i>&nbsp;&nbsp;Try Enterprise</a>
    <a href="#"><i class="bi bi-robot"></i>&nbsp;&nbsp;Copilot</a>
    <a href="#"><font-awesome-icon icon="fa-solid fa-flask"/>&nbsp;&nbsp;Feature preview</a>
    <a href="#"><i class="bi bi-gear"></i>&nbsp;&nbsp;Settings</a>
    <a href="#"><i class="bi bi-book"></i>&nbsp;&nbsp;GitHub Docs</a>
    <a href="#"><i class="bi bi-people"></i>&nbsp;&nbsp;GitHub Support</a>
    <a href="#" @click="this.logout()">Sign out</a>
  </div>
</template>

<script>
import DeveloperService from '@/services/DeveloperService';
import AuthService from '@/services/AuthService';
import { toast } from 'vue3-toastify';

export default {
  props: {
    isProfileOpen: Boolean,
  },
  mounted() {
    DeveloperService.getUserAvatar(localStorage.getItem("username"))
          .then(res => {
              // console.log(res);
              this.currentAvatar = res.data
          })
          .catch(err => {
              console.log(err);
          });
  },
  data() {
    return {
      currentAvatar: '',
      username: localStorage.getItem("username"),
    };
  },
  methods: {
    logout() {
      /* eslint-disable */
      AuthService.logout({
        "refresh": localStorage.getItem("refresh_token"),
      }).then(result => {
        console.log("Logged out");
        this.deleteTokens();
        this.redirectToLogin();
      }).catch(_err => {
        toast("Error occured!", {
              autoClose: 1000,
              type: 'error',
              position: toast.POSITION.BOTTOM_RIGHT
        });
      })
    },
    deleteTokens() {
      localStorage.clear()
    },
    redirectToLogin() {
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.profile-picture-main{
  max-height: 1.6rem;
  max-width: 100%;
  border-radius: 25px;
}

.basic-info{
  padding-bottom: 0.5rem;
  padding-top: 0.5rem;
}

.slide-profile-menu {
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  right: -250px;
  height: 100%;
  width: 250px;
  background-color: #333;
  border-radius: 10px;
  padding-inline-start: 1rem;
  transition: left 0.4s ease-in-out;
  z-index: 100;
}

.slide-profile-menu a {
  padding-inline-start: 0.5rem;
  padding-top: 0.1rem;
  width: 90%;
  color: #fff;
  text-decoration: none;
  font-size: 10px;
  margin-bottom: 10px;
}

.slide-profile-menu a:hover{
  background: #515050;
  border-radius: 1rem;
}

.slide-in {
  right: 0;
}

.profile-picture-main{
  max-height: 1.6rem;
  max-width: 100%;
  border-radius: 25px;
}
</style>
