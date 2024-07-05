<template>
  
  
  <div class="header">
    <div class="logo" @click="menu = !menu">🦝 RAG-Chat</div>
    <User />
  </div>
  <div class='app'>
    <SideBar v-if="menu" />
    <div class='content'>
      <Info v-if="activePage=='info'"/>
      <Chat v-if="activePage==='chat'"/>
      <Config v-if="activePage==='config'"/>
      <Documents v-if="activePage==='documents'"/>
      <Spinner v-if="spinning"/>
    </div>
  </div>
</template>

<script>
import EventBus from './eventBus.js';
import User from './components/navigation/User.vue';
import SideBar from './components/navigation/SideBar.vue';
import Spinner from './components/utils/Spinner.vue';
import Chat from './components/chat/Chat.vue';
import Config from './components/Config.vue';
import Documents from './components/documents/Documents.vue';
import Info from './components/info/Info.vue';

export default {
  components: {
    User,
    SideBar,
    Chat,
    Documents,
    Spinner,
    Config,
    Info
  },

  data: () => ({
    activePage: "info",
    spinning: false,
    menu: true
  }),

  created() {
    EventBus.on('changePage', this.changePage);
    EventBus.on('toggleSpinner', this.toggleSpinner);
  },

  methods: {
    toggleSpinner() {
      this.spinning = !this.spinning;
    },    
    changePage(page) {
      this.activePage = page;
      console.debug(this.activePage)
    }
  }
};
</script>

<style>
* {
  box-sizing: border-box;
}

html {
  font-family: 'Lucida Console', 'Georama', sans-serif;
}

body {
  margin: 0;
}

.header{
  width: 100%;
  background-color: var(--sidebar-background);
  display: flex;
  flex-direction: row;
  align-items: center;
  height: 5vh;
  border-bottom: 1px solid;
}

.logo {
  font-weight: 800;
  font-size: 20px;
  color: var(--logo-color);
  border-radius: 10px;
  margin: 0.5em;
}

.app {
  display: flex;
}

.content {
  width: 100%;
}

svg:hover {
  color: var(--color-hover);
}
</style>
