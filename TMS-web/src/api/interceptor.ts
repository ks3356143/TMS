import axios, { AxiosRequestConfig, AxiosResponse } from 'axios';
import { Message, Modal } from '@arco-design/web-vue';
import { useUserStore } from '@/store';
import { getToken } from '@/utils/auth';
import { duration } from 'moment';

export interface HttpResponse<T = unknown> {
  status: number;
  message: string;
  code: number;
  data: T;
}

if (import.meta.env.VITE_API_BASE_URL) {
  axios.defaults.baseURL = import.meta.env.VITE_API_BASE_URL;
}

axios.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    // 让每个请求携带令牌
    // 此示例使用JWT令牌
    // 授权是自定义标头密钥
    // 请根据实际情况修改
    const token = getToken();
    if (token) {
      if (!config.headers) {
        config.headers = {};
      }
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // 做点什么
    return Promise.reject(error);
  }
);
// 添加响应拦截器
axios.interceptors.response.use(
  (response: AxiosResponse<HttpResponse|any>) => {
    const res = response.data;
    // 如果自定义代码不是20000，则判断为错误.
    if (res.code !== 20000) {
      Message.error({
        content: res.message || '错误',
        duration: 5 * 1000,
      });
      // 50008: 非法令牌; 50012: 其他客户端已登录; 50014: 令牌已过期;
      if (
        [50008, 50012, 50014].includes(res.code) &&
        response.config.url !== '/api/user/info'
      ) {
        Modal.error({
          title: '确认注销',
          content:
            '您已注销，您可以取消以保留此页面，或再次登录',
          okText: 'Re-Login',
          async onOk() {
            const userStore = useUserStore();

            await userStore.logout();
            window.location.reload();
          },
        });
      }
      return Promise.reject(new Error(res.message || '错误'));
    }
    return res;
  },
  (error) => {
    Message.error({
      content: error.message || '请求错误',
      duration: 5 * 1000,
    });
    return Promise.reject(error);
  }
);
