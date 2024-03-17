import api from '../api'

const get_diff = (repoName, sha) => {
    return api.get(`commit/diff/${repoName}/${sha}/`);
}

export default { get_diff };
