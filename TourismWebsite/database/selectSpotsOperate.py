# coding=utf-8
from pymongo import MongoClient
##from initialize import spotDistance
import urllib,json
from bson.objectid import ObjectId
from urllib import urlencode
import copy
# from math import ceil
client = MongoClient('localhost', 27017)
mydb = client.mydb

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

def spotDistance(origin, destination, city):
    url = "http://restapi.amap.com/v3/direction/transit/integrated?"
    orilng = mydb.spot.find_one({"_id": origin})["mapID"]["LngLat"][0]
    orilat = mydb.spot.find_one({"_id": origin})["mapID"]["LngLat"][1]
    deslng = mydb.spot.find_one({"_id": destination})["mapID"]["LngLat"][0]
    deslat = mydb.spot.find_one({"_id": destination})["mapID"]["LngLat"][1]
    params = {
        "origin": str(orilng) + ','+ str(orilat),
        "destination": str(deslng) + ','+ str(deslat),
        "city": city,
        "output": "json",
        "key": "a33b52f76e71d0efdf120c6a0997c380",
    }
    params = urlencode(params)
    f = urllib.urlopen(url, params)
    content = f.read()
    res = json.loads(content)
    return int(res["route"]["transits"][0]["duration"])

def getTimeBetweenSpots(spots):
    city = mydb.spot.find_one({"_id":spots[0]})["city"] + '市'
    time = []
    for spot1 in spots:
        temp = []
        for spot2 in spots:
            if spot1 != spot2:
                temp.append(spotDistance(spot1, spot2, city))
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
    route = {'spots': spots, 'time': time, 'date': date, 'shared': shared}
    routeId = mydb.route.insert(route)
    routeID = mydb.user.find_one({"name": user})["routeID"]
    routeID.append(routeId)
    mydb.user.update({'name': user}, {'$set': {'routeID': routeID}})
    return routeId

def getSpotInfo(spotId):
    spotinfo = mydb.spot.find_one({"_id": ObjectId(spotId)})
    dict = {}
    dict["name"] = spotinfo["name"]
    dict["coordinate"] = spotinfo["mapID"]["LngLat"]
    dict["visit_time"] = spotinfo["visit_time"]
    return dict

if __name__ == '__main__':
#     print saveRoute(mydb.user.find_one({"name": "华泽文"})["_id"], 0, ['1/8/2017','1/9/2017'],
#                     [[mydb.spot.find_one({"name": "五角场"})["_id"]], [mydb.spot.find_one({"name": "迪士尼"})["_id"]]],
#                     [[['13:30', '16:30']], [['9:00', '18:00']]])
#     print getTimeBetweenSpots([mydb.spot.find_one({"name":"五角场"})["_id"], mydb.spot.find_one({"name":"豫园"})["_id"], mydb.spot.find_one({"name":"东方明珠"})["_id"]])
#     print generateBestRoute(2, [mydb.spot.find_one({"name":"五角场"})["_id"], mydb.spot.find_one({"name":"豫园"})["_id"], mydb.spot.find_one({"name":"东方明珠"})["_id"]])
    print getSpotInfo("5877051fd9eca40fec0488d7")