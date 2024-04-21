import api from '../api'

const create = (username, repoName, data) => {
    return api.post(`pr/create/${username}/${repoName}/`, data);
}

const getAll = (username, repoName) => {
    return api.get(`pr/get_all/${username}/${repoName}/`);
}

const getAllQueryPrs = (query) => {
    return api.get(`pr/query_pull_reqs/${query}`);
}

const getOne = (username, repoName, pullId) => {
    return api.get(`pr/get/${username}/${repoName}/${pullId}/`);
}

const getPossibleAssignees = (username, repoName) => {
    return api.get(`pr/assignees/${username}/${repoName}/`);
}

const update = (username, repoName, pullId, data) => {
    return api.put(`pr/update/${username}/${repoName}/${pullId}/`, data);
}

const updateTitle = (username, repoName, pullId, data) => {
    return api.put(`pr/title/${username}/${repoName}/${pullId}/`, data);
}

const close = (username, repoName, pullId) => {
    return api.put(`pr/close/${username}/${repoName}/${pullId}/`);
}

const reopen = (username, repoName, pullId) => {
    return api.put(`pr/reopen/${username}/${repoName}/${pullId}/`);
}

const markClosed = (username, repoName, data) => {
    return api.put(`pr/mark_closed/${username}/${repoName}/`, data);
}

const markOpen = (username, repoName, data) => {
    return api.put(`pr/mark_open/${username}/${repoName}/`, data);
}

const merge = (username, repoName, pullId) => {
    return api.put(`pr/merge/${username}/${repoName}/${pullId}/`);
}

export default { create, getAll, getOne, getPossibleAssignees, update, updateTitle, 
    close, reopen, markOpen, markClosed, merge, getAllQueryPrs };