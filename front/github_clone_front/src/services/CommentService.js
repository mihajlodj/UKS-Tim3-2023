import api from '../api'


const getAllComments = (owner_username, repository_name, entity_type, type_id) => {
    if (entity_type === null || entity_type === undefined) {
        return null;
    }
    
    if (entity_type === 'pull_request') {
        return api.get(`comment/all/${owner_username}/${repository_name}/pull_request/${type_id}`);
    }
    else if (entity_type === 'milestone') {
        return api.get(`comment/all/${owner_username}/${repository_name}/milestone/${type_id}`);
    }
    else if (entity_type === 'issue') {
        return api.get(`comment/all/${owner_username}/${repository_name}/issue/${type_id}`);
    }
    else {
        return null;
    }
}

const createNewComment = (owner_username, repository_name, data) => {
    return api.post(`comment/create/${owner_username}/${repository_name}/`, data);
}

const deleteComment = (owner_username, repository_name, commentId) => {
    return api.delete(`comment/delete/${owner_username}/${repository_name}/${commentId}`);
}

export default { getAllComments, createNewComment, deleteComment };