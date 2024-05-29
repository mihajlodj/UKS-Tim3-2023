<template>
  <div class="entire-page">
    <nav-bar :user="user" />
    <div class="main-content">
      <IssueTableForMainButton :issues-for-display="this.issues"></IssueTableForMainButton>
    </div>
  </div>
</template>

<script>
import NavBar from '../util/MainPageUtil/Nav-bar.vue';
import IssueService from '@/services/IssueService';
import IssueTableForMainButton from '@/components/issue/IssueTableForMainButton.vue';


export default {
  components: {
    NavBar,
    IssueTableForMainButton
  },
  mounted() {
    console.log(localStorage.getItem('username'));
    IssueService.getAllLogegdUsersIssues(localStorage.getItem('username')).then((res) => {
      this.issues = res.data;
    });
  },
  data() {
    return {
      issues: []
    };
  },
};
</script>

<style scoped>
.entire-page {
  min-height: 100vh;
  margin: 0px;
  padding: 0;
  background: #24292e;
}

.main-content {
  display: flex;
  overflow: auto;
  padding: 0;
  margin: 0;
  height: 100%;
  min-height: 92.5vh;
}
</style>
