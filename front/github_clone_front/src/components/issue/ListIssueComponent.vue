<template>
  <div>
    <RepoNavbar starting="issues" />
  </div>
  <div class="input-group mb-3">
    <span class="input-group-text" id="basic-addon1">Search:</span>
    <input @keydown="this.doFilter" :value="this.issueFilter" type="text" class="form-control" placeholder="Issue name" aria-label="Issue name" aria-describedby="basic-addon1">
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
  <div class="modal fade" id="exampleModalUpdate" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
    aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Update issue</h5>
          <!-- <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span> -->
          <!-- </button> -->
        </div>
        <div class="modal-body">
          <UpdateIssueComponent :title="this.propTitle" :description="this.propDescription" :id="this.propId"
            @updateIssue="edit" @propModified="updateMilestone" @updateTitle="((val) => this.propTitle = val)"
            @updateDescription="((val) => this.propDescription = val)" />
        </div>
        <div class="modal-footer">
          <!-- <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary">Add</button> -->
        </div>
      </div>
    </div>
  </div>
  <div>
    <span font-size="28px" font-weight="bold">Open issues</span>
    <hr>
    <table class="tg mt-5 bg-light" style="margin-left:auto;margin-right:auto; border-radius: 10px;">
      <thead>
        <tr>
          <th class="tg-lboi">Title</th>
          <th class="tg-lboi">Description</th>
          <th class="tg-lboi">Created</th>
          <th class="tg-lboi">Managing developer</th>
          <th class="tg-lboi">Milestone</th>
          <th colspan="3" class="tg-lboi"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in this.filterOpenIssues()" :key="index">
          <td class="tg-c7q8">{{ item.title }}</td>
          <td class="tg-c7q8">{{ item.description }}</td>
          <td class="tg-c7q8">{{ item.created.slice(0, 10) }}</td>
          <td class="tg-c7q8">{{ item.manager }}</td>
          <td class="tg-c7q8">{{ item.milestone == undefined ? 'None' : item.milestone }}</td>
          <td class="tg-c7q8">
            <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModalUpdate"
              @click="setProps(index)">Edit</button>
          </td>
          <td class="tg-c7q8">
            <button type="button" class="btn btn-warning" @click="close(item.id)">Close</button>
          </td>
          <td class="tg-c7q8">
            <button type="button" class="btn btn-danger" @click="this.delete(item.id)">Delete</button>
          </td>
        </tr>
        <tr>
          <td colspan="7">
            <button type="button" data-bs-toggle="modal" data-bs-target="#exampleModalAdd"
              class="flex-item btn btn-info text-center">Open new issue</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
  <div>
    <span font-size="28px" font-weight="bold">Closed issues</span>
    <hr>
    <table class="tg mt-5 bg-light" style="margin-left:auto;margin-right:auto; border-radius: 10px;">
      <thead>
        <tr>
          <th class="tg-lboi">Title</th>
          <th class="tg-lboi">Description</th>
          <th class="tg-lboi">Created</th>
          <th class="tg-lboi">Managing developer</th>
          <th class="tg-lboi">Milestone</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in this.filterClosedIssues()" :key="index">
          <td class="tg-c7q8">{{ item.title }}</td>
          <td class="tg-c7q8">{{ item.description }}</td>
          <td class="tg-c7q8">{{ item.created.slice(0, 10) }}</td>
          <td class="tg-c7q8">{{ item.manager }}</td>
          <td class="tg-c7q8">{{ item.milestone == undefined ? 'None' : item.milestone }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<script>
import RepoNavbar from '@/components/repository/RepoNavbar.vue'
import AddIssueComponent from './modals/AddIssueComponent.vue';
import UpdateIssueComponent from './modals/UpdateIssueComponent.vue';
import IssueService from '@/services/IssueService';
import MilestoneService from '@/services/MilestoneService';
import { toast } from 'vue3-toastify';
export default {
  name: 'ListIssueComponent',
  components: {
    AddIssueComponent,
    UpdateIssueComponent,
    RepoNavbar
  },
  mounted() {
    IssueService.getIssues(this.$route.params.username, this.$route.params.repoName).then(res => {
      this.issues = res.data;
      this.allIssues = res.data;
      console.log(this.issues);
    }).catch(err => { console.log(err); });
    MilestoneService.getAllMilestones(this.$route.params.username, this.$route.params.repoName).then(res => {
      console.log(res);
      this.milestones = res.data;
    }).catch(err => console.log(err));
  },
  data() {
    return {
      issueFilter: '',
      propIndex: 0,
      propTitle: '',
      propDescription: '',
      propMilestone: '',
      propId: 0,
      issues: [],
      allIssues: [],
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
      if (this.issueFilter == '')
      {
        this.issues = this.allIssues;
        return;
      }
      this.issues = this.allIssues.filter((issue) => issue.title.includes(this.issueFilter) || issue.description.includes(this.issueFilter))
    },
    edit() {
      let updatedIssue = {
        id: this.propId,
        title: this.propTitle,
        description: this.propDescription,
        milestone: this.propMilestone,
        repoName: this.$route.params.repoName
      }
      IssueService.updateIssue(updatedIssue)
        .then((res) => {
          console.log(res);
          toast("Issue updated", this.toastSuccess);
          location.reload();
        }).catch((err) => {
          console.log(err);
          toast("Issue update failed", this.toastFailed);
        });
    },
    close(id) {
      IssueService.closeIssue(this.$route.params.repoName, id).then((res) => {
        console.log(res);
        toast("Issue updated", this.toastSuccess);
        location.reload()
      }).catch((err) => {
        console.log(err);
        toast("Issue closure failed", this.toastFailed);
      });
    },
    delete(id) {
      IssueService.deleteIssue(this.$route.params.repoName, id).then((res) => {
        console.log(res);
        toast("Issue deleted", this.toastSuccess);
        location.reload()
      }).catch((err) => {
        console.log(err);
        toast("Issue deletion failed", this.toastFailed);
      });
    },
    filterOpenIssues() {
      return this.issues.filter((issue) => issue.open)
    },
    filterClosedIssues() {
      return this.issues.filter((issue) => !issue.open)
    },
    setProps(index) {
      this.propIndex = index;
      this.propId = this.issues[index].id;
      this.propTitle = this.issues[index].title;
      this.propDescription = this.issues[index].description;
      this.propMilestone = this.issues[index].milestone;
    },
    updateMilestone(modifiedValue) {
      this.propMilestone = modifiedValue;
      this.issues[this.propIndex].milestone = modifiedValue;
    }
  }
}
</script>
<style scoped>
.tg {
  border-collapse: collapse;
  border-color: #bbb;
  border-spacing: 0;
  border-radius: 10px;
}

.tg td {
  border-color: #bbb;
  border-style: solid;
  border-bottom: 0px;
  color: #594F4F;
  font-family: Arial, sans-serif;
  font-size: 14px;
  overflow: hidden;
  padding: 10px 5px;
  word-break: normal;
}

.tg th {
  border-color: #bbb;
  border-style: solid;
  border-bottom: 0px;
  color: #493F3F;
  font-family: Arial, sans-serif;
  font-size: 14px;
  font-weight: normal;
  overflow: hidden;
  padding: 10px 5px;
  word-break: normal;
}

.tg .tg-cly1 {
  text-align: center;
  vertical-align: middle
}

.tg .tg-lboi {
  border-color: inherit;
  text-align: center;
  vertical-align: middle
}

.tg .tg-c7q8 {
  text-align: center;
  vertical-align: middle
}

button {
  color: white;
}
</style>