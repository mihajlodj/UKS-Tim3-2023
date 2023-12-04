<template>
    <div :class="`form-floating mt-${mt} mb-${mb}`">
        <input :id="id" :type="type" class="form-control form-control-lg" :placeholder="placeholder" :name="name"
            v-model="val" @input="update" :value="value" :min="min" />
        <label :for="id" class="form-label fw-bold text-dark">{{ placeholder }}</label>
    </div>
</template>

<script>

export default {
    name: 'InputField',
    props: ['id', 'type', 'placeholder', 'name', 'value', 'mt', 'mb', 'min'],
    data() {
        return {
            val: this.value
        }
    },
    methods: {
        update() {
            this.$emit('update', {
                val: this.val
            });
        }
    }
}
</script>

<style>
label {
    color: #C0C0C0;
}
</style>