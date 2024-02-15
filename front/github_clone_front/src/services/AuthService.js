import api from '../api'

const register = (registrationData) => {
    return api.post("auth/register/", registrationData);
}

const verifyCode = (verificationData) => {
    return api.post("auth/register-confirm/", verificationData);
}

const login = (credentials) => {
    return api.post("auth/login/", credentials);
}

const logout = (refreshToken) => {
    return api.post("auth/logout/", refreshToken)
}

export default { register, verifyCode, login, logout };
