<template>
  <div class="dev-box">
    <div class="dev-header">
      <img :src="developer.avatar" alt="User Avatar" class="dev-avatar">
      <div class="dev-info">
        <a href="#" class="dev-name">{{developer.user.username}}</a>
        <button type="button" class="btn btn-secondary" id="btn-confirm" @click="follow">
                      Follow
        </button>
        <button type="button" class="btn btn-danger" id="btn-ban" v-if="!developer.banned" @click="ban_unban">
                      Ban
        </button>
        <button type="button" class="btn btn-warning" id="btn-unban" v-if="developer.banned" @click="ban_unban">
                      Unban
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import DeveloperService from '@/services/DeveloperService';

export default {
  name: 'DevBox',
  props: ['developer'],
  methods: {
    follow() {
      console.log("followed");
    },
    ban_unban() {
      DeveloperService.update_user_ban_status(this.developer.user.username)
          .then(res => {
                  console.log(res);
                  this.$emit('toggle-ban-status', this.developer.user.username);
              })
              .catch(err => {
                  console.log(err);
              });
    },
  }
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

