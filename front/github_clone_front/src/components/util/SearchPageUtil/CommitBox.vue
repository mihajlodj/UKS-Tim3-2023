<template>
  <div class="commit-box">
    <div class="commit-header">
      <img :src="avatar" alt="User Avatar" class="commit-avatar">
      <div class="commit-info">
        <p class="commit-name">{{ committer.user.username}}</p>
        <a :href="'/view/' + repo_owner +'/' +project +'/'+branch.name+'/commit/'+sha" class="commit-name">{{message}}</a>
        <p class="commit-name">{{ branch.name }} </p>
        <p class="commit-status">{{ formattedDate }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CommitBox',
  props: ['message','branch','author','committer','timestamp','repo_owner','project','sha','avatar'],
  computed: {
    formattedDate() {
      const date = new Date(this.timestamp);
      return date.toLocaleString();
    },
  }
};
</script>

<style scoped>
#btn-confirm{
  margin-left: auto;
}

.commit-box {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
  color: white;
}

.commit-header {
  display: flex;
  align-items: center;
  color: white;
}

.commit-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

.commit-info {
  display: flex;
  align-items: center;
  flex: 1;
  padding: 0.5rem;
}

.commit-name {
  font-size: 1.2rem;
  align-content: center;
  padding: 0.5rem;
  max-width: 20rem;
  min-width: 15rem;
}

.commit-status {
  padding: 0.5rem;
  font-style: italic; 
  font-weight: 600;
  background: rgb(92, 92, 92);
  border-radius: 1rem;
  margin-left: auto;
  color: white;
}
</style>

