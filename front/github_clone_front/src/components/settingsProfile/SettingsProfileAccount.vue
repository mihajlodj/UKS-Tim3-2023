<template>
  <div class="main">
    <div class="form-group">
      <label for="currentpassword">Current Password</label>
      <input type="password" id="currentpassword" v-model="currentpassword"/>
    </div>

    <div class="form-group">
      <label for="newpassword">New Password</label>
      <input type="password" id="newpassword" v-model="newpassword"/>
    </div>

    <div class="form-group">
      <label for="confirmnewpassword">Confirm New Password</label>
      <input type="password" id="confirmnewpassword" v-model="confirmnewpassword"/>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentpassword: '',
      newpassword: '',
      confirmnewpassword: '',
    };
  },
  methods: {
  },
};
</script>

<style scoped>
.main {
  width: 60%;
  margin: auto;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label{
  color: white;
}

.form-group input, textarea, select {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  margin-bottom: 10px;
  box-sizing: border-box;
}

.github-button {
  background-color: #2ea44f;
  color: #ffffff;
  border: none;
  padding: 10px;
  cursor: pointer;
}

.github-button:hover {
  background-color: #22863a;
}

.github-button-delete {
  background-color: #a4362e;
  color: #ffffff;
  border: none;
  padding: 10px;
  cursor: pointer;
}

.github-button-delete:hover {
  background-color: #863122;
}
</style>
