from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import datetime

QUERIES = {'followed','recent-streak', 'leek-coins'}
CACHE_STALE_FACTOR = 0  #TODO: CHANGE THIS

uri = f"mongodb+srv://cbloodsworth:{os.getenv('DB_KEY')}@leek-db.dvn5v5v.mongodb.net/?retryWrites=true&w=majority"
db_client = MongoClient(uri, server_api=ServerApi('1'))

# pls dont change this :sob:
if os.getenv('CALL_KEY') == '$': db = db_client['leek-db']
else: db = db_client['dev-leek-db']  

collection = db['followed-users']
cache = db['cache']


"""
Pushes a <username, problem> pair to the cache database with the value of the current timestamp
"""
def push_cache(username: str, problem: str):
    # if <username, problem> is not already in cache, push pair to cache as key with current timestamp as value
    cache_entry = cache.find_one({'username': username, 'problem': problem})

    if not cache_entry:
        timestamp = datetime.datetime.now()
        cache.insert_one({'username': username, 'problem': problem, 'timestamp': timestamp})
        return True

    return False


"""
Checks through cache and deletes any stale cache entries
"""
def clean_cache():
    stale_timestamp = datetime.datetime.now() - datetime.timedelta(hours=CACHE_STALE_FACTOR)
    result = cache.delete_many({'timestamp': {'$lt': stale_timestamp}})


"""
Attempts to follow/unfollow the user.
If user is not in the database, initializes that user.
"""
def change_follow(username: str, status: bool):
    init_user(username)
    collection.update_one({'username': username}, {'$set':{'followed': status}})


"""
Fetches current streak for user
"""
def get_streak(username):
    return query_user(username)['recent-streak']


"""
Resets streak to 0
"""
def reset_streak(username):
    collection.update_one({'username': username}, {'$set':{'recent-streak': 0}})


"""
Updates streak by 1.
"""
def update_streak(username) -> int:
    user = query_user(username)
    new_streak = int(user['recent-streak']) + 1
    collection.update_one({'username': username}, {'$set':{'recent-streak': new_streak}})
    return new_streak


"""
For internal use only, should not be called by discord user
"""
def set_leekcoins(username: str, amount: int):
    user = query_user(username)
    coins = user['leek-coins'] + amount
    collection.update_one({'username': username}, {'$set':{'leek-coins': coins}})
    return coins


def get_leekcoins(username: str) -> int:
    user = query_user(username)
    return user['leek-coins']

"""
Initializes user if it doesn't already exist in the database, does not do anything else.
"""
def init_user(username: str):
    user = query_user(username)
    if user: return user
    user = {
        'username': username,
        'followed': False,
        'recent-streak': 0,
        'leek-coins': 0
        }
    collection.insert_one(user)
    return user 


"""
Queries the database based on a username.
If only given a username, it will return True if the user was found and False if not.

If given a query on that user, it will return the parameter that the query specified.
    If no such parameter exists, it will return False
"""
def query_user(username: str, query = None) -> dict:
    result = collection.find_one({'username': username})

    # Returns None if user was not found
    if not result: 
        return {}

    # If the caller provided a query parameter
    if query: 
        # If the query parameter is invalid
        if query not in QUERIES:
            print(f"Error [query_user()]: Could not find parameter {query}")
            return {}

        # else, return the query
        return result[query]

    # else, return the result, as this username is in the DB
    else: return result 


def get_followed() -> list[str]:
    results = collection.find({'followed': True})
    return [res['username'] for res in results]

