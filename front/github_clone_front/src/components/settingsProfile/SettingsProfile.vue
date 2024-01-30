<template>
  <div class="entire-page">
    <nav-bar :user="user" />
    <div class="main-content">
      <div class="left-side">
        <div id="avatar-id">
          <img src="../../assets/git_profile_picture.png" alt="User Avatar" class="profile-picture-main" />
        </div>
        <div id="profile-info-id">
          <a href="#" id="profile_name">{{ profileName }}</a>
          <label id="personal-acc">Your personal account</label>
        </div>
      </div>
      <div class="right-side"></div>
    </div>
  </div>
</template>

<script>
import NavBar from '../util/MainPageUtil/Nav-bar.vue';

export default {
  components: {
    NavBar,
  },
  data() {
    return {
      profileName: 'SimicAleksa',
      user: {
        login: "your_username",
        avatar_url: "url_to_your_avatar",
        bio: "Your bio goes here",
      },
    };
  },
  methods: {},
};
</script>

<style scoped>
#profile-info-id {
  padding-top: 0.3rem;
  float: left;
  display: flex;
  flex-direction: column; 
  align-items: flex-start;
}

#personal-acc {
  font-size: 0.7rem;
  color: rgb(18, 18, 18);
  padding-inline-start: 0.5rem;
  margin-top: -0.2rem;
}

#profile_name {
  color: white;
  padding-top: 0.3rem;
  padding-inline-start: 0.5rem;
  font-size: 0.9rem;
  display: block;
  text-decoration: none;
  color: rgb(255, 255, 255);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 9.5rem;
}

#profile_name:hover {
  text-decoration: underline;
}

#avatar-id {
  width: auto;
  justify-content: left;
  float: left;
  display: flex;
}

.profile-picture-main {
  max-height: 3.5rem;
  max-width: 100%;
  border-radius: 5rem;
  padding: 0.5rem;
}

.left-side {
  width: 30%;
  float: left;
  height: auto;
  background: rgb(79, 78, 78);
}

.right-side {
  width: 70%;
  float: left;
  height: auto;
  background: rgb(60, 60, 60);
}

.entire-page {
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
