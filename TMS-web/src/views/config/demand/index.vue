<template>
  <a-drawer :width="600" :visible="DrawVisible" @ok="handleOk" @cancel="handleCancel" unmountOnClose>
    <template #title>
      {{ DrawTitle }}
    </template>
    <div>
      您可以根据当前情况讨论正文。一旦您按下OK（确定）按钮。
    </div>
  </a-drawer>
  <div class="container">
    <div class="left-side">
      <div class="panel">
          <a-form :model="DemandSearch" layout="inline">
            <a-form-item>
              <a-select :style="{width:'160px'}" :loading="ProductLoading" placeholder="请搜索项目代号..." 
              @search="DemandProductSearch" :filter-option="false" allow-search allow-clear>
                <a-option v-for="ProductItem of ProductOptions" :value="ProductItem" :key="ProductItem.id">{{ProductItem}}</a-option>
              </a-select>
            </a-form-item>
            <a-form-item>
              <a-input
                v-model="DemandSearch.name"
                allow-clear
                placeholder="需求名称模糊搜索"
              />
            </a-form-item>
            <a-form-item>
              <a-input
                v-model="DemandSearch.document"
                allow-clear
                placeholder="需求文档名称"
              />
            </a-form-item>
            <a-form-item>
              <a-input
                v-model="DemandSearch.importer"
                allow-clear
                placeholder="录入者搜索"
              />
            </a-form-item>
            <a-form-item>
              <a-input
                v-model="DemandSearch.chaptername"
                allow-clear
                placeholder="需求章节名称搜索"
              />
            </a-form-item>
            <a-form-item>
              <a-select :style="{width:'160px'}" v-model="DemandSearch.step" placeholder="请选择轮次..."  :filter-option="false" allow-clear>
                <a-option value="第一轮测试" key=1>第一轮测试</a-option>
                <a-option value="第二轮测试" key=2>第二轮测试</a-option>
                <a-option value="第三轮测试" key=3>第三轮测试</a-option>
              </a-select>
            </a-form-item>
            <a-form-item>
              <a-range-picker
                  style="width: 380px; margin: 0 24px 24px 0;"
                  :time-picker-props="{ defaultValue: ['00:00:00', '00:00:00'] }"
                  format="YYYY-MM-DD"
                  v-model="DemandSearch.DatePickData"
                />
            </a-form-item>
            <a-form-item>
              <a-button-group>
              <a-button type="primary" @click="btnDemandSearch">
                <template #icon>
                  <icon-search />
                </template>
                搜索
              </a-button>
              <a-button type="outline" @click="btnDemandReset">
                重置
              </a-button>
            </a-button-group>
            </a-form-item>
            <a-button type="primary" @click="btnDrawOpen" status="success">
              <template #icon>
                <icon-plus-circle />
              </template>
              新增需求</a-button>
          </a-form>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { apiProductOrigin , apiProductList } from "@/api/product";
import { ref, reactive, unref } from "vue";
import { TableData } from "@arco-design/web-vue/es/table/interface";
import moment from "moment";
import * as Console from "console";
import { valid } from "mockjs";

const formatDate = (date: any) => {
  return moment(date).format("YYYY-MM-DD");
};

// 搜索条目的数据绑定，首先创建响应式变量v-model绑定
const DemandSearch = reactive({
  name: undefined,
  document: undefined,
  step: undefined,
  importer:undefined,
  chaptername:undefined,
  DatePickData:undefined,
  pageSize: 10,
  currentPage: 1,
});

// 定义项目搜索options,首先请求获取已有的options值
const SelectOptionsGet = async () => {
  const res = await apiProductList();
  if (res.code === 20000) {
    ProductOptions.value = [] // 初始化空
    Object.keys(res.data).forEach(key=>{
      ProductOptions.value.push(res.data[key].keyCode)
    })
  } else {
    console.log("项目搜索失败");
  }
};
SelectOptionsGet();
const ProductOptions = ref([]);
const ProductLoading = ref(false);
const DemandProductSearch = (value:string) => {
      if (value) {
        ProductLoading.value = true;
        const dataOrigin = { keyCode:value }
        window.setTimeout(() => {
          apiProductOrigin(dataOrigin).then((res:any)=>{
            ProductOptions.value = [] // 初始化空
            Object.keys(res.data).forEach(key=>{
              ProductOptions.value.push(res.data[key].keyCode)
            })
            ProductLoading.value = false;
        }).catch((err:string)=>{
          console.log('错误编号')
        })
        }, 500)
      } else {
        ProductOptions.value = []
      }
    };

// TODO:搜索按钮点击接口btnDemandSearch

// TODO:重置搜索组合点击按钮btnDemandReset

// 抽屉相关操作
const DrawTitle = ref('新增需求')
const DrawVisible = ref(false)
const handleCancel = () => {
  DrawVisible.value = false;
    }
// 新增需求按钮
const btnDrawOpen = () => {
  DrawVisible.value = true
}


</script>

<script lang="ts">
export default {
  name: "Demand",
};
</script>

<style scoped>
.container {
  background-color: var(--color-fill-2);
  padding: 16px 20px;
  padding-bottom: 0;
  display: flex;
}
.left-side {
  flex: 1;
  overflow: auto;
}
.panel {
  padding-top: 10px;
  background-color: var(--color-bg-2);
  border-radius: 4px;
  overflow: auto;
}
:deep(.panel-border) {
  margin-bottom: 0;
  border-bottom: 1px solid rgb(var(--gray-2));
}

.buttonclass {
  padding-left: 20px;
  padding-bottom: 10px;
  border-radius: 0px 5px;
}

.paginclass{
  padding-left:20px ;
  padding-bottom: 10px;
}
</style>
