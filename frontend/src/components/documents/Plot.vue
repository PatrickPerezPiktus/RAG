<template>
  
  <div class="plot-info"> 
    <button @click="this.umap = !this.umap; this.fetchData()">Dimensionsreduzierung wechseln</button>
    <div class="reduktion-mth">
      <div v-if="this.umap">&nbsp; UMAP</div>
      <div v-if="!this.umap">&nbsp; PCA</div>
    </div>
  </div>
  
  <div class="plot-info">
    Hervorgehobene Chunks: &nbsp;
    <div v-if="this.highlightChunks && this.highlightChunks.length > 0" v-for="chunk in this.highlightChunks"> {{ chunk }} &nbsp;</div>
  </div>
  <div class="plot">
    <div ref="plotContainer"></div>
    <ChunkRow v-if="this.chunk" :chunkID="this.chunk?.chunkID" :content="this.chunk?.content" @click="this.chunk = null;"/>
  </div>
</template>

<script>
import EventBus from '../../eventBus';
import Plotly from 'plotly.js-dist-min';
import axios from '@/axios';
import { mapGetters, mapActions } from 'vuex';
import ChunkRow from '../utils/ChunkRow.vue';

export default {
  components: {
    ChunkRow
  }, 

  computed: {
    ...mapGetters(['activeChat'])
  },

  data() {
    return {
      show: false,
      rawData: [],
      rawIds: [],
      chunk: null,
      documents: [],
      activePoint: null,
      highlightChunks: [],
      umap: false,
    }
  },
  mounted() {
    if (this.activeChat.length > 0) {
      this.highlightChunks = this.activeChat[this.activeChat.length-1].sources;
    }
    this.fetchData();
  },
  methods: {
    ...mapActions(['addLog']),  

    async fetchData() {
      EventBus.emit('toggleSpinner');
      try {
        const docs = await axios.get('/documents');
        this.documents = docs.data.documents;
        this.setColors();
        let response;
        //const response = await axios.get('/embedded_data_umap');
        if (this.umap) {
          response = await axios.get('/embedded_data_umap');
        } else {
          response = await axios.get('/embedded_data');
        }
        this.rawData = response.data.vectors;
        this.rawIds = response.data.ids; 
        this.drawPlot();
        console.log("Vektoren für Ploting geladen:",  response);
        this.addLog({author: "Plot", text: "Vektoren für Ploting geladen"});
      } catch (error) {
        console.log("Fehler beim Laden der Vektoren:",  error);
        this.addLog({author: "Plot", text: "Fehler beim Laden der Vektoren"});
      }
      EventBus.emit('toggleSpinner');
    },

    drawPlot() {
      const xData = this.rawData.map(point => point[0]);
      const yData = this.rawData.map(point => point[1]);
      const zData = this.rawData.map(point => point[2]);
      const labels = this.rawIds.map(id => id);
      const colors = labels.map(label => this.getColorByLabel(label));
      const sizes = labels.map(label => this.getSize(label));
      this.originalColors = colors;
      const data = [{
        x: xData,
        y: yData,
        z: zData,
        text: labels,
        mode: 'markers',
        type: 'scatter3d',
        marker: {
          color: colors,
          size: sizes,
          opacity: 0.8
        }
      }];

      
      const layout = {
        title: '3D Scatter Plot',
        autosize: true,
        margin: {
          l: 0,
          r: 0,
          b: 0,
          t: 0
        }
      };
      
      Plotly.newPlot(this.$refs.plotContainer, data, layout);
      this.$refs.plotContainer.on('plotly_click', this.onPointClick);
    },

    setColors() {
      this.documents.forEach(doc => {
        doc.name = doc.name.split('.')[0];
        doc.color = '#'+Math.floor(Math.random()*16777215).toString(16);
      });
    },

    getColorByLabel(label) {
      let color = 'blue';
      this.documents.forEach(doc => {
        if (label.includes(doc.name)) { color = doc.color; }
      });
      if (this.highlightChunks && this.highlightChunks.length > 0) {
        this.highlightChunks.forEach(chunk => {
          if (label.includes(chunk)) { color = 'red'; }
        });
      }
      return color;  
    },

    getSize(label) {
      let size = 8;
      if (this.highlightChunks && this.highlightChunks.length > 0) {
        this.highlightChunks.forEach(chunk => {
          if (label.includes(chunk)) { size = 16; }
        });
      }
      return size;  
    },

    async onPointClick(data) {
      this.activePoint = data;
      const id = data.points[0].text;
      await this.getChunk(id);
    },
        
    async getChunk(chunkID) {
      try {
        const response = await axios.get('/load_chunk_by_id?chunkID='+chunkID);
        console.log("Chunk geladen: {}", response.data);
        this.addLog({author: "Plot", text: "chunk "+chunkID+" geladen"});

        this.chunk = response.data;
      } catch (error) {
        console.error("Es ist ein Fehler aufgetreten", error);
        this.addLog({author: "Plot", text: "Es ist ein Fehler beim laden eines Chunks aufgetreten"});
      }
    }

  }
}
</script>

<style>

.main-svg {
  background: transparent !important;
}

.plot {
  margin: 0 auto;
  max-width: 800px;
}

.plot-info {
  margin: 0 auto;
  width: 800px;
  align-items: center;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}

</style>
<style scoped>
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
</style>
