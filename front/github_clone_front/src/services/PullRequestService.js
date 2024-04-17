import api from '../api'

const create = (username, repoName, data) => {
    return api.post(`pr/create/${username}/${repoName}/`, data);
}

const getAll = (repoName) => {
    return api.get(`pr/get_all/${repoName}/`);
}

const getAllQueryPrs = (query) => {
    return api.get(`pr/query_pull_reqs/${query}`);
}

const getOne = (repoName, pullId) => {
    return api.get(`pr/get/${repoName}/${pullId}/`);
}

const getPossibleAssignees = (repoName) => {
    return api.get(`pr/assignees/${repoName}/`);
}

const update = (repoName, pullId, data) => {
    return api.put(`pr/update/${repoName}/${pullId}/`, data);
}

const updateTitle = (repoName, pullId, data) => {
    return api.put(`pr/title/${repoName}/${pullId}/`, data);
}

const close = (repoName, pullId) => {
    return api.put(`pr/close/${repoName}/${pullId}/`);
}

const reopen = (repoName, pullId) => {
    return api.put(`pr/reopen/${repoName}/${pullId}/`);
}

const markClosed = (repoName, data) => {
    return api.put(`pr/mark_closed/${repoName}/`, data);
}

const markOpen = (repoName, data) => {
    return api.put(`pr/mark_open/${repoName}/`, data);
}

const merge = (repoName, pullId) => {
    return api.put(`pr/merge/${repoName}/${pullId}/`);
}

export default { create, getAll, getOne, getPossibleAssignees, update, updateTitle, 
    close, reopen, markOpen, markClosed, merge, getAllQueryPrs };