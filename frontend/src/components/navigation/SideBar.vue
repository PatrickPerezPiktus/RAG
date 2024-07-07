<template>
  <div class="side-bar">
    <div class="menu">
      
      <div class="side-bar-elm" @click="changePage('config')">
        <div class="text"><font-awesome-icon :icon="['fas', 'gear']"  /> Einstellungen</div>
      </div>
      
      <div class="side-bar-elm" @click="changePage('documents')">
        <div class="text"><font-awesome-icon :icon="['fas', 'database']"  /> Daten</div>
      </div>
      
      <div class="side-bar-elm" @click="changePage('info')">
        <div class="text"><font-awesome-icon :icon="['fas', 'info']"  /> Info</div>
      </div>
      
      <div class="side-bar-elm" @click="openChat(0)">
        <div class="text"><font-awesome-icon :icon="['fas', 'comment']"  /> neuer Chat</div>
      </div>
      <hr>
    </div>
    <div class="chats">
    <div v-for='chat in this.chats' class="side-bar-elm" @click="openChat(chat)">
        <div v-if='!chat.showInput' class="elm-content text">{{ chat.name }} </div>
        <div class="elm-content" v-if='!chat.showInput' @click="chat.showInput = !chat.showInput">
          <font-awesome-icon :icon="['fas', 'bars']" />
        </div>
        <div class="elm-content delete" v-if='chat.showInput' @click="deleteChat(chat)">
          <font-awesome-icon :icon="['fas', 'trash']" />
        </div>
        <input class="elm-content" v-if='chat.showInput' v-model="chat.name" />
        <div class="elm-content" v-if='chat.showInput'
              @click="renameChat(chat); chat.showInput = !chat.showInput">
          <font-awesome-icon :icon="['fas', 'pen']" />
        </div>
        <div class="elm-content" v-if='chat.showInput' @click="chat.showInput = !chat.showInput">
          <font-awesome-icon :icon="['fas', 'x']" />
        </div>
      </div>
      
    </div>
  </div>
</template>

<script>
import EventBus from '../../eventBus.js';
import axios from '@/axios';
import { mapGetters, mapActions } from 'vuex';

export default {
  computed: {
    ...mapGetters(['chats', 'user', 'activeChat', 'chatID'])
  },
  data() {
    return {
      name: '',
      showInput: false,
    };
  },

  created() {
    EventBus.on('getChats', this.getChats);
  },

  methods: {
    ...mapActions(['addLog', 'setChats', 'setActiveChat', 'setChatID', 'delChat', 'renChat']),  

    toggleSpinner() {
      this.loading = !this.loading;
    },

    changePage(page) {
      EventBus.emit('changePage', page);
    },

    async openChat(chat) {
      if (chat == 0) {
        this.setActiveChat([{
          id: 0,
          author: "chat",
          message: "Frag etwas...",
          loading: false
        }]);
        this.setChatID(0);
      } else {
        try {
          const response = await axios.get('/chat?chatID='+chat.id);
          console.log("Chat geladen: ",  response);
          this.addLog({author: "SideBar", text: "Chat wurde geladen"});
          
          response.data.forEach(msg => {
            if (msg.sources != '') {  
              let sourcesList = JSON.parse(msg.sources.replace(/'/g, '"'));
              msg.sources = sourcesList;
            }            
          });
          this.setChatID(chat.id);
          this.setActiveChat(response.data);
        } catch (error) {
          console.error('Fehler beim Laden eines Chats:', error);
          this.addLog({author: "SideBar", text: "Fehler beim Laden eines Chats"});
        }
      }
      EventBus.emit('changePage', 'chat');
    },

    async getChats() {
      if (this.user.id == '') {
        this.setChats([]);
        this.chatID = 0;
        return;
      }
      try {
        const response = await axios.get('/user_chats?userID='+this.user.id);
        console.log('Chats geladen', response);
        this.addLog({author: "SideBar", text: "Chats geladen"});
        this.setChats(response.data);
      } catch (error) {
        console.error('Fehler beim Laden eines Chats:', error);
        this.addLog({author: "SideBar", text: "Fehler beim Laden eines Chats"});
        return;
      }
    },

    async deleteChat(chat) {
      try {
          const response = await axios.post('/delete_chat?chatID='+chat.id);
          console.log('Chat gelöscht: ', response);
          this.addLog({author: "SideBar", text: "Chat gelöscht"});
          
          this.delChat(chat.id);
          this.setChatID(0);
          this.setActiveChat([{
            id: 0,
            author: "system",
            text: "Frag etwas...",
            loading: false
          }]);
        } catch (error) {
          console.error('Fehler beim Löschen eines Chats:', error);
          this.addLog({author: "SideBar", text: "Fehler beim Löschen eines Chats"});
        }
    },
    
    async renameChat(chat) {
        try {
          const response = await axios.post('/rename_chat', {chatID: chat.id, chatName: chat.name});
          console.log('Chat umbenannt: ', response);
          this.addLog({author: "SideBar", text: "Chat umbenannt"});

          this.renChat(response.data);
        } catch (error) {
          console.error('Fehler beim Umbenennen des Chats:', error);
          this.addLog({author: "SideBar", text: "Fehler beim Umbenennen des Chats"});
        }
        this.showInput = false;
    }
  },
};
</script>

<style scoped>
.menu {
  padding-top: .5em;
}

.side-bar {
  height: 95vh;
  overflow-y: auto;
  background: var(--sidebar-background);
  width: 300px;
  border-right: 1px solid;
}
@media screen and (max-width: 600px) {
  .side-bar {
    min-width: 100%;
  }
}
.side-bar-elm {
  padding: 1em;
  border-radius: 10px;
  margin: 0 0.5em;
}

button, label {
  padding: 0.4em;
  margin: .5em .2em;
  background-color: var(--btn-background-color);
  color: var(--btn-color);
  font-size: .75em;
  border-radius:10px;
  min-width: fit-content;
  border: none;
  cursor: pointer;
}

#fileInput {
  display: none;
}

.side-bar-elm {
  padding: 1em;
  border-radius: 10px;
  margin: 0.5em;
  display: flex;
}

.side-bar-elm:hover {
  background: var(--sidebar-elm-background-color);
  cursor: pointer;
}

input {
  font-size: 1em; 
  margin: 0;
  min-width: auto;
  width: 100%;
  color: var(--color-input);
  background: transparent;
  border: 1px solid;
  border-radius: 5px;
}


.elm-content {
  padding: 0 0.25em;
}

.text {
  width: 100%;
  overflow: hidden;
}

.delete {
  margin: 0;
}

.delete svg:hover {
  color: var(--warn);
}
</style>
