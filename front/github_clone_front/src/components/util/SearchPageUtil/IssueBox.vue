<template>
  <div class="issue-box">
    <div class="issue-header">
      <div class="issue-info">
        <p class="issue-description">{{ title }}</p>
        <a href="#" class="issue-name">{{username}}/{{ name }}</a>
        <p class="issue-description">{{ description }}</p>
        <p class="issue-description">{{ milestone_title }}</p>
        <p class="issue-access">{{ created }}</p>
        <p class="issue-access">{{ open }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'IssueBox',
  props: ['username', 'created', 'name', 'title', 'milestone_title','description','open']
};
</script>

<style scoped>
.issue-box {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
  color: white;
}

.issue-header {
  display: flex;
  align-items: center;
  color: white;
}

.issue-info {
  display: flex;
  align-items: center;
  flex: 1;
  padding: 0.5rem;
}

.issue-name {
  font-size: 1.2rem;
  align-content: center;
  padding: 0.5rem;
  max-width: 20rem;
  min-width: 15rem;
  color: rgb(16, 109, 249);
}

.issue-description {
  padding: 0.5rem;
  margin-top: 5px;
  margin-bottom: 5px;
  color: white;
}

.issue-access {
  padding: 0.5rem;
  font-style: italic; 
  font-weight: 600;
  background: rgb(92, 92, 92);
  border-radius: 1rem;
  margin-left: auto;
  color: white;
}
</style>

