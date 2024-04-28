<template>
  <div class="search-page">
    <nav-bar :user="user"/>
    <div class="main-content">
      <div class="left-section">
        <div class="left-section-filters">
          <label class="filter-text">Filter by </label>
          <a href="#" class="filter-buttons" :class="{ 'selected-filter': preselected_field === 'Repositories' }" @click="preselected_field = 'Repositories'; clearSearchLink()"><i class="bi bi-journal-bookmark"></i>&nbsp; Repositories</a>
          <!-- <a href="#" class="filter-buttons" :class="{ 'selected-filter': preselected_field === 'Code' }" @click="preselected_field = 'Code'; clearSearchLink()"><i class="bi bi-code">&nbsp;</i> Code</a> -->
          <a href="#" class="filter-buttons" :class="{ 'selected-filter': preselected_field === 'Issues' }" @click="preselected_field = 'Issues'; clearSearchLink()"><i class="bi bi-record-circle">&nbsp;</i> Issues</a>
          <a href="#" class="filter-buttons" :class="{ 'selected-filter': preselected_field === 'Pull_requests' }" @click="preselected_field = 'Pull_requests'; clearSearchLink()"><i class="bi bi-bezier2">&nbsp;</i> Pull requests</a>
          <a href="#" class="filter-buttons" :class="{ 'selected-filter': preselected_field === 'Users' }" @click="preselected_field = 'Users'; clearSearchLink()"><i class="bi bi-person">&nbsp;</i> Users</a>
          <a href="#" class="filter-buttons" :class="{ 'selected-filter': preselected_field === 'Commits' }" @click="preselected_field = 'Commits'; clearSearchLink()"><i class="bi bi-bezier">&nbsp;</i> Commits</a>
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
          <a :href="generateSearchLink('is:open')" class="filter-buttons">&#8857; &nbsp; Open</a>
          <a :href="generateSearchLink('is:closed')" class="filter-buttons">&#10003; &nbsp; Closed</a>
        </div>

        <div class="left-section-advanced">
          <label class="filter-text-2">Advanced</label>
          <a :href="generateSearchLink('owner:')" class="filter-buttons">&#43; &nbsp; Owner</a>
          <a :href="generateSearchLink('is:public')" class="filter-buttons">&#43; &nbsp; Public</a>
          <a :href="generateSearchLink('is:private')" class="filter-buttons">&#43; &nbsp; Private</a>
          <a :href="generateSearchLink('created:')" class="filter-buttons">&#43; &nbsp; Date created</a>
          <a :href="generateSearchLink('assignee:')" class="filter-buttons">&#43; &nbsp; Assignee</a>
          <a :href="generateSearchLink('committer:')" class="filter-buttons">&#43; &nbsp; Committer</a>
          <a :href="generateSearchLink('followers:')" class="filter-buttons">&#43; &nbsp; Number of followers</a>
          <a :href="generateSearchLink('stars:')" class="filter-buttons">&#43; &nbsp; Number of stars</a>
          <a :href="generateSearchLink('repositories:')" class="filter-buttons">&#43; &nbsp; Number of repositories</a>
        </div>
      </div>
      <div class="middle-section" v-if="this.preselected_field=='Repositories'">
          <repo-box
          v-for="(result, index) in repositories"
            :key="index"
            :username="result.developer.user.username"
            :avatar="result.developer.avatar"
            :name="result.project.name"
            :description="result.project.description"
            :access_modifier="result.project.access_modifier"
            :starred = "result.starred"
          />
      </div>
      <div class="middle-section" v-if="this.preselected_field=='Issues'">
          <issue-box
          v-for="(result, index) in issues"
            :key="index"
            :username="result.developer.user.username"
            :created="result.created"
            :name="result.project.name"
            :title="result.title"
            :description="result.description"
            :open="result.open"
            :milestone_title="result.milestone.title"
          />
      </div>
      <div class="middle-section" v-if="this.preselected_field=='Pull_requests'">
          <pr-box
          v-for="(result, index) in prs"
            :key="index"
            :developer="result.developer"
            :project="result.project.name"
            :title="result.title"
            :author="result.author.user.username"
            :timestamp="result.timestamp"
            :status="result.Status"
          />
      </div>
      <div class="middle-section" v-if="this.preselected_field=='Users'">
          <dev-box @toggle-ban-status="toggleBanStatus"
          v-for="(result, index) in devs"
            :key="index"
            :developer="result"
          />
      </div>
      <div class="middle-section" v-if="this.preselected_field=='Commits'">
          <commit-box
          v-for="(result, index) in commits"
            :key="index"
            :message="result.message"
            :branch="result.branch"
            :author="result.author"
            :committer="result.committer"
            :timestamp="result.timestamp"
          />
      </div>
    </div>
  </div>
    
