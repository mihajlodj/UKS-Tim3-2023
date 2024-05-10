<template>
  <div>
    <RepoNavbar starting="issues" />
  </div>
  <div class="input-group mb-3" width="200px">
    <span class="input-group-text" id="basic-addon1">Search:</span>
    <input v-on:keyup.enter="this.doFilter()" v-model="this.issueFilter" type="text" class="form-control" placeholder="Issue name"
      aria-label="Issue name" aria-describedby="basic-addon1">
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
          <UpdateIssueComponent :title="this.propTitle" :description="this.propDescription" :id="this.propId" :milestone="this.propMilestone"
            @updateIssue="edit" @propModified="updateMilestone" @updateTitle="((val) => this.propTitle = val)"
            :allMilestones="this.milestones"
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
    <table style="margin-left:auto; margin-right:auto; width: 80%;">
      <tr colspan="8">
        <span font-size="28px" font-weight="bold">Open issues</span>
        <hr>
      </tr>
      <tr colspan="8">
        <table class="table" style="margin-left:auto;margin-right:auto; border-radius: 10px;">
          <thead class="thead-dark">
            <tr>
              <th >Title</th>
              <th >Description</th>
              <th >Created</th>
              <th >Managing developer</th>
              <th >Milestone</th>
              <th colspan="4" ></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in this.filteredOpenIssues" :key="index">
              <td >{{ item.title }}</td>
              <td >{{ item.description }}</td>
              <td >{{ item.created.slice(0, 10) }}</td>
              <td >{{ item.manager }}</td>
              <td >{{ item.milestone == undefined ? 'None' : item.milestone.title }}</td>
              <td >
                <button type="button" class="btn btn-primary" data-bs-toggle="modal"
                  data-bs-target="#exampleModalUpdate" @click="this.setProps(index, this.filteredOpenIssues)">Edit</button>
              </td>
              <td>
                <button type="button" class="btn btn-success" @click="goToIssueDetails(item)">
                  Details
                </button>
              </td>
              <td >
                <button type="button" class="btn btn-warning" @click="this.close(item.id)">Close</button>
              </td>
              <td >
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
      </tr>
    </table>

  </div>
  <div>
    <table style="margin-left:auto; margin-right:auto; width: 80%;">
      <tr>
        <span font-size="28px" font-weight="bold">Closed issues</span>
        <hr>
      </tr>
      <tr>
        <table class="table" style="margin-left:auto;margin-right:auto; border-radius: 10px;">
          <thead class="thead-dark" >
            <tr >
              <th >Title</th>
              <th >Description</th>
              <th >Created</th>
              <th >Managing developer</th>
              <th >Milestone</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in this.filteredClosedIssues" :key="index">
              <td >{{ item.title }}</td>
              <td >{{ item.description }}</td>
              <td >{{ item.created.slice(0, 10) }}</td>
              <td >{{ item.manager }}</td>
              <td >{{ item.milestone == undefined ? 'None' : item.milestone.title }}</td>
              <td>
                <button type="button" class="btn btn-success" @click="goToIssueDetails(item)">
                  Details
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </tr>
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
    IssueService.getIssues(this.$route.params.ownerUsername, this.$route.params.repoName).then(res => {
      this.issues = res.data;
      this.allIssues = res.data;
      this.filteredOpenIssues = this.filterOpenIssues();
      this.filteredClosedIssues = this.filterClosedIssues();
      console.log(this.issues);
    }).catch(err => { console.log(err); });
    MilestoneService.getAllMilestones(this.$route.params.ownerUsername, this.$route.params.repoName).then(res => {
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
      if (this.issueFilter == '') {
        this.issues = this.allIssues;
        return;
      }
      this.issues = this.allIssues.filter((issue) => issue.title.includes(this.issueFilter) || issue.description.includes(this.issueFilter))
      this.filteredOpenIssues = this.filterOpenIssues();
      this.filteredClosedIssues = this.filterClosedIssues();
    },
    edit() {
      let updatedIssue = {
        id: this.propId,
        title: this.propTitle,
        description: this.propDescription,
        milestone: this.propMilestone,
        project: this.$route.params.repoName
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
      return this.issues.filter((issue) => issue.open);
    },
    filterClosedIssues() {
      return this.issues.filter((issue) => !issue.open)
    },
    setProps(index, issuesList) {
      this.propIndex = index;
      this.propId = issuesList[index].id;
      this.propTitle = issuesList[index].title;
      this.propDescription = issuesList[index].description;
      this.propMilestone = issuesList[index].milestone;
      console.log(this.propMilestone)
    },
    updateMilestone(modifiedValue) {
      this.propMilestone = modifiedValue;
      this.filteredOpenIssues[this.propIndex].milestone = modifiedValue;
    },
    goToIssueDetails(issue) {
      let username = this.$route.params.ownerUsername;
      let repoName = this.$route.params.repoName;
      let issue_id = issue.id;
      let route = '/view/' + username + '/' + repoName + '/issues/' + issue_id;

      this.$router.push(route);
      
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
</style>