import { createRouter, createWebHistory } from 'vue-router';
import ItemManager from '../components/ItemManager.vue';

const routes = [
  { path: '/', component: ItemManager }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;