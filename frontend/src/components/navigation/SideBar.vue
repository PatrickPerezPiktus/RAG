<template>
  <div class="side-bar">
    <div class="elements-wrapper">
      <div>
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
            <input class="elm-content" v-if='chat.showInput' v-model="chat.name" />
            <div class="elm-content" v-if='chat.showInput'
                  @click="renameChat(chat); chat.showInput = !chat.showInput">
              <font-awesome-icon :icon="['fas', 'pen']" />
            </div>
            <div class="elm-content" v-if='chat.showInput' @click="deleteChat(chat)">
              <font-awesome-icon :icon="['fas', 'trash']" />
            </div>
          </div>
          
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import EventBus from '../../eventBus.js';
import axios from 'axios';
import { mapGetters, mapActions } from 'vuex';

export default {
  computed: {
    ...mapGetters(['chats', 'user', 'activeChat', 'chatID'])
  },
  created() {
    EventBus.on('loadChats', this.getChats);
  },
  data() {
    return {
      name: '',
      showInput: false,
    };
  },

  methods: {
    
    ...mapActions(['setChats', 'setActiveChat', 'setChatID', 'delChat', 'renChat']),  
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
          const response = await axios.get('http://localhost:9000/chat?chatID='+chat.id);
          console.debug(response)
          
          response.data.forEach(msg => {
            console.debug(msg);
            if (msg.sources != '') {  
              let sourcesList = JSON.parse(msg.sources.replace(/'/g, '"'));
              msg.sources = sourcesList;
            }            
          });
          this.setChatID(chat.id);
          this.setActiveChat(response.data);
        } catch (error) {
          console.error('Fehler beim Laden der Chats:', error);
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
        console.debug(this.user);
        const response = await axios.get('http://localhost:9000/user_chats?userID='+this.user.id);
        this.setChats(response.data);
        console.log('Chats:', response.data);
        
        EventBus.emit('add-log',{
          author: 'sidebar',
          text: response.data
        });
      } catch (error) {
        if (error.response.status == 404) {
          console.log("keine msgs des Chats gefunden");
          return;
        }
        console.error('Fehler beim Laden der Chats:', error);
        EventBus.emit('add-log',{
          author: 'sidebar',
          text: error
        });
      }
    },
    async deleteChat(chat) {
      console.debug(this.chatID);
      try {
          const response = await axios.post('http://localhost:9000/delete_chat?chatID='+chat.id);
          console.debug(response);
          
          let index = this.chats.findIndex(obj => {console.debug(obj); return obj.id != chat.id});
          
          this.delChat(chat.id);
          this.setChatID(0);
          this.setActiveChat([{
            id: 0,
            author: "system",
            text: "Frag etwas...",
            loading: false
          }]);
          console.debug(this.chatID);

        } catch (error) {
          console.error('Fehler beim Laden der Chats:', error);
        }
    },
    async renameChat(chat) {
        console.debug("rename");
        try {
          const response = await axios.post('http://localhost:9000/rename_chat', {chatID: chat.id, chatName: chat.name});
          console.debug(response.data);
          this.renChat(response.data);
        } catch (error) {
          console.error('Fehler beim Laden der Chats:', error);
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

.elements-wrapper {
  height: 95vh;
  overflow-y: auto;
}

.side-bar-elm {
  padding: 1em;
  border-radius: 10px;
  margin: 0 0.5em;
}

.side-bar {
  background: var(--sidebar-background);
  width: 280px;
  height: 95vh;
  border-right: 1px solid;
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
</style>
