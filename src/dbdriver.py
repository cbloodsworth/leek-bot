from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

uri = f"mongodb+srv://cbloodsworth:{os.getenv('DB_KEY')}@leek-db.dvn5v5v.mongodb.net/?retryWrites=true&w=majority"
db_client = MongoClient(uri, server_api=ServerApi('1'))

db = db_client['leek-db']
collection = db['followed-users']

"""
Places if not exists, otherwise doesn't update
"""
def place_user(username: str, followed: bool) -> bool:
    data = {username : followed}
    result = collection.find_one(data)
    if result is None: 
        collection.insert_one(data)
        return True
    else: 
        return False

"""
Overwrites if already exists, returns if it was overwritten
"""
def push_user(username: str, followed: bool) -> bool:
    query = {'username' : username}
    update = {'$set': {'value': followed}}
    result = collection.update_one(query, update, upsert=True)
    return result.modified_count > 0 or result.upserted_id is not None

def query_user(username: str):
    result = collection.find_one({'username': username})
    if result: return result['value']
    else: return None 
