<template>
  <div>
    <NavBar :user="user" />
    <div class="main-content">
      <div class="left-section">
        <RepositoryList :repositories="repositories" />
      </div>
      <div class="middle-section">
        
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../util/MainPageUtil/Nav-bar.vue';
import RepositoryList from '../util/MainPageUtil/RepositoryList.vue';

export default {
  components: {
    NavBar,
    RepositoryList
  },
  data() {
    return {
      user: {
        login: "your_username",
        avatar_url: "url_to_your_avatar",
        bio: "Your bio goes here",
      },
      repositories: [
        { id: 1, name: "repo1" },
        { id: 2, name: "repo2" },
      ],
    };
  },
};
</script>

<style scoped>
.main-content {
  display: flex;
  margin: 20px;
}

.left-section {
  flex: 1;
}

.middle-section {
  flex: 4;
  background-color: #f0f0f0;
  padding: 20px;
  border-radius: 8px;
  margin-left: 20px;
}
</style>
