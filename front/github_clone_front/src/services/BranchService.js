import api from '../api'

const getAllBranches = (username, repoName) => {
    return api.get(`branch/all/${username}/${repoName}/`);
}

const createBranch = (ownerUsername, createdBy, repoName, data) => {
    return api.post(`branch/create/${ownerUsername}/${createdBy}/${repoName}/`, data);
}

const deleteBranch = (username, repoName, branchName) => {
    return api.delete(`branch/delete/${username}/${repoName}/${branchName}/`);
}

const getCommits = (username, repoName, branchName) => {
    return api.get(`branch/commits/${username}/${repoName}/${branchName}`);
}

const getCommitters = (username, repoName, branchName) => {
    return api.get(`branch/committers/${username}/${repoName}/${branchName}`);
}

export default { getAllBranches, createBranch, deleteBranch, getCommits, getCommitters }