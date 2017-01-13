from flask import Blueprint
from flask import request
from flask import jsonify
import json
import bson
import sys, os
import json
sys.path.append(os.path.dirname(__file__)+'/../database/')
from database.selectSpotsOperate import *
import datetime


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
    days = int(date[1][3:5]) - int(date[0][3:5]) + 1
    print (spots_id)
    spots_id = generateBestRoute(days, spots_id)

    time = []
    name = []
    coordinate = []
    spots_id_serial = []
    for x in spots_id:
        for y in x:
            spots_id_serial.append(y)
    time_between_spots = getTimeBetweenSpots(spots_id_serial)

    num = 0
    print (time_between_spots)
    for i in range(days):
        time.append([])
        name.append([])
        coordinate.append([])
        for j in range(len(spots_id[i])):
            # print (spots_id[i][j])
            city = getSpotInfo(spots_id[i][j])
            # print (city)
            if j == 0:
                time[i].append([0, city['visit_time']])
            else:
                print (i, j, num)
                start_time = time[i][j-1][1] + time_between_spots[num-1][num]
                end_time = start_time + city['visit_time']
                time[i].append([start_time, end_time])
            name[i].append(city['name'])
            coordinate[i].append(city['coordinate'])
            num = num + 1

    # print (time, name, corrdinate)
    for i in range(len(spots_id)):
        for j in range(len(spots_id[i])):
            spots_id[i][j] = str(spots_id[i][j])
    print ('lalalal')
    print (name)
    return jsonify(spots_id=spots_id, time=time, name=name, coordinate=coordinate)
    # return jsonify(namw="lyc")

@selectSpots.route('/confirmSelectedSpots', methods=['POST'])
def confirm_route():
    data = request.form['data']
    data = json.loads(data)
    print (data)
    print (type(data))

    user = data['user']
    shared = int(data['shared'])
    date = data['date']
    spots = data['spots_id']
    time = data['time']
    print (user,shared,date,spots,time)

    if (type(saveRoute(user,shared,date,spots,time)) == bson.objectid.ObjectId):
        return jsonify({'success':True})
    else:
        return jsonify{'success':False}




























