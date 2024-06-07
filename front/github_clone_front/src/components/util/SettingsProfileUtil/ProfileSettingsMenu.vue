<template>
  <div class="profile-settings-menu">
    <button @click="selectItem('publicProfile')"><i class="bi bi-person"></i>&nbsp;&nbsp;Public profile</button>
    <button @click="selectItem('account')"><i class="bi bi-gear"></i>&nbsp;&nbsp;Account</button>
    <!-- <a href="#"><i class="bi bi-envelope"></i>&nbsp;&nbsp;Email</a> -->
    <!-- <a href="#"><i class="bi bi-shield-lock"></i>&nbsp;&nbsp;Password and authentication</a> -->
    <a href="/notifications"><i class="bi bi-bell"></i>&nbsp;&nbsp;Notifications</a>
  </div>
</template>

<script>
export default {
  props: {
    isOpen: Boolean,
  },
  methods: {
    selectItem(item) {
      this.$emit('menuItemSelected', item);
    },
  },
};
</script>

<style scoped>
.profile-settings-menu {
  display: flex;
  border-top: 1px solid rgb(34, 34, 34);
  flex-direction: column;
  height: auto;
  width: 100%;
  padding: 0.5rem;
}

.profile-settings-menu a {
  color: #fff;
  padding: 5px;
  text-decoration: none;
  font-size: 10px;
}

.profile-settings-menu a:hover {
  background: #605f5f;
}

.profile-settings-menu button {
  color: #fff;
  background: none;
  border: none;
  justify-content: left;
  display: flex;
  padding: 5px;
  text-decoration: none;
  font-size: 10px;
}

.profile-settings-menu button:hover {
  background: #605f5f;
}

</style>
