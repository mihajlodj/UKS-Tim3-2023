import api from '../api'

const createIssue = (issueData) => {
    return api.post("issue/create/", issueData);
}

const getIssue = (id) => {
    return api.get("issue/" + id + "/");
}

const getAllQueryIssues = (query) => {
    return api.get(`issue/query_issues/${query}`);
}

const getIssues = (username, repoName) => {
    return api.get(`issue/issues/${username}/${repoName}/`);
}

const updateIssue = (issueData) => {
    return api.patch("issue/update/", issueData);
}

const closeIssue = (repoName, id) => {
    return api.patch("issue/close/" + repoName + "/" + id + "/");
}

const reopenIssue = (repoName, id) => {
    return api.patch("issue/reopen/" + repoName + "/" + id + "/");
}

const deleteIssue = (repoName, id) => {
    return api.delete("issue/" + repoName + "/" + id + "/");
}

export default { createIssue, getIssue, getIssues, updateIssue, deleteIssue, closeIssue, getAllQueryIssues, reopenIssue};