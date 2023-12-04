import api from '../api'

const register = (registrationData) => {
    return api.post("auth/register/", registrationData);
}

export default { register };
