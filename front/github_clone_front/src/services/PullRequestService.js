import api from '../api'

const create = (username, repoName, data) => {
    return api.post(`pr/create/${username}/${repoName}/`, data);
}

const getAll = (repoName) => {
    return api.get(`pr/get_all/${repoName}/`);
}

export default { create, getAll };