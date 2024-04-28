<template>
  <div class="main">
    <div>
      <label style="color:white; padding:1rem;font-size:0.8rem">Starred repositories</label>
    </div>
    <repository-container v-for="(repo, index) in repos" :key="index" :projectName="repo.name" :isPrivate="repo.access_modifier" />
  </div>
</template>

<script>
import RepositoryContainer from './RepositoryContainer.vue';
import RepositoryService from '@/services/RepositoryService';

export default {
  name: 'ProfilePageStars',
  components: {
    RepositoryContainer,
  },
  mounted() {
    RepositoryService.getAllStaredUserRepos(localStorage.getItem("username"))
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
