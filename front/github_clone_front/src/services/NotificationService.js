import api from '../api'

const markAsRead = (id) => {
    return api.put(`notifications/mark_as_read/${id}/`);
}

const get = () => {
    return api.get('notifications/');
}

export default { markAsRead, get }