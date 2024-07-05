<template>
  <div class="user-elm">
    <div class="user-info" @click="showBtn = !showBtn">
      <div ref="user">&nbsp; ID:{{this.user?.id}} &nbsp; User: {{this.user?.name}} &nbsp;</div>
      <font-awesome-icon :icon="['fas', 'user']"  />
    </div>
    <div @click="logout">
      <font-awesome-icon :icon="['fas', 'right-from-bracket']"  />
    </div>
    <div v-if="showBtn" class="delete" @click="deleteUser">
      <font-awesome-icon :icon="['fas', 'trash']"  />
    </div>
  </div>

  <div class="user-config-elm" v-if="show" >
    <div class="user-config-wrapper">
      <div class="user-config">
        <div>
          <input v-model="username" placeholder="username" />
        </div>
        <div>
          <input v-model="pw" type="password" placeholder="pw" />
        </div>
        <div class="btn-wrapper">
          <button class="btn" @click="createUser">Create User</button>
          <button class="btn" @click="login">login</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters, mapActions } from 'vuex';
import EventBus from '../../eventBus.js';

export default {
  computed: {
    ...mapGetters(['user'])
  },
  data() {
    return {
      showBtn: false,
      show: true,
      username: '',
      pw: '',
    }
  },
  
  created() {
    EventBus.on('login', this.login);
  },

  methods: {

    ...mapActions(['setUser']),  
    async createUser() {
      try {
        const response = await axios.post('http://localhost:9000/user', { name: this.username, pw: this.pw });
        console.debug(response.data);
        this.setUser({id: response.data.id, pw: response.data.pw, name: response.data.name });
        this.login();
        EventBus.emit('loadChats');
        this.show = false;
      } catch (err) {
        console.debug('Failed to create user: ' + err);
      }
    },
    async deleteUser() {
      if (JSON.parse(localStorage.getItem('user')).name == '') {
        console.debug("no user loged in to delete")
        return;
      }
      try {
        const response = await axios.post(`http://localhost:9000/user/delete`, this.user);
        this.setUser({'id': '', 'name': '', 'pw': ''});
        EventBus.emit('loadChats');
        this.show = true;
      } catch (err) {
        console.debug('Failed to delete user: ' + err.response.data.detail);
      }
    },
    async getUsers() {
      try {
        const response = await axios.get('http://localhost:9000/users');
      } catch (err) {
        console.debug('Failed to load users: ' + err.response.data.detail);
      }
    },
    async login() {
      console.debug();
      try {
        if (JSON.parse(localStorage.getItem('user')) && JSON.parse(localStorage.getItem('user')).name) {          
          this.setUser(JSON.parse(localStorage.getItem('user')));
          this.username = this.user.name;
          this.pw = this.user.pw;
        } else if (this.show) {
          this.setUser({ name: this.username, pw: this.pw });
        }

        if (this.user.name == '') return;
        const response = await axios.post('http://localhost:9000/login', {name: this.user.name, pw: this.user.pw});
        
        this.setUser(response.data);
        localStorage.setItem('user',JSON.stringify({'id': this.user.id,'name': this.user.name, 'pw': this.user.pw}));
      
        EventBus.emit('loadChats');
        this.show = false;
      } catch (err) {
        this.setUser({'id': '', 'name': '', 'pw': ''});
        console.debug('Failed to load users: ' + err);
      }
    }, 
    async logout()  {
      this.pw = '';
      this.username = '';
      localStorage.removeItem("user");
      this.setUser({'id': '', 'name': '', 'pw': ''});
      EventBus.emit('loadChats');
      this.show = true;
    }
  },
  mounted() {
    this.login();
  }
};
</script>

<style>
.user-elm {  
  margin: 0 .5em 0 auto;
  display: flex;
  align-items: center;
}

svg {
  cursor: pointer;
}

.user-info {
  display: flex;
  margin: 0 1em;
}

input {
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 10px;
  font-size: 1.25em;
  border: transparent;
  background: var(--input-background);
}

.btn {
  margin: 5px;
  padding: 10px 20px;
  background-color: var(--btn-background-color);
  color: var(--btn-color);
  font-size: .75em;
  border-radius: 10px;
  min-width: fit-content;
  border: none;
  cursor: pointer;
}

.user-config-elm {
  position: absolute;
  top: 0;
  width: 100%;
  height: 100%;
  background: #454545a8;
  z-index: 1;
}

.user-config {
  width: 300px;
  margin: auto;
  margin-top: 4em;
  padding: 1em;
}

.btn-wrapper {
  display: flex;
  flex-direction: column;
}

.delete {
  margin: 0 1em;
}

.delete svg:hover {
  color: var(--warn);
}
</style>
