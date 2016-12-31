#coding=utf-8

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
mydb = client.mydb

myuser = mydb.user
users = [{'name':'华泽文', 'password':'hzw', 'email':''},
         {'name':'曾一帆', 'password':'zyf', 'email':'123', 'phone':'18221225358'},
         {'name':'李逸超', 'password':'lyc', 'email':''},
         {'name':'赵昂悠悠', 'password':'zayy', 'email':''}]
myuser.insert(users)

myspot = mydb.spot
spots = [{'name':'东方明珠', 'mapid':{'LngLat':[111,91], 'exact_name':'东方明珠电视塔'}, 'time':60},
         {'name':'五角场', 'mapid':{'LngLat':[131, 94], 'exact_name':'五角场商业中心'}, 'time':180},
         {'name':'豫园', 'mapid':{'LngLat':[98, 73], 'exact_name':'豫园商业区'}, 'time':150},
         {'name':'迪斯尼', 'mapid':{'LngLat':[107, 81], 'exact_name':'迪斯尼乐园'}, 'time':480},
         {'name':'佘山', 'mapid':{'LngLat':[114, 90], 'exact_name':'佘山旅游景点'}, 'time':360}]
myspot.insert(spots)

myroute = mydb.route
routes = [{'spots':[myspot.find_one({"name":"东方明珠"})["_id"], myspot.find_one({"name":"豫园"})["_id"]], 'time':[['8:30', '12:00'], ['13:00', '17:00']]}]
myuser.update({'name':'华泽文'}, {'$set':{'routid':myroute.insert(routes)}})

mycity = mydb.city
citys = [{'name':'上海', 'centerposition':[110, 98], 'spots':[myspot.find_one({"name":"东方明珠"})["_id"], myspot.find_one({"name":"五角场"})["_id"], myspot.find_one({"name":"豫园"})["_id"], myspot.find_one({"name":"迪斯尼"})["_id"]], 'recommended_spots':[myspot.find_one({"name":"迪斯尼"})["_id"]]},
         {'name':'南京', 'centerposition':[111, 96], 'spots':[myspot.find_one({"name":"佘山"})["_id"]], 'recommended_spots':[myspot.find_one({"name":"佘山"})["_id"]]},
         {'name':'苏州', 'centerposition':[115, 97]}]
mycity.insert(citys)

myprovince = mydb.province
provinces = [{'name':'上海', 'citys':['上海']},
             {'name':'江苏', 'citys':['南京', '苏州']}]
myprovince.insert(provinces)