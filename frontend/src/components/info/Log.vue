<template>
  <div>
    <div class="text {{class}}">{{ text }} </div>
  </div>
</template>

<script>

export default {
  components: {
  },
  props: [
    'text', 
    'author',
    'class',
  ]
}
</script>

<style scoped>
.log {
  background: var(--msg-background);
  border-radius: 10px;
  padding: 1rem;
  width: fit-content;
  max-width: 800px;
}

.log.dark {
  background: var(--msg-dark-background);
}

.author {
  font-weight: bolder;
  font-size: 1.5em;
  margin-bottom: 0.5em;
}

</style>