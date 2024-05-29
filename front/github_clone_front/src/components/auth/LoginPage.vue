<template>
    <div class="bg is-fullheight min-vh-100">
        <div class="d-flex justify-content-center">
            <svg height="50" aria-hidden="true" viewBox="0 0 16 16" width="50" fill="#c4d0de" style="margin: 30px;">
                <path d="M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"></path>
            </svg>
        </div>
        <h3 class="mb-4 d-flex justify-content-center">Sign in to GitHub Clone</h3>
        <div class="d-flex flex-column align-items-center justify-content-center">
            <div class="card" style="border-radius: 15px; background: #2c333b; width: 460px;">
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
                            <span class="bright me-1">
                                Don't have an account?
                            </span>
                            <a href='/register' class="fw-bold text-body"><u class="bright">Sign up here</u></a>
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
                    localStorage.setItem("hasUnreads", false);
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
    background-color: #1c2127;
}

#btn-login {
    background-color: #1f883d;
    color: white;
}

img {
    width: 55px;
}

h3 {
    color: white;
}

.bright {
    color: #c1c9d4;
}
</style>