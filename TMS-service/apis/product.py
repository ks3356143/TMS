# -*- coding:utf-8 -*-

from flask import Blueprint
import pymysql
from flask import request
import json

app_product = Blueprint("app_product", __name__)

def connectDB():
    connection = pymysql.connect(host='localhost',  # 数据库IP地址或链接域名
                                 user='root',  # 设置的具有增改查权限的用户
                                 password='root',  # 用户对应的密码
                                 database='TPMStore',  # 数据表
                                 charset='utf8mb4',  # 字符编码
                                 cursorclass=pymysql.cursors.DictCursor)  # 结果作为字典返回游标
    return connection


@app_product.route("/list", methods=['GET'])
def product_list():
    connection = connectDB()
    with connection.cursor() as cursor:
        # 查询产品信息表-按更新时间新旧排序
        sql = "SELECT * FROM `products` WHERE `status`=0 ORDER BY `Update` DESC"
        cursor.execute(sql)
        data = cursor.fetchall()

    # 按返回模式格式进行json结果返回
    resp_data = {
        "code": 20000,
        "data": data
    }
    return resp_data


@app_product.route("/create", methods=['POST'])
def product_create():
    connection = connectDB()
    # 定义默认返回体
    resp_data = {
        "code": 20000,
        "message": "成功",
        "data": []
    }

    # 获取请求传递json body
    body = request.get_data()
    body = json.loads(body)
    # 表单非空验证
    print(body)
    if 'keyCode' not in body:
        resp_data['message'] = '所填项目代号为空'
        resp_data['code'] = 20001
        return resp_data
    if 'title' not in body:
        resp_data['message'] = '所填项目名称为空'
        resp_data['code'] = 20001
        return resp_data
    if 'tester' not in body:
        resp_data['message'] = '所填项目负责人为空'
        resp_data['code'] = 20001
        return resp_data
    if 'seller' not in body:
        resp_data['message'] = '所填商务人员为空'
        resp_data['code'] = 20001
        return resp_data
    if 'step' not in body:
        resp_data['message'] = '所填项目阶段为空'
        resp_data['code'] = 20001
        return resp_data
    if 'customer' not in body:
        resp_data['message'] = '所填客户单位为空'
        resp_data['code'] = 20001
        return resp_data
    # 先做个判断看keyCode是否重复
    with connection:
        with connection.cursor() as cursor:
            select = "SELECT * FROM `products` WHERE `keyCode` = %s AND `status`=0"
            cursor.execute(select, (body['keyCode']), )
            result = cursor.fetchall()

        if len(result) > 0:
            resp_data['code'] = 200001
            resp_data['message'] = f"唯一项目代号{body['keyCode']}已经存在，请检查项目代号"
            return resp_data

        with connection.cursor() as cursor:
            print(body)
            sql = "INSERT INTO `products` (`type`,`keyCode`,`title`,`tester`,`step`,`customer`,`seller`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (
            body['type'], body['keyCode'], body['title'], body['tester'], body['step'], body['customer'],
            body['seller']))
            connection.commit()
        return resp_data


@app_product.route("/update", methods=['POST'])
def product_update():
    connection = connectDB()
    # 定义默认返回体
    resp_data = {
        "code": 20000,
        "message": "success",
        "data": []
    }

    # 获取请求传递json body
    body = request.get_data()
    body = json.loads(body)

    # 先做个判断看keyCode是否重复
    with connection:
        with connection.cursor() as cursor:
            select = "SELECT * FROM `products` WHERE `keyCode` = %s AND `status`=0"
            cursor.execute(select, (body['keyCode']), )
            result = cursor.fetchall()

        if len(result) > 0 and body['id'] != result[0]['id']:
            resp_data['code'] = 200001
            resp_data['message'] = f"唯一项目代号{body['keyCode']}已经存在"
            return resp_data

        with connection.cursor() as cursor:
            sql = "UPDATE `products` SET `type`=%s,`keyCode`=%s,`title`=%s,`tester`=%s,`step`=%s,`customer`=%s,`seller`=%s,`update`=NOW()  WHERE `id`= %s"
            cursor.execute(sql, (
            body['type'], body['keyCode'], body['title'], body['tester'], body['step'], body['customer'],
            body['seller'], body['id']))
            connection.commit()
        return resp_data


