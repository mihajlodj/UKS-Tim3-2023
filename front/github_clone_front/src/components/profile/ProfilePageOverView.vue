<template>
  <div class="main">
    <div>
      <label style="color:white; padding:1rem;font-size:0.8rem">Popular repositories</label>
    </div>
    <repository-container v-for="(repo, index) in popularRepositories" :key="index" :projectName="repo.name" :isPrivate="repo.isPrivate" />
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
      dummyRepos: [
        { name: 'Uks-Project', isPrivate: true },
        { name: 'pythonProject', isPrivate: false },
        { name: 'WebApp-Instagram-MyNewApplication', isPrivate: true },
        { name: 'Uks-Project', isPrivate: true },
        { name: 'pythonProject', isPrivate: false },
        { name: 'WebApp-Instagram-MyNewApplication', isPrivate: true },
        { name: 'Uks-Project', isPrivate: true },
        { name: 'pythonProject', isPrivate: false },
        { name: 'WebApp-Instagram-MyNewApplication', isPrivate: true },
        { name: 'Uks-Project', isPrivate: true },
        { name: 'pythonProject', isPrivate: false },
        { name: 'WebApp-Instagram-MyNewApplication', isPrivate: true },
      ],
    };
  },
  computed: {
    popularRepositories() {
      return this.dummyRepos.slice(-6);
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
