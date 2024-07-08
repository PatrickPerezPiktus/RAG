<template>
  <div class="chat-elm">
    <div class='messages'>
        <div v-for='message in this.activeChat' :class="['message', message.author]" :key="message.id">
          <div class="text">{{ message.message }} </div>
          <div v-if="message.sources" class="sources">
            <div class="source-wrapper">
              <div class="source-text">Quellen: &nbsp;</div>
              <div class="source" v-for="s in message.sources" @click="getChunk(s, message); message.showChunk = true"> {{ s }} &nbsp;</div>
              <font-awesome-icon :icon="['fas', 'minus']" v-if="message.showChunk" @click="message.showChunk = !message.showChunk;"/>
            </div>
            <ChunkRow v-if="message.showChunk" :chunkID="message.chunk?.chunkID" :content="message.chunk?.content"/>
          </div>
          <div v-if="message.loading"><Loading/></div>
        </div>
    </div>
    <div class="togleData">
      <button @click="this.show = !this.show">Datenansicht wechseln</button>
    </div>
    <QueryInput v-if="this.activeChat.length > 0" />
    <Plot v-if="this.show"></Plot>
  </div>
</template>

<script>
import EventBus from '../../eventBus.js';
import axios from '@/axios';
import { mapGetters, mapActions } from 'vuex';
import Loading from './Loading.vue';
import QueryInput from "./QueryInput.vue";
import ChunkRow from '../utils/ChunkRow.vue';
import Plot from '../documents/Plot.vue';

export default {
  components: {
    QueryInput,
    Loading,
    ChunkRow,
    Plot
  },

  computed: {
    ...mapGetters(['chats', 'user', 'activeChat', 'chatID'])
  },

  data() {
    return {
      loading: false,
      chunk: false,
      show: false
    }
  },

  created() {
    EventBus.on('toggle-spinner', this.toggleSpinner);
  },

  methods: {
    ...mapActions(['addLog', 'setActiveChat', 'addActiveChat']),  

    toggleSpinner() {
      this.loading = !this.loading;
    },

    async getChunk(chunkID, message) {
      try {
        const response = await axios.get('/load_chunk_by_id?chunkID='+chunkID);
        console.log("Chunk geladen: {}", response.data);
        this.addLog({author: "Chat", text: "chunk "+chunkID+" geladen"});

        message.chunk = response.data;
      } catch (error) {
        console.error("Es ist ein Fehler aufgetreten", error);
        this.addLog({author: "Chat", text: "Es ist ein Fehler beim laden eines Chunks aufgetreten"});
      }
    }
  },
};
</script>

<style scoped>
.chat-elm {
  overflow-y: auto;
  max-height: 95vh;
  height: 95vh;
  display: flex;
  flex-direction: column;
}

.messages {
  background: var(--msgs-background);
  padding: .5em;
  margin: .5em auto;
  max-width: 800px;
  width: 100%;
}

.message + .message {
  margin: .5em .5em 0 0;
}

.message {
  background: var(--msg-background);
  border-radius: 10px 10px 0 10px;
  padding: .5em;
  width: fit-content;
}

.message.user {
  background: var(--msg-dark-background);
  margin-left: auto;
}

.author {
  font-weight: bolder;
  font-size: 1.5em;
  margin-bottom: 0.5em;
}

.sources {
  font-size: 14px;
  display: flex;
  flex-direction: column;
  border-top: 2px solid;
  margin-top: 1em;
}

.source-wrapper {
  display: flex;
  flex-direction: row;
  margin: .5em 0;
}

.source-text {
  color: var(--color);
  margin-right: 1em;
  display: flex;
  flex-direction: row;
}

.source:hover {
  color: var(--btn-hover-background-color);
  cursor: pointer;
}

.chunk-row {
  text-align: justify;
  border: none;
}

.hl {
  font-size: 20px!important;
}

button {
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

.togleData {
  padding-left: 1em;
  margin: 0 auto; 
  width: 800px;
}

@media (min-width: 1024px) {
  body {
    place-items: center;
  }

  #app {
    margin: 0 2rem;
  }
}

</style>
