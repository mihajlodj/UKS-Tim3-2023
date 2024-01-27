<template>
  <div class="slide-menu" :class="{ 'slide-in': isOpen }">
    <a href="#">Menu Item 1</a>
    <a href="#">Menu Item 2</a>
    <a href="#">Menu Item 3</a>
  </div>
</template>

<script>
export default {
  props: {
    isOpen: Boolean,
  },
};
</script>

<style scoped>
.slide-menu {
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: -250px;
  height: 100%;
  width: 250px;
  background-color: #333;
  padding: 20px;
  transition: left 0.4s ease-in-out;
  z-index: 100;
}

.slide-menu a {
  color: #fff;
  text-decoration: none;
  font-size: 18px;
  margin-bottom: 15px;
}

.slide-in {
  left: 0;
}
</style>
