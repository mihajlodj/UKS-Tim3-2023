import api from '../api'

const getAllBranches = (username, repoName) => {
    return api.get(`branch/all/${username}/${repoName}/`);
}

const createBranch = (createdBy, repoName, data) => {
    return api.post(`branch/create/${createdBy}/${repoName}/`, data);
}

export default { getAllBranches, createBranch }