import api from '../api'


const getAllCommentsForMilestone = (owner_username, repository_name, type_id) => {
    return api.get(`comment/all/${owner_username}/${repository_name}/milestone/${type_id}`);
}

const getAllCommentsForPullRequest = (owner_username, repository_name, type_id) => {
    return api.get(`comment/all/${owner_username}/${repository_name}/pull_request/${type_id}`);
}

const getAllCommentsForIssue = (owner_username, repository_name, type_id) => {
    return api.get(`comment/all/${owner_username}/${repository_name}/issue/${type_id}`);
}

const createNewComment = (owner_username, repository_name, data) => {
    return api.post(`comment/create/${owner_username}/${repository_name}/`, data);
}

const deleteComment = (owner_username, repository_name, commentId) => {
    return api.delete(`comment/delete/${owner_username}/${repository_name}/${commentId}`);
}

export default { getAllCommentsForMilestone, getAllCommentsForPullRequest, 
    getAllCommentsForIssue, createNewComment, deleteComment };