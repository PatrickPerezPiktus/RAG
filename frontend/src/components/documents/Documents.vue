<template>
  <div class="database">
    
    <div class="header-row">
      <div class="header-elm"> ID </div>
      <div class="header-elm"> Name </div>
    </div>

    <TableRow v-for='element in elements'
            :id='element.id'
            :name='element.name'
            :chunks='element.chunks'/>
    <div class="file-upload">
        <input type="file" id="fileInput" @change="onFileChange" />
        <label for="fileInput" class="custom-file-upload">
          Datei auswählen
        </label>
        <span v-if="selectedFile">{{ selectedFile.name }}</span>
        <button @click="uploadFile">Upload</button>
      </div>
  </div>
</template>

<script>
import EventBus from '../../eventBus';
import axios from 'axios';
import { onMounted, ref } from 'vue';
import TableRow from './TableRow.vue'

export default {
  components: {
    TableRow
  }, 
  setup() {
    const selectedFile = ref(null);
    const elements = ref([]);

    const onFileChange = (event) => {
      selectedFile.value = event.target.files[0];
    };

    const getData = async () => {
      
      EventBus.emit('toggleSpinner');
      try {
        const response = await axios.get('http://localhost:9000/documents_with_chunks');
        console.log('aktuelle Dokumente:', response.data);
        EventBus.emit('add-log',{
              author: 'Documents',
              text: response.data
            });
        elements.value = response.data.documents;
      } catch (error) {
        console.error('Fehler beim Laden der Dokumente:', error);
        EventBus.emit('add-log',{
              author: 'Documents',
              text: error
            });
      }
      EventBus.emit('toggleSpinner');
    };

  
    const uploadFile = async () => {
      if (selectedFile.value) {
        EventBus.emit('toggleSpinner');
        const formData = new FormData();
        formData.append('file', selectedFile.value);
        try {
          const response = await axios.post('http://localhost:9000/add', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          });
          console.log('File uploaded successfully', response.data);
              
          EventBus.emit('add-log',{
              author: 'Documents',
              text: response.data
            });
          getData();
        } catch (error) {
          console.error('Error uploading file', error);
          EventBus.emit('add-log',{
              author: 'Documents',
              text: error
            });
        }
        EventBus.emit('toggleSpinner');
      } else {
        console.warn('No file selected');

      }
    };

    onMounted(() => {
      getData();
    });

    return {
      elements,
      selectedFile,
      onFileChange,
      uploadFile
    };
  }
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
</style>
