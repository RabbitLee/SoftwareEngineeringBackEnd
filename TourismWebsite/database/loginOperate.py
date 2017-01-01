from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['test']
collect = db['blog']

def isUserValid(name, password):
    if collect.find_one({'name': name})['password'] == password:
        return True
    else:
        return False

if __name__ == '__main__':
    print(isUserValid('lyc', 'lyc123'))
