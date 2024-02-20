import api from '../api'

const create = (username, repoName, data) => {
    return api.post(`pr/create/${username}/${repoName}/`, data);
}

const getAll = (repoName) => {
    return api.get(`pr/get_all/${repoName}/`);
}

const getOne = (repoName, pullId) => {
    return api.get(`pr/get/${repoName}/${pullId}/`);
}

const getPossibleAssignees = (repoName) => {
    return api.get(`pr/assignees/${repoName}/`);
}

export default { create, getAll, getOne, getPossibleAssignees };