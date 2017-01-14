# -*- coding: UTF-8 -*-
import urllib,json
from urllib import urlencode
import re
import random
##from urllib import urlencode
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
users = [{'name':'华泽文', 'password':'hzw', 'email':'hzw@163.com', 'phone':'18221037351', 'routeID':[], 'detailrouteID':[]},
         {'name':'曾一帆', 'password':'zyf', 'email':'zyf@126.com', 'phone':'18221225358', 'routeID':[], 'detailrouteID':[]},
         {'name':'李逸超', 'password':'lyc', 'email':'lyc@gmail.com', 'phone':'18211111111', 'routeID':[], 'detailrouteID':[]},
         {'name':'赵昂悠悠', 'password':'zayy', 'email':'zayy@qq.com', 'phone':'18222222222', 'routeID':[], 'detailrouteID':[]}]
myuser.insert(users)

myagency = mydb.agency
agencies = [{'name':'中国青旅', 'password':'zgql', 'email':'555', 'phone':'11111111'},
            {'name':'中国国旅', 'password':'zggl', 'email':'666', 'phone':'22222222'},
            {'name':'北京青旅', 'password':'bjql', 'email':'777', 'phone':'33333333'},
            {'name': '中旅国际', 'password': 'zlgj', 'email': '888', 'phone': '44444444'}]
myagency.insert(agencies)

def getLngLat(address, city):
    url = "http://restapi.amap.com/v3/geocode/geo?"
    params = {
        "address": address,
        "city": city,
        "output": "JSON",
        "key": "ca67bcc4b9fc499bb058e983b2a9b10f",
    }
    params = urlencode(params)
    f = urllib.urlopen(url, params)
    content = f.read()
    res = json.loads(content)
    if res['count'] == '0':
        return False
    else:
        return (res['geocodes'][0]['location'])

def initializeSpotsByCity(city):
    def getHtml(url):
        page = urllib.urlopen(url)
        html = page.read()
        return html
    def getImg(html):
        reg = r'<a\s+href="http://www.tuniu.com.g' + city + r'/whole-sh-0/list-d.+?-h0-i-j0_0/"\s+rel="nofollow">\s+(.+?)\s+</a>'
        #reg = r'<a href="/poi/.+?\.html" target="_blank" title="(.+?)\">'
        #r'A 上海市景点 (.+?)\<br>'
        imgre = re.compile(reg)
        imglist = re.findall(imgre, html)
        return imglist
    html = getHtml("http://www.tuniu.com/g" + city + "/whole-sh-0/list-h0-j0_0/")
    return getImg(html)

def randlevel():
    if random.randint(0, 5) == 0:
        return 1
    else:
        return 0

myspot = mydb.spot

citys = [["三亚", "906"],["海口","902"],["重庆","300"]]
spots = []

for city in citys:
    s = initializeSpotsByCity(city[1])
    n = 0
    for i in s:
        if n >= 15:
            break
        LngLat = getLngLat(i, city[0])
        if LngLat != False and not ("酒店" in i):
            LngLat = LngLat.split(',')
            LngLat[0] = float(LngLat[0])
            LngLat[1] = float(LngLat[1])
            spots.append({'name': i, 'city': city[0], 'mapID': {'LngLat': LngLat}, 'visit_time': 30 * random.randint(2, 12),'level': randlevel()})
            n += 1
myspot.insert(spots)

