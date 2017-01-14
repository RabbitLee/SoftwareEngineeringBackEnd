# coding=utf-8
from pymongo import MongoClient
##from initialize import spotDistance
import urllib,json
from bson.objectid import ObjectId
from urllib import urlencode
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import copy
# from math import ceil
client = MongoClient('localhost', 27017)
mydb = client.mydb
import datetime

def getAllProvinces():
    dict = {}
    dict["provinces"] = []
    for province in mydb.province.find():
        dict["provinces"].append(province["name"])
    return dict

def getAllCities(province):
    dict = {}
    dict["cities"] = []
    for city in mydb.province.find_one({"name": province})["citys"]:
        dict["cities"].append(city)
    return dict

def getAllSpots(city):
    dict = {}
    citys = mydb.city.find_one({"name": city})
    dict["centerPosition"] = citys["centerposition"]
    dict["spots"] = []
    for spot in mydb.city.find_one({"name": city})["spots"]:
        # dict["spots"].append(mydb.spot.find_one({"_id": spot}))
        dict1 = {}
        dict["spots"].append(dict1)
        dict1["spotid"] = []
        dict1["name"] = []
        dict1["visit_time"] = []
        dict1["coordinate"] = []
        dict1["level"] = []
        dict1["spotid"].append(str(mydb.spot.find_one({"_id": spot})['_id']))
        dict1["name"].append(mydb.spot.find_one({"_id": spot})["name"])
        dict1["visit_time"].append(mydb.spot.find_one({"_id": spot})["visit_time"])
        dict1["coordinate"].append(mydb.spot.find_one({"_id": spot})["mapID"]["LngLat"])
        dict1["level"].append(mydb.spot.find_one({"_id": spot})["level"])
    return dict


def getTimeBetweenSpots(spots):
    if type(spots[0]) != ObjectId:
        for i in range(len(spots)):
            spots[i] = ObjectId(spots[i])
    city = mydb.spot.find_one({"_id":spots[0]})["city"] + '市'
    time = []
    for spot1 in spots:
        temp = []
        for spot2 in spots:
            if spot1 != spot2:
                temp.append(mydb.distance.find_one({"origin":spot1,"destination":spot2})["distance"])
            else:
                temp.append(0)
        time.append(temp)
    return time

def generateBestRoute(days, spots_id):
    time_between_spots = getTimeBetweenSpots(spots_id)
    n = len(spots_id)
    spots_number_in_day = []
    for i in range(days):
        spots_number_in_day.append(int(n/days))
    if days > 1:
        spots_number_in_day[1] += n - int(n/days)*days
    best_route = {
        'route': [],
        'time': 1e10
    }
    route=[]
    for i in range(days):
        route.append([])

    def distributeSpots(route, num):
        if num == n:
            total_time = calcuate_time(route)
            # global best_route, best_time
            # print (total_time < best_route['time'])
            if total_time < best_route['time']:
                # best_route['route'] = route[:]
                best_route['route'] = copy.deepcopy(route)
                best_route['time'] = total_time
            return
        for i in range(days):
            if len(route[i])<spots_number_in_day[i]:
                route[i].append(num)
                distributeSpots(route, num+1)
                route[i].pop()
    def calcuate_time(route):
        total_time = 0
        for i in range(days):
            for j in range(spots_number_in_day[i]-1):
                total_time += time_between_spots[route[i][j]][route[i][j+1]]
        return total_time

    distributeSpots(route, 0)
    ans = []
    for i in range(days):
        ans.append([])
        for j in range(len(best_route['route'][i])):
            # print (i, j, spots_id[best_route['route'][1][0]])
            ans[i].append(spots_id[best_route['route'][i][j]])
    return ans

def saveRoute(user, shared, date, spots, time):
    for i in range(len(spots)):
        for j in range(len(spots[i])):
            spots[i][j] = ObjectId(spots[i][j])
    route = {'spots': spots, 'time': time, 'date': date, 'shared': shared}
    routeId = mydb.route.insert(route)
    routeID = mydb.user.find_one({"name": user})["routeID"]
    routeID.append(routeId)
    mydb.user.update({'name': user}, {'$set': {'routeID': routeID}})
    if shared == 1:
        detailrouteID = mydb.detailroute.insert({'routeID': routeId, 'user': [[user, "False", "未支付"]], 'agency': []})
        temp = mydb.user.find_one({"name": user})["detailrouteID"]
        temp.append(detailrouteID)
        mydb.user.update({'name': user}, {'$set': {'detailrouteID': detailrouteID}})
    return routeId

def getSpotInfo(spotId):
    spotinfo = mydb.spot.find_one({"_id": ObjectId(spotId)})
    dict = {}
    dict["name"] = spotinfo["name"]
    dict["coordinate"] = spotinfo["mapID"]["LngLat"]
    dict["visit_time"] = spotinfo["visit_time"]
    return dict

# if __name__ == '__main__':
#      print saveRoute(mydb.user.find_one({"name": "华泽文"})["name"], 1, ['1/8/2017','1/9/2017'],
#                      [[str(mydb.spot.find_one({"name": "五角场"})["_id"])], [str(mydb.spot.find_one({"name": "迪士尼"})["_id"])]],
#                      [[['13:30', '16:30']], [['9:00', '18:00']]])
#      print getTimeBetweenSpots([mydb.spot.find_one({"name":"五角场"})["_id"], mydb.spot.find_one({"name":"豫园"})["_id"], mydb.spot.find_one({"name":"东方明珠"})["_id"]])
#
# #     print generateBestRoute(2, [mydb.spot.find_one({"name":"五角场"})["_id"], mydb.spot.find_one({"name":"豫园"})["_id"], mydb.spot.find_one({"name":"东方明珠"})["_id"]])
#
#     #print getSpotInfo("5877051fd9eca40fec0488d7")
#
# #     print getSpotInfo("5877051fd9eca40fec0488d7")
#      temp = getAllSpots('上海')
#
#      print (temp)

#     ans = []
#     for i in range(len(temp['spots'])):
#         ans.append(temp['spots'][i]['spotid'][0])
#     print ans

