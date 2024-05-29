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

const getIssuesForMilestone = (username, repoName, milestone_id) => {
    return api.get(`issue/issuesformilestone/${username}/${repoName}/${milestone_id}/`);
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

const getPossibleAssignees = (ownerUsername, repoName, id) => {
    return api.get("issue/" + ownerUsername + '/' + repoName + "/managers/" + id + "/");
}

const assignManager = (repoName, ownerUsername, data) => {
    return api.put("issue/" + ownerUsername + '/' + repoName + "/managers/assign/", data);
}

const unassignManager = (repoName, ownerUsername, data) => {
    return api.patch("issue/" + ownerUsername + '/' + repoName + "/managers/un_assign/", data);
}
export default { createIssue, getIssue, getIssues, getIssuesForMilestone, updateIssue, deleteIssue, closeIssue, getAllQueryIssues, reopenIssue, unassignManager, assignManager, getPossibleAssignees };
