<template>
  <div class="dev-box">
    <div class="dev-header">
      <img :src="developer.avatar" alt="User Avatar" class="dev-avatar">
      <div class="dev-info">
        <a href="#" class="dev-name">{{developer.user.username}}</a>
        <button type="button" class="btn btn-secondary" id="btn-confirm">
                      Follow
        </button>
        <button type="button" class="btn btn-danger" id="btn-ban" v-if="!developer.banned">
                      Ban
        </button>
        <button type="button" class="btn btn-warning" id="btn-unban" v-if="developer.banned">
                      Unban
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DevBox',
  props: ['developer']
};
</script>

<style scoped>
#btn-confirm{
  margin-left: auto;
}

.dev-box {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 10px;
  color: white;
}

.dev-header {
  display: flex;
  align-items: center;
  color: white;
}

.dev-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 10px;
}

.dev-info {
  display: flex;
  align-items: center;
  flex: 1;
  padding: 0.5rem;
}

.dev-name {
  font-size: 1.2rem;
  align-content: center;
  padding: 0.5rem;
  max-width: 20rem;
  min-width: 15rem;
  color: rgb(16, 109, 249);
}
</style>

