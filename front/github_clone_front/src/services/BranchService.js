import api from '../api'

const getAllBranches = (username, repoName) => {
    return api.get(`branch/all/${username}/${repoName}/`);
}

export default { getAllBranches }