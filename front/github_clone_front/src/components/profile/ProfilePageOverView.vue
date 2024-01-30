<template>
  <div class="main">
    <div class="left-side">
        <div id="avatar-id">
            <a href="#" >
                <img src="../../assets/git_profile_picture.png" alt="User Avatar" class="profile-picture-main"/>
            </a>
        </div>
        <div>
            <label id="profile_name">SimicAleksa</label>
        </div>
        <div id="edit-button-div">
            <button type="button" class="edit_btn">Edit profile</button>
        </div>
    </div>
    <div class="right-side">
        <div>
            <label style="color:white; padding:1rem;font-size:0.8rem">Popular repositories</label>
        </div>
        <repository-container/>
        <repository-container/>
        <repository-container/>
        <repository-container/>
        <repository-container/>
    </div>
  </div>
</template>

<script>
import RepositoryContainer from '../profile/RepositoryContainer.vue';

export default {
  name: 'ProfilePageOverView',
  components: {
    RepositoryContainer
  },
}
</script>

<style scoped>
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
