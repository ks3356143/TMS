import { DEFAULT_LAYOUT } from '@/router/constants';

export default {
  path: '/config', // 路由路径
  name: 'Config', // 路由名称
  component: DEFAULT_LAYOUT, // 跳转的组件页面
  meta: {
    locale: 'menu.config',
    requiresAuth: true,
    icon: 'icon-home',
    order: 1,
  },
  children: [
    {
      path: 'product',
      name: 'Product',
      component: ()=> import('@/views/config/product/index.vue'),
      meta: {
        locale: 'menu.config.product',
        requiresAuth: true,
        roles: ['*'],
      }
    },
    {
      path: 'demand',
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
