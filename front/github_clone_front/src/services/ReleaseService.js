import api from '../api'

const createRelease = (ownerUsername, repoName, new_release) => {
    return api.post(`/release/${ownerUsername}/${repoName}/create/`, new_release);
}

const getReleases = (ownerUsername, repoName) => {
    return api.get(`/release/${ownerUsername}/${repoName}/releases/`);
}

const deleteRelease = (ownerUsername, repoName, tagName) => {
    return api.delete(`/release/delete/${ownerUsername}/${repoName}/${tagName}/`);
}

const updateRelease = (ownerUsername, repoName, updatedRelease) => {
    return api.patch(`/release/update/${ownerUsername}/${repoName}/`, updatedRelease);
}

const getReleaseById = (ownerUsername, repoName, id) => {
    return api.get(`/release/${ownerUsername}/${repoName}/${id}}/`);
}

const getReleaseByTagName = (ownerUsername, repoName, tagName) => {
    return api.post(`/release/get/${ownerUsername}/${repoName}/${tagName}/`);
}

export default { createRelease, getReleases, deleteRelease, updateRelease, getReleaseById, getReleaseByTagName };