from flask import Blueprint
from flask import request
from flask import jsonify
import bson
import sys, os
sys.path.append(os.path.dirname(__file__)+'/../database/')
from database.selectSpotsOperate import *


selectSpots = Blueprint('selectSpots', __name__)


@selectSpots.route('/getGaodeDeveloperKey', methods=['POST'])
def get_gaode_developer_key():
   key = '9ddd6a45bb2946d784a0c4bdd8bb5e15'
   return key

@selectSpots.route('/getAllProvinces', methods=['POST'])
def get_all_provinces():
    return jsonify(getAllProvinces())

@selectSpots.route('/getAllCities', methods=['POST'])
def get_all_cities():
    provinceName = request.form['provinceName']
    return jsonify(getAllCities(provinceName))

@selectSpots.route('/getAllSpots', methods=['POST'])
def get_all_spots():
    cityName = request.form['cityName']
    return jsonify(getAllSpots(cityName))

@selectSpots.route('/submitSelectedSpots')
def submit_selected_spots():
    date = request.form['date']
    spots_id = request.form['spots_id']
    days = int(date['end_date'][3:5]) - int(date['start_date'][3:5])
    spots_id = generateBestRoute(days, spots_id)
    time = []
    for i in range(days):
        time.append([])
        for j in range(len(spots_id[i])):
            if j == 0:
                time[i].append([0, ])

@selectSpots.route('/confirmSelectedSpots', methods=['POST'])
def confirm_route():
    user = request.form['user']
    shared = request.form['shared']
    spots = request.form['spots_id']
    date = request.form['date']
    time = request.form['time']
    if (type(saveRoute(user,shared,date,spots,time)) == bson.objectid.ObjectId):
        return {'success':True}
    else:
        return {'success':False}




























