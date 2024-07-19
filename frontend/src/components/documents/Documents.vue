<template>
  <div class="togleData">
    <button @click="this.show = !this.show">Datenansicht wechseln</button>
      <input type="file" id="fileInput" @change="onFileChange" />
      <label for="fileInput" class="custom-file-upload">
        Datei auswählen
      </label>
      <span class="sel-file" v-if="this.selectedFile">{{ this.selectedFile.name }}</span>
      <button v-if="this.selectedFile" @click="uploadFile">Upload</button>
  </div>
  <div v-if="!show" class="database">    
    <div class="header-row">
      <div class="header-elm"> ID </div>
      <div class="header-elm"> Name </div>
    </div>

    <TableRow v-for='element in this.elements'
            :id='element.id'
            :name='element.name'
            :chunks='element.chunks'/>
  </div>
  <Plot v-if="show"></Plot>
</template>

<script>
import EventBus from '../../eventBus';
import axios from '@/axios';
import TableRow from './TableRow.vue'
import Plot from './Plot.vue';
import { mapActions } from 'vuex';

export default {
  components: {
    TableRow,
    Plot
  }, 


  data() {
    return {
      selectedFile: null,
      elements: [],
      show: false
    };
  },

  methods: {    
    ...mapActions(['addLog']),  

    async getData() {
      EventBus.emit('toggleSpinner');
      try {
        const response = await axios.get('/documents_with_chunks');
        console.log("Dokumente mit Chunks geladen: ",  response.data);
        this.addLog({author: "Docuemnts", text: "Dokumente mit Chunks geladen"});
        this.elements = response.data.documents;
      } catch (error) {
        this.addLog({author: "Docuemnts", text: error});
        console.error("Es ist ein Fehler aufgetreten",  error);
        this.addLog({author: "Documents", text: "Es ist ein Fehler beim laden der Dokumente mit Chunks aufgetreten"});
      }
      EventBus.emit('toggleSpinner');
    },

    async uploadFile() {
      if (this.selectedFile) {
        EventBus.emit('toggleSpinner');
        const formData = new FormData();
        formData.append('file', this.selectedFile);
        try {
          const response = await axios.post('/add', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
          console.log("Dokument hochgeladen:",  response);
          this.addLog({author: "Documents", text: "Dokument erfolgreich hochgeladen"});
          this.getData();
        } catch (error) {
          console.error('Es ist ein Fehler beim Hochladen einer Datei vorgekommen', error);
          this.addLog({author: "Documents", text: "Dokument konnte nicht hochgeladen werden"});
        }
        EventBus.emit('toggleSpinner');
      } else {
        console.warn('No file selected');
      }
    },
    
    onFileChange(event) {
      this.selectedFile = event.target.files[0];
    },
  }, 
  
  mounted() {
    this.getData();
  },
};
</script>

<style scoped>
.database {
  margin-top: 1em;
  padding: .5em 2em;
  display: flex;
  flex-direction: column;
}

.file-upload > input, button, label {
  padding: 0.4em;
  margin: .5em .2em;
  background-color: var(--btn-background-color);
  color: var(--btn-color);
  font-size: .75em;
  border-radius:10px;
  min-width: fit-content;
  border: none;
  cursor: pointer;
  font-family: Arial, Helvetica, sans-serif;
}

#fileInput {
  display: none;
}

.header-row {
    margin: 0.25em;    
    display: flex;
    flex-direction: row;
    font-weight: bold;
}

.header-elm {
  width: 40%;
  margin-left: .5em;
}

.togleData {
  margin: 0 auto; 
  margin-top: 1em;
  padding-left: 2em;
  display: flex;
  flex-direction: row;
}

.sel-file {
  align-self: center;
}
</style>
