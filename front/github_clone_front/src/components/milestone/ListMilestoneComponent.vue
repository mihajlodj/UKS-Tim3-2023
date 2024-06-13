<template>
	<div>
		<RepoNavbar starting="milestones" />
	</div>
	<!-- Modal add -->
	<div class="modal fade" id="exampleModalAdd" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
		aria-hidden="true">
		<div class="modal-dialog" role="document" style="background-color: #24292e; border: 2px solid;">
			<div class="modal-content" style="background-color: #24292e;">
				<div class="modal-header">
					<h5 class="modal-title" id="exampleModalLabel" style="color: beige">Create new milestone</h5>
					<button type="button" id="addModalCloseId" class="btn-close" data-bs-dismiss="modal"
						aria-label="Close"></button>
				</div>
				<div class="modal-body">
					<AddMilestoneComponent @milestoneAdded="milestoneAdded" />
				</div>
			</div>
		</div>
	</div>
	<!-- Modal edit -->
	<div class="modal fade" id="exampleModalUpdate" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
		aria-hidden="true">
		<div class="modal-dialog" role="document" style="background-color: #24292e; border: 2px solid;">
			<div class="modal-content" style="background-color: #24292e;">
				<div class="modal-header">
					<h5 class="modal-title" id="exampleModalLabel" style="color: beige">Update milestone</h5>
					<button type="button" id="editModalCloseId" class="btn-close" data-bs-dismiss="modal"
						aria-label="Close"></button>
				</div>
				<div class="modal-body">
					<UpdateMilestoneComponent :selectedMilestone="selectedMilestone"
						@milestoneUpdated="milestoneUpdated" v-if="selectedMilestone !== null" />
				</div>
			</div>
		</div>
	</div>

	<div style="background-color: #24292e; height: 100vh;">
		<div class="container w-75 pt-4" style="background-color: #24292e;">
			<div class="d-flex justify-content-between">
				<h3 style="color: beige;">Milestones</h3>
				<button v-if="canModifyMilestones()" type="button" data-bs-toggle="modal"
					data-bs-target="#exampleModalAdd" class="btn btn-create">
					Create new milestone
				</button>
			</div>
		</div>

		<div class="container w-75 pt-4" style="margin-left:auto; margin-right:auto; width: 80%;">
			<div class="btn-group mb-3" style="text-align: left;" role="group"
				aria-label="Basic radio toggle button group">
				<input type="radio" @click="this.showOpen = true; this.showClosed = false;" class="btn-check"
					name="btnradio" id="btnradio1" autocomplete="off" :checked="this.showOpen">
				<label class="btn btn-outline-primary" for="btnradio1">Open milestones</label>

				<input type="radio" @click="this.showOpen = false; this.showClosed = true;" class="btn-check"
					name="btnradio" id="btnradio2" autocomplete="off" :checked="this.showClosed">
				<label class="btn btn-outline-primary" for="btnradio2">Closed milestones</label>

				<input type="radio" @click="this.showOpen = true; this.showClosed = true;" class="btn-check"
					name="btnradio" id="btnradio3" autocomplete="off" :checked="this.showOpen && this.showClosed">
				<label class="btn btn-outline-primary" for="btnradio3">All milestones</label>
			</div>
			<div v-if="this.showOpen">
				<table class="mt-3" style="margin-left:auto; margin-right:auto; width: 100%;">
					<tr colspan="9">
						<span font-size="28px" font-weight="bold" class="bright">Open milestones: {{
						this.filteredOpenMilestones?.length }}</span>
						<hr>
					</tr>
					<tr colspan="9">

						<!-- Table for displaying open milestones -->
						<table class="table" style="margin-left:auto;margin-right:auto; border-radius: 10px;"
							v-if="this.filteredOpenMilestones?.length !== 0">
							<thead class="thead-dark">
								<tr>
									<th>Title</th>
									<th>Description</th>
									<th>Due date</th>
									<th>State</th>
									<th colspan="4"></th>
								</tr>
							</thead>
							<tbody>
								<tr v-for="(item, index) in this.filteredOpenMilestones" :key="index">
									<td>{{ item.title }}</td>
									<td>{{ item.description }}</td>
									<td>{{ this.formatDate(item.due_date) }}</td>
									<td>{{ item.state }}</td>
									<td>
										<button v-if="canModifyMilestones()" type="button" class="btn btn-primary"
											data-bs-toggle="modal" data-bs-target="#exampleModalUpdate"
											@click="setSelectedMilestone(item)">Edit</button>
									</td>
									<td>
										<button type="button" class="btn btn-success"
											@click="goToMilestoneDetails(item)">
											Details
										</button>
									</td>
									<td>
										<button type="button" class="btn btn-warning" @click="this.close(item.id)"
											:disabled="item.state === 'Closed'">Close</button>
									</td>
									<td>
										<button v-if="canModifyMilestones()" type="button" class="btn btn-danger"
											@click="deleteMilestone(item.title)">Delete</button>
									</td>
								</tr>
							</tbody>
						</table>
					</tr>
				</table>

			</div>
			<div v-if="this.showClosed">

				<!-- Table for displaying closed milestones -->
				<table class="mt-3" style="margin-left:auto; margin-right:auto; width: 100%;">
					<tr>
						<span font-size="28px" font-weight="bold" class="bright">Closed milestones: {{
						this.filteredClosedMilestones?.length }}</span>
						<hr>
					</tr>
					<tr>
						<table class="table" style="margin-left:auto;margin-right:auto; border-radius: 10px;"
							v-if="this.filteredClosedMilestones?.length !== 0">
							<thead class="thead-dark">
								<tr>
									<th>Title</th>
									<th>Description</th>
									<th>Due date</th>
									<th>State</th>
									<th colspan="4"></th>
								</tr>
							</thead>
							<tbody>
								<tr v-for="(item, index) in this.filteredClosedMilestones" :key="index">
									<td>{{ item.title }}</td>
									<td>{{ item.description }}</td>
									<td>{{ this.formatDate(item.due_date) }}</td>
									<td>{{ item.state }}</td>
									<td>
										<button v-if="canModifyMilestones()" type="button" class="btn btn-primary"
											data-bs-toggle="modal" data-bs-target="#exampleModalUpdate"
											@click="setSelectedMilestone(item)">Edit</button>
									</td>
									<td>
										<button type="button" class="btn btn-success"
											@click="goToMilestoneDetails(item)">
											Details
										</button>
									</td>
									<td>
										<button type="button" class="btn btn-warning" @click="this.close(item.id)"
											:disabled="item.state === 'Closed'">Close</button>
									</td>
									<td>
										<button v-if="canModifyMilestones()" type="button" class="btn btn-danger"
											@click="deleteMilestone(item.title)">Delete</button>
									</td>
								</tr>
							</tbody>
						</table>
					</tr>
				</table>

			</div>
		</div>
	</div>
