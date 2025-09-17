import { createRouter, createWebHistory } from 'vue-router';
import Home from './pages/Home.vue';
import Live_Demo from './pages/Live_Demo.vue';
import Download from './pages/Download.vue';
import Publication from './pages/Publication.vue';
import Contact_Us from './pages/Contact_Us.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/Live_Demo', component: Live_Demo },
  { path: '/Download', component: Download },
  { path: '/Publication', component: Publication },
  { path: '/Contact_Us', component: Contact_Us }
];

export default createRouter({
  history: createWebHistory(),
  routes
});