@app_product.route("/delete", methods=['DELETE'])
def product_delete():
    # 定义默认返回体
    resp_data = {
        "code": 20000,
        "message": "success",
        "data": []
    }

    # 获取请求传递json body
    ID = request.args.get('id')
    print(ID)
    if ID is None:
        resp_data['code'] = 200002
        resp_data['message'] = "请求参数id不存在"
        return resp_data

    connection = connectDB()
    with connection.cursor() as cursor:
        sql = "DELETE from `products` WHERE `id`=%s"
        cursor.execute(sql, ID)
        connection.commit()
    return resp_data


# [POST方法]根据id更新状态项目状态，做软删除
@app_product.route("/remove", methods=['POST'])
def product_remove():
    # 返回的reponse
    resp_data = {
        "code": 20000,
        "message": "success",
        "data": []
    }
    ID = request.args.get('id')
    # 做个参数必填校验
    if ID is None:
        resp_data["code"] = 20002
        resp_data["message"] = "请求id参数为空"
        return resp_data
    # 重新链接数据库
    print(ID)
    connection = connectDB()
    with connection.cursor() as cursor:
        # 状态默认正常状态为0，删除状态为1
        # alter table products add status int default 0 not null comment '状态有效0，无效0' after `desc`;
        sql = "UPDATE `products` SET `status`=1 WHERE id=%s"
        cursor.execute(sql, ID)
        connection.commit()

    return resp_data

@app_product.route("/search",methods=['GET'])
def product_search():
    print('进入到product_search接口')
    # 获取title和keyCode
    title = request.args.get('title')
    keyCode = request.args.get('keyCode')

    # 基础语句定义
    sql = "SELECT * FROM `products` WHERE `status`=0"

    # 如果title不为空，拼接tilite的模糊查询
    if title is not None:
        sql = sql + " AND `title` LIKE '%{}%'".format(title)
    # 如果keyCode不为空，拼接tilite的模糊查询
    if keyCode is not None:
        sql = sql + " AND `keyCode` LIKE '%{}%'".format(keyCode)

    # 排序最后拼接(分页查询）
    sql = sql + " ORDER BY `update` DESC"

    connection = connectDB()

    # 使用python的with..as控制流语句（相当于简化的try except finally）
    with connection.cursor() as cursor:
        # 按照条件进行查询
        cursor.execute(sql)
        data = cursor.fetchall()

    # 按返回模版格式进行json结果返回
    resp_data = {
        "code": 20000,
        "data": data
    }

    return resp_data

@app_product.route("/searchPage",methods=['GET'])
def product_search_page():
    # 获取title和keyCode
    title = request.args.get('title')
    keyCode = request.args.get('keyCode')

    # 新增页数和每页个数参数，空时候做默认处理，并注意前端传过来可能是字符串，需要做个强制转换
    pageSize = 10 if request.args.get('pageSize') is None else int(request.args.get('pageSize'))
    currentPage = 1 if request.args.get('currentPage') is None else int(request.args.get('currentPage'))

    sql = "SELECT * FROM `products` WHERE `status`=0"
    # 增加基础全量个数统计
    sqlCount = "SELECT COUNT(*) as `count` FROM `products` WHERE `status`=0"

    # 条件拼接全量统计也需要同步

    if title is not None:
        sql = sql + " AND `title` LIKE '%{}%'".format(title)
        sqlCount = sqlCount + " AND `title` LIKE '%{}%'".format(title)
    if keyCode is not None:
        sql = sql + " AND `keyCode` LIKE '%{}%'".format(keyCode)
        sqlCount = sqlCount + " AND `keyCode` LIKE '%{}%'".format(keyCode)

    # 排序最后拼接带分页查询
    sql = sql + ' ORDER BY `update` DESC LIMIT {},{}'.format((currentPage - 1) * pageSize, pageSize)

    connection = connectDB()

    # 使用python的with..as控制流语句（相当于简化的try except finally）
    with connection:
        # 先查询总数
        with connection.cursor() as cursor:
            cursor.execute(sqlCount)
            total = cursor.fetchall()

        # 执行查询分页查询
        with connection.cursor() as cursor:
            # 按照条件进行查询
            cursor.execute(sql)
            data = cursor.fetchall()

    # 带着分页查询结果和总条数返回，total注意是list字段需要下角标key取值
    resp_data = {
        "code": 20000,
        "message": "success",
        "data": data,
        "total": total[0]['count']
    }

    return resp_data