spots = [{'name':'东方明珠', 'city':'上海', 'mapID':{'LngLat':[121.52063, 31.239136], 'exact_name':'东方明珠电视塔'}, 'visit_time':90, 'level': 0},
         {'name':'五角场', 'city':'上海', 'mapID':{'LngLat':[121.514158, 31.299059], 'exact_name':'五角场商业中心'}, 'visit_time':180, 'level': 0},
         {'name':'豫园', 'city':'上海', 'mapID':{'LngLat':[121.492289, 31.227401], 'exact_name':'豫园商业区'}, 'visit_time':210, 'level': 0},
         {'name':'迪士尼', 'city':'上海', 'mapID':{'LngLat':[121.674272, 31.164291], 'exact_name':'迪士尼乐园'}, 'visit_time':480, 'level': 1},
         {'name':'佘山', 'city':'南京', 'mapID':{'LngLat':[112.196778, 31.094494], 'exact_name':'佘山旅游景点'}, 'visit_time':360, 'level': 1},
         {'name':'朱家角', 'city':'上海', 'mapID':{'LngLat':[121.053464, 31.108869], 'exact_name':'朱家角古镇旅游区'}, 'visit_time':360, 'level': 0},
         {'name':'同济大学', 'city':'上海', 'mapID':{'LngLat':[121.503799, 31.283220], 'exact_name':'同济大学四平路校区'}, 'visit_time':40, 'level': 1},
         {'name':'上海海洋馆', 'city':'上海', 'mapID':{'LngLat':[121.501550, 31.240499], 'exact_name':'上海海洋馆'}, 'visit_time':120, 'level': 0},
         {'name':'金茂大厦', 'city':'上海', 'mapID': {'LngLat':[121.504774, 31.234743], 'exact_name':'上海金茂大厦'}, 'visit_time':60, 'level': 0},
         {'name':'欢乐谷', 'city':'上海', 'mapID': {'LngLat': [121.218011, 31.094381], 'exact_name':'上海欢乐谷'},'visit_time':400, 'level': 0},
         {'name':'外滩', 'city':'上海', 'mapID': {'LngLat': [121.491084, 31.234991], 'exact_name':'上海外滩'},'visit_time':20, 'level': 1},
         {'name': '玉佛寺', 'city': '上海', 'mapID': {'LngLat': [121.445043, 31.241043], 'exact_name': '上海玉佛寺'},'visit_time': 30, 'level': 0},
         {'name': '上海博物馆', 'city': '上海', 'mapID': {'LngLat': [121.475410, 31.228254], 'exact_name': '上海博物馆'},'visit_time': 100, 'level': 0},
         {'name': '中华艺术宫', 'city': '上海', 'mapID': {'LngLat': [121.494590, 31.184375], 'exact_name': '上海中华艺术宫'},'visit_time': 80, 'level': 0},
         {'name': '上海杜莎夫人蜡像馆', 'city': '上海', 'mapID': {'LngLat': [121.473819, 31.234775], 'exact_name': '上海杜莎夫人蜡像馆'},'visit_time': 80, 'level': 0},
         {'name': '上海鲁迅公园', 'city': '上海', 'mapID': {'LngLat': [121.483015, 31.271649], 'exact_name': '上海鲁迅公园'},'visit_time': 30, 'level': 0}]
         # {'name': '朱家角', 'city': '上海', 'mapID': {'LngLat': [121.053464, 31.108869], 'exact_name': '朱家角古镇旅游区'}, 'visit_time': 360, 'level': 1},
         # {'name': '同济大学', 'city': '上海', 'mapID': {'LngLat': [121.503799, 31.283220], 'exact_name': '同济大学四平路校区'}, 'visit_time': 40, 'level': 0},
         # {'name': '上海海洋馆', 'city': '上海', 'mapID': {'LngLat': [121.501550, 31.240499], 'exact_name': '上海海洋馆'}, 'visit_time': 120, 'level': 0},
         # {'name': '金茂大厦', 'city': '上海', 'mapID': {'LngLat': [121.504774, 31.234743], 'exact_name': '上海金茂大厦'}, 'visit_time': 60, 'level': 1},
         # {'name': '欢乐谷', 'city': '上海', 'mapID': {'LngLat': [121.218011, 31.094381], 'exact_name': '上海欢乐谷'}, 'visit_time': 400, 'level': 1}]

