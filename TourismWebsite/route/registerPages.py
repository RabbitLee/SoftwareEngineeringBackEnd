from flask import Blueprint
from flask import request
from flask import jsonify
from database.registerOperate import *

registers = Blueprint('register', __name__)


@registers.route('/', methods=['POST'])
def register_account():
   name = request.form['name']
   password = request.form['password']
   email = request.form['email']
   phone = request.form['phone']
   if (register(name, password, email, phone) == True):
      return jsonify(isValid=True)
   else:
      return jsonify(isValid=False)