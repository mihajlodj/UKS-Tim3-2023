<template>
    <div>
        <section class="h-100 bg-custom">
            <div class="container py-5 h-100">
                <div class="row justify-content-center align-items-center h-100">
                    <div class="col-12 col-lg-9 col-xl-7">
                        <div class="card shadow-2-strong card-registration"
                            style="border-radius: 15px; background: #0c162d">
                            <div class="card-body p-4 p-md-5">
                                <h3 class="d-flex justify-content-center pb-4" id="title">Welcome to GitHub Clone!</h3>
                                <form>
                                    <div class="row">
                                        <div class="col-md-6 mb-3">
                                            <InputField id="name-input" type="text" placeholder="Name" name="name"
                                                :value="name" @update="updateName" />
                                            <p v-if="!validation.name" class="text-danger ms-1">Name must not be empty</p>
                                        </div>
                                        <div class="col-md-6 mb-3">
                                            <InputField id="surname-input" type="text" placeholder="Surname" name="surname"
                                                :value="surname" @update="updateSurname" />
                                            <p v-if="!validation.surname" class="text-danger ms-1">Surname must not be empty
                                            </p>
                                        </div>
                                    </div>

                                    <div class="row">
                                        <div class="col-md-12 mb-2 pb-2">
                                            <InputField id="email-input" type="email" placeholder="Email" name="email"
                                                class="w-100" :value="email" @update="updateEmail" />
                                            <p v-if="!validation.email" class="text-danger ms-1">Email must not be empty</p>
                                        </div>
                                    </div>

                                    <div class="row">
                                        <div class="col-md-12 mb-2 pb-2">
                                            <InputField id="username-input" type="text" placeholder="Username"
                                                name="username" class="w-100" :value="username" @update="updateUsername" />
                                            <p v-if="!validation.username" class="text-danger ms-1">Username must not be
                                                empty</p>
                                        </div>
                                    </div>

                                    <div class="row">
                                        <div class="col-md-12 mb-2 pb-2">
                                            <InputField id="password-input" type="password" placeholder="Password"
                                                name="password" class="w-100" :value="password" @update="updatePassword" />
                                            <p v-if="!validation.password" class="text-danger ms-1">
                                                Password must not be empty
                                            </p>
                                        </div>
                                    </div>

                                    <div class="mt-4 mb-3 d-flex flex-column">
                                        <button type="button" class="btn btn-lg text-center" id="btn-register"
                                            @click="submit">REGISTER
                                        </button>
                                    </div>
                                    <p class="text-center text-muted mt-4 mb-3 light">
                                        <span class="light me-2">
                                            Already have an account?
                                        </span>
                                        <a href='/' class="fw-bold text-body"><u class="light">Login here</u></a>
                                    </p>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import InputField from '../util/InputField.vue'
import AuthService from '@/services/AuthService';
import { toast } from 'vue3-toastify';

export default {
    name: 'DeveloperRegistration',
    components: {
        InputField,
    },

    data() {
        return {
            name: '',
            surname: '',
            email: '',
            username: '',
            password: '',
            validation: {
                name: true,
                surname: true,
                email: true,
                password: true,
                username: true,
            }
        }
    },
    methods: {
        submit() {
            this.validate();
            /* eslint-disable */
            if (Object.values(this.validation).every(value => value === true)) {
                AuthService.register({
                    first_name: this.name, last_name: this.surname,
                    username: this.username, email: this.email, password: this.password
                }).then(result => {
                    localStorage.setItem("email", result.data.email);
                    localStorage.setItem("username", result.data.username);
                    this.$router.push('/account_verification');
                }).catch(_err => {
                    toast("User already registered!", {
                        autoClose: 1000,
                        type: 'error',
                        position: toast.POSITION.BOTTOM_RIGHT
                    });
                });
            }
        },

        validateEmail() { this.validation.email = (this.email != ''); },
        validateUsername() { this.validation.username = (this.username != ''); },
        validatePassword() { this.validation.password = (this.password != ''); },
        validateName() { this.validation.name = (this.name != ''); },
        validateSurname() { this.validation.surname = (this.surname != ''); },
        validate() {
            this.validateName();
            this.validateSurname();
            this.validateEmail();
            this.validatePassword();
            this.validateUsername();
        },

        updateName(data) {
            this.name = data.val;
            this.validateName();
        },
        updateSurname(data) {
            this.surname = data.val;
            this.validateSurname();
        },
        updateEmail(data) {
            this.email = data.val;
            this.validateEmail();
        },
        updatePassword(data) {
            this.password = data.val;
            this.validatePassword();
        },
        updateUsername(data) {
            this.username = data.val;
            this.validateUsername();
        }
    }
}

</script>

<style>
.bg-custom {
    background-image: linear-gradient(45deg, #042a66, #4d204c);
    height: 100%;
    min-height: 100vh;
}

.card,
#btn-register {
    background: #0c162d;
}

#btn-register {
    border: 1px solid #76829c;
}

#title,
.light,
#btn-register {
    color: #76829c;
}

#btn-register:hover {
    color: #0c162d;
    border: 1px solid #0c162d;
    background: #76829c;
}
</style>