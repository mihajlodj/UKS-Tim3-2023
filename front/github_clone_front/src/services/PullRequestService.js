import api from '../api'

const create = (username, repoName, data) => {
    return api.post(`pr/create/${username}/${repoName}/`, data);
}

const getAll = (repoName) => {
    return api.get(`pr/get_all/${repoName}/`);
}

const getOne = (repoName, pullId) => {
    return api.get(`pr/get/${repoName}/${pullId}/`);
}

const getPossibleAssignees = (repoName) => {
    return api.get(`pr/assignees/${repoName}/`);
}

const update = (repoName, pullId, data) => {
    return api.post(`pr/update/${repoName}/${pullId}/`, data);
}

const updateTitle = (repoName, pullId, data) => {
    return api.post(`pr/title/${repoName}/${pullId}/`, data);
}

const close = (repoName, pullId) => {
    return api.post(`pr/close/${repoName}/${pullId}/`);
}

const reopen = (repoName, pullId) => {
    return api.post(`pr/reopen/${repoName}/${pullId}/`);
}

const markClosed = (repoName, data) => {
    return api.post(`pr/mark_closed/${repoName}/`, data);
}

const markOpen = (repoName, data) => {
    return api.post(`pr/mark_open/${repoName}/`, data);
}

export default { create, getAll, getOne, getPossibleAssignees, update, updateTitle, close, reopen, markOpen, markClosed };