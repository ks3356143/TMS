from flask import Flask
from flask_cors import CORS
#注册导入蓝图
from apis.product import app_product
from apis.user import app_user
from apis.testmanager import test_manager
from apis.apps import app_application

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.register_blueprint(app_product, url_prefix="/api/product") #后面一个参数可以省略清爽
app.register_blueprint(app_user, url_prefix="/api/user")
app.register_blueprint(test_manager)
app.register_blueprint(app_application, url_prefix="/api/application")

@app.route('/')
def hello_world():
    return '你好我是陈俊亦！'

if __name__ == '__main__':
    app.run(debug=True)
