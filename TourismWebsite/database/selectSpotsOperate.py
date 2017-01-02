# coding=utf-8
from pymongo import MongoClient

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

if __name__ == '__main__':
    # print(getAllSpots('上海'))
    a = []
    a = [110,115]
    print str(a[0]) + ","+ str(a[1])