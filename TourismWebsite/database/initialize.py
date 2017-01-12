# -*- coding: UTF-8 -*-
import urllib,json
from urllib import urlencode
from pymongo import MongoClient
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

client = MongoClient('localhost', 27017)
mydb = client.mydb

mydb.user.remove()
mydb.spot.remove()
mydb.distance.remove()
mydb.route.remove()
mydb.agency.remove()
mydb.detailedroute.remove()
mydb.detailroute.remove()
mydb.city.remove()
mydb.province.remove()

myuser = mydb.user
users = [{'name':'华泽文', 'password':'hzw', 'email':'111', 'phone':'18221037351', 'routeID':[], 'detailrouteID':[]},
         {'name':'曾一帆', 'password':'zyf', 'email':'222', 'phone':'18221225358', 'routeID':[], 'detailrouteID':[]},
         {'name':'李逸超', 'password':'lyc', 'email':'333', 'phone':'18211111111', 'routeID':[], 'detailrouteID':[]},
         {'name':'赵昂悠悠', 'password':'zayy', 'email':'444', 'phone':'18222222222', 'routeID':[], 'detailrouteID':[]}]
myuser.insert(users)

myagency = mydb.agency
agencies = [{'name':'中国青旅', 'password':'zgql', 'email':'555', 'phone':'11111111'},
            {'name':'中国国旅', 'password':'zggl', 'email':'666', 'phone':'22222222'},
            {'name':'北京青旅', 'password':'bjql', 'email':'777', 'phone':'33333333'},
            {'name': '中旅国际', 'password': 'zlgj', 'email': '888', 'phone': '44444444'}]
myagency.insert(agencies)

myspot = mydb.spot
spots = [{'name':'东方明珠', 'city':'上海', 'mapID':{'LngLat':[121.52063, 31.239136], 'exact_name':'东方明珠电视塔'}, 'visit_time':90, 'level': 0},
         {'name':'五角场', 'city':'上海', 'mapID':{'LngLat':[121.514158, 31.299059], 'exact_name':'五角场商业中心'}, 'visit_time':180, 'level': 0},
         {'name':'豫园', 'city':'上海', 'mapID':{'LngLat':[121.492289, 31.227401], 'exact_name':'豫园商业区'}, 'visit_time':210, 'level': 0},
         {'name':'迪士尼', 'city':'上海', 'mapID':{'LngLat':[121.674272, 31.164291], 'exact_name':'迪士尼乐园'}, 'visit_time':480, 'level': 1},
         {'name':'佘山', 'city':'南京', 'mapID':{'LngLat':[112.196778, 31.094494], 'exact_name':'佘山旅游景点'}, 'visit_time':360, 'level': 1},
         {'name':'朱家角', 'city':'上海', 'mapID':{'LngLat':[121.053464, 31.108869], 'exact_name':'朱家角古镇旅游区'}, 'visit_time':360, 'level': 1},
         {'name':'同济大学', 'city':'上海', 'mapID':{'LngLat':[121.503799, 31.283220], 'exact_name':'同济大学四平路校区'}, 'visit_time':40, 'level': 0},
         {'name':'上海海洋馆', 'city':'上海', 'mapID':{'LngLat':[121.501550, 31.240499], 'exact_name':'上海海洋馆'}, 'visit_time':120, 'level': 0},
         {'name':'金茂大厦', 'city':'上海', 'mapID': {'LngLat':[121.504774, 31.234743], 'exact_name':'上海金茂大厦'}, 'visit_time':60, 'level': 1},
         {'name':'欢乐谷', 'city':'上海', 'mapID': {'LngLat': [121.218011, 31.094381], 'exact_name':'上海欢乐谷'},'visit_time':400, 'level': 1}]
myspot.insert(spots)
#myspot.update({'name':'东方明珠'}, {'$set':{'spotid':str(myspot.find_one({"name":"东方明珠"})["_id"])}})
#myspot.update({'name':'五角场'}, {'$set':{'spotid':str(myspot.find_one({"name":"五角场"})["_id"])}})
#myspot.update({'name':'豫园'}, {'$set':{'spotid':str(myspot.find_one({"name":"豫园"})["_id"])}})
#myspot.update({'name':'迪斯尼'}, {'$set':{'spotid':str(myspot.find_one({"name":"迪斯尼"})["_id"])}})
#myspot.update({'name':'佘山'}, {'$set':{'spotid':str(myspot.find_one({"name":"佘山"})["_id"])}})

myroute = mydb.route
route = {'spots':[[myspot.find_one({"name":"东方明珠"})["_id"], myspot.find_one({"name":"五角场"})["_id"]], [myspot.find_one({"name":"豫园"})["_id"]]], 'time':[[['8:30', '10:00'], ['14:00', '17:00']], [['13:00', '16:30']]], 'date':['1/1/2017','2/1/2017'], 'shared': 0}
routeID = myuser.find_one({"name":"华泽文"})["routeID"]
routeID.append(myroute.insert(route))
myuser.update({'name':'华泽文'}, {'$set':{'routeID':routeID}})

mydetailroute = mydb.detailroute
detailroute = [{'routeID':myuser.find_one({"name":"华泽文"})["routeID"][0],
                   'user':[[myuser.find_one({"name":"华泽文"})["name"], myagency.find_one({"name":"中国青旅"})["name"]], [myuser.find_one({"name":"曾一帆"})["name"], myagency.find_one({"name":"北京青旅"})["name"]]],
                   'agency':[{"agencyID":myagency.find_one({"name":"中国青旅"})["name"], "fare":1200, "poll":1}, {"agencyID":myagency.find_one({"name":"中国国旅"})["name"], "fare":1500, "poll":0}, {"agencyID":myagency.find_one({"name":"北京青旅"})["name"], "fare":998, "poll":1}]}]
detailrouteID = mydetailroute.insert(detailroute)
temp = myuser.find_one({"name":"华泽文"})["detailrouteID"]
temp.append(detailrouteID)
myuser.update({'name':'华泽文'}, {'$set':{'detailrouteID':detailrouteID}})
temp = myuser.find_one({"name":"曾一帆"})["detailrouteID"]
temp.append(detailrouteID)
myuser.update({'name':'曾一帆'}, {'$set':{'detailrouteID':detailrouteID}})

mycity = mydb.city
citys = [{'name':'上海', 'centerposition':[110, 98], 'spots':[]},
         {'name':'南京', 'centerposition':[111, 96], 'spots':[]},
         {'name':'苏州', 'centerposition':[115, 97], 'spots':[]}]
for city in citys:
    for spot in myspot.find():
        if spot["city"] == city["name"]:
            city["spots"].append(spot["_id"])
mycity.insert(citys)

myprovince = mydb.province
provinces = [{'name':'上海', 'citys':['上海']},
             {'name':'江苏', 'citys':['南京', '苏州']}]
myprovince.insert(provinces)

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

# mydistance = mydb.distance
# for city in mycity.find():
#     for spot1 in city["spots"]:
#         for spot2 in city["spots"]:
#             if spot1 != spot2:
#                 mydistance.insert({'origin': spot1, 'destination': spot2, 'distance': spotDistance(spot1, spot2, city["name"] + '市')})

if __name__ == '__main__':
    a = 1
    if (type(a) == int):
        print 11
