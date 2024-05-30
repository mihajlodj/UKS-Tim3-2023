<template>
  <div class="entire-page">
    <nav-bar :user="user" />
    <div class="main-content">
      <div class="left-section">
        <repository-list :repositories="repositories" />
      </div>
      <div class="middle-section fill">
        <router-view name="middle_section"></router-view>
        <img alt="Logo" src="../../assets/github_lie_2.png" style="width: 800px;" class="mt-2 ms-2">
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../util/MainPageUtil/Nav-bar.vue';
import RepositoryList from '../util/MainPageUtil/RepositoryList.vue';
import RepositoryService from '@/services/RepositoryService';
import DeveloperService from '@/services/DeveloperService';

export default {
  components: {
    NavBar,
    RepositoryList
  },
  mounted() {
    console.log(localStorage.getItem('username'));
    RepositoryService.getAllUserWorkingOnRepos(localStorage.getItem('username')).then((res) => {
      console.log(res.data);
      this.repositories = res.data;
    });

    DeveloperService.getRoles(localStorage.getItem('username')).then(res => {
      const roles = res.data;
      for (const roleObj of roles) {
        const repoName = roleObj['repository'];
        const roleName = roleObj['role']
        localStorage.setItem(repoName, roleName);
      }
    }).catch(err => {
      console.log(err);
    });
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
      ]
    };
  },
};
</script>

<style scoped>
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
  margin: 0;
  height: 100%;
  min-height: 92.5vh;
}

.left-section {
  flex: 1;
}

.fill {
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}
.fill img {
  flex-shrink: 0;
  min-width: 100%;
  min-height: 100%;
}

.middle-section {
  flex: 4;
  border-top: 1px solid #929191;
  background-color: #1c2127;
  padding: 20px;
}
</style>
