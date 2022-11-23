<template>
  <div class="container">
    <div class="left-side">
      <div class="panel">
          <a-form :model="DemandSearch" layout="inline">
            <a-form-item>
              <a-select :style="{width:'280px'}" :loading="ProductLoading" placeholder="请搜索项目代号..." multiple
              @search="DemandProductSearch" :filter-option="false">
                <a-option v-for="ProductItem of ProductOptions" :value="ProductItem" :key="ProductItem.id">{{ProductItem}}</a-option>
              </a-select>
            </a-form-item>
          </a-form>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { apiProductOrigin } from "@/api/product";
import { ref, reactive, unref } from "vue";
import { TableData } from "@arco-design/web-vue/es/table/interface";
import moment from "moment";
import * as Console from "console";
import { valid } from "mockjs";

const formatDate = (date: any) => {
  return moment(date).format("YYYY-MM-DD");
};

// 定义项目搜索options
const ProductOptions = ref([]);
const ProductLoading = ref(false);
const DemandProductSearch = (value:any) => {
      if (value) {
        ProductLoading.value = true;
        const dataOrigin = { keyCode:value }
        window.setTimeout(() => {
          apiProductOrigin(dataOrigin).then((res:any)=>{
            Object.keys(res.data).forEach(key=>{
              ProductOptions.value.push(res.data[key].keyCode)
            })
            ProductLoading.value = false;
        }).catch((err:any)=>{
          console.log('错误编号')
        })
        }, 1000)
      } else {
        ProductOptions.value = []
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
}

.paginclass{
  padding-left:20px ;
  padding-bottom: 10px;
}
</style>
