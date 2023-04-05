from pymongo import MongoClient
from os import environ
client = MongoClient(environ['url'])
db = client['main']['tokens']
def add(id, amount):
  try:
    new = db.find_one({"_id": id})['tokens']
  except:
    db.insert_one({'_id': id, 'urls': 0})
  new += amount
  db.update_one({'_id': id}, {'$set': {"_id": id, 'tokens': new}})
  return None

def remove(id, amount) -> bool:
  try:
    new = db.find_one({"_id": id})['tokens']
  except:
    return False
  new -= amount
  db.update_one({'_id': id}, {'$set': {"_id": id, 'tokens': new}})
  return True

def get_coin(id):
  try:
    return db.find_one({"_id": id})['tokens']
  except:
    return 0