myspot.insert(spots)
#myspot.update({'name':'东方明珠'}, {'$set':{'spotid':str(myspot.find_one({"name":"东方明珠"})["_id"])}})
#myspot.update({'name':'五角场'}, {'$set':{'spotid':str(myspot.find_one({"name":"五角场"})["_id"])}})
#myspot.update({'name':'豫园'}, {'$set':{'spotid':str(myspot.find_one({"name":"豫园"})["_id"])}})
#myspot.update({'name':'迪斯尼'}, {'$set':{'spotid':str(myspot.find_one({"name":"迪斯尼"})["_id"])}})
#myspot.update({'name':'佘山'}, {'$set':{'spotid':str(myspot.find_one({"name":"佘山"})["_id"])}})

myroute = mydb.route
route = {'spots':[[myspot.find_one({"name":"东方明珠"})["_id"], myspot.find_one({"name":"上海海洋馆"})["_id"]], [myspot.find_one({"name":"豫园"})["_id"],myspot.find_one({"name":"五角场"})["_id"],myspot.find_one({"name":"迪士尼"})["_id"]]], 'time':[[['8:30', '10:00'], ['14:00', '17:00']], [['8:00', '9:30'], ['10:00', '11:30'], ['1:00', '4:30']]], 'date':['01/01/2017','01/02/2017'], 'shared': 0}
routeID = myuser.find_one({"name":"华泽文"})["routeID"]
routeID.append(myroute.insert(route))
myuser.update({'name':'华泽文'}, {'$set':{'routeID':routeID}})

route = {'spots':[[myspot.find_one({"name":"中华艺术宫"})["_id"], myspot.find_one({"name":"上海杜莎夫人蜡像馆"})["_id"]], [myspot.find_one({"name":"外滩"})["_id"],myspot.find_one({"name":"五角场"})["_id"],myspot.find_one({"name":"玉佛寺"})["_id"]]], 'time':[[['8:30', '10:00'], ['14:00', '16:00']], [['9:00', '9:30'], ['10:00', '11:30'], ['1:00', '3:30']]], 'date':['02/04/2017','02/05/2017'], 'shared': 1}
routeID = myuser.find_one({"name":"华泽文"})["routeID"]
routeID.append(myroute.insert(route))
myuser.update({'name':'华泽文'}, {'$set':{'routeID':routeID}})

route = {'spots':[[myspot.find_one({"name":"金茂大厦"})["_id"], myspot.find_one({"name":"上海鲁迅公园"})["_id"]], [myspot.find_one({"name":"豫园"})["_id"],myspot.find_one({"name":"同济大学"})["_id"],myspot.find_one({"name":"五角场"})["_id"]]], 'time':[[['8:30', '10:00'], ['15:00', '17:00']], [['9:00', '10:30'], ['10:00', '11:30'], ['2:00', '4:30']]], 'date':['03/01/2017','03/02/2017'], 'shared': 1}
routeID = myuser.find_one({"name":"华泽文"})["routeID"]
routeID.append(myroute.insert(route))
myuser.update({'name':'华泽文'}, {'$set':{'routeID':routeID}})

route = {'spots':[[myspot.find_one({"name":"东方明珠"})["_id"], myspot.find_one({"name":"上海海洋馆"})["_id"]], [myspot.find_one({"name":"豫园"})["_id"],myspot.find_one({"name":"五角场"})["_id"],myspot.find_one({"name":"迪士尼"})["_id"]], [myspot.find_one({"name":"外滩"})["_id"], myspot.find_one({"name":"同济大学"})["_id"]]], 'time':[[['8:30', '10:00'], ['14:00', '17:00']], [['8:00', '9:30'], ['10:00', '11:30'], ['1:00', '4:30']], [['8:30', '10:00'], ['14:00', '17:00']]], 'date':['02/01/2017','02/03/2017'], 'shared': 1}
routeID = myuser.find_one({"name":"华泽文"})["routeID"]
routeID.append(myroute.insert(route))
myuser.update({'name':'华泽文'}, {'$set':{'routeID':routeID}})

