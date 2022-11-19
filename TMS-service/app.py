from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return '你好我是陈俊亦！'


if __name__ == '__main__':
    app.run()
