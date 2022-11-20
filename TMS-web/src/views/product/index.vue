<template>
  <div>
    <div class="container">
      <div class="left-side">
        <div class="panel">
          <a-form :model="productSearch" layout="inline">
            <a-form-item>
              <a-input
                v-model="productSearch.title"
                allow-clear
                placeholder="项目名称模糊搜索"
              />
            </a-form-item>
            <a-form-item>
              <a-input
                v-model="productSearch.keyCode"
                allow-clear
                placeholder="项目代号精确搜索"
              />
            </a-form-item>
            <a-form-item>
              <a-button type="primary" @click="btnSearchClick">
                <template #icon>
                  <icon-search />
                </template>
                搜索
              </a-button>
            </a-form-item>
          </a-form>
        </div>
        <div class="panel buttonclass">
          <a-button type="primary" @click="addButtonClick">新增项目</a-button>
        </div>

        <div class="panel">
          <a-table :columns="columns" :data="renderList" :pagination="false">
            <template #optional="{ record }">
              <a-button type="text" @click="editButtonClick(record)">编辑</a-button>
              <a-popconfirm
                content="你确定要废弃此项目吗？"
                type="warning"
                @ok="removeButtonClick(record.id)"
              >
                <a-button type="text">废弃</a-button>
              </a-popconfirm>
              <a-button type="text" @click="delBtnClick(record?.id)">删除</a-button>
            </template>
            <template #update="{ record }">
              <div>{{ formatDate(record.update) }}</div>
            </template>
            <template #begintime="{ record }">
              <div>{{ formatDate(record.begintime) }}</div>
            </template>
          </a-table>
        </div>

        <div class="panel paginclass">
        <a-pagination
          :total="productTotal"
          :page-size-options="[10, 20, 30, 50, 100]"
          default-page-size="10条/页"
          @change="pageChange"
          @pageSizeChange="pageSizeChange"
          show-total
          show-page-size
        />
      </div>
        <a-modal
          v-model:visible="addModalVisible"
          title="添加项目"
          @before-ok="addModalOk"
          @cancel="addModalCancel"
        >
          <a-form :model="productForm">
            <a-form-item field="title" label="名称">
              <a-input v-model="productForm.title" placeholder="项目线名称" />
            </a-form-item>
            <a-form-item field="keyCode" label="唯一码">
              <a-input v-model="productForm.keyCode" placeholder="keycode不可重复" />
            </a-form-item>
            <a-form-item field="desc" label="备注">
              <a-textarea v-model="productForm.desc" placeholder="一些备注说明" />
            </a-form-item>
          </a-form>
        </a-modal>
        <a-modal
          v-model:visible="editModalVisible"
          title="编辑项目"
          @before-ok="editModalOk"
          @cancel="editModalCancel"
        >
          <a-form :model="productForm">
            <a-form-item field="id" label="编号" disabled>
              <a-input v-model="productForm.id" />
            </a-form-item>
            <a-form-item field="title" label="名称">
              <a-input v-model="productForm.title" placeholder="项目线名称" />
            </a-form-item>
            <a-form-item field="keyCode" label="唯一码">
              <a-input v-model="productForm.keyCode" placeholder="keycode不可重复" />
            </a-form-item>
            <a-form-item field="desc" label="备注">
              <a-textarea v-model="productForm.desc" placeholder="一些备注说明" />
            </a-form-item>
          </a-form>
        </a-modal>
        <a-modal
          v-model:visible="delModalVisible"
          title="删除项目"
          @before-ok="delModalOk"
          okText="删除"
          :okButtonProps="modalOkPros"
        >
          <div>确定需要删除该项目吗</div>
        </a-modal>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {
  apiProductList,
  apiProductAdd,
  apiProductUpdate,
  apiProductRemove,
  apiProductDelete,
  apiProductSearch,
  apiProductSearchPage,
} from "@/api/product";
import { ref, reactive } from "vue";
import { TableData } from "@arco-design/web-vue/es/table/interface";
import moment from "moment";
import * as Console from "console";

const formatDate = (date: any) => {
  return moment(date).format("YYYY-MM-DD");
};

