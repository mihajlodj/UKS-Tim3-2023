<template>
    <div class="contain">
        <div class="cover"></div>
        <h5>Request</h5>
        <input type="text"/>
        <p>Nothing to show</p>
    </div>
</template>

<style scoped>
.contain {
    position: relative;
    background-color: pink;
    border: 1px solid white;
    border-radius: 10px;
    z-index: 4;
}
.cover{
    position:fixed;
    top:0px;
    left:0px;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0,0,0,0.5);
    z-index:3;
}
</style>