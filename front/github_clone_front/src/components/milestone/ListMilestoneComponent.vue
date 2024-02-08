<template>
    <div>
      <RepoNavbar starting="issues" />
    </div>
    <!-- Modal add -->
    <div class="modal fade" id="exampleModalAdd" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
      aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="exampleModalLabel">Create new milestone</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <AddMilestoneComponent />
          </div>
          <div class="modal-footer">
          </div>
        </div>
      </div>
    </div>
    <!-- Modal edit -->
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
            <UpdateIssueComponent title="" description="" id="" />
          </div>
          <div class="modal-footer">
            <!-- <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary">Add</button> -->
          </div>
        </div>
      </div>
    </div>
    <div>
      <table class="tg mt-5 bg-light" style="margin-left:auto;margin-right:auto; border-radius: 10px;">
        <thead>
          <tr>
            <th class="tg-lboi">Title</th>
            <th class="tg-lboi">Due date</th>
            <th class="tg-lboi">State</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in this.milestones" :key="index">
            <td class="tg-c7q8">{{ item.title }}</td>
            <td class="tg-c7q8">{{ item.due_date }}</td>
            <td class="tg-c7q8">{{ item.state }}</td>
            <td class="tg-c7q8">
              <button type="button" class="btn btn-primary"  data-bs-toggle="modal" data-bs-target="#exampleModalUpdate">Edit</button>
            </td>
            <td class="tg-c7q8">
              <button type="button" class="btn btn-danger"  @click="(e) => { }">Delete</button>
            </td>
          </tr>
          <tr>
            <td colspan="7">
              <button type="button" data-bs-toggle="modal" data-bs-target="#exampleModalAdd"
                class="flex-item btn btn-info text-center">Create new milestone</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
<script>
import RepoNavbar from '@/components/repository/RepoNavbar.vue'
import AddMilestoneComponent from '@/components/milestone/AddMilestoneComponent.vue';
import MilestoneService from '@/services/MilestoneService';
// import UpdateIssueComponent from './modals/UpdateIssueComponent.vue';
export default {
  name: 'ListIssueComponent',
  components: {
    AddMilestoneComponent,
    // UpdateIssueComponent,
    RepoNavbar
  },
  mounted() {
    this.getAllMilestonesForRepo();
  },
  data() {
    return {
      repo: this.$route.params.repoName,
      milestones: []
    }
  },
  methods: {
    getAllMilestonesForRepo() {
      MilestoneService.getAllMilestones(this.repo)
      .then(res => {
        this.milestones = res.data;
      }).catch(err => {
        console.log(err);
      })
    },
    edit() {
    //   IssueService.updateIssue({}).then((res) => console.log(res)).catch((err) => console.log(err));
    },
    add() {
    //   IssueService.createIssue({}).then((res) => console.log(res)).catch((err) => console.log(err));
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
  vertical-align: middle;
  padding: 3em;
}

button {
  color: white;
}
</style>
