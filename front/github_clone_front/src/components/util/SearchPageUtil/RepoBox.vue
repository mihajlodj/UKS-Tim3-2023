<template>
  <div class="repo-box">
    <div class="repo-header">
      <img :src="avatar" alt="User Avatar" class="repo-avatar">
      <div class="repo-info">
        <a href="#" class="repo-name">{{username}}/{{ name }}</a>
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
  color: white;
}

.repo-header {
  display: flex;
  align-items: center;
  color: white;
}

.repo-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

.repo-info {
  display: flex;
  align-items: center;
  flex: 1;
  padding: 0.5rem;
}

.repo-name {
  font-size: 1.2rem;
  align-content: center;
  padding: 0.5rem;
  max-width: 20rem;
  min-width: 15rem;
  color: rgb(16, 109, 249);
}

.repo-description {
  padding: 0.5rem;
  margin-top: 5px;
  margin-bottom: 5px;
  color: white;
}

.repo-access {
  padding: 0.5rem;
  font-style: italic; 
  font-weight: 600;
  background: rgb(92, 92, 92);
  border-radius: 1rem;
  margin-left: auto;
  color: white;
}
</style>

