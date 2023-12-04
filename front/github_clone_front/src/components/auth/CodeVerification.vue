<template>
    <div class="bg is-fullheight min-vh-100 d-flex align-items-center justify-content-center">
        <div class="card shadow-2-strong card-registration w-50" style="border-radius: 15px; background: #0c162d;">
            <div class="card-body p-4 p-md-5">
                <h4 class="d-flex justify-content-start title">You're almost done!</h4>
                <h6 class="d-flex justify-content-start pb-3 title">We sent a launch code to
                    <span class="email ms-2">{{ email }}</span>
                </h6>
                <h5 class="d-flex justify-content-start pb-3" style="color: #e147a5">
                    <font-awesome-icon icon="fa-solid fa-angle-right" class="me-2" style="margin-top: 3px" />
                    Enter code
                </h5>

                <div class="row">
                    <div class="col-md-12 mb-2 pb-2">
                        <InputField id="code-input" type="text" placeholder="Verification code" name="code" class="w-100"
                            :value="code" @update="updateCode" />
                        <p v-if="!validation.code" class="text-danger ms-1">Verification code must not be empty</p>
                    </div>
                </div>

                <div class="mt-3 d-flex justify-content-end">
                    <button type="button" class="btn btn-lg text-center" id="btn-confirm" @click="submit">
                        Confirm
                    </button>
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
    name: 'DeveloperRegistration',
    components: {
        InputField,
    },

    data() {
        return {
            code: '',
            email: localStorage.getItem("email"),
            validation: {
                code: true,
            }
        }
    },

    methods: {
        submit() {
            this.validateCode();
            if (this.validation.code === true) {
                /* eslint-disable */
                AuthService.verifyCode({ code: this.code, username: localStorage.getItem("username") }).then(_result => {
                    this.$router.push('/');
                }).catch(_err => {
                    toast("Verification failed!", {
                        autoClose: 1000,
                        type: 'error',
                        position: toast.POSITION.BOTTOM_RIGHT
                    });
                });
            }
        },
        validateCode() { this.validation.code = (this.code != ''); },
        updateCode(data) {
            this.code = data.val;
            this.validateCode();
        }
    }

}

</script>

<style>
.bg {
    background-image: linear-gradient(45deg, #042a66, #4d204c);
    background-size: cover;
    height: fit-content;
    opacity: 1;
    position: absolute;
    top: 0;
    width: 100%;
    overflow: visible;
}

.title,
#btn-confirm {
    color: #76829c;
}

.email {
    color: #0dbc79;
}

#btn-confirm {
    border: 1px solid #76829c;
}

#btn-confirm:hover {
    background: #76829c;
    color: #0c162d;
    border: 1px solid #0c162d;
}
</style>