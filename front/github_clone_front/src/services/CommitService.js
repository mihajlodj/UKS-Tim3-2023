import api from '../api'

const get_diff = (repoName, sha) => {
    return api.get(`commit/diff/${repoName}/${sha}/`);
}

const get_info = (repoName, sha) => {
    return api.get(`commit/info/${repoName}/${sha}/`);
}

export default { get_diff, get_info };
