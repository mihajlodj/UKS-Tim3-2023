import api from '../api'

const getTags = (ownerUsername, repoName) => {
    return api.get(`/tag/${ownerUsername}/${repoName}/tags/`);
}

const deleteTag = (ownerUsername, repoName, tagId) => {
    return api.delete(`/tag/${ownerUsername}/${repoName}/tag/${tagId}`);
}


export default { getTags, deleteTag };