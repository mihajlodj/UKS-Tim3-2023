<template>
  <div class="entire-page">
    <nav-bar :user="user" />
    <profile-nav-bar-extension starting="overview" @activeLinkExtension="handleActiveLinkExtension"/>
    <div class="main-content">
      <div class="left-side">
        <div id="avatar-id">
          <a href="/profile/settings">
            <img :src="currentAvatar" alt="Current Avatar" class="profile-picture-main" />
          </a>
          <span class="tooltiptext">Change your avatar</span>
        </div>
        <div>
          <label v-if="!editing" id="profile_name">{{ this.username }}</label>
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
        <profile-page-over-view v-if="activeLinkExtension==='overview'" :username ="username" />
        <profile-page-repositories v-if="activeLinkExtension==='repositories'" :username ="username" />
        <profile-page-stars v-if="activeLinkExtension==='stars'"/>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../util/MainPageUtil/Nav-bar.vue';
import ProfileNavBarExtension from '../profile/ProfileNavBarExtension.vue';
import ProfilePageOverView from '../profile/ProfilePageOverView.vue';
import ProfilePageStars from '../profile/ProfilePageStars.vue';
import ProfilePageRepositories from '../profile/ProfilePageRepositories.vue';
import DeveloperService from '@/services/DeveloperService';
import { toast } from 'vue3-toastify';

export default {
  components: {
    NavBar,
    ProfileNavBarExtension,
    ProfilePageOverView,
    ProfilePageStars,
    ProfilePageRepositories
  },
  mounted() {
    DeveloperService.getUserAvatar(localStorage.getItem("username"))
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
      editing: false,
      activeLinkExtension: 'overview',
      username: localStorage.getItem("username"),
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
    startEditing() {
      this.editing = true;
      this.newProfileName = this.username;
    },
    saveChanges() {
      DeveloperService.update({ "username": this.newProfileName }, this.username).then(res => {
                console.log(res.data);
                this.username = this.newProfileName;
                localStorage.setItem("username", this.newProfileName);
                this.editing = false;
                toast("Changes saved!", {
                    autoClose: 500,
                    type: 'success',
                    position: toast.POSITION.BOTTOM_RIGHT
                });
            }).catch(err => {
                console.log(err);
            });

    },
    cancelEditing() {
      this.editing = false;
    },
    handleActiveLinkExtension(name) {
      this.activeLinkExtension = name;
    },
  },
};
</script>

<style scoped>
.cancel-btn-div{
  display: flex;
  float: left;
  padding: 0.5rem;
}

.save-btn-div{
  display: flex;
  float: left;
  padding: 0.5rem;
}

#new-profile-name {
  color: white;
  padding: 0.5rem;
  background: rgb(60, 60, 60);
  border: 1px solid gray;
  border-radius: 0.5rem;
  width: 100%;
  box-sizing: border-box;
}

.save-btn{
  margin-top: 0.5rem;
  float: left;
  background: rgb(6, 160, 6);
  border: 1px solid gray;
  color: rgb(212, 212, 212);
  font-size: 0.8rem;
  width: 100%;
  border-radius: 0.5rem;
}

.save-btn:hover{
  background: rgba(5, 199, 5, 0.778);
}


.cancel-btn {
  margin-top: 0.5rem;
  float: left;
  border: 1px solid gray;
  color: rgb(212, 212, 212);
  font-size: 0.8rem;
  width: 100%;
  border-radius: 0.5rem;
  background: rgb(71, 71, 71);
}

.cancel-btn:hover {
  background: rgba(153, 153, 153, 0.584);
}

#edit-button-div{
    display: flex;
    justify-content: center;
}

.edit_btn{
    background: rgb(71, 71, 71);
    border: 1px solid gray;
    color: rgb(212, 212, 212);
    font-size: 0.8rem;
    width: 100%;
    border-radius: 0.5rem;
}

.edit_btn:hover{
    background: rgb(91, 91, 91);
}

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

#avatar-id:hover .tooltiptext {
  visibility: visible;
}

#avatar-id .tooltiptext {
  display: flex;
  flex-direction: column;
  justify-content: center;
  height: auto;
  border-radius: 5rem;
  padding-inline-end: 0.5rem;
  padding-inline-start: 0.5rem;
  margin-top: -1.5rem;
  visibility: hidden;
  background: gray;
  color: rgb(214, 214, 214);
  font-size: 0.8rem;
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
