from flask import Flask

app = Flask(__name__)

@app.route('/index')
def index():
    return app.send_static_file('index.html')

from route.loginPages import login
app.register_blueprint(login, url_prefix='/login')

from route.loginPages import agencyLogin
app.register_blueprint(agencyLogin, url_prefix='/agencyLogin')

from route.registerPages import registers
app.register_blueprint(registers, url_prefix='/register')

from route.selectSpotsPages import selectSpots
app.register_blueprint(selectSpots, url_prefix='/selectSpots')


if __name__ == '__main__':
    app.run(debug=True)
