# coding=utf-8
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
mydb = client.mydb

def register(name, password, email, phone):
    if mydb.user.find({"name": name}).count() == 0:
        mydb.user.insert({'name': name, 'password': password, 'email': email, 'phone': phone})
        return True
    else:
        return False