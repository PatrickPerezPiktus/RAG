<template>
  <div id="spinner"></div>
</template>

<script>

</script>

<style scoped>
  #spinner {
    position: absolute; 
    width: 50px;
    height: 50px;
    border: 6px solid var(--spinner-border);
    border-radius: 50%;
    margin: 2em;
    bottom: 0;
    border-top-color: transparent;
    animation: spin 1s ease-in-out infinite;
    -webkit-animation: spin 1s ease-in-out infinite;
  }

  @keyframes spin {
    to { -webkit-transform: rotate(360deg); }
  }
  
  @-webkit-keyframes spin {
    to { -webkit-transform: rotate(360deg); }
  }
</style>