<template>
    <div class="bg d-flex justify-content-between py-1">
        <div class="d-flex justify-content-start align-items-center ms-2">
            <button type="button" class="btn-avatar">
                <img :src="collaborator.avatar"/>
            </button>

            <div class="ms-1 mt-1">
                <button type="button" class="btn-username">{{ collaborator.username }}</button>
                <h6 class="role ms-1">{{ role }}</h6>
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

    methods: {
        remove() {
            this.$emit('remove', this.collaborator.username);
        }
    },

    computed: {
        role() {
            return this.collaborator.role.charAt(0).toUpperCase() + this.collaborator.role.slice(1).toLowerCase();
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
</style>