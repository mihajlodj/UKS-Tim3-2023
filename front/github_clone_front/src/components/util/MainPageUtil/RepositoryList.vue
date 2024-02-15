<template>
  <div class="repository-list">
    <label id="profile-name"><img :src="currentAvatar" alt="Current Avatar" class="profile-picture-main" /> {{this.username}}</label>
    <br>
    <div class="repo-searchj-new">
      <div id="top-repo">
        <label id="repositories-id">Top repositories</label>
      </div>
      <div id="btn-new-repo">
        <button type="button" class="new-repo-btn"><i class="bi bi-journal-plus"></i> &nbsp;New</button>
      </div>
    </div>
    <div id="search-bar-div">
        <input type="text" v-model="searchQuery" placeholder="Find a repository..." class="search-bar">
      </div>
    <ul class="repo-ul">
      <li class="repo-li" v-for="repo in filteredRepositories" :key="repo.id" >
        <img :src="currentAvatar" alt="Current Avatar"  class="profile-picture-main" />
        <a :href="'/view/' + username +'/' + repo.name">{{ username + '/' + repo.name }}</a>
      </li>
    </ul>
  </div>
</template>

<script>
import DeveloperService from '@/services/DeveloperService';

export default {
  props: {
    repositories: Array,
  },
  mounted() {
    DeveloperService.getUserAvatar(localStorage.getItem("username"))
          .then(res => {
              this.currentAvatar = res.data
          })
          .catch(err => {
              console.log(err);
          });
  },
  data() {
    return {
      currentAvatar: '',
      searchQuery: '',
      username: localStorage.getItem("username"),
    };
  },
  computed: {
    filteredRepositories() {
      return this.repositories.filter(repo =>
        repo.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
};
</script>

<style scoped>
#btn-new-repo{
  margin-inline-start: 3rem;
}

#search-bar-div{
  margin-inline-start:1rem;
  margin-inline-end:1rem;
}

.repo-searchj-new{
  display: flex;
}

#top-repo{
  float: left;
}
#new-repo-btn{
  float: left;
}

.search-bar {
  margin-bottom: 0.5rem;
  padding: 0.1rem;
  font-size: 9px;
  background: black;
  border:none;
  color: white;
  width: 100%;
}

.new-repo-btn{
  background: rgb(6, 146, 55);
  border: none;
  margin-inline-start: 1rem;
  margin-top: 0.9rem;
  margin-inline-end: 1rem;
  border-radius: 5px;
  color: white;
  float: right;
  font-size: 0.7rem;
}

.new-repo-btn:hover{
  background: rgb(7, 181, 68);
}

#repositories-id{
  margin-inline-start: 1rem;
  margin-bottom: 0.5rem;
  margin-top: 1rem;
  font-size: 0.8rem;
}

.profile-picture-main{
  max-height: 1rem;
  max-width: 100%;
  border-radius: 25px;
}


.repository-list {
  background-color: #24292e;
  border-top: 1px solid #929191;
  border-right: 1px solid #929191;
  color: white;
  height: 100%;
  display: flex;
  flex-direction: column;
}

#profile-name {
  padding: 1rem;
  font-size: 0.8rem;
  margin-bottom: 10px;
}

.repo-ul {
  list-style-type: none;
  padding: 0;
  font-size: 0.7rem;
  margin-inline-start: 1rem;
}

.repo-li {
  background-color: none;
  padding: 2px;
  margin-bottom: 5px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.repo-li:hover {
  background-color: #929191;
}
</style>
