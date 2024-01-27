import api from '../api'

const create = (repoData) => {
    return api.post("repository/", repoData);
}

export default { create };