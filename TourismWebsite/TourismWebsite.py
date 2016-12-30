from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'True'

@app.route('/index')
def index():
    return app.send_static_file('index.html')
    # return 'nihao'

from route.loginPages import login
app.register_blueprint(login, url_prefix='/login')

if __name__ == '__main__':
    app.run()
