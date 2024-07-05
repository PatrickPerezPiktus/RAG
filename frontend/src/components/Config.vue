<template>
  <div class="config">
    <form @submit.prevent="saveConfig">
      <div class="paramWrapper">
        <div class="param">
          <label for="llm">Sprachmodell:</label>
          <select v-model="this.config.llm" id="llm" required>
            <option v-for="option1 in this.config.llmOptions" :key="option1" :value="option1">{{ option1 }}</option>
          </select>
        </div>
        <div class="param">
          <label for="embedding-model">Embedding-Model:</label>
          <select v-model="this.config.embeddingModel"  id="embedding-model" required>
            <option v-for="option2 in this.config.embeddingModelOptions" :key="option2" :value="option2">{{ option2 }}</option>
          </select>
        </div>
        <div class="param">
          <label for="vektor-DB">Vektor-DB:</label>
          <select v-model="this.config.vectorDB" id="vecttor-db" required>
            <option v-for="option3 in this.config.vectorDBOptions" :key="option3" :value="option3">{{ option3 }}</option>
          </select>
        </div>
      </div>
      <div class="param">
        <label for="prompt">Prompt:</label>
        <textarea  v-model="this.config.promptTemplate" id="prompt" required />
      </div>
      <div class="param">
        <label for="test-Prompt">Test-Promopt:</label>
        <textarea  v-model="this.config.testPrompt" id="test-prompt" required />
      </div>
      <div class="param">
        <label for="dbPath">SQL-DB:</label>
        <input v-model="this.config.dbPath" id="dbPath" type="text" required />
      </div>
      <div class="param">
        <label for="dataDump">Daten:</label>
        <input v-model="this.config.dataDump" id="dataDump" type="input" required />
      </div>
      <div class="paramWrapper">
        <div class="param">
          <label for="k">Suchparameter(k-val)</label>
          <input v-model="this.config.k" id="k" type="number" required />
        </div>
        <div class="param">
          <label for="chunkSize">Chunk-Größe:</label>
          <input v-model="this.config.chunk_size" id="chunkSize" type="number" required />
        </div>
        <div class="param">
          <label for="chunkOverlap">Chunk-Overlap:</label>
          <input v-model="this.config.chunk_overlap" id="chunkOverlap" type="number" required />
        </div>
      </div>
      <button type="submit">Speichern</button>
    </form>
  </div>
</template>

<script>
import axios from '@/axios';
import { mapActions } from 'vuex';

export default {
  data() {
    return {
      config: {
        llmOptions: ["openai","mistral"],
        embeddingModelOptions: ["openai", "cohore"],
        vectorDBOptions: ["chroma", "pinecone"],
        llm: "openai",
        embeddingModel: 'openai',
        vectorDB: 'chroma',
        promptTemplate: '',
        testPrompt: '',
        dbPath: '',
        dataDump: '',
        k: 3,
        chunk_size: 800,
        chunk_overlap: 80,
        apiKey: ''
      }
    }
  },

  methods: {
    ...mapActions(['addLog']),

    async getConfig() {
      try {
        const response = await axios.get('/get_config');
        this.addLog({author: "Config", text: "konfiguration geladen"});
        console.log('aktuelle Konfiguration:', response.data);
  
        this.config = response.data.config;
      } catch (error) {
        this.addLog({author: "Config", text: "error"})
        console.error('Fehler beim Laden der Konfiguration:', error);
      }
    },

    async saveConfig() {
      try {
        const response = await axios.post('/update_config', this.config);
        console.log('Konfiguration gespeichert:', response.data);
        this.addLog({author: "Config", text: "konfiguration gespeichert"});
      } catch (error) {
        console.error('Fehler beim Speichern der Konfiguration:', error);
        this.addLog({author: "Config", text: "Fehler beim Speichern der Konfiguration"});
      }
    }
  },

  mounted() {
    this.getConfig();
  }
};
</script>

<style scoped>
.paramWrapper {
  display: flex;
  flex-direction: row;
}

input, select, textarea {
  padding: 5px;
  width: 100%;
  border-radius: 10px;
  border: transparent;
  background: var(--input-background);
}

textarea {
  height: 8em;
}

button {
  padding: 10px 20px;
  background-color: var(--btn-background-color);
  color: var(--btn-color);
  font-size: 1.25em;
  border-radius: 10px;
  min-width: fit-content;
  border: none;
  cursor: pointer;
}

form {
  padding: .5em 2em;
  display: flex;
  flex-direction: column;
}

.param {
  margin: auto;
  margin-bottom: 20px;
  width: 100%;
  padding: 0 .2em;
}

@media screen and (min-width: 1200px) {
  .param {
    width: 66%;
  }
}

</style>
