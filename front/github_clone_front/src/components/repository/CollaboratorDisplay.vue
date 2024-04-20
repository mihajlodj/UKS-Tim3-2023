<template>
    <div class="bg d-flex justify-content-between py-1">
        <div class="d-flex justify-content-start align-items-center ms-2">
            <button type="button" class="btn-avatar">
                <img :src="collaborator.avatar" />
            </button>

            <div class="ms-1 mt-1">
                <button type="button" class="btn-username">{{ collaborator.username }}</button>
                <div v-if="!changingRole" class="d-flex justify-content-start">
                    <h6 class="role ms-1">{{ role }}</h6>
                    <button v-if="role !== 'Pending'" type="button" class="btn-change" @click="startChangingRole">
                        <font-awesome-icon icon="fa-solid fa-pen"></font-awesome-icon>
                    </button>
                </div>

                <div v-else class="d-flex justify-content-start ms-1 mb-1">
                    <button class="btn nav-link dropdown-toggle btn-gray" type="button" id="roleChoice" role="button"
                        data-bs-toggle="dropdown" aria-expanded="false">
                        <span class="me-1 mb-1">{{ role }}</span>
                    </button>
                    <ul class="dropdown-menu" id="branches-list" aria-labelledby="roleChoice" style="background-color: #2c333b">
                        <li>
                            <button class="btn dropdown-item" @click="changeRole('Readonly')"
                                style="color: #a5b2bf;">
                                Readonly
                            </button>
                        </li>
                        <li>
                            <button class="btn dropdown-item" @click="changeRole('Developer')"
                                style="color: #a5b2bf;">
                                Developer
                            </button>
                        </li>
                        <li>
                            <button class="btn dropdown-item" @click="changeRole('Maintainer')"
                                style="color: #a5b2bf;">
                                Maintainer
                            </button>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="d-flex justify-content-end align-items-center">
            <button type="button" class="btn-remove me-1" @click="remove">Remove</button>
        </div>
    </div>
</template>

<script>
export default {
    name: "CollaboratorDisplay",
    props: ["collaborator"],

    data() {
        return {
            changingRole: false,
            role: this.collaborator.role[0] + this.collaborator.role.slice(1).toLowerCase()
        }
    },

    methods: {
        remove() {
            this.$emit('remove', this.collaborator.username);
        },

        changeRole(newRole) {
            this.changingRole = false;
            this.$emit('changeRole', {role: newRole.toUpperCase(), username: this.collaborator.username});
            this.role = newRole;
        },

        startChangingRole() {
            this.changingRole = true;
        }
    }
}
</script>

<style scoped>
.bg {
    background-color: #22272d;
    border: 1px solid #72808d;
}

img {
    height: 30px;
    border-radius: 50%;
}

.btn-avatar {
    border: none;
    background: none;
}

.btn-remove {
    border: none;
    background: none;
    color: #72808d;
    padding: 5px 10px;
}

.btn-remove:hover {
    border-radius: 7px;
    background-color: #363e47;
    color: #c44f4f;
}

.btn-username {
    background: none;
    border: none;
    color: #4481d2;
    font-weight: 600;
}

.btn-username:hover {
    text-decoration: underline;
}

.role {
    color: #72808d;
}

.btn-change {
    background: none;
    border: none;
    color: #72808d;
}

.fa-pen {
    height: 15px;
    margin-bottom: 4px;
    margin-left: 5px;
}

#roleChoice {
    color: #72808d;
}
</style>