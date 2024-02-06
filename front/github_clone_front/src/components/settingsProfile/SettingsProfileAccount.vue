<template>
  <div class="main">
    <div class="profile-form">
      <div class="form-title">
        <h2>Password</h2>
      </div>
      <div class="form-group">
        <label for="currentpassword">Current Password</label>
        <input type="password" id="currentpassword" v-model="currentpassword"/>

        <label for="newpassword">New Password</label>
        <input type="password" id="newpassword" v-model="newpassword"/>

        <label for="confirmnewpassword">Confirm New Password</label>
        <input type="password" id="confirmnewpassword" v-model="confirmnewpassword"/>

        <button class="form-button" @click="changePassword">Update Password</button>
      </div>
    </div>

    <div class="profile-form">
      <div class="form-title">
        <h2>Manage Email Addresses</h2>
      </div>
      <div class="form-group">
        <div class="newEmailButtonClass">
          <label for="newEmailAddress">Add New Email Address</label>
          <input type="email" id="newEmailAddress" v-model="newEmailAddress"/>
          
          <button class="form-button" @click="addEmailAddress">Add Email Address</button>
        </div>

        <div v-for="(email, index) in emailAddresses" :key="index" class="emailDiv">
          <div class="emailInfoDiv">
            <span class="emailSpan">{{ email.email }}</span>
            <span class="emailAvtivePrimery" v-if="email.primary">Primary</span>
            <span class="emailAvtivePrimery" v-if="email.verified">Activated</span>
          </div>
          <div class="makePrimAndRmoveBtns">
            <button class="form-button-email" @click="removeEmail(index)" v-if="!email.primary">Remove</button>
          </div>
        </div>
      </div>
    </div>

  <div class="profile-form" style="border: 1px solid #e42a0a;">
      <div class="form-title-delete">
        <h2>Delete Your Account </h2>
      </div>
      <span class="warning">
         <i class="bi bi-exclamation-triangle"></i>&nbsp;This operation will permanently delete your user account. It&nbsp;<b>CANNOT</b>&nbsp;be undone.
      </span>
      <div class="form-group">
        <label for="usersPassowrd">Password</label>
        <input type="password" id="usersPassowrd" v-model="usersPassowrd"/>
        <button class="form-button-delete" @click="deleteUser">Confirm Deletion</button>
      </div>
    </div>

  </div>
</template>

<script>
import DeveloperService from '@/services/DeveloperService';
import { toast } from 'vue3-toastify';

export default {
  mounted(){
    DeveloperService.getUsersEmails(localStorage.getItem("username"))
        .then(res => {
            console.log(res);
            this.emailAddresses = res.data
        })
        .catch(err => {
            console.log(err);
        });
  },
  data() {
    return {
      currentpassword: '',
      newpassword: '',
      confirmnewpassword: '',
      currentEmailAddress:'',
      newEmailAddress:'',
      usersPassowrd:'',
      emailAddresses: '',
    };
  },
  methods: {
    deleteUser(){
      if(this.usersPassowrd !== ""){
          DeveloperService.deleteUser(this.usersPassowrd.toString(), localStorage.getItem("username")).then(res => {
                console.log(res);
                location.reload()
            }).catch(err => {
                console.log(err);
                toast("Incorect data filled in!", {
                      autoClose: 500,
                      type: 'error',
                      position: toast.POSITION.BOTTOM_RIGHT
                  });
            });
      }
      else{
         toast("Incorect data filled in!", {
            autoClose: 500,
            type: 'error',
            position: toast.POSITION.BOTTOM_RIGHT
        });
      }
    },
    changePassword() {
      if(this.currentpassword === "" || this.newpassword!==this.confirmnewpassword){
        toast("Incorect data filled in!", {
            autoClose: 500,
            type: 'error',
            position: toast.POSITION.BOTTOM_RIGHT
        });
      }
      else{
          DeveloperService.updateUsersPassword({ 'current_password': this.currentpassword, 'new_password':this.newpassword, 'new_password_repeat':this.confirmnewpassword}, localStorage.getItem("username")).then(res => {
                console.log(res);
                location.reload()
            }).catch(err => {
                console.log(err);
                toast("Incorect data filled in!", {
                      autoClose: 500,
                      type: 'error',
                      position: toast.POSITION.BOTTOM_RIGHT
                  });
            });
      }
    },
    addEmailAddress() {
      this.emailAddresses.push({
        email: this.newEmailAddress,
        primary: false,
        verified: true,
      });

      DeveloperService.addEmailAddress({ 'secondary_emails': this.newEmailAddress}, localStorage.getItem("username")).then(res => {
                console.log(res);
            }).catch(err => {
                console.log(err);
            });
      this.newEmailAddress = '';
    },
    removeEmail(index) {
      DeveloperService.deleteEmailAddress(this.emailAddresses[index]['email'], localStorage.getItem("username")).then(res => {
                console.log(res);
                this.emailAddresses.splice(index, 1);
            }).catch(err => {
                console.log(err);
            });
    },
  },
};
</script>

<style scoped>
.warning{
  background: rgb(149, 42, 42);;
  padding: 0.5rem;
  margin: 1rem;
  display: flex;
  border-radius: 0.5rem;
  color: rgb(226, 226, 226);
}

.emailInfoDiv {
  width: 70%;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.makePrimAndRmoveBtns{
  width: auto;
}
.newEmailButtonClass{
  margin-bottom: 5rem;
}

.emailDiv{
margin: 1rem;
display: flex;
align-items: center;
}
.emailAvtivePrimery{
  background: #1da3b2;
  color: white;
  border: none;
  margin-inline-end: 0.2rem;
  margin-inline-start: 0.2rem;
  padding: 0.2rem;
  border-radius: 0.4rem;
  font-size: 0.7rem;
  align-self: center;
}

.emailSpan{
  color: white;
  margin-inline-end: 1rem;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis; 
}

.main {
  width: 60%;
  margin: auto;
  margin-top: 1rem;
}

.profile-form {
  border: 1px solid #ccc;
  border-radius: 1rem;
  margin-bottom: 1rem;
}

.form-title-delete {
  text-align: left;
  padding: 0.5rem;
  color: white;
  border-radius: 1rem 1rem 0 0;
  background: rgb(149, 42, 42);
}

.form-title-delete h2 {
  font-size: 1.3rem;
}

.form-title {
  text-align: left;
  padding: 0.5rem;
  color: white;
  border-radius: 1rem 1rem 0 0;
  background: rgb(89, 86, 86);
}

.form-title h2 {
  font-size: 1.3rem;
}

.form-group {
  padding: 0.5rem;
  margin-bottom: 3rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: white;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 1rem;
  color: white;
  background: rgb(55, 53, 53);
  border: 1px solid gray;
  box-sizing: border-box;
}

.form-button {
  background-color: #2b8f47;
  color: #ffffff;
  border: none;
  border-radius: 0.5rem;
  padding: 0.5rem;
  cursor: pointer;
  float: left;
  margin-right: 0.5rem;
}

.form-button:hover {
  background-color: #22863a;
}

.form-button-delete {
  background-color: #ea280f;
  color: #ffffff;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  float: left;
  margin-right: 0.5rem;
}

.form-button-delete:hover {
  background-color: #22863a;
}


.form-button-email {
  background-color: #2b8f47;
  color: #ffffff;
  border: none;
  border-radius: 0.5rem;
  padding: 0.3rem;
  cursor: pointer;
  float: left;
  font-size: 0.9rem;
  margin-right: 0.5rem;
}

.form-button-email:hover {
  background-color: #22863a;
}

</style>
