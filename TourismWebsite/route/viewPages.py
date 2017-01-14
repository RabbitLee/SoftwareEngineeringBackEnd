from flask import Blueprint
from flask import request
from flask import jsonify
import json
import sys, os
sys.path.append(os.path.dirname(__file__)+'/../database/')
from database.viewOperate import *

personInfo = Blueprint('personInfo', __name__)
agencyPersonInfo = Blueprint('agencyPersonInfo', __name__)

@personInfo.route('/showRouteInPage', methods=['POST'])
def show_route_in_page():
    userID = request.form['userID']
    list = showRouteInPage(userID)
    return jsonify(list=list)

@personInfo.route('/showAllAgency', methods=['POST'])
def show_all_agency():
    userID = request.form['userID']
    list = showAllAgency(userID)
    return jsonify(list=list)

@agencyPersonInfo.route('/showAgencyRoute', methods=['POST'])
def show_agency_route():
    agencyname = request.form['agencyname']
    list = showAgencyRoute(agencyname)
    return jsonify(list=list)

@agencyPersonInfo.route('/getSelectedRoute', methods=['POST'])
def get_selected_route():
    agencyname = request.form['agencyname']
    detailRouteID = request.form['detailRouteID']
    list = getSelectedRoute(agencyname, detailRouteID)
    return jsonify(list=list)