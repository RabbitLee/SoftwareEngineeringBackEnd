from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['test']
collect = db['blog']


collect.insert_one({
    'name': 'lyc',
    'password': 'lyc123'
})
