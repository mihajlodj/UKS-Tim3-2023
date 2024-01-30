<template>
  <div class="repository-container">
    <div style="display: flex;">
      <a :href="projectLink" class="project-link">{{ projectName }}</a>
    </div>
    <div id="outer">
      <div id="repo-state">
        <label id="state-label">{{ isPrivate ? 'private' : 'public' }}</label>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    projectName: {
      type: String,
      required: true,
    },
    isPrivate: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    projectLink() {
      return this.isPrivate ? '#' : `#/${this.projectName}`;
    },
  },
};
</script>

<style scoped>
#repo-state {
  border: 1px solid gray;
  padding-inline-end: 0.3rem;
  padding-inline-start: 0.3rem;
  color: rgb(225, 225, 225);
  border-radius: 1rem;
  height: 1.6rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

#outer {
  justify-content: right;
  display: flex;
  width: 100%;
}

#state-label {
  font-size: 0.7rem;

}

.project-link {
  padding-inline-start: 0.5rem;
  font-size: 0.9rem;
  display: block;
  padding-top: 0.1rem;
  padding-bottom: 0.1rem;
  text-decoration: none;
  color: rgb(17, 109, 230);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 9.5rem;
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
