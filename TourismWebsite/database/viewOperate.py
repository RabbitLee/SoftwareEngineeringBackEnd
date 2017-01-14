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

def showRouteInPage(userID):
    l = []
    for detailroute in mydb.user.find_one({"name":userID})["detailrouteID"]:
        detailrouteinfo = mydb.detailroute.find_one({"_id": detailroute})
        dict = {}
        dict["routeID"] = str(detailrouteinfo["_id"])
        routeinfo = mydb.route.find_one({"_id":detailrouteinfo["routeID"]})
        for user in mydb.user.find():
            if routeinfo["_id"] in user["routeID"]:
                dict["creator"] = user["name"]
        dict["date"] = routeinfo["date"]
        dict["city"] = mydb.spot.find_one({"_id":routeinfo["spots"][0][0]})["city"]
        dict["spot"] = []
        dict["spot"].append(mydb.spot.find_one({"_id": routeinfo["spots"][0][0]})["name"])
        dict["spot"].append(mydb.spot.find_one({"_id": routeinfo["spots"][len(routeinfo["spots"]) - 1][len(routeinfo["spots"][len(routeinfo["spots"]) - 1]) - 1]})["name"])
        l.append(dict)
    return l


def showAllAgency(userID):
    l = []
    for detailroute in mydb.user.find_one({"name":userID})["detailrouteID"]:
        detailrouteinfo = mydb.detailroute.find_one({"_id":detailroute})
        dict = {}
        for user in detailrouteinfo["user"]:
            if user[0] == userID:
                if user[1] == "False":
                    return "未投票"
                else:
                    dict["agency"] = user[1]
                    dict["state"] = user[2]
        dict["routeID"] = str(detailroute)
        routeinfo = mydb.route.find_one({"_id": detailrouteinfo["routeID"]})
        dict["date"] = routeinfo["date"]
        dict["city"] = mydb.spot.find_one({"_id":routeinfo["spots"][0][0]})["city"]
        l.append(dict)
    return l

def hasbidden(agencyname, agencyinfo):
    for agency in agencyinfo:
        if agency["agencyID"] == agencyname:
            return True
    return False

def showAgencyRoute(agencyname):
    l = []
    for detailroute in mydb.detailroute.find():
        if hasbidden(agencyname, detailroute["agency"]):
            dict = {}
            dict["routeID"] = str(detailroute["_id"])
            route = detailroute["routeID"]
            for user in mydb.user.find():
                if route in user["routeID"]:
                    dict["creator"] = user["name"]
            routeinfo = mydb.route.find_one({"_id": route})
            dict["date"] = routeinfo["date"]
            dict["city"] = mydb.spot.find_one({"_id": routeinfo["spots"][0][0]})["city"]
            dict["spot"] = []
            dict["spot"].append(mydb.spot.find_one({"_id": routeinfo["spots"][0][0]})["name"])
            dict["spot"].append(mydb.spot.find_one({"_id": routeinfo["spots"][len(routeinfo["spots"]) - 1][len(routeinfo["spots"][len(routeinfo["spots"]) - 1]) - 1]})["name"])
            l.append(dict)
    return l

def getSelectedRoute(agencyname, detailRouteID):
    detailRouteID = ObjectId(detailRouteID)
    dict = {}
    dict["routeId"] = str(detailRouteID)
    route = mydb.detailroute.find_one({"_id":detailRouteID})["routeID"]
    for user in mydb.user.find():
        if route in user["routeID"]:
            dict["creator"] = user["name"]
    routeinfo = mydb.route.find_one({"_id": route})
    dict["city"] = mydb.spot.find_one({"_id": routeinfo["spots"][0][0]})["city"]
    users = mydb.detailroute.find_one({"_id":detailRouteID})["user"]
    dict["participants"] = []
    for u in users:
        userinfo = mydb.user.find_one({"name": u[0]})
        dict["participants"].append([userinfo["name"], userinfo["email"], u[2]])
    dict["agency"] = mydb.detailroute.find_one({"_id":detailRouteID})["agency"]
    dict["spot_id"] = []
    for spot_d in routeinfo["spots"]:
        temp = []
        for spot in spot_d:
            temp.append(str(spot))
        dict["spot_id"].append(temp)
    dict["time"] = routeinfo["time"]
    dict["date"] = routeinfo["date"]
    dict["spotsName"] = []
    for spot_d in routeinfo["spots"]:
        temp = []
        for spot in spot_d:
            temp.append(mydb.spot.find_one({"_id": spot})["name"])
        dict["spotsName"].append(temp)
    dict["coordinate"] = []
    for spot_d in routeinfo["spots"]:
        temp = []
        for spot in spot_d:
            temp.append(mydb.spot.find_one({"_id": spot})["mapID"]["LngLat"])
        dict["coordinate"].append(temp)
    return dict

if __name__ == '__main__':
    print showRouteInPage("华泽文")
    # print showAllAgency("华泽文")
    # print showAgencyRoute("中国青旅")
    print getSelectedRoute("中国青旅", "58797135a7c709bbacc588b6")
    # print getSelectedRoute("587651d3d9eca43414dbbd2e", "华泽文")
    # print joinRoute("587651d3d9eca43414dbbd2e", "李逸超")
    # print voteRoute("587651d3d9eca43414dbbd2e", "李逸超", "北京青旅")
    # print bidForRoute("北京青旅", "587651d3d9eca43414dbbd2e", 500)
