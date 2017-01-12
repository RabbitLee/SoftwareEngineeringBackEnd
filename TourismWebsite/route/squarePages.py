from flask import Blueprint
from flask import request
from flask import jsonify
import json
import sys, os
sys.path.append(os.path.dirname(__file__)+'/../database/')
from database.squareOperate import *

square = Blueprint('square', __name__)

@square.route('/showAllRoute', methods=['POST'])
def show_all_route():
    list = []
    list = getAllRoutes()
    return json.dumps(list)

@square.route('/getSelectedRoute', methods=['POST'])
def get_selected_route():
    id = request.form['detailRouteID']
    user = request.form['user']
    return jsonify(getSelectedRoute(id,user))

@square.route('/voteRoute', methods=['POST'])
def vote_route():
    detailRouteID = request.form['detailRouteID']
    user = request.form['user']
    voteFor = request.form['voteFor']
    return voteRoute(detailRouteID, user, voteFor)

@square.route('/joinRoute', methods=['POST'])
def join_route():
    detailRouteID = request.form['detailRouteID']
    user = request.form['user']
    return joinRoute(detailRouteID, user)

@square.route('/bidForRoute', methods=['POST'])
def bid_for_route():
    agency = request.form['agency']
    bidFor = request.form['bidFor']
    fare = request.form['fare']
    return bidForRoute(agency, bidFor, fare)