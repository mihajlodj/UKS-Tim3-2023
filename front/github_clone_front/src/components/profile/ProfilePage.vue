<template>
  <div class="entire-page">
    <nav-bar :user="user" />
    <profile-nav-bar-extension starting="code"/>
    <div class="main-content">
      <profile-page-over-view/>
    </div>
  </div>
</template>

<script>
import NavBar from '../util/MainPageUtil/Nav-bar.vue';
import ProfileNavBarExtension from '../profile/ProfileNavBarExtension.vue';
import ProfilePageOverView from '../profile/ProfilePageOverView.vue';

export default {
  components: {
    NavBar,
    ProfileNavBarExtension,
    ProfilePageOverView
  },
  data() {
    return {
      user: {
        login: "your_username",
        avatar_url: "url_to_your_avatar",
        bio: "Your bio goes here",
      },
      repositories: [
        { id: 1, name: "SimicAleksa/NvtKts" },
        { id: 2, name: "SimicAleksa/pythonProject" },
      ],
    };
  },
};
</script>

<style scoped>
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
  margin: 0;
  height: 100%;
  min-height: 92.5vh;
}
</style>
