import api from '../api'

const createMilestone = (username, repoName, data) => {
    return api.post(`milestone/create/${username}/${repoName}/`, data);
}

const editMilestone = (username, title, data) => {
    return api.patch(`milestone/update/${username}/${title}/`, data);
}

const deleteMilestone = (username, repo_name, milestone_title) => {
    return api.delete(`milestone/delete/${username}/${repo_name}/${milestone_title}/`);
}

const getAllMilestones = (username, repoName) => {
    return api.get(`milestone/all/${username}/${repoName}/`);
}

const getOneMilestone = (username, repoName, milestone_id) => {
    return api.get(`milestone/one/${username}/${repoName}/${milestone_id}/`);
}

const closeMilestone = (username, repoName, milestone_id) => {
    return api.patch(`milestone/close/${username}/${repoName}/${milestone_id}/`);
}

const reOpenMilestone = (username, repoName, milestone_id) => {
    return api.patch(`milestone/reopen/${username}/${repoName}/${milestone_id}/`);
}

export default { createMilestone, editMilestone, deleteMilestone, getAllMilestones, getOneMilestone, closeMilestone, reOpenMilestone }