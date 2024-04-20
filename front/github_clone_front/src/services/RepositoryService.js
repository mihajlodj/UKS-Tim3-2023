import api from '../api'

const create = (repoData) => {
    return api.post("repository/", repoData);
}

const get = (username, repoName) => {
    return api.get(`repository/data/${username}/${repoName}`);
}

const getAllQueryRepos = (query) => {
    return api.get(`repository/query_repos/${query}`);
}

const getAllUserRepos = (owner_username) => {
    return api.get(`repository/all_repos/${owner_username}`);
}

const getOwner = (username) => {
    return api.get(`repository/owner/${username}`);
}

const getIsUsersRepo = (username,repository) => {
    return api.get(`repository/is_users_repo/${username}/${repository}`);
}

const getRootContent = (username, repoName, refName) => {
    return api.get(`repository/content/${username}/${repoName}/${refName}/`);
}

const getFolderContent = (username, repoName, branch, path) => {
    return api.get(`repository/folder/${username}/${repoName}/${branch}/${path}/`);
}

const update = (repoData, name) => {
    return api.patch(`repository/update/${name}/`, repoData);
}

const deleteReposiory = (username, repoName) => {
    return api.delete(`repository/delete/${username}/${repoName}`);
}

const getFile = (username, repoName, branchName, path) => {
    return api.get(`repository/file/${username}/${repoName}/${branchName}/${path}/`);
}

const editFile = (username, repoName, path, data) => {
    return api.put(`repository/edit_file/${username}/${repoName}/${path}/`, data);
}

const deleteFile = (username, repoName, path, data) => {
    return api.put(`repository/delete_file/${username}/${repoName}/${path}/`, data);
}

const createFile = (username, repoName, path, data) => {
    return api.post(`repository/create_file/${username}/${repoName}/${path}/`, data);
}


const inviteCollaborator = (repoName, invitedUsername, role) => {
    return api.post(`repository/invite/${repoName}/${invitedUsername}/`, {'role': role});
}

const respondToInvitation = (ownerUsername, repoName, invitedUsername, choice) => {
    return api.post(`repository/inviteResponse/${ownerUsername}/${repoName}/${invitedUsername}/${choice}/`);
}

const getInvitation = (repoName, invitedUsername) => {
    return api.get(`repository/invitation/${repoName}/${invitedUsername}`);
}

const getCollaborators = (ownerUsername, repoName) => {
    return api.get(`repository/collaborators/${ownerUsername}/${repoName}`);
}

const removeCollaborator = (ownerUsername, repoName, collaboratorUsername) => {
    return api.delete(`repository/removeCollaborator/${ownerUsername}/${repoName}/${collaboratorUsername}`);
}

const changeRole = (ownerUsername, repoName, collaboratorUsername, role) => {
    return api.put(`repository/editRole/${ownerUsername}/${repoName}/${collaboratorUsername}/`, {'role': role});
}

const transfer = (ownerUsername, repoName, newOwnerUsername) => {
    return api.post(`repository/transfer/${ownerUsername}/${repoName}/`, {'new_owner': newOwnerUsername});
}

export default { getIsUsersRepo,getAllQueryRepos,create, get, getOwner, getRootContent, getFolderContent, update, deleteReposiory, getAllUserRepos, getFile,
    editFile, deleteFile, createFile, inviteCollaborator, respondToInvitation, getInvitation, getCollaborators, removeCollaborator, changeRole, transfer };
