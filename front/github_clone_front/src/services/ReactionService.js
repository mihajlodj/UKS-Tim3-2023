import api from '../api'

const createNewReaction = (owner_username, repository_name, data) => {
    return api.post(`reaction/create/${owner_username}/${repository_name}/`, data);
}

const deleteReaction = (owner_username, repository_name, reactionId) => {
    return api.delete(`reaction/delete/${owner_username}/${repository_name}/${reactionId}/`);
}

const getReactionsForComment = (owner_username, repository_name, commentId) => {
    return api.get(`reaction/all/${owner_username}/${repository_name}/${commentId}/`);
}

export default { createNewReaction, deleteReaction, getReactionsForComment };
