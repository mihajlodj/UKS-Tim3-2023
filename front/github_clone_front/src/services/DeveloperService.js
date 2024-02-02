import api from '../api'


const update = (developerData, username) => {
    return api.patch(`developer/update/${username}/`, developerData);
}

const getUser = (username) => {
    return api.get(`developer/${username}`);
}

export default { update, getUser};