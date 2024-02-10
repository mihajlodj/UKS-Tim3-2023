import api from '../api'

const createMilestone = (repoName, data) => {
    return api.post(`milestone/create/${repoName}/`, data);
}

const editMilestone = (title, data) => {
    return api.patch(`milestone/update/${title}/`, data);
}

const deleteMilestone = (username, repo_name, milestone_title) => {
    return api.delete(`milestone/delete/${username}/${repo_name}/${milestone_title}/`);
}

const getAllMilestones = (repoName) => {
    return api.get(`milestone/all/${repoName}/`);
}

export default {createMilestone, editMilestone, deleteMilestone, getAllMilestones}