import api from '../api'

const getAllLabels = (username, repoName) => {
    return api.get(`label/all/${username}/${repoName}/`);
}

const createLabels = (username, repoName, data) => {
    return api.post(`label/create/${username}/${repoName}/`, data);
}

const updateLabel = (username, repoName, labelId, data) => {
    return api.patch(`label/update/${username}/${repoName}/${labelId}/`, data);
}

const deleteLabel = (username, repoName, labelId) => {
    return api.delete(`label/delete/${username}/${repoName}/${labelId}/`);
}

const linkLabelAndMilestone = (username, repoName, labelId, milestoneId) => {
    return api.put(`label/link/milestone/${username}/${repoName}/${labelId}/${milestoneId}/`);
}

const linkLabelAndIssue = (username, repoName, labelId, issueId) => {
    return api.put(`label/link/issue/${username}/${repoName}/${labelId}/${issueId}/`);    
}

const linkLabelAndPullRequest = (username, repoName, labelId, pullRequestId) => {
    return api.put(`label/link/pull_request/${username}/${repoName}/${labelId}/${pullRequestId}/`);    
}

export default { getAllLabels, createLabels, updateLabel, deleteLabel, 
    linkLabelAndMilestone, linkLabelAndIssue, linkLabelAndPullRequest }
