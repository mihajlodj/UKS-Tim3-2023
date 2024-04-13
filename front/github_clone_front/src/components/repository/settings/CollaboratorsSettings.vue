<template>
    <div class="mt-4 container">
        <h3>Manage access</h3>

        <div class="no-collaborators d-flex flex-column mt-3">
            <div class="d-flex justify-content-center align-items-center h-31 mt-4">
                <font-awesome-icon icon="fa-solid fa-user-lock"></font-awesome-icon>
            </div>

            <div class="d-flex justify-content-center align-items-center h-31">
                <h4>You haven't invited any collaborators yet</h4>
            </div>

            <div class="d-flex justify-content-center align-items-center h-31 mb-4">
                <button type="button" class="btn-add-people">Add people</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "CollaboratorsSettings"
}
</script>

<style scoped>

.no-collaborators {
    height: 250px;
    width: 100%;
    border: 1px solid #7f848b;
    border-radius: 10px;
}

.container {
    width: 50%;
    min-width: 700px;
    max-width: 850px;
}

.btn-add-people {
    background-color: #347d38;
    color: #fff;
    border-radius: 7px;
    border: none;
    padding: 7px 17px;
    height: 45px;
}

.fa-user-lock {
    height: 40px;
    color: #1f84f5;
}

.h-31 {
    height: 31%;
}

h3, h4 {
    color: #c5d1df;
}

</style>