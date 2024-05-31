<template>
  <div class="main">
    <repository-container v-for="(repo, index) in popularRepositories" :key="index" :projectName="repo.name" :username="username" :isPrivate="repo.access_modifier" />
  </div>
</template>

<script>
import RepositoryContainer from './RepositoryContainer.vue';
import RepositoryService from '@/services/RepositoryService';

export default {
  props: {
    username: String
  },
  name: 'ProfilePageRepositories',
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
      return this.repos;
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
