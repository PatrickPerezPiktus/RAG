<template>
  <div class="log-wrapper">
    <div class="logs-wrapper">
      <div v-if="logs.length > 0" ref='logs' class='logs'>
        <Log v-for='log in logs'
            :key='log.time'
            :class='["log", log.logClass]'
            :dark='log.isMine'
            :text='log.text'
            :author='log.author'
        />
        
      </div>
    </div>
  </div>
</template>

<script>
import EventBus from '../../eventBus.js';
import { mapGetters, mapActions } from 'vuex';
import Log from "./Log.vue";

export default {
  components: {
    Log,
  },

  computed: {
    ...mapGetters(['logs'])
  },

  data() {
    return {
      user: { name: "User", id: 1 },
      loading: false
    };
  },

  created() {
    EventBus.on('add-log', this.addLog);
  },

  methods: {

    ...mapActions(['addLog']),
    toggleSpinner() {
      this.loading = !this.loading;
    },
    addNewLog() {
      const newLog = {
        author: 'user',
        text: 'New log entry',
        logClass: 'info'
      };
      this.addLog(newLog);
    }
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

@media (min-width: 1024px) {
  body {
    place-items: center;
  }

  #app {
    margin: 0 2rem;
  }
}
</style>
