import api from '../api'


const update = (developerData, username) => {
    return api.patch(`developer/update/${username}/`, developerData);
}

const getAllQueryDevelopers = (query) => {
    return api.get(`developer/query_devs/${query}`);
}

const getAllQueryCommitts = (query) => {
    return api.get(`developer/query_commits/${query}`);
}

const deleteUser = (usersPassword, username) => {
    return api.delete(`developer/delete/self/${username}/${usersPassword}`);
}

const deleteEmailAddress = (usersEmail, username) => {
    return api.delete(`developer/delete/email/${username}/${usersEmail}`);
}

const deleteUsersAvatar = (username) => {
    return api.delete(`developer/delete/avatar/${username}`);
}

const addEmailAddress = (newEmail, username) => {
    return api.post(`developer/newEmail/${username}/`,newEmail);
}

const updateDeveloperAvatar = (developerData, username) => {
    return api.patch(`developer/updateAvatar/${username}/`, developerData);
}

const updateUsersPassword = (userData, username) => {
    return api.patch(`developer/update/password/${username}/`, userData);
}

const getUserBasicInfo = (username) => {
    return api.get(`developer/${username}`);
}

const getUserBasicInfoFromId = (id) => {
    return api.get(`developer/info/${id}`);
}

const getDeveloperBasicInfoFromId = (id) => {
    return api.get(`developer/info/developer/${id}`);
}

const getUserGiteaBasicInfo = (username) => {
    return api.get(`developer/gitea/${username}`);
}

const getUserAvatar = (username) => {
    console.log(username)
    return api.get(`developer/avatar/${username}`);
}

const getUsersEmails = (username) => {
    return api.get(`developer/emails/${username}`);
}

const getDevelopers = (username, repoName) => {
    return api.get(`developer/all/${username}/${repoName}`);
}

const getRoles = (username) => {
    return api.get(`developer/roles/${username}`);
}

const update_user_ban_status = (username) => {
    return api.patch(`developer/update_user_ban_status/${username}`);
}

export default { update, getUserBasicInfo, getUserBasicInfoFromId, getDeveloperBasicInfoFromId, getUserGiteaBasicInfo, getUserAvatar,
     getUsersEmails, updateDeveloperAvatar, updateUsersPassword, deleteUser, addEmailAddress
    , getAllQueryDevelopers, getAllQueryCommitts,deleteEmailAddress, deleteUsersAvatar, getDevelopers, getRoles,update_user_ban_status};