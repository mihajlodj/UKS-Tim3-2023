<template>
  <div class="navbar">
    <div>
      <div id="id-toggle-menu">
        <button class="toggle-menu-button" @click="toggleMenu" v-if="!loggedInUserPresent">
          <i class="bi bi-list"></i>
        </button>
      </div>
      <div id="id-git-logo">
        <a href="/">
          <img alt="Logo" src="../../../.. /../assets/logo_dark.png" class="logo-image-main">
        </a>
      </div>
      <div id="id-dashboard">
        <button class="dashboard-menu-button" @click="$router.push(`/main`)" v-if="!loggedInUserPresent">
          Dashboard
        </button>
      </div>
    </div>

    <div id="id-search-bar" v-if="!isSearchPage">
      <search-bar></search-bar>
    </div>

    <div id="id-search-bar-2" v-if="isSearchPage">
      <search-bar></search-bar>
    </div>

    <div class="right-btns-navbar">
        <button class="notification_button" @click="this.$router.push('/new');" v-if="!loggedInUserPresent"><i class="bi bi-journal-plus"></i></button>
      <button class="notification_button" @click="displayNotifications" :key="notificationKey" v-if="!loggedInUserPresent">
        <i class="bi bi-inbox"></i>
        <font-awesome-icon v-if="hasUnreads" icon="fa-solid fa-circle"></font-awesome-icon>
      </button>
      <button class="notification_button" @click="this.$router.push('/view/pulls')" v-if="!loggedInUserPresent"><i class="bi bi-bezier2"></i></button>
      <button class="notification_button" @click="this.$router.push('/view/users_issues')" v-if="!loggedInUserPresent"><i class="bi bi-record-circle"></i></button>

      <button class="profile_button" @click="toggleProfileMenu" v-if="!loggedInUserPresent">
        <div style="">
          <div class="profile-image-container">
            <div style="margin-top:13px"> </div>
            <img :src="currentAvatar" alt="Current Avatar" class="profile-picture-main" />
          </div>
        </div>
      </button>
      <button class="profile_button" @click="this.$router.push('/register')" v-if="loggedInUserPresent">
        Sign up
      </button>
    </div>

    <transition name="fade">
      <div v-if="isMenuOpen || isProfileMenuOpen" class="backdrop" @click="closeMenu"></div>
    </transition>
    <transition name="fadelight">
      <div v-if="isDropdownOpen" class="backdropLight" @click="closeMenu"></div>
    </transition>
    <slide-menu :is-open="isMenuOpen" @close="closeMenu" v-if="!loggedInUserPresent" />
    <slide-profile-menu :is-profile-open="isProfileMenuOpen" @close="closeMenu"  v-if="!loggedInUserPresent"/>
  </div>
</template>

<script>
import SearchBar from './Search-bar.vue';
import SlideMenu from './SlideMenu.vue';
import SlideProfileMenu from './SlideProfileMenu.vue';
import DeveloperService from '@/services/DeveloperService';

export default {
  components: {
    SlideMenu,
    SearchBar,
    SlideProfileMenu
  },
  // Nisam siguran da li ce trebati
  // props: {
  //   user: Object,
  // },
  computed:{
    isSearchPage() {
      return this.$route.path === '/search';
    },
    loggedInUserPresent(){
      return localStorage.getItem("username") === null
    }
  },
  mounted() {
    if(!this.loggedInUserPresent){
    DeveloperService.getUserAvatar(localStorage.getItem("username"))
          .then(res => {
              // console.log(res);
              this.currentAvatar = res.data
          })
          .catch(err => {
              console.log(err);
          });
    }
  },
  data() {
    return {
      currentAvatar: '',
      isMenuOpen: false,
      isProfileMenuOpen: false,
      isDropdownOpen: false,
      connection: null,
      hasUnreads: false,
      notificationKey: 1
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
      this.isProfileMenuOpen = false;
    },
    toggleProfileMenu() {
      this.isProfileMenuOpen = !this.isProfileMenuOpen;
      this.isDropdownOpen = false;
    },
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },

    displayNotifications() {
      localStorage.setItem("hasUnreads", "false");
      this.hasUnreads = false;
      this.notificationKey++;
      this.$router.push("/notifications");
    }
  },

  created() {
    this.hasUnreads = localStorage.getItem("hasUnreads") === "true" ? true : false;
    this.notificationKey++;
    const connectionStr = `ws://localhost:8000/ws/notify/${localStorage.getItem("username")}/`;
    this.connection = new WebSocket(connectionStr);

    this.connection.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const message = data.message;
        console.log(message);
        localStorage.setItem("hasUnreads", "true");
        this.hasUnreads = true;
        this.notificationKey++;
        console.log(this.hasUnreads);
    }

    this.connection.onopen = (event) => {
        console.log(event);
        console.log("Opened");
    }
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
  width: 15rem;
  float: right;
  z-index: 99;
}

#id-search-bar-2{
  width: 60%;
  float: right;
  z-index: 99;
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
  background-color: #1c2127;
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
  z-index: 98;
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

.backdropLight {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0);
  z-index: 98;
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
  background-color: #1e1e1e;
  min-width: 160px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  z-index: 100;
  padding: 8px; 
  margin-inline-start: -7rem;
  border-radius: 7px;
}

.isDropdownOpen .dropdown-content {
  display: block;
}

.dropdown-content a {
  display: block;
  padding-top: 0.1rem;
  padding-bottom: 0.1rem;
  text-decoration: none;
  color: #ffffff;
  transition: background-color 0.3s; 
}

.dropdown-content a:hover {
  background-color: #2c2c2c;
}

.fa-circle {
  height: 8px;
  color: #f04444;
  margin-bottom: 10px;
}
</style>
