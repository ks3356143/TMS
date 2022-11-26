<template>
  <div>
  <a-drawer :width="600" :visible="DrawVisible" @ok="handleOk" @cancel="handleCancel" unmountOnClose>
    <template #title>
      <a-typography-title :heading="5" bold=True>
        {{ DrawTitle }}
      </a-typography-title>
    </template>
      <a-form ref="DemandFormRef" :model="DemandForm" :style="{width:'540px'}" :rules="rulesCreate">
        <a-form-item field="productId" label="选择项目" :validate-trigger="['change','input']">
          <a-select  :loading="DemandSelectLoading" placeholder="请搜索项目代号或项目名称" 
          @search="DemandSearchProduct" :filter-option="false" allow-search allow-clear v-model="DemandForm.productId">
            <a-option v-for="Item of ProductOptionsSearch" :value="Item.id" :key="Item.id">{{Item.keyCode + ' : ' + Item.title}}</a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="name" label="需求名称" >
          <a-input max-length=50 v-model="DemandForm.name" allow-clear/>
        </a-form-item>
        <a-form-item field="document" label="需求文档名称" >
          <a-input max-length=50 v-model="DemandForm.document" allow-clear/>
        </a-form-item>
        <a-form-item field="step" label="测试轮次" >
          <a-select v-model="DemandForm.step" placeholder="请选择轮次..."  :filter-option="false" allow-clear>
            <a-option value="第一轮测试" key=1>第一轮测试</a-option>
            <a-option value="第二轮测试" key=2>第二轮测试</a-option>
            <a-option value="第三轮测试" key=3>第三轮测试</a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="chapter" label="需求文档章节" placeholder="Please enter something">
          <a-input v-model="DemandForm.chapter" allow-clear>
          <template #append>
            X.X.X.XX格式
          </template>
          </a-input>
        </a-form-item>
        <a-form-item field="chaptername" label="需求章节名称" placeholder="Please enter something">
          <a-input v-model="DemandForm.chaptername" allow-clear>
          </a-input>
        </a-form-item>
        <a-form-item field="content" label="需求内容录入" >
          <a-textarea v-model="DemandForm.content" allow-clear/>
        </a-form-item>
        <a-form-item field="priority" label="优先级" >
          <a-select v-model="DemandForm.priority" placeholder="请选择优先级..."  :filter-option="false" allow-clear>
            <a-option value="高" key=1>高</a-option>
            <a-option value="中" key=2>中</a-option>
            <a-option value="低" key=3>低</a-option>
          </a-select>
        </a-form-item>
      </a-form>
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
</div>
</template>

<script lang="ts" setup>
import { apiProductOrigin , apiProductList , apiOriginProduct } from "@/api/product";
import { ref, reactive, unref } from "vue";
import { TableData } from "@arco-design/web-vue/es/table/interface";
import moment from "moment";
import * as Console from "console";
import { valid } from "mockjs";
import { stringLiteral } from "@babel/types";

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
  const res:any = await apiProductList();
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
const ProductOptions = ref<any>([]);
const ProductLoading = ref(false);
const DemandProductSearch =  async (value:string) => {
      if (value) {
        ProductLoading.value = true;
        const dataOrigin = { keyCode:value as any }
          await apiProductOrigin(dataOrigin).then((res:any)=>{
            ProductOptions.value = [] // 初始化空
            Object.keys(res.data).forEach(key=>{
              ProductOptions.value.push(res.data[key].keyCode)
            })
            ProductLoading.value = false;
        }).catch((err:string)=>{
          console.log('错误编号')
        })
      } else {
        ProductOptions.value = []
      }
    };

// #TODO:搜索按钮点击接口btnDemandSearch

// #TODO:重置搜索组合点击按钮btnDemandReset

// 抽屉相关操作1-打开抽屉操作
const DrawTitle = ref<string>('新增需求')
const DrawVisible = ref(false)
const handleCancel = () => {
  DrawVisible.value = false;
    }
const btnDrawOpen = () => {
  DrawVisible.value = true
  SelectOptionsDemand(); // 初始化收集项目ID
}
const DemandForm = reactive({
  ProductName:undefined,
});
// 抽屉操作-2-其中项目搜索与绑定
const ProductOptionsSearch = ref<any>([]); // 储存select的option-列表
const SelectOptionsDemand = async () => { // 搜索项目列表，获取期productId以及keyCode还有title
  const res:any = await apiProductList();
    if (res.code === 20000) {
      ProductOptionsSearch.value = [] // 初始化空
      Object.keys(res.data).forEach(key=>{
        ProductOptionsSearch.value.push(res.data[key])
      })
    } else {
      console.log("项目搜索失败");
    }
};
const DemandSelectLoading = ref<boolean>(false)
const DemandSearchProduct =  async (value:string) => {
      if (value) {
        DemandSelectLoading.value = true;
        const valueOrigin = { content:value as string }
          await apiOriginProduct(valueOrigin as any).then((res:any)=>{
            ProductOptionsSearch.value = [] // 初始化空
            Object.keys(res.data).forEach(key=>{
              // ProductOptionsSearch.value.push(`${res.data[key].keyCode} : ${res.data[key].title}`)
              ProductOptionsSearch.value.push(res.data[key])
            })
            DemandSelectLoading.value = false;
        }).catch((err:string)=>{
          console.log('错误项目名搜索')
        })
      } else {
        ProductOptionsSearch.value = []
      }
    };


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
