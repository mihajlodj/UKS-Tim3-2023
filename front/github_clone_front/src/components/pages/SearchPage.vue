<template>
  <div class="search-page">
    <nav-bar :user="user" />
    <div class="main-content">
      <div class="left-section">
        <div class="left-section-filters">
          <label class="filter-text">Filter by </label>
          <a href="#" class="filter-buttons"><i class="bi bi-code">&nbsp;</i> Code</a>
          <a href="#" class="filter-buttons"><i class="bi bi-journal-bookmark"></i>&nbsp; Repositories</a>
          <a href="#" class="filter-buttons"><i class="bi bi-record-circle">&nbsp;</i> Issues</a>
          <a href="#" class="filter-buttons"><i class="bi bi-bezier2">&nbsp;</i> Pull requests</a>
          <a href="#" class="filter-buttons"><i class="bi bi-person">&nbsp;</i> Users</a>
          <a href="#" class="filter-buttons"><i class="bi bi-bezier">&nbsp;</i> Commits</a>
        </div>

        <div class="left-section-languages">
          <label class="filter-text-2">Languages</label>
          <a :href="generateSearchLink('language:JavaScript')" class="filter-buttons">&#128308; &nbsp; JavaScript</a>
          <a :href="generateSearchLink('language:Python')" class="filter-buttons">&#128309; &nbsp; Python</a>
          <a :href="generateSearchLink('language:Java')" class="filter-buttons">&#128994; &nbsp; Java</a>
          <a :href="generateSearchLink('language:HTML')" class="filter-buttons">&#128995; &nbsp; HTML</a>
          <a :href="generateSearchLink('language:C++')" class="filter-buttons">&#128992; &nbsp; C++</a>
          <a :href="generateSearchLink('language:CSS')" class="filter-buttons">&#128996; &nbsp; CSS</a>
        </div>

        <div class="left-section-state">
          <label class="filter-text-2">State</label>
          <a href="#" class="filter-buttons">&#8857; &nbsp; Open</a>
          <a href="#" class="filter-buttons">&#10003; &nbsp; Closed</a>
        </div>

        <div class="left-section-advanced">
          <label class="filter-text-2">Advanced</label>
          <a href="#" class="filter-buttons">&#43; &nbsp; Owner</a>
          <a href="#" class="filter-buttons">&#43; &nbsp; Public</a>
          <a href="#" class="filter-buttons">&#43; &nbsp; Private</a>
          <a href="#" class="filter-buttons">&#43; &nbsp; Date created</a>
          <a href="#" class="filter-buttons">&#43; &nbsp; Assignee</a>
          <a href="#" class="filter-buttons">&#43; &nbsp; Number of followers</a>
          <a href="#" class="filter-buttons">&#43; &nbsp; Number of stars</a>
          <a href="#" class="filter-buttons">&#43; &nbsp; Number of repositories</a>
        </div>
      </div>
      <div class="middle-section">
      </div>
    </div>
  </div>
    
</template>

<script>
import NavBar from '../util/MainPageUtil/Nav-bar.vue';

export default {
  components: {
    NavBar,
  },
  data() {
    return {
      query: '',
      language: '',
      loading: false,
      repositories: [],
      error: null
    };
  },
  methods: {
    generateSearchLink(query) {
      const currentQuery = this.$route.query.q || '';
      const combinedQuery = currentQuery + ' ' + query;
      const encodedQuery = encodeURIComponent(combinedQuery);
      return '/search?q=' + encodedQuery;
    }
  }
};
</script>

<style scoped>
.filter-text{
  color: white;
  margin-top: 5px;
  width: 100%;
  margin-bottom: 5px;
  font-weight: 600;
  font-size: 1.5rem;
}

.filter-text-2{
  color: whitesmoke;
  margin-top: 5px;
  width: 100%;
  margin-bottom: 5px;
  font-weight: 400;
  font-size: 1rem;
}

.filter-buttons{
  background: none;
  color: white;
  width: 90%;
  padding: 5px;
  text-decoration: none;
}

.filter-buttons:hover{
  background: #383f46;
  border-radius: 0.5rem;
}


.search-page {
  background: #24292e;
  margin: 0 auto;
  min-height: 100vh;
  padding: 20px;
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
  border-right: 0.5px solid gainsboro;
}

.left-section-filters{
  flex: 1;
  display: flex;
  flex-direction: column;
  border-bottom: 0.5px solid gainsboro;
}

.left-section-languages{
  flex: 1;
  display: flex;
  flex-direction: column;
  border-bottom: 0.5px solid gainsboro;
}

.left-section-advanced{
  flex: 1;
  display: flex;
  flex-direction: column;
  border-bottom: 0.5px solid gainsboro;
}

.left-section-state{
  flex: 1;
  display: flex;
  flex-direction: column;
  border-bottom: 0.5px solid gainsboro;
}

.middle-section {
  flex: 4;
  background-color:  #24292e;
  padding: 20px;
}
</style>
