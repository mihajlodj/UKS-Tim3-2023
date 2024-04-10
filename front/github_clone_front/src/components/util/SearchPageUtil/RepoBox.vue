<template>
  <div class="repo-box">
    <div class="repo-header">
      <img :src="avatar" alt="User Avatar" class="repo-avatar">
      <div class="repo-info">
        <h3 class="repo-name">{{ name }}</h3>
        <p class="repo-description">{{ description }}</p>
        <p class="repo-access">{{ access_modifier }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RepoBox',
  props: ['username', 'avatar', 'name', 'description', 'access_modifier']
};
</script>

<style scoped>
.repo-box {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
}

.repo-header {
  display: flex;
  align-items: center;
}

.repo-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

.repo-info {
  flex: 1;
}

.repo-name {
  font-size: 1.2rem;
  margin: 0;
}

.repo-description {
  margin-top: 5px;
  margin-bottom: 5px;
  color: #666;
}

.repo-access {
  font-style: italic;
  color: #888;
}
</style>

