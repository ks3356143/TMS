# Arcodesign常规组件的使用

## （1）model

### 1.基础用法

先看下面代码，以下ref是vue3和vue2区别，注意

1、ref是需要导入的

2、a-button作为子组件要使用父组件model的属性，需要在

```typescript
<templete>
    <a-button @click="handleClick">打开Model</a-button>
	<a-model v-model:visibel="visible" @ok="handleOk" @cancel="handleCancel">
        <template #title>
        	Title
        </template>
		<div>我是model显示内容</div>
</template>

<script>
import {ref} from 'vue';

export default{
    setup(){
        const visible = ref(false);
        const handleClick = () => {visible.value = true;};
        const handleOk = () => {visible.value = false;};
        const handleCancel = () => {visible.value = false;}
        return {
            visible,
            handleClick,
            handleOk,
            handleCancel
        }
    }
}
```

这里就要了解setup()函数的使用

### 2.Setup()函数的使用

1、setup()函数时，它接收2个参数：（props，context（包含attrs、slots、emit））

```js
context包含三个参数，可通过解构方式写
context该上下文对象是非响应式的，可以安全地解构：
export default{
    setup(props,{attrs,slots,emit,expose}){
        // Attribute（非响应式的对象，等价于 $attrs）
        console.log(attrs)
        // 插槽（非响应式对象，等价于$slots）
        console.log(slots)
        // 触发时间（函数，等价于$emit）
        console.log(emit)
        // 暴露公共property（函数）
        console.log(expose)
    }
}
```

2、setup()函数执行时机是在beforeCreated和created()两个生命周期函数之前

3、setup()里面没有vue实例，故想通过this访问会返回`undefined`

4、setup()函数定义的所有变量和方法，需要return出去，否则vue文件（模板）中无法使用

5、在渲染函数中可以直接使用在同一作用域下声明的响应式状态

```javascript
import {h,ref} from 'vue'
export default {
    setup(){
        const count = ref{0}
        return() => h('div',count.value) //h 函数就是 Vue中的createElement方法,其有3个参数可以为一个html标签，一个组件，一个异步组件，或者是一个函数式组件
    }
}
```

6、子组件内部的方法想暴露给父组件使用通过ref方式去获取使用

```javascript
import { ref } from 'vue'
 
export default {
  setup(props, { expose }) {
    const num= ref(0)
    const count = ref(0)
    const increment = () => ++count.value
    expose({
      count,
      increment
    })
  }
}
父组件： <child ref='childCom'></child>
调用：   this.$refs.childCom.increment  // 成功，可以获取到对应方法
调用：   this.$refs.childCom.count      // 成功，可以获取到对应值
调用：   this.$refs.childCom.num        // 失败，不可以获取到对应值
expose未导出的属性，父组件中调用就会是undefined，即未暴露的属性或方法父组件是拿不到的！！！
```



## （2）表单Form

具有数据收集、校验和提交功能的表单，内部组件包含复选框、单选框、输入框、下拉选择框等，根据需要进行自由基础组件组合扩展

表单支持三种布局方式：horizontal、vertical、inline通过form属性layout=""设置

### 1.基础用法

由input、checkbox、button组成的表单，在提交时候获取表单项值

-   <a-form>为表单主包包裹，:mode绑定组值对象
-   <a-form-item>为子项，field（数据项必填）表单元素在数据对象中的path，label标签的文本
-   @submit表单提交时候触发时间

```javascript
<template>
    <a-form :model="form" :style ="width:'600px' @submit="handleSubmit">
		<a-form-item field='name' label='Username'>
            <a-input v-model="form.name" placeholder="请输入用户名" />
		</a-form-item>
		<a-form-item field='post' label='Post'>
            <a-input v-model="form.post" placeholder="请输入Post" />
		</a-form-item>
		<a-form-item field='isRead'>
            <a-checkbox v-model='form.isRead'>
               我阅读了手册
			</a-checkbox>
		</a-form-item>
		<a-form-item>
     		<a-button html-type="submit">Submit</a-button>
    	</a-form-item>
	</a-form>
	{{ form }}
</template>

<script>
import {reactive} from 'vue'
export default {
    setup(){
        const form = reactive({
            name:'',
            post:'',
            isRead:false,
        })
        const handleSubmit = (data) => {
            console.log(data)
        }
        return {
            form,
            handleSubmit
        }
    }
}
```

### 2.ref和reactive from 'vue'什么意思

#### a、ref

作用：定义一个响应式的数据

语法：const xxx = ref(initValue)

```
创建一个包含响应式数据的引用对象（reference对象，简称 ref 对象）
JS中操作数据：xxx.value
模板中读取数据：不需要.value，直接：<div>{{xxx}}</div>
js中需要.value模板中直接{{xxx}}
接受的数据可以是：基本类型，也可以是对象类型
```

#### b、reactive

作用：定义一个对象类型的响应式数据（基本类型用ref）

语法：const 代理对象 = reactive(源对象)接收一个对象（或数组），返回一个代理对象（Proxy的实例对象，简称proxy对象

#### C、ref和reactive对比

从定义数据比对：ref定义基本类型数据、reactive定义对象或数组，ref也可以定义对象数组内部自动转为reactive

从原理比对：ref通过Object.defineProperty()的get与set来实现响应式（数据劫持），reactive通过Proxy来实现响应式（数据劫持），并通过Reflect操作源对象内部的数据

#### d、从使用角度比对

-   ref操作数据需要.value，读取数据时候模板中直接xxx

-   reactive定义的数据：操作数据与读取数据：均不需要.value



## （3）Input

​	arco独特设计

1.  前缀图标：用于描述输入框中可输入的内容及格式（如：电话、日期图标）；

2.  后缀图标：根据不同场景具有多样的功能，常用场景如下：

3.  1.  错误提示，可与辅助文字中的错误提示结合出现；
    2.  内容清除按钮，可点击一键清除输入框中已输入的内容；
    3.  语音输入按钮，点击触发语音输入功能；
    4.  密码隐藏按钮；

![image-20221121111429836](C:\Users\chenjunyi\AppData\Roaming\Typora\typora-user-images\image-20221121111429836.png)

​	3.组件类型：单行输入框、多行输入框（随容器向下扩展）、文本域（可拉动右下角调整）

### 1、基本用法

使用方法很简单，一般在父组件引用a-input即可，比如`allow-clear`支持清空输入



## （4）按钮button

arco在基本样式之外还有以下样式

图标按钮：按钮可以嵌入图标，按钮宽高相等

样式按钮：可以指定大小、形状和状态、线性、文本

组合按钮：通过组件使按钮以组合的方式出现，可用在统计多项操作中

### 1、基本用法-有slot和events配置

在需要渲染位置上引用`<a-button></a-button>`，其<>内为`Props``Events`\`Slots`配置，><内为文本

```javascript
<template>
    <a-space>
        <a-button type="primary">主要按钮</a-button>
        <a-button>次要按钮</a-button>
        <a-button type="dashed">虚线按钮</a-button>
        <a-button type="outline">线性按钮</a-button>
        <a-button type="text">文本按钮</a-button>
    </a-space>
</template>
```

