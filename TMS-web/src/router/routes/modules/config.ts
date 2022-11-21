import { DEFAULT_LAYOUT } from '@/router/constants';

export default {
  path: '/config',
  name: 'Config',
  component: DEFAULT_LAYOUT,
  meta: {
    locale: 'menu.config',
    requiresAuth: true,
    icon: 'icon-home',
    order: 0,
  },
  children: [
    {
      path: '/product',
      name: 'Product',
      component: ()=> import('@/views/config/product/index.vue'),
      meta: {
        locale: 'menu.config.product',
        requiresAuth: true,
        roles: ['*'],
      }
    },
    {
      path: '/demand',
      name: 'Demand',
      component: ()=> import('@/views/config/demand/index.vue'),
      meta: {
        locale: 'menu.config.demand',
        requiresAuth: true,
        roles: ['*'],
      },
    }
  ],
};
