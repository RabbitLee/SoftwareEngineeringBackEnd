from flask import Blueprint
from flask import request
from flask import jsonify
import json
import bson
import sys, os
import json
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
    print (request.form)
    cityName = request.form['cityName']
    return jsonify(getAllSpots(cityName))

@selectSpots.route('/submitSelectedSpots', methods=['POST'])
def submit_selected_spots():
    data = json.loads(request.form['data'])
    date = data['date']
    spots_id = data['spots_id']
    days = int(date[1][3:5]) - int(date[0][3:5])
    spots_id = generateBestRoute(days, spots_id)
    print (spots_id)
    time = []
    name = []
    corrdinate = []
    time_between_spots = getTimeBetweenSpots(spots_id)
    for i in range(days):
        time.append([])
        name.append([])
        corrdinate.append()
        for j in range(len(spots_id[i])):
            city = getSpotInfo(spots_id[i][j])
            if j == 0:
                time[i].append([0, city['visit_time']])
            else:
                start_time = time[i][j-1][1]+time_between_spots[spots_id[i][j-1]][spots_id[i][j]];
                end_time = start_time + city['visit_time']
                time[i].append([start_time, end_time])
            name[i].append(city['name'])
            corrdinate[i].append(city['corrdinate'])
    return jsonify(spots_id=spots_id, time=time, name=name, corrdinate=corrdinate)
    # return jsonify(name=True)


@selectSpots.route('/confirmSelectedSpots', methods=['POST'])
def confirm_route():
    data = request.form['data']
    data = json.loads(data)

    user = data['user']
    shared = data['shared']
    date = data['date']
    spots = data['spots']
    time = data['time']

    if (type(saveRoute(user,shared,date,spots,time)) == bson.objectid.ObjectId):
        return {'success':True}
    else:
        return {'success':False}




























