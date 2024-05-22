<template>
    <div class="loading-modal">
        <div class="spinner"></div>
        <p>Loading...</p>
    </div>
</template>

<script>
export default {
    name: 'LoadingPage'
}
</script>

<style scoped>
.loading-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.8);
    display: flex;
    justify-content: center;
    align-items: center;
}
.spinner {
    border: 15px solid #f3f3f3;
    border-radius: 50%;
    border-top: 15px solid #488be6;
    width: 120px;
    height: 120px;
    animation: spin 2s linear infinite;
}
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>