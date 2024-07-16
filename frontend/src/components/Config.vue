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
          <select v-model="this.config.vectorDB" id="vektor-db" required>
            <option v-for="option3 in this.config.vectorDBOptions" :key="option3" :value="option3">{{ option3 }}</option>
          </select>
        </div>
        <div class="param">
          <label for="rag-method">rag-Methode:</label>
          <select v-model="this.config.activeRAG" id="rag-method" required>
            <option v-for="option4 in this.config.RAGOptOptions" :key="option4" :value="option4">{{ option4 }}</option>
          </select>
        </div>
      </div>
      <div class="param">
        <label for="prompt">Prompt:</label>
        <textarea  v-model="this.config.promptTemplate" id="prompt" required />
      </div>
      <div class="param">
        <label for="multiQuery_template">MultiQuery-Prompt:</label>
        <textarea  v-model="this.config.multiQuery_template" id="multiQuery_template" required />
      </div>
      <div class="param">
        <label for="hyde_template">HyDE-Prompt:</label>
        <textarea  v-model="this.config.hyde_template" id="hyde_template" required />
      </div>
      <div class="paramWrapper">
        <div class="param">
          <label for="temperature">LLM-Kreativität</label>
          <input v-model="this.config.temperature" id="temperature" type="number" required />
        </div>
        <div class="param">
          <label for="k">Chunk-Anzahl bei Suche</label>
          <input v-model="this.config.k" id="k" type="number" required />
        </div>
      </div>
      <div class="paramWrapper">
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
        llmOptions: ["openai", "mistral", "llama"],
        embeddingModelOptions: ["openai", "cohore", "local"],
        vectorDBOptions: ["chroma"],
        RAGOptOptions: ["simple", "hyde", "multi"],
        llm: "openai",
        embeddingModel: '',
        vectorDB: '',
        activeRAG: '',
        promptTemplate: '',
        multiQuery_template: '',
        hyde_template: '',
        temperature: 0,
        k: 0,
        chunk_size: 0,
        chunk_overlap: 0
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
.config {
  max-width: 800px;
  margin: 0 auto;
}

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
</style>
