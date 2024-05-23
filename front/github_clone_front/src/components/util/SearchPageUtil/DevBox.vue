<template>
  <div class="dev-box">
    <div class="dev-header">
      <img :src="developer.developer_avatar" alt="User Avatar" class="dev-avatar">
      <div class="dev-info">
        <a href="#" class="dev-name">{{ developer.developer.user.username }}</a>
        <button v-if="showBanButton" :class="[banButtonClass]" @click="toggleBanUnban" id="btn-confirm">
          {{ banButtonText }}
        </button>
        <button type="button" class="btn btn-secondary" @click="follow" id="btn-confirm">
          Follow
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
  computed: {
    showBanButton() {
      return localStorage.getItem('username') === 'administrator';
    },
    banButtonClass() {
      return this.developer.banned ? 'btn btn-warning' : 'btn btn-danger';
    },
    banButtonText() {
      return this.developer.banned ? 'Unban' : 'Ban';
    }
  },
  methods: {
    follow() {
      console.log("followed");
    },
    toggleBanUnban() {
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
#btn-confirm {
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
