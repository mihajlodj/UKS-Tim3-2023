<template>
    <div>
        <div class="container w-50 py-5">
            <h3 class="mb-3">Create a new repository</h3>
            <h6 class="sub">A repository contains all project files, including the revision history</h6>
            <hr>
            <h6><i>Required fields are marked with an asterisk (*)</i></h6>
            <hr>

            <div class="d-flex flex-column">
                <label class="bold mb-2">Repository name *</label>
                <input type="text" class="mb-3 repo-name" />
            </div>

            <div class="d-flex flex-column">
                <label class="bold mb-2">Description <span>(optional)</span></label>
                <input type="text" class="w-100" />
            </div>

            <hr>
            <div class="d-flex justify-content-start">
                <input class="form-check-input mt-3" type="radio" name="access-modifier" id="public-radio" checked>
                <font-awesome-icon icon="fa-solid fa-book-bookmark" class="ms-4 me-3 mt-2" />
                <div class="d-flex flex-column">
                    <span class="bold">Public</span>
                    <span class="smaller">Anyone on the internet can see this repository. You choose who can commit.</span>
                </div>
            </div>
            <div class="d-flex justify-content-start mt-3">
                <input class="form-check-input mt-3" type="radio" name="access-modifier" id="private-radio">
                <font-awesome-icon icon="fa-solid fa-lock" class="ms-4 me-3 mt-2" />
                <div class="d-flex flex-column">
                    <span class="bold">Private</span>
                    <span class="smaller">You choose who can see and commit to this repository.</span>
                </div>
            </div>

            <hr>
            <div class="d-flex justify-content-start">
                <font-awesome-icon icon="fa-solid fa-circle-info" class="me-2" style="margin-top: 6px; color: #7a8188" />
                <p class="sub">You are creating a private repository in your personal account.</p>
            </div>

            <hr>
            <div class="d-flex justify-content-end">
                <button class="btn">Create repository</button>
            </div>
        </div>
    </div>
</template>

<script>

</script>

<style scoped>
button {
    background-color: #20883d;
    color: white;
    font-size: large;
}

.container {
    max-width: 900px;
}

h3 {
    font-weight: 600;
}

.sub {
    color: #656e77;
}

.bold {
    font-weight: 600;
    font-size: large;
}

.repo-name {
    width: 50%;
    min-width: 250px;
    max-width: 350px;
}

.smaller {
    font-size: small;
    color: #656e77;
}

.fa-book-bookmark, .fa-lock {
    height: 25px;
}
</style>