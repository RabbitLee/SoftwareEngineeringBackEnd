# coding=utf-8
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import jsonify
client = MongoClient('localhost', 27017)
mydb = client.mydb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def findCreator(detailroute):
    for user in mydb.user.find():
        if detailroute in user["detailrouteID"]:
            return user["name"]
    return False

def getAllRoutes():
    l = []
    for detailroute in mydb.detailroute.find():
        dict = {}
        dict["routeID"] = str(detailroute["_id"])
        dict["creator"] = findCreator(detailroute["_id"])
        routeinfo = mydb.route.find_one({"_id":detailroute["routeID"]})
        dict["date"] = routeinfo["date"]
        dict["city"] = mydb.spot.find_one({"_id":routeinfo["spots"][0][0]})["city"]
        dict["spot"] = []
        dict["spot"].append(mydb.spot.find_one({"_id":routeinfo["spots"][0][0]})["name"])
        dict["spot"].append(mydb.spot.find_one({"_id": routeinfo["spots"][len(routeinfo["spots"])-1][len(routeinfo["spots"][len(routeinfo["spots"])-1])-1]})["name"])
        l.append(dict)
    return l

def findmyVote(votes, user):
    for vote in votes:
        if vote[0] == user:
            return vote[1]
    return False

def getSelectedRoute(detailRoute, user):
    detailRoute = ObjectId(detailRoute)
    user = unicode(user, "utf8")
    dict = {}
    dict["routeID"] = str(detailRoute)
    dict["creator"] = findCreator(detailRoute)
    routeinfo = mydb.route.find_one({"_id": mydb.detailroute.find_one({"_id":detailRoute})["routeID"]})
    dict["city"] = mydb.spot.find_one({"_id": routeinfo["spots"][0][0]})["city"]
    dict["participants"] = mydb.detailroute.find_one({"_id":detailRoute})["user"]
    dict["myVote"] = findmyVote(dict["participants"], user)
    dict["agency"] = mydb.detailroute.find_one({"_id":detailRoute})["agency"]
    dict["spot_id"] = routeinfo["spots"]
    dict["time"] = routeinfo["time"]
    dict["date"] = routeinfo["date"]
    dict["spotsName"] = []
    for spot_d in routeinfo["spots"]:
        temp = []
        for spot in spot_d:
            temp.append(mydb.spot.find_one({"_id":spot})["name"])
        dict["spotsName"].append(temp)
    dict["coordinate"] = []
    for spot_d in routeinfo["spots"]:
        temp = []
        for spot in spot_d:
            temp.append(mydb.spot.find_one({"_id":spot})["mapID"]["LngLat"])
        dict["coordinate"].append(temp)
    return dict

def joinRoute(detailRoute, user):
    detailRoute = ObjectId(detailRoute)
    user = user
    users = mydb.detailroute.find_one({'_id':detailRoute})["user"]
    for u in users:
        if u[0] == user:
            return jsonify(success=False)
    mydb.user.find_one({"name":user})["detailedrouteID"] = detailRoute
    users.append([user, False])
    mydb.detailroute.update({'_id':detailRoute}, {'$set':{'user':users}})
    return jsonify(success=True)

def voteRoute(detailRoute, user, voteFor):
    detailRoute = ObjectId(detailRoute)
    user = user
    voteFor = voteFor
    users = mydb.detailroute.find_one({'_id':detailRoute})["user"]
    agencies = mydb.detailroute.find_one({'_id':detailRoute})["agency"]
    for u in users:
        if u[0] == user:
            u[1] = voteFor
            for a in agencies:
                if a["agencyID"] == voteFor:
                    a["poll"] += 1
            break
    mydb.detailroute.update({'_id':detailRoute}, {'$set':{'user':users, 'agency':agencies}})
    return jsonify(success=True)

def bidForRoute(agency, bidFor, fare):
    bidFor = ObjectId(bidFor)
    agency = agency
    agencies = mydb.detailroute.find_one({'_id': bidFor})["agency"]
    for a in agencies:
        if a["agencyID"] == agency:
            return jsonify(success=False)
    agencies.append([agency, fare, 0])
    mydb.detailroute.update({'_id': bidFor}, {'$set': {'agency': agencies}})
    return jsonify(success=True)

if __name__ == '__main__':
    print getAllRoutes()
    print getSelectedRoute("587651d3d9eca43414dbbd2e", "华泽文")
    print joinRoute("587651d3d9eca43414dbbd2e", "李逸超")
    print voteRoute("587651d3d9eca43414dbbd2e", "李逸超", "北京青旅")
    print bidForRoute("北京青旅", "587651d3d9eca43414dbbd2e", 500)
