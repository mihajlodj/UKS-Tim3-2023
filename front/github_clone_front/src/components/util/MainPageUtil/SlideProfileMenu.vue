<template>
  <div class="slide-profile-menu" :class="{ 'slide-in': isProfileOpen }">
    <a href="#">Menu Item 1</a>
    <a href="#">Menu Item 2</a>
    <a href="#">Menu Item 3</a>
  </div>
</template>

<script>
export default {
  props: {
    isProfileOpen: Boolean,
  },
};
</script>

<style scoped>
.slide-profile-menu {
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  right: -250px;
  height: 100%;
  width: 250px;
  background-color: #333;
  border-radius: 10px;
  padding: 20px;
  transition: left 0.4s ease-in-out;
  z-index: 100;
}

.slide-profile-menu a {
  color: #fff;
  text-decoration: none;
  font-size: 18px;
  margin-bottom: 15px;
}

.slide-in {
  right: 0;
}
</style>
