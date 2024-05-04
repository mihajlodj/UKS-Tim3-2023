<template>
    <div class="d-flex justify-content-start filters">
        <button class="nav-link dropdown-toggle p-2" type="button" role="button" id="btn-filter" data-bs-toggle="dropdown"
            aria-expanded="false">
            Filters
        </button>
        <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
            <li>
                <button class="btn dropdown-item">Open issues and pull requests</button>
                <hr />
            </li>
            <li>
                <button class="btn dropdown-item">Your issues</button>
                <hr />
            </li>
            <li>
                <button class="btn dropdown-item">Your pull requests</button>
                <hr />
            </li>
            <li>
                <button class="btn dropdown-item">Everything assigned to you</button>
            </li>
        </ul>

        <input type="text" class="filter" />

        <div class="mx-3 d-flex justify-content-">
            <button type="button" class="btn-lbl px-4">
                <font-awesome-icon icon="fa-solid fa-tag" class="me-1" />
                Labels
            </button>
            <button type="button" class="btn-ms px-4" @click="$router.push(`milestones`)">
                <svg viewBox="0 0 16 16" class="svg me-1 mb-1" aria-hidden="true" width="16" height="16" fill="#adbbc8">
                    <path
                        d="M7.75 0a.75.75 0 0 1 .75.75V3h3.634c.414 0 .814.147 1.13.414l2.07 1.75a1.75 1.75 0 0 1 0 2.672l-2.07 1.75a1.75 1.75 0 0 1-1.13.414H8.5v5.25a.75.75 0 0 1-1.5 0V10H2.75A1.75 1.75 0 0 1 1 8.25v-3.5C1 3.784 1.784 3 2.75 3H7V.75A.75.75 0 0 1 7.75 0Zm4.384 8.5a.25.25 0 0 0 .161-.06l2.07-1.75a.248.248 0 0 0 0-.38l-2.07-1.75a.25.25 0 0 0-.161-.06H2.75a.25.25 0 0 0-.25.25v3.5c0 .138.112.25.25.25h9.384Z">
                    </path>
                </svg>
                Milestones
            </button>
        </div>
    </div>
</template>

<script>
export default {
    name: "FilterBar",
}
</script>

<style scoped>
div.filters {
    width: 85%;
}

#btn-filter {
    color: #adbbc8;
    background-color: #373e48;
    border-bottom-left-radius: 7px;
    border-top-left-radius: 7px;
    border: 1px solid #444d56;
}

#btn-filter:hover, .btn-lbl:hover, .btn-ms:hover {
    background-color: #404853;
}

button.dropdown-item {
    background-color: #373e48;
    color: #adbbc8;
}

button.dropdown-item:hover {
    background-color: #404853;
}

.dropdown-menu {
    background-color: #373e48;
}

hr {
    color: #adbbc8;
    padding: 0;
    margin: 0;
}

input {
    border: 1px solid #444d56;
    color: #444d56;
    background-color: #1c2127;
    width: 75%;
}

.btn-lbl, .btn-ms {
    border: 1px solid #444d56;
    background-color: #22272d;
    color: #adbbc8;
    min-width: 170px;
}

.btn-lbl {
    border-bottom-left-radius: 7px;
    border-top-left-radius: 7px;
}

.btn-ms {
    border-bottom-right-radius: 7px;
    border-top-right-radius: 7px;
}
</style>