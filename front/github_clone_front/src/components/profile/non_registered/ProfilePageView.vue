<template>
  <div class="entire-page">
    <nav-bar :user="user" />
    <profile-nav-bar-extension starting="overview" @activeLinkExtension="handleActiveLinkExtension"/>
    <div class="main-content">
      <div class="left-side">
        <div id="avatar-id">
            <img :src="currentAvatar" alt="Current Avatar" class="profile-picture-main" />
        </div>
        <div>
          <label v-if="!editing" id="profile_name">{{ this.username }}</label>
        </div>
      </div>
      <div class="right-side">
        <profile-page-over-view-view v-if="activeLinkExtension==='overview'" :username ="username"/>
        <profile-page-repositories-view v-if="activeLinkExtension==='repositories'" :username ="username"/>
        <profile-page-stars-view v-if="activeLinkExtension==='stars'" :username ="username"/>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../../util/MainPageUtil/Nav-bar.vue';
import ProfileNavBarExtension from '../ProfileNavBarExtension.vue';
import ProfilePageOverViewView from './ProfilePageOverViewView.vue';
import ProfilePageRepositoriesView from './ProfilePageRepositoriesView.vue';
import ProfilePageStarsView from './ProfilePageStarsView.vue';
import DeveloperService from '@/services/DeveloperService';

export default {
  components: {
    NavBar,
    ProfileNavBarExtension,
    ProfilePageOverViewView,
    ProfilePageStarsView,
    ProfilePageRepositoriesView
  },
  mounted() {
    DeveloperService.getUserAvatar(this.$route.params.username)
          .then(res => {
              console.log(res);
              this.currentAvatar = res.data
          })
          .catch(err => {
              console.log(err);
          });
  },
  data() {
    return {
      currentAvatar: '',
      activeLinkExtension: 'overview',
      username: this.$route.params.username,
      user: {
        login: "your_username",
        avatar_url: "url_to_your_avatar",
        bio: "Your bio goes here",
      },
      repositories: [],
    };
  },
  methods: {
    handleActiveLinkExtension(name) {
      this.activeLinkExtension = name;
      console.log(localStorage.getItem("username"));
    },
  },
};
</script>

<style scoped>

#profile_name{
    color: white;
    padding: 0.5rem;
}

#avatar-id{
    width: auto;
    justify-content: center;
    align-items: center;
    display: flex;
    flex-direction: column;
}

.profile-picture-main{
  max-height: 10rem;
  max-width: 100%;
  border-radius: 5rem;
  padding: 0.5rem;
}

.left-side {
  width: 30%;
  float: left;
  height: auto;
  background: rgb(79, 78, 78);
  flex-direction: column;
  margin-top: 0px;
  display: flex;
}

.right-side {
  width: 70%;
  float: left;
  height: auto;
  background: rgb(60, 60, 60);
}

.entire-page{
  min-height: 100vh;
  margin: 0px;
  padding: 0;
  background: #24292e;
}

.main-content {
  display: flex; 
  overflow: auto;
  padding: 0;
  margin-inline-end: 10rem;
  margin-inline-start: 10rem;
  height: auto;
  min-height: 92.5vh;
}
</style>

