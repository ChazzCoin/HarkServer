from FAIR.Core import LIST, DICT
from Mongo import MCollection
from Mongo.mQuery import Q
import Mongo
from rsLogger import Log
Log = Log("mURL")

sources_collection = "sources"
urls_collection = "urls"
STATUS = "status"
SOURCE = "source"
URLS = "urls"
RSS_FIELD = "rss"
COUNT = "count"

SOURCES = "sources"
SOURCE_URLS = { STATUS: "8294", URLS: "" }
QUEUED_STATUS = "000"
QUEUED_URLS = { STATUS: QUEUED_STATUS, URLS: "" }
SUCCESSFUL_STATUS = "200"
SUCCESSFUL_URLS = { STATUS: SUCCESSFUL_STATUS, URLS: "" }
FAILED_STATUS = "400"
FAILED_URLS = { STATUS: FAILED_STATUS, URLS: "" }

SET_QUERY = Q.SET

class mURL:
    collection: MCollection

    """ -> SETUP <- """
    def init_urls(self):
        self.set_collection(urls_collection)
        if not self.collection.is_valid():
            return False

    def init_sources(self):
        self.set_collection(sources_collection)
        if not self.collection.is_valid():
            return False

    def set_collection(self, collection_name="urls"):
        self.collection = Mongo.GET_COLLECTION(collection_name)

    @classmethod
    def INIT_URLS(cls):
        nc = cls()
        return nc.init_urls()

    @classmethod
    def GET_SOURCES(cls, source):
        nc = cls()
        if not nc.init_sources():
            return False
        return nc.get_sources(source)

    @classmethod
    def ADD_TO_SOURCES(cls, source, list_of_urls):
        nc = cls()
        if not nc.init_sources():
            return False
        return nc.add_sources(source, list_of_urls)

    """ -> QUEUED (000) <- """
    @classmethod
    def ADD_TO_QUEUED(cls, list_of_urls):
        nc = cls()
        if not nc.init_urls():
            return False
        nc.add_urls(QUEUED_STATUS, list_of_urls)
        return nc

    @classmethod
    def POP_QUEUED(cls, removeFromQueued=False):
        nc = cls()
        if not nc.init_urls():
            return False
        qued = list(nc.get_urls(QUEUED_STATUS))
        next_url = qued.pop()
        if removeFromQueued:
            nc.remove_urls(next_url, status=QUEUED_STATUS)
        return next_url

    @classmethod
    def GET_QUEUED_LIST(cls):
        nc = cls()
        if not nc.init_urls():
            return False
        qued = list(nc.get_urls(QUEUED_STATUS))
        return qued

    @classmethod
    def CLEAR_QUEUED_LIST(cls):
        nc = cls()
        if not nc.init_urls():
            return False
        nc.clear_urls(QUEUED_STATUS)
        return nc

    @classmethod
    def CLEAN_QUEUED_LIST(cls):
        nc = cls()
        if not nc.init_urls():
            return False
        nc.remove_successful_from_queued()
        return nc.remove_failed_from_queued()

    @classmethod
    def REMOVE_SUCCESSFUL_FROM_QUEUED(cls):
        nc = cls()
        if not nc.init_urls():
            return False
        return nc.remove_successful_from_queued()

    @classmethod
    def REMOVE_FAILED_FROM_QUEUED(cls):
        nc = cls()
        if not nc.init_urls():
            return False
        return nc.remove_failed_from_queued()

    """ -> SUCCESSFUL (200) <- """
    @classmethod
    def ADD_TO_SUCCESSFUL(cls, list_of_urls, removeFromQueued=True):
        nc = cls()
        if not nc.init_urls():
            return False
        nc.add_urls(SUCCESSFUL_STATUS, list_of_urls)
        if removeFromQueued:
            nc.remove_urls(list_of_urls, status=QUEUED_STATUS)
        return nc

    """ -> FAILED (400) <- """
    @classmethod
    def ADD_TO_FAILED(cls, list_of_urls, removeFromQueued=True):
        nc = cls()
        if not nc.init_urls():
            return False
        nc.add(FAILED_STATUS, list_of_urls)
        if removeFromQueued:
            nc.remove_urls(list_of_urls, status=QUEUED_STATUS)
        return nc

    """ -> PRIVATE HELPERS <- """
    def remove_successful_from_queued(self):
        success = self.get_urls(SUCCESSFUL_STATUS)
        if success and len(success) > 0:
            return self.remove_urls(list(success), status=QUEUED_STATUS)
        return False

    """ -> PRIVATE HELPERS <- """
    def remove_failed_from_queued(self):
        failed = self.get_urls(FAILED_STATUS)
        if failed and len(failed) > 0:
            return self.remove_urls(list(failed), status=QUEUED_STATUS)
        return False

    def get_sources(self, source) -> []:
        results = self.collection.query({ SOURCE: source })
        item = LIST.get(0, results)
        urls = DICT.get(URLS, item)
        return urls

    def get_urls(self, status):
        results = self.collection.query({STATUS: status})
        item = LIST.get(0, results)
        urls = DICT.get(URLS, item)
        return urls if urls else False

    def add_urls(self, status, *list_of_urls):
        safe_list = LIST.flatten(list_of_urls)
        q1 = {STATUS: status}
        q2 = {"$addToSet": {URLS: {"$each": safe_list}}}
        return self.add( q1, q2 )

    def add_sources(self, source, *list_of_urls):
        safe_list = LIST.flatten(list_of_urls)
        q1 = {SOURCE: source}
        q2 = {"$addToSet": {URLS: {"$each": safe_list}}}
        return self.add(q1, q2)

    def add(self, queryOne, queryTwo):
        try:
            Log.v(f"queryOne = [ {queryOne} ] -- queryTwo = [ {queryTwo} ]")
            self.collection.collection.update_one(queryOne, queryTwo, upsert=True)
            Log.s(f"add: successfully added urls!")
            return True
        except Exception as e:
            Log.e(f"add: Failed to save urls.", error=e)
            return False

    def remove_urls(self, *urls, status):
        urls = LIST.flatten(urls)
        s = {STATUS: status}
        q = {"$pullAll": {URLS: urls}}
        return self.collection.update_record(s, q)

    def clear_urls(self, status):
        return self.update_urls(status, [])

    def update_urls(self, status, list_of_urls):
        """ PRIVATE METHOD """
        try:
            list_of_urls = list(set(list_of_urls))
            newQuery = {"$set": {URLS: list_of_urls} }
            self.collection.update_record({STATUS: status}, newQuery)
            Log.s(f"UPDATED {status} Successfully updated URLs")
            return True
        except Exception as e:
            Log.e(f"UPDATED {status} FAILED.]", error=e)
            return False


if __name__ == '__main__':
    temp = ["www.bullshit.com", "www.shit.com", "www.fuckme.com", "www.jack.com"]
