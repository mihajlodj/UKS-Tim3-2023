import api from '../api'

const get_diff = (username, repoName, sha) => {
    return api.get(`commit/diff/${username}/${repoName}/${sha}/`);
}

const get_info = (username, repoName, sha) => {
    return api.get(`commit/info/${username}/${repoName}/${sha}/`);
}

export default { get_diff, get_info };
