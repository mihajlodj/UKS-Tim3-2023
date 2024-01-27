<template>
  <div class="navbar">
    <button class="toggle-menu-button"  @click="toggleMenu">
      <i class="bi bi-list"></i>
    </button>
    <span>GitHub</span>
    <input type="text" placeholder="Search repositories...">
    <div class="user-profile">
      <img :src="user.avatar_url" alt="User Avatar">
    </div>
    <transition name="fade">
      <div v-if="isMenuOpen" class="backdrop" @click="closeMenu"></div>
    </transition>
    <slide-menu :is-open="isMenuOpen" @close="closeMenu" />
  </div>
</template>

<script>
import SlideMenu from './SlideMenu.vue';

export default {
  components: {
    SlideMenu
  },
  props: {
    user: Object,
  },
  data() {
    return {
      isMenuOpen: false,
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
    },
    closeMenu() {
      this.isMenuOpen = false;
    },
  },
};
</script>

<style scoped>
.navbar {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #24292e;
  color: #ffffff;
  padding: 10px 20px;
}

.toggle-menu-button {
  background: none;
  border: none;
  color: #ffffff;
  cursor: pointer;
  font-size: 16px;
}

.navbar span {
  font-size: 24px;
  font-weight: bold;
}

input {
  padding: 8px;
  font-size: 16px;
  border: none;
  border-radius: 4px;
}

.backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 99;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
