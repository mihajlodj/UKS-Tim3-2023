<template>
  <div class="repository-list">
    <h2>Your Repositories</h2>
    <ul>
      <li v-for="repo in repositories" :key="repo.id">{{ repo.name }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  props: {
    repositories: Array,
  },
};
</script>

<style scoped>
.repository-list {
  margin-top: 20px;
  background-color: #24292e;
  color: white;
}

h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

li {
  background-color: #c6c3c357;
  padding: 10px;
  margin-bottom: 5px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

li:hover {
  background-color: #929191;
}
</style>
