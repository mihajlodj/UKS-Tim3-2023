<template>
  <div class="main">
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
      <div>
        <label style="color:white; padding:1rem;font-size:0.8rem">Popular repositories</label>
      </div>
      <repository-container />
      <repository-container />
      <repository-container />
      <repository-container />
      <repository-container />
    </div>
  </div>
</template>

<script>
import RepositoryContainer from '../profile/RepositoryContainer.vue';

export default {
  name: 'ProfilePageOverView',
  components: {
    RepositoryContainer,
  },
  data() {
    return {
      editing: false,
      profileName: 'SimicAleksa',
      newProfileName: '',
    };
  },
  methods: {
    startEditing() {
      this.editing = true;
      this.newProfileName = this.profileName;
    },
    saveChanges() {
      this.profileName = this.newProfileName;
      this.editing = false;
    },
    cancelEditing() {
      this.editing = false;
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

.links:hover{
 background: rgba(132, 132, 132, 0.623);
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
  height: 95%;
  background: rgb(79, 78, 78);
}

.right-side {
  width: 70%;
  float: left;
  height: 95%;
  background: rgb(60, 60, 60);
}

.main {
  margin-inline-start: 10rem;
  margin-inline-end: 10rem;
  width: 100%;
  background: red;
}
</style>
