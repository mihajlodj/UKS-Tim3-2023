import api from '../api'

const create = (username, repoName, data) => {
    return api.post(`pr/create/${username}/${repoName}/`, data);
}

export default { create };