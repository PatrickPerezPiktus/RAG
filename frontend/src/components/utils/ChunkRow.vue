<template>
  <div class="chunk-row">
    <div class="hl">{{ chunkID }}</div>
    <div class="text">{{ content }}</div>
  </div>
</template>

<script>
export default {
  props: [
    'chunkID',
    'content'
  ]
}
</script>

<style scoped>
.hl {
  font-weight: 600;
  margin-bottom: 1em;
  font-size: 22px;
}

.text {
  font-family: sans-serif;
}

.chunk-row {
  border-radius: 10px;
  margin: 0.25em;    
  display: flex;;
  flex-direction: column;
  padding: .25em;
  border: 1px solid;
}

.chunk-elm:last-child {
  border-right: none;
}

.chunk-elm {
  border-right: 1px solid;
  padding: .5em;
  width: 40%;
}
</style>