</template>

<script>
import NavBar from '../util/MainPageUtil/Nav-bar.vue';
import RepoBox from '../util/SearchPageUtil/RepoBox.vue';
import PrBox from '../util/SearchPageUtil/PrBox.vue';
import CommitBox from '../util/SearchPageUtil/CommitBox.vue';
import DevBox from '../util/SearchPageUtil/DevBox.vue';
import IssueBox from '../util/SearchPageUtil/IssueBox.vue';
import RepositoryService from '@/services/RepositoryService';
import IssueService from '@/services/IssueService';
import DeveloperService from '@/services/DeveloperService';
import PullRequestService from '@/services/PullRequestService';

export default {
  components: {
    NavBar,RepoBox,IssueBox,PrBox,DevBox,CommitBox
  },
  created(){
    this.preselected_field = 'Repositories';
    if (this.preselected_field=='Repositories'){
      console.log(this.preselected_field);
      this.fetchRepositories();
    }
    else{
      this.repositories = []
    }
  },
  watch: {
      '$route.query.q': {
        immediate: true,
        handler(newQuery, oldQuery) {
          if (newQuery !== oldQuery) {
            if (this.preselected_field=='Repositories'){
              console.log(this.preselected_field);
              this.fetchRepositories();
              this.issues = []
              this.prs=[]
              this.devs=[]
              this.commits = []
            }
            else if (this.preselected_field=='Issues'){
              console.log(this.preselected_field);
              this.getIssues();
              this.repositories = []
              this.prs=[]
              this.devs=[]
              this.commits = []
            }
            else if (this.preselected_field=='Pull_requests'){
              console.log(this.preselected_field);
              this.getPrs();
              this.repositories = []
              this.issues = []
              this.devs=[]
              this.commits = []
            }
            else if (this.preselected_field=='Users'){
              console.log(this.preselected_field);
              this.getDevs();
              this.repositories = []
              this.issues = []
              this.prs=[]
              this.commits = []
            }
             else if (this.preselected_field=='Commits'){
              console.log(this.preselected_field);
              this.getCommits();
              this.repositories = []
              this.issues = []
              this.prs=[]
              this.devs=[]
            }
            else{
              this.repositories = []
              this.issues = []
              this.prs=[]
              this.devs=[]
            }
          }
        },
      },
  },
  data() {
    return {
      query: '',
      language: '',
      preselected_field: 'Repositories',
      user : localStorage.getItem("username"),
      loading: false,
      repositories: [],
      issues: [],
      prs: [],
      devs: [],
      commits: [],
      error: null
    };
  },
  methods: {
    toggleBanStatus(username) {
      const developerIndex = this.devs.findIndex(dev => dev.user.username === username);
      if (developerIndex !== -1) {
        this.devs[developerIndex].banned = !this.devs[developerIndex].banned
      }
    },
    generateSearchLink(query) {
      const currentQuery = this.$route.query.q || '';
      const combinedQuery = currentQuery + '&' + query;
      const encodedQuery = encodeURIComponent(combinedQuery);
      return '/search?q=' + encodedQuery;
    },
    clearSearchLink(){
      this.$router.replace({ query: { q: '' } });
    },
    fetchRepositories() {
      RepositoryService.getAllQueryRepos(this.$route.query.q,this.user)
          .then(res => {
                  this.repositories = res.data
                  console.log(res.data)
              })
              .catch(err => {
                  console.log(err);
              });
    },
    getIssues() {
      IssueService.getAllQueryIssues(this.$route.query.q)
          .then(res => {
                  this.issues = res.data
                  console.log(res.data)
              })
              .catch(err => {
                  console.log(err);
              });
    },
    getPrs() {
      PullRequestService.getAllQueryPrs(this.$route.query.q)
          .then(res => {
                  this.prs = res.data
                  console.log(res.data)
              })
              .catch(err => {
                  console.log(err);
              });
    },
    getDevs() {
      DeveloperService.getAllQueryDevelopers(this.$route.query.q)
          .then(res => {
                  this.devs = res.data
                  console.log(res.data)
              })
              .catch(err => {
                  console.log(err);
              });
    },
    getCommits() {
      DeveloperService.getAllQueryCommitts(this.$route.query.q)
          .then(res => {
                  this.commits = res.data
                  console.log(res.data)
              })
              .catch(err => {
                  console.log(err);
              });
    },
  }
};
</script>

<style scoped>
.selected-filter {
  font-size: 1.5rem;
  font-weight: 500;
}

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