</template>
<script>
import RepoNavbar from '@/components/repository/RepoNavbar.vue'
import AddMilestoneComponent from '@/components/milestone/AddMilestoneComponent.vue';
import MilestoneService from '@/services/MilestoneService';
import UpdateMilestoneComponent from '@/components/milestone/UpdateMilestoneComponent.vue';

import { toast } from 'vue3-toastify';
import dayjs from 'dayjs';
import utc from 'dayjs/plugin/utc';

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
			showOpen: true,
			showClosed: false,

			repo: this.$route.params.repoName,
			milestones: [],
			filteredOpenMilestones: [],
			filteredClosedMilestones: [],
			selectedMilestone: null,
		}
	},
	methods: {
		getAllMilestonesForRepo() {
			MilestoneService.getAllMilestones(this.$route.params.username, this.repo)
				.then(res => {
					this.milestones = res.data;
					this.filteredOpenMilestones = this.filterOpenMilestones();
					this.filteredClosedMilestones = this.filterClosedMilestones();
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
		},

		goToMilestoneDetails(milestone) {
			let username = this.$route.params.username;
			let repoName = this.$route.params.repoName;
			let milestone_id = milestone.id;
			let route = '/view/' + username + '/' + repoName + '/milestones/' + milestone_id;

			this.$router.push(route);
		},

		close(milestone_id) {
			MilestoneService.closeMilestone(this.$route.params.username, this.repo, milestone_id)
				.then(res => {
					console.log(res);
					toast("Milestone closed!", {
						autoClose: 500,
						type: 'success',
						position: toast.POSITION.BOTTOM_RIGHT,
						theme: toast.THEME.DARK
					});
					this.getAllMilestonesForRepo();
				})
				.catch(err => {
					console.log(err);
					toast("Milestone closure failed.", {
						autoClose: 1000,
						type: 'error',
						position: toast.POSITION.BOTTOM_RIGHT,
						theme: toast.THEME.DARK
					});
				});
		},

		filterOpenMilestones() {
			return this.milestones.filter((milestone) => milestone.state === 'Open');
		},
		filterClosedMilestones() {
			return this.milestones.filter((milestone) => milestone.state !== 'Open');
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
thead th {
	background-color: #e9ecef;
}

button:hover {
	color: white;
}

button {
	color: white;
}

.bright {
	color: #ffffff;
}

button {
	color: white;
}

table thead tr th {
	background-color: #24292e;

}

table tbody tr td {
	background-color: #24292e;
}

.table th,
.table td {
	border: none;
	color: #ffffff;
}

.table thead {
	background-color: #24292e;
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

.btn-create,
.btn-create:hover {
	color: white;
	background-color: #20883d;
	height: 90%;
}
</style>