const columns = [
  {
    title: "ID",
    dataIndex: "id",
    width: 50,
  },
  {
    title: "项目类型",
    dataIndex: "type",
    width: 100,
  },
  {
    title: "项目代号",
    dataIndex: "keyCode",
    width: 100,
  },
  {
    title: "项目名称",
    dataIndex: "title",
    ellipsis: true,
    tooltip: true,
  },
  {
    title: "测试人员",
    dataIndex: "tester",
    width: 100,
  },
  {
    title: "销售人员",
    dataIndex: "seller",
    width: 100,
  },
  {
    title: "测评阶段",
    dataIndex: "step",
    width: 100,
  },
  {
    title: "开始时间",
    dataIndex: "begintime",
    slotName: "begintime",
  },
  {
    title: "更新时间",
    dataIndex: "update",
    slotName: "update",
  },
  {
    title: "操作",
    slotName: "optional",
    fixed: "right",
    width: 220,
  },
];

const renderList = ref<TableData[]>();
// const fetchData = async () => {
//   try {
//     const { data } = await apiProductList();
//     renderList.value = data;
//   } catch (err) {
//     console.log(err);
//   }
// };
// fetchData();
// 添加/编辑使用表单对象
const productForm = reactive({
  id: undefined,
  type:undefined,
  keyCode:undefined,
  title: undefined,
  tester:undefined,
  seller:undefined,
  step:undefined,
});

const productTotal = ref<number>();
const productSearch = reactive({
  title: undefined,
  keyCode: undefined,
  pageSize: 5,
  currentPage: 1,
});
const pageChange = (current: number) => {
  console.log(current);
  productSearch.currentPage = current;
  btnSearchClick();
};
const pageSizeChange = (pageSize: number) => {
  console.log(pageSize);
  productSearch.pageSize = pageSize;
  btnSearchClick();
};
const btnSearchClick = async () => {
  // const res = await apiProductSearch(productSearch);
  const res = await apiProductSearchPage(productSearch);
  if (res.code === 20000) {
    renderList.value = res.data;
    productTotal.value = res.total;
  } else {
    console.log("项目搜索失败");
  }
};
btnSearchClick();

/* 项目添加对话框start */
const addModalVisible = ref(false); // 新增控制显示和隐藏布尔值，默认为flase
const addButtonClick = () => {
  // 新增项目线按钮触发事件
  addModalVisible.value = true; // 新增赋值为True显示
};
const addModalOk = async () => {
  // 添加对话框确定按钮，提交数据操作
  const res = await apiProductAdd(productForm);
  if (res.code === 20000) {
    addModalVisible.value = false; // 新增对话框
    btnSearchClick(); // 添加成功重新请求列表
  } else {
    console.log("项目添加失败");
  }
};
const addModalCancel = () => {
  // 对话框取消按钮，赋值使其关闭对话框
  addModalVisible.value = false;
};
/* 项目添加对话框end */

/* 项目编辑部分start */
const editModalVisible = ref(false); // 控制显示和隐藏编辑对话框布尔值，默认为flase
const editButtonClick = (record) => {
  // 修改项目线按钮触发事件
  productForm.id = record.id;
  productForm.title = record.title;
  productForm.keyCode = record.keyCode;
  productForm.desc = record.desc;
  editModalVisible.value = true; // 编辑显隐赋值为True显示
};
const editModalOk = async () => {
  // 编辑对话框确定按钮，提交数据操作
  const res = await apiProductUpdate(productForm);
  if (res.code === 20000) {
    editModalVisible.value = false; // 新增对话框
    btnSearchClick(); // 添加成功重新请求列表
  } else {
    console.log("项目修改失败");
  }
};
const editModalCancel = () => {
  // 编辑对话框取消按钮，赋值使其关闭对话框
  editModalVisible.value = false;
};
/* 项目编辑部分end */

/* 项目删除部分 */
const removeButtonClick = async (id) => {
  const res = await apiProductRemove(id);
  if (res.code === 20000) {
    btnSearchClick(); // 删除成功重新请求列表
  } else {
    console.log("项目删除失败");
  }
};
// 控制删除确认对话框
const delModalVisible = ref(false);
const delId = ref("");
const modalOkPros = {
  status: "warning",
};
const delBtnClick = (id) => {
  delId.value = id;
  delModalVisible.value = true;
};
const delModalOk = async () => {
  const res = await apiProductRemove(delId.value);
  if (res.code === 20000) {
    delModalVisible.value = false;
    btnSearchClick();
  } else {
    console.log("项目移除失败");
  }
};
</script>

<script lang="ts">
export default {
  name: "Product",
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
