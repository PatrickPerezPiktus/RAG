import { createStore } from 'vuex';

export default createStore({
  state: {
    logs: [{
      time: new Date().getTime(),
      author: 'store',
      text: 'System Up',
    }],
    user: { name: '', pw: ''},
    chats: [],
    activeChat: [],
    chatID: 0
  },
  mutations: {
    ADD_LOG(state, log) {
      state.logs.push({
        time: new Date().getTime(),
        author: log.author,
        text: log.text,
      });
    },
    SET_USER(state, user) {
      state.user = user; 
    },
    SET_CHATS(state, chats) {
      state.chats = chats; 
    },
    ADD_CHAT(state, chat) {
      state.chats.push(chat);
    },
    DEL_CHAT(state, chatID) {
      state.chats = state.chats.filter(elm => elm.id != chatID);
    },
    RENAME_CHAT(state, chat) {
      const obj = state.chats.find(elm  => elm.id === chat.id);
      obj.name = chat.name; 
    },
    SET_ACTIVECHAT(state, activeChat) {
      state.activeChat = activeChat; 
    },
    SET_CHATID(state, chatID) {
      state.chatID = chatID; 
    },
    ADD_ACTIVECHAT(state, activeChat) {
      state.activeChat.push(activeChat); 
    },
    ADD_MESSAGE(state, message) {
      state.activeChat[state.activeChat.length-1].message = message;
      state.activeChat[state.activeChat.length-1].loading = false; 
    },
    ADD_SOURCE(state, source) {
      state.activeChat[state.activeChat.length-1].sources = source;
    }
  },
  actions: {
    addLog({ commit }, log) {
      commit('ADD_LOG', log);
    },
    setUser({ commit }, user) {
      commit('SET_USER', user);
    },
    setChats({ commit }, chats) {
      commit('SET_CHATS', chats);
    },
    addChat({ commit }, chat) {
      commit('ADD_CHAT', chat);
    },
    delChat({ commit }, chatID) {
      commit('DEL_CHAT', chatID);
    },
    renChat({ commit }, chatID) {
      commit('RENAME_CHAT', chatID);
    },
    setActiveChat({ commit }, activeChat) {
      commit('SET_ACTIVECHAT', activeChat);
    },
    addActiveChat({ commit }, activeChat) {
      commit('ADD_ACTIVECHAT', activeChat);
    },
    setChatID({ commit }, chatID) {
      commit('SET_CHATID', chatID);
    },
    addMessage({ commit }, message) {
      commit('ADD_MESSAGE', message);
    },
    addSource({ commit }, source) {
      commit('ADD_SOURCE', source);
    }
  },
  getters: {
    logs: state => state.logs,
    user: state => state.user,
    chats: state => state.chats,
    activeChat: state => state.activeChat,
    chatID: state => state.chatID
  }
});