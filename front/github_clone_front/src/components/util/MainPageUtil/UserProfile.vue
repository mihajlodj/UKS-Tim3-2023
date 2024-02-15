<template>
  <div class="user-profile">
    <img :src="user.avatar_url" alt="User Avatar">
    <h2>{{ user.login }}</h2>
    <p>{{ user.bio }}</p>
  </div>
</template>

<script>
export default {
  props: {
    user: Object,
  },
};
</script>

<style scoped>
.user-profile {
  text-align: center;
  margin-top: 20px;
}

.user-profile img {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  margin-bottom: 10px;
}

.user-profile h2 {
  font-size: 24px;
  margin-bottom: 5px;
}

.user-profile p {
  font-size: 16px;
  color: #777;
}
</style>

