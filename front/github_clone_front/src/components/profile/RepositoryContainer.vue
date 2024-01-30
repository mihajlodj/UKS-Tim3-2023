<template>
  <div class="repository-container">
    <div style="display: flex;">
      <a id="project-name" href="#">UKS-Project</a>
    </div>
    <div id="repo-state">
      <label id="state-label">private</label>
    </div>
  </div>
</template>

<script>
export default {
}
</script>

<style scoped>
#repo-state {
  float: right;
  display: flex;
  justify-content: center;
  border: 1px solid gray;
  padding-top: 0.5rem;
  padding-inline-start: 0.3rem;
  padding-inline-end: 0.3rem;
  color: rgb(225, 225, 225);
  background: rgb(145, 145, 145);
  border-radius: 1rem;
  margin-left: auto;
}

#state-label{
  font-size: 0.7rem;
}

#project-name {
  padding: 1rem;
  font-size: 0.9rem;
  display: block;
  padding-top: 0.1rem;
  padding-bottom: 0.1rem;
  text-decoration: none;
  color: rgb(17, 109, 230);
}

.repository-container {
  float: left;
  border: 1px solid gray;
  border-radius: 1rem;
  display: flex;
  padding: 0.2rem;
  width: 13rem;
  height: 3rem;
  margin: 1rem;
}

</style>
