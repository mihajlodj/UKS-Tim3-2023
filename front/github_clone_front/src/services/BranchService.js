import api from '../api'

const getAllBranches = (username, repoName) => {
    return api.get(`branch/all/${username}/${repoName}/`);
}

const createBranch = (createdBy, repoName, data) => {
    return api.post(`branch/create/${createdBy}/${repoName}/`, data);
}

const deleteBranch = (username, repoName, branchName) => {
    return api.delete(`branch/delete/${username}/${repoName}/${branchName}/`);
}

const getCommits = (repoName, branchName) => {
    return api.get(`branch/commits/${repoName}/${branchName}`);
}

const getCommitters = (repoName, branchName) => {
    return api.get(`branch/committers/${repoName}/${branchName}`);
}

export default { getAllBranches, createBranch, deleteBranch, getCommits, getCommitters }