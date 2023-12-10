import api from '../api'

const register = (registrationData) => {
    return api.post("auth/register/", registrationData);
}

const verifyCode = (verificationData) => {
    return api.post("auth/register-confirm/", verificationData);
}

export default { register, verifyCode };
