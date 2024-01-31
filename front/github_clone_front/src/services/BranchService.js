import api from '../api'

const getAllBranches = (repoName) => {
    return api.get(`branch/all/${repoName}/`);
}

const createBranch = (createdBy, repoName, data) => {
    return api.post(`branch/create/${createdBy}/${repoName}/`, data);
}

const deleteBranch = (repoName, branchName) => {
    return api.delete(`branch/delete/${repoName}/${branchName}/`);
}

export default { getAllBranches, createBranch, deleteBranch }