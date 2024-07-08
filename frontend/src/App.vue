<template>
  <div class="header">
    <div class="logo" @click="menu = !menu; ">🦝 RAG</div>
    <User />
    <div class="theme-btn">
      <font-awesome-icon :icon="['fas', 'moon']" v-if="!thema" @click="this.toogleTheme()"  />
      <font-awesome-icon :icon="['fas', 'sun']" v-if="thema" @click="this.toogleTheme()"  />
    </div>
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
import Info from './components/Info.vue';

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
    menu: true,
    thema: false
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
    },

    toogleTheme() {
      this.thema = !this.thema;
      let lightElements = document.getElementsByClassName("light");
      let darkElements = document.getElementsByClassName("dark");

      if (lightElements.length > 0) {
        for (let i = 0; i < lightElements.length; i++) {
          lightElements[i].classList.add('dark');
          lightElements[i].classList.remove('light');
        }
      } else {
        for (let i = 0; i < darkElements.length; i++) {
          darkElements[i].classList.add('light');
          darkElements[i].classList.remove('dark');
        }
      }
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
  /**font-family: 'Courier New', monospace; */
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
  cursor: pointer;
}

.app {
  display: flex;
  background: var(--main-background);
}

.content {
  width: 100%;
  height: 95vh;
  max-height: 95vh;
  overflow: auto;  
}

svg:hover {
  color: var(--color-hover);
}

.theme-btn {
  margin: 0 .5em 0 0;
}
</style>
