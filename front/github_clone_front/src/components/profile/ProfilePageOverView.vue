<template>
  <div class="main">
    <div>
      <label style="color:white; padding:1rem;font-size:0.8rem">Popular repositories</label>
    </div>
    <repository-container v-for="(repo, index) in popularRepositories" :key="index" :projectName="repo.name" :username="username" :isPrivate="repo.access_modifier" />
  </div>
</template>

<script>
import RepositoryContainer from '../profile/RepositoryContainer.vue';
import RepositoryService from '@/services/RepositoryService';

export default {
  props: {
    username: String
  },
  name: 'ProfilePageOverView',
  components: {
    RepositoryContainer,
  },
  mounted() {
    RepositoryService.getAllUserRepos(localStorage.getItem("username"))
          .then(res => {
              console.log(res);
              this.repos = res.data
          })
          .catch(err => {
              console.log(err);
          });
  },
  data() {
    return {
      repos: '',
    };
  },
  computed: {
    popularRepositories() {
      return this.repos.slice(-6);
    },
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
.main {
  float: left;
  width: 100%;
  height: auto;
  background: rgb(60, 60, 60);
}
</style>
