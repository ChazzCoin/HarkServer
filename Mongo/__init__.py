from Mongo.MCore import MCore
from Mongo.mQuery import Q
from Mongo.mURL import mURL
from Mongo.mArchive import mArchive

DATABASE_INSTANCE = None

if not DATABASE_INSTANCE:
    DATABASE_INSTANCE = MCore.Sozin()

def GET_COLLECTION(collection_name):
    if DATABASE_INSTANCE:
        return DATABASE_INSTANCE.get_collection(collection_name)
    return MCore.Collection(collection_name)