import { createApp } from 'vue';
import App from './App.vue';
import store from './store';

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faBars, faPen, faTrash, faUser } from '@fortawesome/free-solid-svg-icons'
import { faRightFromBracket } from '@fortawesome/free-solid-svg-icons';
import { faGear } from '@fortawesome/free-solid-svg-icons';
import { faDatabase } from '@fortawesome/free-solid-svg-icons';
import { faInfo } from '@fortawesome/free-solid-svg-icons';
import { faComment } from '@fortawesome/free-solid-svg-icons';

library.add(faBars, faPen, faTrash, faUser, faRightFromBracket, faGear, faDatabase, faInfo, faComment);

const app = createApp(App);

app.use(store);
app.component('font-awesome-icon', FontAwesomeIcon);
app.mount('#app');