<template>
    <div class="bg is-fullheight min-vh-100">
        <div class="d-flex justify-content-center">
            <img alt="Logo" src="../../assets/logo_light.png" id="logo-img" class="mb-5 mt-4">
        </div>
        <h3 class="mb-4 d-flex justify-content-center">Sign in to GitHub Clone</h3>
        <div class="d-flex flex-column align-items-center justify-content-center">
            <div class="card" style="border-radius: 15px; background: #f6f8fa; width: 460px;">
                <div class="card-body px-5 pt-5 pb-4">
                    <form>
                        <div class="row">
                            <div class="col-md-12 mb-3 pb-2">
                                <InputField type="text" placeholder="Username" name="username" class="w-100"
                                    :value="username" @update="updateUsername" />
                                <p v-if="!validation.username" class="text-danger ms-1">
                                    Username must not be empty
                                </p>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-md-12 mb-2 pb-2">
                                <InputField type="password" placeholder="Password" name="password" class="w-100"
                                    :value="password" @update="updatePassword" />
                                <p v-if="!validation.password" class="text-danger ms-1">
                                    Password must not be empty
                                </p>
                            </div>
                        </div>

                        <div class="mt-4 mb-3 d-flex flex-column">
                            <button type="button" class="btn btn-lg text-center" id="btn-login" @click="submit">
                                Sign in
                            </button>
                        </div>
                        <p class="text-center text-muted mt-4 light">
                            <span class="light me-1">
                                Don't have an account?
                            </span>
                            <a href='/register' class="fw-bold text-body"><u class="light">Sign up here</u></a>
                        </p>
                    </form>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import InputField from '../util/InputField.vue'
import AuthService from '@/services/AuthService';
import { toast } from 'vue3-toastify';

export default {
    name: 'LoginPage',
    components: {
        InputField,
    },
    created(){
        console.log(localStorage.getItem("access_token"));
    },

    data() {
        return {
            username: '',
            password: '',
            validation: {
                username: true,
                password: true
            }
        }
    },

    methods: {
        submit() {
            this.validate();
            /* eslint-disable */
            if (Object.values(this.validation).every(value => value === true)) {
                AuthService.login({
                    "username": this.username,
                    "password": this.password
                }).then(result => {
                    localStorage.clear();
                    localStorage.setItem("access_token", result.data.access);
                    localStorage.setItem("refresh_token", result.data.refresh);
                    localStorage.setItem("username", this.username);
                    this.$router.push('/main');
                }).catch(_err => {
                    toast("Invalid credentials!", {
                        autoClose: 1000,
                        type: 'error',
                        position: toast.POSITION.BOTTOM_RIGHT
                    });
                })
            }
        },

        validateUsername() { this.validation.username = (this.username != ''); },
        validatePassword() { this.validation.password = (this.password != ''); },
        validate() {
            this.validateUsername();
            this.validatePassword();
        },

        updateUsername(data) {
            this.username = data.val;
            this.validateUsername();
        },
        updatePassword(data) {
            this.password = data.val;
            this.validatePassword();
        }
    },
}
</script>

<style scoped>
.bg {
    background-color: white;
}

#btn-login {
    background-color: #1f883d;
    color: white;
}

img {
    width: 55px;
}
</style>