<template>
  <div class="main">
    <label class="github-label">
      Control how your profile is shown to other users. Your primary email address will be used for notifications, password recovery, and web-based Git operations.
    </label>

    <div class="form-group">
      <label for="username">Username:</label>
      <input type="text" id="username" v-model="username" placeholder="Enter your username" />
    </div>

    <div class="form-group">
      <label for="fullName">Full Name:</label>
      <input type="text" id="fullName" v-model="fullName" placeholder="Enter your full name" />
    </div>

    <div class="form-group">
      <label for="email">Email Address:</label>
      <input type="email" id="email" v-model="email" placeholder="Enter your email address" />
    </div>

    <div class="form-group">
      <label for="bio">Biography:</label>
      <textarea id="bio" v-model="biography" placeholder="Write a short bio"></textarea>
    </div>

    <div class="form-group">
      <div class="user-visib">
        <label for="visibility">User Visibility:</label>
        <select id="visibility" v-model="visibility">
          <option value="public">Public</option>
          <option value="private">Private</option>
          <option value="limited">Limited</option>
        </select>
      </div>
      <div class="update-profile-class">
        <button class="github-button" @click="updateProfile">Update Profile</button>
      </div>
      <br>
      <hr id="hr-line">
    </div>

    <div class="avatar-section">
      <div class="updating-avatar-part">
        <label for="avatar" class="github-label">Profile Picture:</label>
        <input type="file" id="avatar" @change="selectAvatar" accept="image/*" />
        <button class="github-button" @click="updateAvatar">Update Avatar</button>
        <button class="github-button-delete" @click="deleteAvatar">Delete Avatar</button>
      </div>
      <div class="current-avatar">
        <label class="github-label">Current Avatar:</label>
        <img :src="currentAvatar" alt="Current Avatar" class="profile-picture-main" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: 'SimicAleksa',
      fullName: '',
      email: 'simicmail@gmail.com',
      biography: '',
      visibility: 'public',
      currentAvatar: require("E:/Desktop/UKS_projekat/UKS-Tim3-2023/front/github_clone_front/src/assets/git_profile_picture.png"),
      selectedImage: null,
    };
  },
  methods: {
    updateProfile() {
      
    },
    selectAvatar(event) {
      this.selectedImage = event.target.files[0];
    },
    updateAvatar() {
      if (this.selectedImage) {
        
        const reader = new FileReader();
        reader.onload = () => {
          this.currentAvatar = reader.result;
        };
        reader.readAsDataURL(this.selectedImage);
      }
    },
    deleteAvatar() {
      
    },
  },
};
</script>

<style scoped>
.updating-avatar-part{
  float: left;
}

.updating-avatar-part input{
  color: white;
}

.updating-avatar-part .github-button{
  margin-inline-end: 1rem;
  margin-bottom: 1rem;
}

.updating-avatar-part .github-button-delete{
  margin-inline-end: 1rem;
  margin-bottom: 1rem;
}

.updating-avatar-part input, textarea, select {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  margin-bottom: 10px;
  box-sizing: border-box;
}

.profile-picture-main{
  max-height: 6rem;
  max-width: 100%;
  padding: 0.5rem;
}

.main {
  width: 60%;
  margin: auto;
}

.main .github-label{
  margin-top: 1rem;
}

.update-profile-class{
  width: auto;
  display: flex;
  justify-content: right;
}

#hr-line{
  border-color: white;
  border-width: 2px;
}

.user-visib label{
  width: 15rem;
}

.user-visib{
  width: 30%;
  display: flex;
  padding-inline-end: 1rem;
  align-items: center;
  float: left;
}

.github-label {
  font-size: 14px;
  color: #9fa9b5;
  margin-bottom: 10px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label{
  color: white;
}

.form-group input, textarea, select {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  margin-bottom: 10px;
  box-sizing: border-box;
}

.github-button {
  background-color: #2ea44f;
  color: #ffffff;
  border: none;
  padding: 10px;
  cursor: pointer;
}

.github-button:hover {
  background-color: #22863a;
}

.github-button-delete {
  background-color: #a4362e;
  color: #ffffff;
  border: none;
  padding: 10px;
  cursor: pointer;
}

.github-button-delete:hover {
  background-color: #863122;
}

.avatar-section {
  margin-top: 2rem;
}

.current-avatar img {
  max-width: 200px;
  margin-top: 10px;
  border-radius: 5px;
  float: left;
}
</style>
