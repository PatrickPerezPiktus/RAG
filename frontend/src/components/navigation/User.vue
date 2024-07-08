<template>
  <div class="user-elm">
    <div v-if="showBtn" @click="logout">
      <font-awesome-icon :icon="['fas', 'right-from-bracket']"  />
    </div>
    <div v-if="showBtn" class="delete" @click="deleteUser">
      <font-awesome-icon :icon="['fas', 'trash']"  />
    </div>
    <div class="user-info" @click="showBtn = !showBtn">
      <div ref="user"> &nbsp; {{this.user?.name}} &nbsp; </div>
      <font-awesome-icon :icon="['fas', 'user']"  />
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
import axios from '@/axios';
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
      id: '',
      pw: '',
    }
  },
  
  created() {
    EventBus.on('login', this.login);
  },

  methods: {
    ...mapActions(['addLog','setUser']),  

    async createUser() {
      try {
        const response = await axios.post('/user', { name: this.username, pw: this.pw });
        console.log('Nutzer wurde erstellt: ', response);
        this.addLog({author: "User", text: "Nutzer wurde erstellt"});
        this.setUser({id: response.data.id, name: response.data.name });
        this.login();
        this.show = false;
      } catch (err) {
        console.error('Nutzer konnte nicht erstellt werden: ', err);
        this.addLog({author: "User", text: "Nutzer konnte nicht erstellt werden"});
      }
    },

    async deleteUser() {
      if (JSON.parse(localStorage.getItem('user')).name == '') {
        console.log('Kein Nutzer eingeloggt, der gelöscht werden konnte');
        this.addLog({author: "User", text: "Kein Nutzer eingeloggt, der gelöscht werden konnte"});
        return;
      }
      try {
        const response = await axios.post(`/user/delete`, this.user.name);
        console.log('Nutzer gelöscht: ', response);
        this.addLog({author: "User", text: "Nutzer gelöscht"});
        this.setUser({ 'id': '', 'name': '', 'token': '' });
        localStorage.removeItem('user');
        this.show = true;
      } catch (err) {
        console.error('Es ist ein Fehler beim löschen eines Nutzers aufgetreten: ', error);
        this.addLog({author: "User", text: "Es ist ein Fehler beim löschen eines Nutzers aufgetreten"});
      }
    },

    async getUsers() {
      try {
        const response = await axios.get('/users');
        console.log('Alle Nutzer geladen: ', response);
        this.addLog({author: "User", text: "Alle Nutzer geladen"});
      } catch (err) {
        console.log('Fehler beim laden aller Nutzer geladen: ', err);
        this.addLog({author: "User", text: "Fehler beim laden aller Nutzer geladen"});
      }
    },

    async login() {
      try {
        let response;
        const storedUser = JSON.parse(localStorage.getItem('user'));
        if (storedUser && storedUser.token) {
          response = await axios.post('/token', {}, {
            headers: {
              'Authorization': `Bearer ${storedUser.token}`
            }
          });
          //TODO log
        } else {
          response = await axios.post('/token', { name: this.username, pw: this.pw });
        }

        const { access_token, token_type, id, username } = response.data;
        this.setUser({ id: id, name: username, token: access_token });
        localStorage.setItem('user', JSON.stringify({ id: id, name: username, token: access_token }));
        this.show = false;
        EventBus.emit('getChats');
      } catch (err) {
        if (err.response.status == 401) {
          this.setUser({ 'id': '', 'name': '', 'token': '' });
          localStorage.removeItem("user");
        }
        console.log('Fehler beim Anmelden: ', err);
        this.addLog({ author: "User", text: "Fehler beim Anmelden" });
      }
    },
    
    async logout()  {
      this.pw = '';
      this.username = '';
      localStorage.removeItem("user");
      this.setUser({'id': '', 'name': '', token: ''});
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
