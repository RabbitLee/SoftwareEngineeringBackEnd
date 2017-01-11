# coding=utf-8
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
mydb = client.mydb

def isUserValid(name, password):
    if mydb.user.find({'name': name, 'password': password}).count() == 0:
        return False
    else:
        return True

def isAgencyValid(name, password):
    if mydb.agency.find({'name': name, 'password': password}).count() == 0:
        return False
    else:
        return True

if __name__ == '__main__':
    print(isAgencyValid('中国青旅','zgql'))
