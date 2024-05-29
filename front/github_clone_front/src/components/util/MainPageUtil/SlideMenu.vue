<template>
  <div class="slide-menu" :class="{ 'slide-in': isOpen }">
    <img alt="Logo" src="../../../.. /../assets/logo_dark.png" class="logo-image-main">
    <a href="/main"><i class="bi bi-house-door"></i>&nbsp;&nbsp;Home</a>
    <a href="/view/users_issues"><i class="bi bi-record-circle"></i>&nbsp;&nbsp;Issues</a>
    <a href="/view/pulls"><i class="bi bi-bezier2"></i>&nbsp;&nbsp;Pull reques</a>
    <label id="id-repo-label">Repositories</label>
    <div class="repositories">
      <a v-for="(repo, index) in repos" :key="index" :href="'/view/' + repo.repos_owner + '/' + repo.name">
        <img :src="repo.repos_owner_avatar" alt="Current Avatar" class="profile-picture-main" />&nbsp;&nbsp;{{ repo.repos_owner }}/{{ repo.name }}
      </a>
    </div>
  </div>
</template>

<script>
import RepositoryService from '@/services/RepositoryService';
export default {
  props: {
    isOpen: Boolean,
  },
  mounted() {
    RepositoryService.getAllUserWorkingOnRepos(localStorage.getItem("username"))
          .then(res => {
              // console.log(res);
              this.repos = res.data
          })
          .catch(err => {
              console.log(err);
          });
  },
  data() {
    return {
      currentAvatar: '',
      username: localStorage.getItem("username"),
      repos: []
    };
  }
};
</script>

<style scoped>
.profile-picture-main{
  max-height: 1rem;
  max-width: 100%;
  border-radius: 25px;
}

.repositories{
  display: flex;
  flex-direction: column;
}

#id-repo-label{
  margin-top: 10px;
  font-size: 10px;
}

.logo-image-main {
  max-height: 1.5rem;
  max-width: 1.5rem;
  margin-bottom: 1rem;
}

.slide-menu {
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: -250px;
  height: 100%;
  width: 250px;
  background-color: #333;
  padding: 20px;
  transition: left 0.4s ease-in-out;
  z-index: 100;
  border-radius: 10px;
}

.slide-menu a {
  color: #fff;
  padding: 5px;
  text-decoration: none;
  font-size: 10px;
}

.slide-menu a:hover {
  background: #515050;
}

.slide-in {
  left: 0;
}
</style>
