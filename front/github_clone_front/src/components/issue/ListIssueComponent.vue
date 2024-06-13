<template>
  <div class="bg min-vh-100 is-fullheight">
  <div>
    <RepoNavbar starting="issues" />
  </div>
  <div class="input-group mb-3" width="200px">
    <span class="input-group-text" id="basic-addon1" style="background-color: #373e48;color:#adbbc8;border-color:#adbbc8;">Search:</span>
    <input v-on:keyup.enter="this.doFilter()" v-model="this.issueFilter" type="text" class="form-control" placeholder="Issue name"
      aria-label="Issue name" aria-describedby="basic-addon1" style="background-color: #22272d; color: white;">
  </div>
  <!-- Modal add -->
  <div class="modal fade" id="exampleModalAdd" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
    aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Open issue</h5>
          <!-- <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span> -->
          <!-- </button> -->
        </div>
        <div class="modal-body">
          <AddIssueComponent :milestones="this.milestones" />
        </div>
        <div class="modal-footer">
          <!-- <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary">Add</button> -->
        </div>
      </div>
    </div>
  </div>

  
  <div style="margin-left:auto; margin-right:auto; width: 80%;">
    <div class="btn-group mb-3" style="text-align: left;" role="group" aria-label="Basic radio toggle button group">
    <input type="radio" @click="this.showOpen = true; this.showClosed = false;" class="btn-check" name="btnradio" id="btnradio1" autocomplete="off" :checked="this.showOpen">
    <label class="btn btn-outline-primary" for="btnradio1">Open issues</label>

    <input type="radio" @click="this.showOpen = false; this.showClosed = true;" class="btn-check" name="btnradio" id="btnradio2" autocomplete="off" :checked="this.showClosed">
    <label class="btn btn-outline-primary" for="btnradio2">Closed issues</label>

    <input type="radio" @click="this.showOpen = true; this.showClosed = true;" class="btn-check" name="btnradio" id="btnradio3" autocomplete="off" :checked="this.showOpen && this.showClosed">
    <label class="btn btn-outline-primary" for="btnradio3">All issues</label>
  </div>
  <div v-if="this.showOpen">
    <table class="mt-3" style="margin-left:auto; margin-right:auto; width: 100%;">
      <tr colspan="9">
        <span font-size="28px" font-weight="bold" style="color: #ffffff">Open issues {{ this.filteredOpenIssues.length }}</span>
        <hr>
      </tr>
      <tr colspan="9">
        <IssueList :issueList="this.filteredOpenIssues" :isOpen="true" :milestones="this.milestones" @closeIssueInList="closeIssueInList" @deleteIssueFromList="deleteIssueFromList" />
      </tr>
      <tr>
        <td colspan="9">
          <button type="button" data-bs-toggle="modal" data-bs-target="#exampleModalAdd"
            class="flex-item btn btn-info text-center">Open new issue</button>
        </td>
      </tr>
    </table>

  </div>
  <div v-if="this.showClosed">
    <table class="mt-3" style="margin-left:auto; margin-right:auto; width: 100%;">
      <tr>
        <span font-size="28px" font-weight="bold" style="color:white;">Closed issues {{ this.filteredClosedIssues.length }}</span>
        <hr>
      </tr>
      <tr>
        <IssueList :issueList="this.filteredClosedIssues" :isOpen="false" :milestones="this.milestones" @closeIssueInList="closeIssueInList" @deleteIssueFromList="deleteIssueFromList" />
      </tr>
    </table>

  </div>
  </div>
  </div>
</template>
<script>
import RepoNavbar from '@/components/repository/RepoNavbar.vue'
import AddIssueComponent from './modals/AddIssueComponent.vue';
import IssueList from './IssueList.vue';
import IssueService from '@/services/IssueService';
import MilestoneService from '@/services/MilestoneService';

import { toast } from 'vue3-toastify';
export default {
  name: 'ListIssueComponent',
  components: {
    AddIssueComponent,
    RepoNavbar,
    IssueList
  },
  mounted() {
    IssueService.getIssues(this.$route.params.username, this.$route.params.repoName).then(res => {
      this.issues = res.data;
      this.allIssues = res.data;
      this.filteredOpenIssues = this.filterOpenIssues();
      this.filteredClosedIssues = this.filterClosedIssues();
    }).catch(err => { console.log(err); });
    MilestoneService.getAllMilestones(this.$route.params.username, this.$route.params.repoName).then(res => {
      this.milestones = res.data;
    }).catch(err => console.log(err));
  },
  data() {
    return {
      showOpen: true,
      showClosed: false,

      issueFilter: '',

      issues: [],
      allIssues: [],
      filteredOpenIssues: [],
      filteredClosedIssues: [],
      milestones: [],
      toastSuccess: {
        autoClose: 1000,
        type: 'success',
        position: toast.POSITION.BOTTOM_RIGHT
      },
      toastFailed: {
        autoClose: 1000,
        type: 'error',
        position: toast.POSITION.BOTTOM_RIGHT
      }
    }
  },
  methods: {
    doFilter() {
      if (this.issueFilter == '' || this.issueFilter == null || this.issueFilter == undefined) {
        this.issues = this.allIssues;
      } else {
        this.issues = this.allIssues.filter((issue) => issue.title.toLowerCase().includes(this.issueFilter.toLowerCase()) || issue.description.toLowerCase().includes(this.issueFilter.toLowerCase()))
      }
      this.filteredOpenIssues = this.filterOpenIssues();
      this.filteredClosedIssues = this.filterClosedIssues();

    },
    filterOpenIssues() {
      return this.issues.filter((issue) => issue.open);
    },
    filterClosedIssues() {
      return this.issues.filter((issue) => !issue.open)
    },
    closeIssueInList(id) {
      this.allIssues.forEach((el) => {
        if (el.id === id) {
          el.open = false;
        }
      });
      this.doFilter();
    },  
    deleteIssueFromList(id) {
      this.allIssues = this.allIssues.filter((el) => el.id != id);
      this.doFilter();
    }
  }
}
</script>
<style scoped>
thead th {
  background-color: #e9ecef;
}
button:hover {
  color: white;
}
button {
  color: white;
}
.bg {
  background-color: #2c333b;
}
</style>