<template>
  <div class="pr-box">
    <div class="pr-header">
      <div class="pr-info">
        <a href="#" class="pr-name">{{title}}</a>
        <a href="#" class="pr-name">{{developer}}/{{ project }}</a>
        <p class="pr-author">{{ author }}</p>
        <p class="pr-status">{{ formattedDate }}</p>
        <p class="pr-status">{{ status }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PrBox',
  props: ['developer', 'project', 'title', 'author', 'timestamp', 'status'],
  computed: {
    formattedDate() {
      const date = new Date(this.timestamp);
      return date.toLocaleString();
    },
  }
};
</script>

<style scoped>
.pr-box {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
  color: white;
}

.pr-header {
  display: flex;
  align-items: center;
  color: white;
}

.pr-info {
  display: flex;
  align-items: center;
  flex: 1;
  padding: 0.5rem;
}

.pr-name {
  font-size: 1.2rem;
  padding: 0.5rem;
  max-width: 15rem;
  min-width: 15rem;
  color: rgb(16, 109, 249);
}

.pr-author {
  padding: 0.5rem;
  margin-top: 5px;
  margin-bottom: 5px;
  color: white;
}

.pr-status {
  padding: 0.5rem;
  font-style: italic; 
  font-weight: 600;
  background: rgb(92, 92, 92);
  border-radius: 1rem;
  margin-left: auto;
  color: white;
}
</style>

