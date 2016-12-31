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
    dict["certerPosition"] = citys["centerposition"]
    dict["spots"] = []
    for spot in mydb.city.find_one({"name": city})["spots"]:
        dict["spots"].append(mydb.spot.find_one({"_id":spot}))
    dict["recommendedSpots"] = citys["recommended_spots"]
    return dict

if __name__ == '__main__':
    print(getAllCities('江苏'))