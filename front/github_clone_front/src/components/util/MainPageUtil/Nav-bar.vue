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
        <button class="dashboard-menu-button">
          Dashboard
        </button>
      </div>
    </div>

    <div id="id-search-bar">
      <search-bar></search-bar>
    </div>

    <div class="right-btns-navbar">
      <button class="notification_button"><i class="bi bi-inbox"></i></button>
      <button class="notification_button"><i class="bi bi-bezier2"></i></button>
      <button class="notification_button"><i class="bi bi-record-circle"></i></button>

      <!-- Dropdown Button -->
      <div class="dropdown" :class="{ 'isDropdownOpen': isDropdownOpen }">
        <button class="notification_button" @click="toggleDropdown">
          DropDown
        </button>
        <!-- Dropdown Content -->
        <div class="dropdown-content" v-show="isDropdownOpen" @click.stop>
          <!-- Add your dropdown menu items here -->
          <a href="#">Dropdown Item 1</a>
          <a href="#">Dropdown Item 2</a>
          <a href="#">Dropdown Item 3</a>
        </div>
      </div>

      <button class="profile_button">
        <div style="">
          <div class="profile-image-container">
            <div style="margin-top:13px"> </div>
            <img src="../../../.. /../assets/git_profile_picture.png" alt="User Avatar" class="profile-picture-main">
          </div>
        </div>
      </button>
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
      isDropdownOpen: false,
    };
  },
  methods: {
    toggleMenu() {
      this.isMenuOpen = !this.isMenuOpen;
      this.isDropdownOpen = false;
    },
    closeMenu() {
      this.isMenuOpen = false;
      this.isDropdownOpen = false;
    },
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
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
  margin-inline-end: 2rem;
  float: left;
}
.right-btns-navbar{
  margin-right: 1rem;
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

.dropdown {
  position: relative;
  display: inline-block;
}

.dashboard-menu-button{
  background: none;
  border-radius: 5px;
  font-size: 1rem;
  font-weight: 500;
  border: none;
  color: #cacaca;
}

.profile-image-container {
  display: flex;
  align-items: center; 
  justify-content: center;

}

.dashboard-menu-button:hover{
  background: #cacaca37;
}

.notification_button{
  background: none;
  border: 1px solid rgb(152, 152, 152);
  border-radius: 5px;
  color: #cacaca;
  cursor: pointer;
  font-size: 1rem;
  margin-right: 0.5rem;
}

.notification_button:hover{
  border-color:white;
  background: #cacaca37;
}

.profile_button{
  background: none;
  border: 1px solid rgba(152, 152, 152, 0);
  border-radius: 5px;
  color: #cacaca;
  cursor: pointer;
  font-size: 1rem;
  margin-right: 0.5rem;
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
  max-height: 1.6rem;
  max-width: 100%;
  border-radius: 25px;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.isDropdownOpen .dropdown-content {
  display: block;
}

</style>
