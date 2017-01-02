#coding=utf-8
import sys, urllib, urllib2, json
from urllib import urlencode
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
mydb = client.mydb

mydb.user.remove()
mydb.spot.remove()
mydb.route.remove()
mydb.city.remove()
mydb.province.remove()

myuser = mydb.user
users = [{'name':'华泽文', 'password':'hzw', 'email':'111', 'phone':'18221037351'},
         {'name':'曾一帆', 'password':'zyf', 'email':'222', 'phone':'18221225358'},
         {'name':'李逸超', 'password':'lyc', 'email':'333', 'phone':'18211111111'},
         {'name':'赵昂悠悠', 'password':'zayy', 'email':'444', 'phone':'18222222222'}]
myuser.insert(users)

myspot = mydb.spot
spots = [{'name':'东方明珠', 'mapID':{'LngLat':[111,91], 'exact_name':'东方明珠电视塔'}, 'visit_time':60, 'level': 0},
         {'name':'五角场', 'mapID':{'LngLat':[131, 94], 'exact_name':'五角场商业中心'}, 'visit_time':180, 'level': 0},
         {'name':'豫园', 'mapID':{'LngLat':[98, 73], 'exact_name':'豫园商业区'}, 'visit_time':150, 'level': 0},
         {'name':'迪斯尼', 'mapID':{'LngLat':[107, 81], 'exact_name':'迪斯尼乐园'}, 'visit_time':480, 'level': 1},
         {'name':'佘山', 'mapID':{'LngLat':[114, 90], 'exact_name':'佘山旅游景点'}, 'visit_time':360, 'level': 1}]
myspot.insert(spots)
myspot.update({'name':'东方明珠'}, {'$set':{'spotid':str(myspot.find_one({"name":"东方明珠"})["_id"])}})
myspot.update({'name':'五角场'}, {'$set':{'spotid':str(myspot.find_one({"name":"五角场"})["_id"])}})
myspot.update({'name':'豫园'}, {'$set':{'spotid':str(myspot.find_one({"name":"豫园"})["_id"])}})
myspot.update({'name':'迪斯尼'}, {'$set':{'spotid':str(myspot.find_one({"name":"迪斯尼"})["_id"])}})
myspot.update({'name':'佘山'}, {'$set':{'spotid':str(myspot.find_one({"name":"佘山"})["_id"])}})

myroute = mydb.route
routes = [{'spots':[[myspot.find_one({"name":"东方明珠"})["_id"]], [myspot.find_one({"name":"豫园"})["_id"]]], 'time':[[['8:30', '12:00']], [['13:00', '17:00']]], 'date':['1/1/2017','2/1/2017'], 'shared': 0}]
myuser.update({'name':'华泽文'}, {'$set':{'routeid':myroute.insert(routes)}})

mycity = mydb.city
citys = [{'name':'上海', 'centerposition':[110, 98], 'spots':[myspot.find_one({"name":"东方明珠"})["_id"], myspot.find_one({"name":"五角场"})["_id"], myspot.find_one({"name":"豫园"})["_id"], myspot.find_one({"name":"迪斯尼"})["_id"]]},
         {'name':'南京', 'centerposition':[111, 96], 'spots':[myspot.find_one({"name":"佘山"})["_id"]]},
         {'name':'苏州', 'centerposition':[115, 97]}]
mycity.insert(citys)

myprovince = mydb.province
provinces = [{'name':'上海', 'citys':['上海']},
             {'name':'江苏', 'citys':['南京', '苏州']}]
myprovince.insert(provinces)

def spotDistance(origin, destination):
    url = "http://restapi.amap.com/v3/direction/transit/integrated?"
    params = {
        "origin": "116.481499,39.990475",
        "destination": "116.465063,39.999538",
        "city": "010",
        "output": "json",
        "key": "a33b52f76e71d0efdf120c6a0997c380",
    }
    params = urlencode(params)
    f = urllib.urlopen(url, params)
    content = f.read()
    res = json.loads(content)