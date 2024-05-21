import api from '../api'

const get_diff = (username, repoName, sha) => {
    return api.get(`commit/diff/${username}/${repoName}/${sha}/`);
}

const get_info = (username, repoName, branch, sha) => {
    return api.get(`commit/info/${username}/${repoName}/${branch}/${sha}/`);
}

export default { get_diff, get_info };