mydetailroute = mydb.detailroute
detailroute = {'routeID':myuser.find_one({"name":"华泽文"})["routeID"][0],
                   'user':[[myuser.find_one({"name":"华泽文"})["name"], myagency.find_one({"name":"中国青旅"})["name"], "未支付"], [myuser.find_one({"name":"曾一帆"})["name"], myagency.find_one({"name":"北京青旅"})["name"], "已支付"]],
                   'agency':[{"agencyID":myagency.find_one({"name":"中国青旅"})["name"], "fare":1200, "poll":1}, {"agencyID":myagency.find_one({"name":"中国国旅"})["name"], "fare":1500, "poll":0}, {"agencyID":myagency.find_one({"name":"北京青旅"})["name"], "fare":998, "poll":1}]}
detailrouteID = mydetailroute.insert(detailroute)
temp = myuser.find_one({"name":"华泽文"})["detailrouteID"]
temp.append(detailrouteID)
myuser.update({'name':'华泽文'}, {'$set':{'detailrouteID':detailrouteID}})
temp = myuser.find_one({"name":"曾一帆"})["detailrouteID"]
temp.append(detailrouteID)
myuser.update({'name':'曾一帆'}, {'$set':{'detailrouteID':detailrouteID}})

detailroute = {'routeID':myuser.find_one({"name":"华泽文"})["routeID"][0],
                   'user':[[myuser.find_one({"name":"华泽文"})["name"], myagency.find_one({"name":"中国国旅"})["name"], "已支付"], [myuser.find_one({"name":"李逸超"})["name"], myagency.find_one({"name":"中国青旅"})["name"], "已支付"]],
                   'agency':[{"agencyID":myagency.find_one({"name":"中国青旅"})["name"], "fare":200, "poll":1}, {"agencyID":myagency.find_one({"name":"中国国旅"})["name"], "fare":500, "poll":0}, {"agencyID":myagency.find_one({"name":"中旅国际"})["name"], "fare":398, "poll":1}]}
detailrouteID = mydetailroute.insert(detailroute)
temp = myuser.find_one({"name":"华泽文"})["detailrouteID"]
temp.append(detailrouteID)
myuser.update({'name':'华泽文'}, {'$set':{'detailrouteID':detailrouteID}})
temp = myuser.find_one({"name":"李逸超"})["detailrouteID"]
temp.append(detailrouteID)
myuser.update({'name':'李逸超'}, {'$set':{'detailrouteID':detailrouteID}})



mycity = mydb.city
citys = [{'name':'上海', 'centerposition':[110, 98], 'spots':[]},
         {'name':'南京', 'centerposition':[111, 96], 'spots':[]},
         {'name':'重庆', 'centerposition':[111, 96], 'spots':[]},
         {'name':'苏州', 'centerposition':[115, 97], 'spots':[]},
         {'name':'三亚', 'centerposition':[115, 97], 'spots':[]},
         {'name':'海口', 'centerposition': [115, 97], 'spots':[]}]
for city in citys:
    for spot in myspot.find():
        if spot["city"] == city["name"]:
            city["spots"].append(spot["_id"])
mycity.insert(citys)

myprovince = mydb.province
provinces = [{'name':'上海', 'citys':['上海']},
             {'name':'重庆', 'citys':['重庆']},
             {'name':'海南', 'citys':['三亚', '海口']},
             {'name':'江苏', 'citys':['南京', '苏州']}]
myprovince.insert(provinces)
global z
z = 0
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
        "output": "JSON",
        "key": "ca67bcc4b9fc499bb058e983b2a9b10f",
    }
    params = urlencode(params)
    f = urllib.urlopen(url, params)
    content = f.read()
    res = json.loads(content)
    # global z
    # z += 1
    # if z >= 70:
    #     print res["route"]
    # print z
    # if res["route"]["transits"] == []:
    #     a = int(res["route"]["distance"])/1.0
    #     print a
    #     return a
    return int(res["route"]["transits"][0]["duration"])

mydistance = mydb.distance
for city in mycity.find():
    if city["name"] == "上海":
        for spot1 in city["spots"]:
            for spot2 in city["spots"]:
                if spot1 != spot2:
                    mydistance.insert({'origin': spot1, 'destination': spot2, 'distance': spotDistance(spot1, spot2, city["name"] + '市')})

if __name__ == '__main__':
     a = 1
#     if (type(a) == int):
#         print 11
