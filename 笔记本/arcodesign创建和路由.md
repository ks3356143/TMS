# 创建项目Init Arco

## 1.创建项目

注意如果出现无法识别手脚架命令，需要重新新建，以下是安装手脚架

```lang
npm i -g arco-cli
```

更新npm

```npm install -g npm@9.1.2
npm install -g npm@9.1.2
```

安装arcodesign

**错误：**如果出现提示“请提交你的Git修改后继续操作”那么进行git add、git commit和git push origin main操作

安装yarn

**错误：**很多时候出现初始化失败，可以先

```npm install -g yarn 
npm install -g yarn
```

切换淘宝镜像

```
yarn config set registry https://registry.npm.taobao.org -g
```

初始化arco项目

```
arco init 项目名
```

完成后即可

```
npm run dev
```

记得安装全部包

```
yarn install
```



## 2.关于mock的关闭和flask的跨域解决

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app, supports_credentials=True)
```



## 3.泛型理解（包括接口）

首先查看一下代码，T标识Type，它可以传递传输的类型，冒号后面是返回值的类型

```typescript
function identity<T>(value:T):T {
    return value
}
```



# arcodesign路由

首先为了减少维护了，菜单和路由绑定一起

## 1、主要文件

在`src/router/routes/modules`中一个ts文件表示一级菜单

二级菜单使用children即可

注意在arco中路由需要配置两个地方，第一是`src/router/routes/modules`一级菜单，并且配置路由懒加载

第二是配置children

![image-20221121184225001](C:\Users\chenjunyi\AppData\Roaming\Typora\typora-user-images\image-20221121184225001.png)





