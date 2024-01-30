<template>
  <div class="entire-page">
    <nav-bar :user="user" />
    <div class="main-content">
      <div class="left-side">
        <div id="avatar-id">
          <a href="#">
            <img src="../../assets/git_profile_picture.png" alt="User Avatar" class="profile-picture-main" />
          </a>
        </div>
        <div>
          <label v-if="!editing" id="profile_name">{{ profileName }}</label>
          <input v-else v-model="newProfileName" type="text" id="new-profile-name" />
        </div>
        <div id="edit-button-div">
          <button v-if="!editing" @click="startEditing" type="button" class="edit_btn">Edit profile</button>
          <div v-if="editing">
            <div class="save-btn-div">
              <button @click="saveChanges" type="button" class="save-btn">Save</button>
            </div>
            <div class="cancel-btn-div">
              <button @click="cancelEditing" type="button" class="cancel-btn">Cancel</button>
            </div>
          </div>
        </div>
      </div>
      <div class="right-side">
        <profile-page-over-view v-if="activeLinkExtension==='overview'"/>
      </div>
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
      editing: false,
      activeLinkExtension: 'overview',
      profileName: 'SimicAleksa',
      newProfileName: '',
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
  methods: {
   
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
    display: flex;
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
