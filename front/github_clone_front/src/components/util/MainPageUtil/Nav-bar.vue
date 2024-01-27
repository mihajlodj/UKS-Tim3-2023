<template>
  <div class="navbar">
    <div>
      <div id="id-toggle-menu">
        <button class="toggle-menu-button" @click="toggleMenu">
          <i class="bi bi-list" />
        </button>
      </div>
      <div id="id-git-logo">
        <a href="/">
          <img alt="Logo" src="../../../.. /../assets/logo_dark.png" class="logo-image-main">
        </a>
      </div>
      <div id="id-dashboard">
        <button class="dashboard-menu-button" @click="toggleMenu">
          Dashboard
        </button>
      </div>
    </div>
    <div>
      <div id="id-search-bar">
        <search-bar></search-bar>
      </div>
      <div id="id-user-profile">
        <img src="../../../.. /../assets/git_profile_picture.png" alt="User Avatar" class="profile-picture-main">
      </div>
    </div>
    <transition name="fade">
      <div v-if="isMenuOpen" class="backdrop" @click="closeMenu"></div>
    </transition>
    <slide-menu :is-open="isMenuOpen" @close="closeMenu" />
  </div>
</template>

<script>
import SearchBar from './Search-bar.vue';
import SlideMenu from './SlideMenu.vue';


export default {
  components: {
    SlideMenu,
    SearchBar
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
#id-toggle-menu {
  margin-inline-start: 1rem;
  float:left;
}
#id-git-logo {
  float: left;
  margin-top: -0.1rem;
  margin-inline-start: 0.7rem;
}
#id-dashboard{
  margin-inline-start: 0.5rem;
  float:left;
}
#id-search-bar{
  float: left;
}
#id-user-profile{
  margin-inline-start: 3rem;
  float: left;
}

.navbar {
  position: relative;
  display: flex;
  background-color: #24292e;
  color: #ffffff;
}

.toggle-menu-button {
  background: none;
  border: 1px solid rgb(152, 152, 152);
  border-radius: 5px;
  color: #cacaca;
  cursor: pointer;
  font-size: 1rem;
}

.toggle-menu-button:hover{
  border-color:white;
}

.dashboard-menu-button{
  background: none;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 500;
  border: none;
  color: #cacaca;
}

.dashboard-menu-button:hover{
  background: #cacaca37;
}

.navbar span {
  font-size: 20px;
  font-weight: bold;
}

.repo-search-bar {
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

.logo-image-main {
  max-height: 1.7rem;
  max-width: 100%;
}

.profile-picture-main{
  max-height: 1.7rem;
  max-width: 100%;
  border-radius: 25px;
}

</style>
