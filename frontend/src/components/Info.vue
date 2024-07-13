<template>
  <div class="all-log-wrapper">
    <div class="logs-wrapper">
      <div v-if="logs.length > 0" ref='logs' class='logs'>
        <div class="log" v-for='log in this.logs'>
          <div class="log-wrapper" @click="log.show = !log.show">
            <div class="log-time">{{ new Date(log.time).toLocaleString() }} &nbsp;</div>
            <div class="log-author">{{ log.author }}  </div>
          </div>
          <div v-if="log.show" class="log-text">{{ log.text }}</div>
        </div>
        
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';

export default {
  computed: {
    ...mapGetters(['logs'])
  },

  data() {
    return {
      loading: false
    };
  },

  methods: {
    ...mapActions(['addLog']),

    toggleSpinner() {
      this.loading = !this.loading;
    },
  }
};
</script>

<style scoped>
.logs-wrapper {
  margin: 1em;
}

.logs {
  overflow: auto;
  padding: 1em;
  background: var(--msgs-background);
  margin: 1em auto;
  max-width: 800px;
  border-radius: 10px;
  overflow-y: auto;
}

.log + .log {
  margin-top: 1rem;
}

.log.right {
  margin-left: auto;
}

.log-wrapper {
  display: flex;
  flex-direction: row;
  cursor: pointer;
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
