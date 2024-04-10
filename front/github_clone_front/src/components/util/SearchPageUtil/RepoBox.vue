<template>
    <div :class="`form-floating mt-${mt} mb-${mb}`">
        <input :id="id" :type="type" class="form-control form-control-lg" :placeholder="placeholder" :name="name"
            v-model="val" @input="update" :value="value" :min="min" />
        <label :for="id" class="form-label fw-bold" style="color: #4b4f57">{{ placeholder }}</label>
    </div>
</template>

<script>

export default {
    name: 'RepoBox',
    props: ['name', 'description', 'access_modifier'],
    data() {
        return {
            
        }
    },
    methods: {
    }
}
</script>
