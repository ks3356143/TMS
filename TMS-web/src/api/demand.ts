import axios from 'axios';
import type { TableData } from '@arco-design/web-vue/es/table/interface';

//定义TS的需求字段
export interface demandData {
  id: number;
  productId:number;
  name:string;
  document:string;
  step:string;
  content:string;
  importer:string;
  chapter:string;
  chaptername:string;
  priorit:number;
  person:string;
  note:string;
};

export function apiDemandAdd(data: demandData) {
  return axios.post('/api/demand/create', data);
}

export function apiDemandUpdate(data: demandData) {
  return axios.post('/api/demand/update', data);
}

export function apiDemandDelete(id: number) {
  return axios.delete('/api/demand/delete', {
    params: {id}
  });
}

export function apiDemandRemove(id: number) {
  return axios.post(`/api/demand/remove?id=${id}`);
}

export function apiDemandList() {
  return axios.get<TableData[]>('/api/demand/list');
}

export interface DemandParams {
  title: string;
  keyCode: string;
};
export function apiDemandSearch(data: DemandParams) {
  return axios.get<TableData[]>('/api/demand/search',{
    params: data
  });
}

export interface DemandPageParams {
  title: string;
  keyCode: string;
  pageSize: number,
  currentPage: number
};
export function apiDemandSearchPage(data: DemandPageParams) {
  return axios.get<TableData[]>('/api/demand/searchPage',{
    params: data
  });
}
