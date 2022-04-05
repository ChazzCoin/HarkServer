import time
import Mongo
from FAIR.Core import DICT
from Mongo.MCore import MCore
from Mongo.mQuery import O, Find
from rsLogger import Log
from pymongo.database import Database
Log = Log("MCollection")


class MCollection(MCore):
    collection_name: str = None
    collection: Database = None
    Find: Find = None
    regex_query = {O.REGEX: ""}

    def __init__(self, collection_name):
        super().__init__()
        self.collection_name = collection_name
        self.collection = Mongo.GET_COLLECTION(collection_name)
        self.Find = Find(self.collection)

    def query(self, kwargs, page=0, limit=100):
        return self.Find.base_query(kwargs, page=page, limit=limit)

    def is_valid(self) -> bool:
        if not self.is_connected():
            return False
        if not self.collection:
            return False
        if not self.db.validate_collection(self.collection):
            return False
        return True

    @staticmethod
    def get_arg(key, value, default=False):
        return DICT.get(key, value, default=default)

    def get_document_count(self):
        res = self.collection.find({})
        if res:
            return len(list(res))
        return False

    def insert_record(self, kwargs):
        try:
            time.sleep(1)
            self.collection.insert_one(kwargs)
            Log.s(f"NEW Record created in DB=[ {self.collection_name} ]")
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.collection_name} ]", error=e)

    def update_record(self, findQuery, updateQuery):
        try:
            time.sleep(1)
            self.collection.update_one( findQuery, updateQuery )
            Log.s(f"UPDATED Record in DB=[ {self.collection_name} ]")
        except Exception as e:
            Log.e(f"Failed to save record in DB=[ {self.collection_name} ]", error=e)

    def remove_record(self, kwargs):
        try:
            time.sleep(1)
            self.collection.delete_one(kwargs)
            Log.s(f"Removed Record in DB=[ {self.collection_name} ]")
        except Exception as e:
            Log.e(f"Failed to remove record in DB=[ {self.collection_name} ]", error=e)
