<template>
  <div class="data-row">
    <div class="data-elm">{{ id }} </div>
    <div class="data-elm">{{ name }} </div>
    <div class="data-elm btn-elm">
      <button @click="showChunks=!showChunks">Show Chunks</button>
    </div>
  </div>
  <div class="chunk-wrapper" v-if="showChunks">
      <ChunkRow v-for="chunk in chunks" :key="chunk.chunkID" :chunkID="chunk.chunkID" :content="chunk.content"/>
  </div>
</template>

<script>
import ChunkRow from '../utils/ChunkRow.vue';

export default {
  components: {
    ChunkRow
  },
  props: [
    'id',
    'name',
    'chunks'
  ],
  data() {
    return {
      showChunks: false
    };
  },
}
</script>

<style scoped>
.data-row {
    border-radius: 10px;
    margin: 0.25em;    
    display: flex;
    flex-direction: row;
    border: 1px solid;
}
.data-elm:last-child {
  border-right: none;
}
.data-elm {
  border-right: 1px solid;
  padding: .5em;
  width: 40%;
}
.btn-elm {
  padding: 0cm;
}
button {
  padding: 0.4em;
  background-color: var(--btn-background-color);
  color: var(--btn-color);
  border-radius: 0 10px 10px 0;
  min-width: fit-content;
  border: none;
  cursor: pointer;
  width: 100%;
  height: 100%;
}
</style>