<template>
  <div class="profile-settings-menu">
    <a href="#"><i class="bi bi-person"></i>&nbsp;&nbsp;Public profile</a>
    <a href="#"><i class="bi bi-gear"></i>&nbsp;&nbsp;Account</a>
    <a href="#"><i class="bi bi-envelope"></i>&nbsp;&nbsp;Email</a>
    <a href="#"><i class="bi bi-shield-lock"></i>&nbsp;&nbsp;Password and authentication</a>
    <a href="#"><i class="bi bi-bell"></i>&nbsp;&nbsp;Notifications</a>
    <a href="#"><i class="bi bi-key"></i>&nbsp;&nbsp;SSH and GPG keys</a>
    <a href="#"><i class="bi bi-buildings"></i>&nbsp;&nbsp;Organizations</a>
    <a href="#"><i class="bi bi-globe"></i>&nbsp;&nbsp;Enterprises</a>
    <a href="#"><i class="bi bi-chat-left-dots"></i>&nbsp;&nbsp;Moderation</a>
    <a href="#"><i class="bi bi-journal-bookmark"></i>&nbsp;&nbsp;Repositories</a>
    <a href="#"><i class="bi bi-pc-display-horizontal"></i>&nbsp;&nbsp;Codespaces</a>
    <a href="#"><i class="bi bi-box"></i>&nbsp;&nbsp;Packages</a>
    <a href="#"><i class="bi bi-robot"></i>&nbsp;&nbsp;Copilot</a>
    <a href="#"><i class="bi bi-window-stack"></i>&nbsp;&nbsp;Pages</a>
    <a href="#"><i class="bi bi-arrow-return-left"></i>&nbsp;&nbsp;Saved replies</a>
    <a href="#"><i class="bi bi-shield-lock"></i>&nbsp;&nbsp;Code security and analysis</a>
    <a href="#"><i class="bi bi-file-earmark-code"></i>&nbsp;&nbsp;Security log</a>
    <a href="#"><i class="bi bi-code"></i>&nbsp;&nbsp;Developer settings</a>
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
</style>
