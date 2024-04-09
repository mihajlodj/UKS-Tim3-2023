<template>
  <div class="search-page">
    <nav-bar :user="user" />
    <h1 class="title">Search repositories</h1>
    <form @submit.prevent="searchRepositories" class="search-form">
      <input v-model="query" type="text" placeholder="Search repositories" class="search-input">
      <input v-model="language" type="text" placeholder="Language" class="search-input">
      <!-- Add more input fields for other filters -->
      <button type="submit" class="search-button">Search</button>
    </form>

    <div v-if="loading" class="loading">Loading...</div>

    <div v-if="repositories.length > 0">
      <h2 class="result-title">Search Results</h2>
      <ul class="repository-list">
        <li v-for="repo in repositories" :key="repo.id" class="repository-item">
          <a :href="repo.html_url" target="_blank" class="repository-link">{{ repo.full_name }}</a>
          <p class="repository-description">{{ repo.description }}</p>
          <p class="repository-stats">Stars: {{ repo.stargazers_count }}</p>
          <!-- Display more repository information as needed -->
        </li>
      </ul>
    </div>

    <div v-if="error" class="error">{{ error }}</div>
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
    async searchRepositories() {
      this.loading = true;
      this.error = null;
      
      try {
        const response = await fetch(`YOUR_API_ENDPOINT?q=${this.query}&language=${this.language}`);
        if (!response.ok) {
          throw new Error('Failed to fetch repositories');
        }
        this.repositories = await response.json();
      } catch (error) {
        this.error = error.message;
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.search-page {
  background: #24292e;
  margin: 0 auto;
  min-height: 100vh;
  padding: 20px;
}

.title {
  font-size: 24px;
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  margin-bottom: 20px;
}

.search-input {
  flex: 1;
  padding: 10px;
  font-size: 16px;
  margin-right: 10px;
}

.search-button {
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
}

.loading {
  margin-top: 20px;
}

.result-title {
  font-size: 20px;
  margin-top: 20px;
}

.repository-list {
  list-style: none;
  padding: 0;
}

.repository-item {
  margin-bottom: 20px;
}

.repository-link {
  font-size: 18px;
  color: #007bff;
  text-decoration: none;
}

.repository-link:hover {
  text-decoration: underline;
}

.repository-description {
  margin-top: 5px;
  font-size: 16px;
}

.repository-stats {
  font-size: 14px;
  color: #666;
}

.error {
  color: red;
  margin-top: 20px;
}
</style>
