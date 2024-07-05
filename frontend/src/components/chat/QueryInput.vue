<template>
  <div class="query-input">
    <input v-model="input" placeholder="..." @keydown.enter="sendQuery" />
    <button @click="sendQuery">Send</button>
  </div>
</template>

<script>
import EventBus from '../../eventBus.js';
import axios from '@/axios';
import { mapGetters, mapActions } from 'vuex';

export default {
  computed: {
    ...mapGetters(['user', 'activeChat', 'chatID', 'chats', 'chatID'])
  },

  data() {
    return {
      input: '',
      onSend: false
    };
  },

  methods: {
    ...mapActions(['addLog', 'setChatID', 'addChat', 'addActiveChat', 'addMessage', 'addSource']),  

    async sendQuery() {
      if (this.onSend) { 
        console.log("Es wird auf eine Antwort des Servers gewartet");
        this.addLog({author: "QueryInput", text: "Es wird auf eine Antwort des Servers gewartet"});
        return;
       }

      EventBus.emit('toggle-spinner');
      this.addActiveChat({
        id: this.activeChat.length + 1,
        author: "user",
        message: this.input,
        loading: false
      });
      this.addActiveChat({
        id: this.activeChat.length + 1,
        author: "system",
        message: "",
        loading: true
      });
      this.onSend = true;

      try {
        const response = await axios.post('/chat', {
          chatID: this.chatID,
          userID: this.user.id,
          message: this.input
        });
        console.log("Antwort des RAG-Systems: ",  response);
        this.addLog({author: "QueryInput", text: "Antwort des RAG-Systems erhalten"});
        
        if (this.chatID > 0)  {   ;     
          this.addMessage(response.data.message);
          let sourcesList = JSON.parse(response.data.sources.replace(/'/g, '"'));
          this.addSource(sourcesList);
          this.onSend = false;
          this.addLog({author: "QueryInput", text: "Bestehenden Chat erweitert"});
        } else {
          let message = response.data.chat[response.data.chat.length -1].message;
          let sources = response.data.chat[response.data.chat.length -1].sources;
          let sourcesList = JSON.parse(sources.replace(/'/g, '"'));
          this.setChatID(response.data.chatID);
          this.addChat({userID: this.user.id, name: response.data.name, id: response.data.chatID});
          this.addMessage(message);
          this.addSource(sourcesList);
          this.onSend = false;
          this.addLog({author: "QueryInput", text: "Neuen Chat erstellt"});
        }
      } catch (error) {
        this.addMessage("Es ist ein Fehler aufgetreten");
        this.onSend = false;
        console.error("Es ist ein Fehler aufgetreten",  error);
        this.addLog({author: "QueryInput", text: "Es ist ein Fehler beim kommunizieren mit dem RAG-System aufgetreten"});
      }
      EventBus.emit('toggle-spinner');

      this.input = '';
    },
  },
};
</script>

<style scoped>
.query-input {
  max-width: 900px;
  padding: 20px;
  height: 10vh;
  text-align: center;
  width: 100%;
  margin: auto auto 0 auto;
}

input {
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 10px 0 0 10px;
  font-size: 1.25em;
  width: 77%;
  border: transparent;
  background: var(--input-background);
}

button {
  padding: 10px 20px;
  background-color: var(--btn-background-color);
  color: var(--btn-color);
  font-size: 1.25em;
  border-radius: 0 10px 10px 0;
  width: 23%;
  min-width: fit-content;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: var(--btn-hover-background-color);
}
</style>
