import api from '../api'

const create = (repoData) => {
    return api.post("repository/", repoData);
}

const get = (username, repoName) => {
    return api.get(`repository/${username}/${repoName}`);
}

const getOwner = (username) => {
    return api.get(`repository/owner/${username}`);
}

export default { create, get, getOwner };