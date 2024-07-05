<template>
  <div class="chat-elm">
    <div class='messages'>
        <div v-for='message in this.activeChat' :class="['message', message.author]" :key="message.id">
          <div class="text">{{ message.message }} </div>
          <div v-if="message.sources" class="sources">
            <div class="source-wrapper">
              <div class="source-text" @click="message.showSources = !message.showSources"> 
                Quellen &nbsp;
                <font-awesome-icon :icon="['fas', 'minus']" v-if="message.showSources"/>
                <font-awesome-icon :icon="['fas', 'plus']" v-if="!message.showSources"/>
              </div>
              <div class="source" v-if="message.showSources" v-for="s in message.sources" @click="getChunk(s, message); message.showChunk = true"> {{ s }}</div>
            </div>
            <ChunkRow v-if="message.showChunk" @click="message.showChunk = false" :chunkID="message.chunk?.chunkID" :content="message.chunk?.content"/>
          </div>
          <div v-if="message.loading"><Loading/></div>
        </div>
    </div>
    <QueryInput v-if="this.activeChat.length > 0" />
  </div>
</template>

<script>
import EventBus from '../../eventBus.js';
import axios from '@/axios';
import { mapGetters, mapActions } from 'vuex';
import Loading from './Loading.vue';
import QueryInput from "./QueryInput.vue";
import ChunkRow from '../utils/ChunkRow.vue';

export default {
  components: {
    QueryInput,
    Loading,
    ChunkRow
  },

  computed: {
    ...mapGetters(['chats', 'user', 'activeChat', 'chatID'])
  },

  data() {
    return {
      loading: false,
      chunk: false
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
        this.addLog({author: "Config", text: "chunk "+chunkID+" geladen"});

        message.chunk = response.data;
      } catch (error) {
        console.error("Es ist ein Fehler aufgetreten", error);
        this.addLog({author: "Config", text: "Es ist ein Fehler beim laden eines Chunks aufgetreten"});
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
  max-width: 800px;
  padding: .5em;
  margin: 0 auto;
  width: 100%;
}

.message + .message {
  margin: .5em .5em 0 0;
}

.message.user {
  margin-left: auto;
}

.message {
  background: var(--msg-background);
  border-radius: 10px 10px 0 10px;
  padding: .5em;
  width: fit-content;
  max-width: 800px;
}

.message.user {
  background: var(--msg-dark-background);
}

.author {
  font-weight: bolder;
  font-size: 1.5em;
  margin-bottom: 0.5em;
}

.sources {
  font-size: 14px;
  display: flex;
  border-top: 2px solid;
  margin-top: 1em;
}

.source-wrapper {
  display: flex;
  flex-direction: column;
}

.source-text {
  color: var(--color);
  margin-top: 1em;
  display: flex;
  flex-direction: row;
}

.source:hover {
  color: var(--btn-hover-background-color);
  cursor: pointer;
}

.chunk-row {
  padding: .25em;
  padding-left: 7em;
  text-align: justify;
  border: none;
}

.hl {
  font-size: 20px;
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
