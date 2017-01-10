# coding=utf-8
from pymongo import MongoClient
from initialize import spotDistance
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
        dict1["spotid"].append(mydb.spot.find_one({"_id": spot})["spotid"])
        dict1["name"].append(mydb.spot.find_one({"_id": spot})["name"])
        dict1["visit_time"].append(mydb.spot.find_one({"_id": spot})["visit_time"])
        dict1["coordinate"].append(mydb.spot.find_one({"_id": spot})["mapID"]["LngLat"])
        dict1["level"].append(mydb.spot.find_one({"_id": spot})["level"])
    return dict

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

def saveRoute(userId, shared, date, spots, time):
    route = {'spots': spots, 'time': time, 'date': date, 'shared': shared}
    routeId = mydb.route.insert(route)
    routeID = mydb.user.find_one({"_id": userId})["routeID"]
    routeID.append(routeId)
    mydb.user.update({'_id': userId}, {'$set': {'routeID': routeID}})
    return routeId

# if __name__ == '__main__':
#     print saveRoute(mydb.user.find_one({"name": "华泽文"})["_id"], 0, ['1/8/2017','1/9/2017'],
#                     [[mydb.spot.find_one({"name": "五角场"})["_id"]], [mydb.spot.find_one({"name": "迪士尼"})["_id"]]],
#                     [[['13:30', '16:30']], [['9:00', '18:00']]])
#     print getTimeBetweenSpots([mydb.spot.find_one({"name":"五角场"})["_id"], mydb.spot.find_one({"name":"豫园"})["_id"], mydb.spot.find_one({"name":"东方明珠"})["_id"]])
