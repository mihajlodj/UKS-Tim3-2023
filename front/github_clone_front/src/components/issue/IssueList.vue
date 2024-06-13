<template>
  <table class="table" style="margin-left:auto;margin-right:auto; border-radius: 10px;">
    <thead class="thead-dark">
      <tr>
        <th>Title</th>
        <th>Description</th>
        <th>Created</th>
        <th>Managing developer</th>
        <th>Milestone</th>
        <th colspan="4"></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, index) in this.issueList" :key="index">
        <td>{{ item.title }}</td>
        <td>{{ item.description }}</td>
        <td>{{ this.formatDate(item.created) }}</td>
        <td>{{ (item.manager === undefined || item.manager.length === 0) ? 'None' : item.manager[0] + ',...' }}</td>
        <td>{{ item.milestone == undefined ? 'None' : item.milestone.title }}</td>
        <td>
          <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModalUpdate"
            @click="this.setProps(index, this.issueList)">Edit</button>
        </td>
        <td>
          <button type="button" class="btn btn-success" @click="goToIssueDetails(item)">
            Details
          </button>
        </td>
        <td>
          <button type="button" class="btn btn-warning" @click="this.close(item.id)"
            :disabled="!this.isOpen">Close</button>
        </td>
        <td>
          <button type="button" class="btn btn-danger" @click="this.delete(item.id)">Delete</button>
        </td>
      </tr>
    </tbody>
  </table>

  <!-- Modal edit -->
  <div class="modal fade" id="exampleModalUpdate" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
    aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Update issue</h5>
        </div>
        <div class="modal-body">
          <UpdateIssueComponent :title="this.propTitle" :description="this.propDescription" :id="this.propId"
            :milestone="this.propMilestone" @updateIssue="edit" @propModified="updateMilestone"
            @updateTitle="((val) => this.propTitle = val)" :allMilestones="this.milestones"
            @updateDescription="((val) => this.propDescription = val)" />
        </div>
        <div class="modal-footer">
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import UpdateIssueComponent from './modals/UpdateIssueComponent.vue';
import IssueService from '@/services/IssueService';
import { toast } from 'vue3-toastify';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';

export default {
  name: 'IssueList',
  props: ['issueList', 'isOpen', 'milestones'],
  components: {
    UpdateIssueComponent
  },
  mounted() {

  },
  data() {
    return {
      propIndex: 0,
      propTitle: '',
      propDescription: '',
      propMilestone: '',
      propId: 0,
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
    edit() {
      let updatedIssue = {
        id: this.propId,
        title: this.propTitle,
        description: this.propDescription,
        milestone: this.propMilestone.id,
        project: this.$route.params.repoName
      }
      IssueService.updateIssue(updatedIssue)
        .then((res) => {
          console.log(res);
          location.reload();
          toast("Issue updated", this.toastSuccess);
        }).catch((err) => {
          console.log(err);
          toast("Issue update failed", this.toastFailed);
        });
    },
    setProps(index, issuesList) {
      this.propIndex = index;
      this.propId = issuesList[index].id;
      this.propTitle = issuesList[index].title;
      this.propDescription = issuesList[index].description;
      this.propMilestone = issuesList[index].milestone;
    },
    goToIssueDetails(issue) {
      let username = this.$route.params.username;
      let repoName = this.$route.params.repoName;
      let issue_id = issue.id;
      let route = '/view/' + username + '/' + repoName + '/issues/' + issue_id;

      this.$router.push(route);

    },
    close(id) {
      IssueService.closeIssue(this.$route.params.repoName, id).then((res) => {
        console.log(res);
        this.$emit("closeIssueInList", id);
        toast("Issue updated", this.toastSuccess);
      }).catch((err) => {
        console.log(err);
        toast("Issue closure failed", this.toastFailed);
      });
    },
    delete(id) {
      IssueService.deleteIssue(this.$route.params.repoName, id).then((res) => {
        console.log(res);
        this.$emit("deleteIssueFromList", id);
        toast("Issue deleted", this.toastSuccess);
      }).catch((err) => {
        console.log(err);
        toast("Issue deletion failed", this.toastFailed);
      });
    },
    updateMilestone(modifiedValue) {
      this.propMilestone = modifiedValue;
      // this.issueList[this.propIndex].milestone = modifiedValue;
    },
    formatDate(date) {
      dayjs.extend(utc);
      // Parse the given date string using Day.js, considering it as UTC time
      const parsedDate = dayjs.utc(date);

      // Format the parsed date into the desired format
      return parsedDate.format('DD.MM.YYYY.');
    },
  }

}

</script>

<style scoped>
button {
  color: white;
}

table thead tr th {
  background-color: #22272d;

}

table tbody tr td {
  background-color: #22272d;
}

.table th,
.table td {
  border: none;
  color: #ffffff;
}

.table thead {
  background-color: #22272d;
}

.table thead th {
  border: none;
  color: #ffffff;
}

.table tbody tr {
  border: none;
  color: #ffffff;
}

.table tbody td {
  border: none;
  color: #ffffff;
}
</style>