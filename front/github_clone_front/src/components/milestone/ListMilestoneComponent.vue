<template>
  <div>
    <RepoNavbar starting="milestones" />
  </div>
  <!-- Modal add -->
  <div class="modal fade" id="exampleModalAdd" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
    aria-hidden="true" >
    <div class="modal-dialog" role="document" style="background-color: #24292e; border: 2px solid;">
      <div class="modal-content" style="background-color: #24292e;">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel" style="color: beige">Create new milestone</h5>
          <button type="button" id="addModalCloseId" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <AddMilestoneComponent @milestoneAdded="milestoneAdded"/>
        </div>
      </div>
    </div>
  </div>
  <!-- Modal edit -->
  <div  class="modal fade" id="exampleModalUpdate" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
    aria-hidden="true">
    <div class="modal-dialog" role="document" style="background-color: #24292e; border: 2px solid;">
      <div class="modal-content" style="background-color: #24292e;">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel" style="color: beige">Update milestone</h5>
          <button type="button" id="editModalCloseId" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <UpdateMilestoneComponent :selectedMilestone="selectedMilestone" @milestoneUpdated="milestoneUpdated" v-if="selectedMilestone !== null" />
        </div>
      </div>
    </div>
  </div>

  <div style="background-color: #24292e;">
    <div class="container w-75 pt-4" style="background-color: #24292e;">
      <div class="d-flex justify-content-between">
        <h3 style="color: beige;">Milestones</h3>
        <button v-if="canModifyMilestones()" type="button" data-bs-toggle="modal" data-bs-target="#exampleModalAdd" class="btn btn-create">
          Create new milestone
        </button>
      </div>
    </div>
    <div style="background-color: #24292e;">
      <table class="tg mt-5"
        style="margin-left:auto;margin-right:auto; border-radius: 10px; background-color: #24292e;">
        <thead style="background-color: #24292e;">
          <tr style="background-color: #24292e;">
            <th class="tg-lboi" style="background-color: #24292e; color: beige;">Title</th>
            <th class="tg-lboi" style="background-color: #24292e; color: beige;">Due date</th>
            <th class="tg-lboi" style="background-color: #24292e; color: beige;">State</th>
            <th class="tg-lboi" style="background-color: #24292e;"></th>
            <th class="tg-lboi" style="background-color: #24292e;"></th>
          </tr>
        </thead>
        <tbody style="background-color: #24292e;">
          <tr v-for="(item, index) in this.milestones" :key="index">
            <td class="tg-c7q8">{{ item.title }}</td>
            <td class="tg-c7q8">{{ item.due_date }}</td>
            <td class="tg-c7q8">{{ item.state }}</td>
            <td class="tg-c7q8">
              <button v-if="canModifyMilestones()" type="button" class="btn btn-primary" data-bs-toggle="modal"
                data-bs-target="#exampleModalUpdate" @click="setSelectedMilestone(item)">Edit</button>
            </td>
            <td class="tg-c7q8">
              <button v-if="canModifyMilestones()" type="button" class="btn btn-danger" @click="deleteMilestone(item.title)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<script>
import RepoNavbar from '@/components/repository/RepoNavbar.vue'
import AddMilestoneComponent from '@/components/milestone/AddMilestoneComponent.vue';
import MilestoneService from '@/services/MilestoneService';
import UpdateMilestoneComponent from '@/components/milestone/UpdateMilestoneComponent.vue';

export default {
  name: 'ListIssueComponent',
  components: {
    AddMilestoneComponent,
    UpdateMilestoneComponent,
    RepoNavbar
  },
  mounted() {
    this.getAllMilestonesForRepo();
  },
  data() {
    return {
      repo: this.$route.params.repoName,
      milestones: [],
      selectedMilestone: null,
    }
  },
  methods: {
    getAllMilestonesForRepo() {
      MilestoneService.getAllMilestones(this.$route.params.username, this.repo)
        .then(res => {
          this.milestones = res.data;
        }).catch(err => {
          console.log(err);
        })
    },
    setSelectedMilestone(milestone) {
      this.selectedMilestone = milestone;
    },
    deleteMilestone(milestone_title) {
      let username = localStorage.getItem("username");
      MilestoneService.deleteMilestone(username, this.repo, milestone_title)
        .then(res => {
          console.log(res);
          this.getAllMilestonesForRepo();
        }).catch(err => {
          console.log(err);
        });
    },
    milestoneAdded() {
      this.closeAddModal();
      this.getAllMilestonesForRepo();
    },
    closeAddModal() {
      document.getElementById('addModalCloseId').click();
    },
    milestoneUpdated() {
      this.closeUpdateModal();
      this.selectedMilestone = null;
      this.getAllMilestonesForRepo();
    },
    closeUpdateModal() {
      document.getElementById('editModalCloseId').click();
    },

    canModifyMilestones() {
      const role = localStorage.getItem(this.$route.params.repoName);
      return role === "Owner" || role === "Developer" || role === "Maintainer";
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
  color: beige;
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
  /* border-color: inherit; */
  text-align: center;
  vertical-align: middle
}

.tg .tg-c7q8 {
  text-align: center;
  vertical-align: middle;
  padding: 3em;
}

.btn-create,
.btn-create:hover {
  color: white;
  background-color: #20883d;
  height: 90%;
}

.dark-color {
  background-color: #24292e;
}
</style>
