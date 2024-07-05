<template>
  <div class="query-input">
    <input v-model="input" placeholder="..." @keydown.enter="sendQuery" />
    <button @click="sendQuery">Send</button>
  </div>
</template>

<script>
import EventBus from '../../eventBus.js';
import axios from 'axios';
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
    ...mapActions(['setChatID', 'addChat', 'addActiveChat', 'addMessage', 'addSource']),  
    async sendQuery() {
      if (this.onSend) { console.debug("es wird auf eine Antwort des Servers gewartet"); return; }

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
        const response = await axios.post('http://localhost:9000/chat', {
          chatID: this.chatID,
          userID: this.user.id,
          message: this.input
        });
        if (this.chatID > 0)  {   
          console.debug(response);     
          this.addMessage(response.data.message);
          let sourcesList = JSON.parse(response.data.sources.replace(/'/g, '"'));
          this.addSource(sourcesList);
          this.onSend = false;
        } else {
          let message = response.data.chat[response.data.chat.length -1].message;
          let sources = response.data.chat[response.data.chat.length -1].sources;
          let sourcesList = JSON.parse(sources.replace(/'/g, '"'));
          this.setChatID(response.data.chatID);
          this.addChat({userID: this.user.id, name: response.data.name, id: response.data.chatID});
          this.addMessage(message);
          this.addSource(sourcesList);
          this.onSend = false;
        }
      } catch (error) {
        this.addMessage("Es ist ein Fehler aufgetreten");
        this.onSend = false;
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
  margin: auto 0 0 0;
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
