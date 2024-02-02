import api from '../api'


const update = (developerData, username) => {
    return api.patch(`developer/update/${username}/`, developerData);
}

const getUserBasicInfo = (username) => {
    return api.get(`developer/${username}`);
}

const getUserGiteaBasicInfo = (username) => {
    return api.get(`developer/gitea/${username}`);
}

const getUserAvatar = (username) => {
    return api.get(`developer/avatar/${username}`);
}

const getUsersEmails = (username) => {
    return api.get(`developer/emails/${username}`);
}

export default { update, getUserBasicInfo,getUserGiteaBasicInfo,getUserAvatar, getUsersEmails};