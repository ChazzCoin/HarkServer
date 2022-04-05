from FAIR.Core import LIST, DICT
from Mongo.mQuery import Q
from Mongo.mArticles import mArticles
from rsLogger import Log
from Mongo.MCollection import MCollection
Log = Log("mArchive")

ARCHIVE_COLLECTION = "archive"

class mArchive(MCollection):

    @classmethod
    def constructor(cls):
        return cls(ARCHIVE_COLLECTION)

    @classmethod
    def MIGRATE_ARCHIVE_TO_ARTICLES(cls, *dates):
        dates = LIST.flatten(dates)
        c = mArchive.constructor()
        for date in dates:
            temp = c.get_articles_by_date(date=date)
            if not temp:
                continue
            full_list = []
            id_list = []
            for record in temp:
                _id = DICT.get("_id", record)
                hookups = DICT.get("raw_hookups", record)
                full_list.append(hookups)
                id_list.append(_id)
            # Add list to Articles
            mArticles.ADD_ARTICLES(full_list)
            # remove archive records
            for i in id_list:
                c.remove_from_archive_by_id(i)

    @classmethod
    def GET_ARCHIVE_BY_DATE(cls, **kwargs):
        newCls = cls(ARCHIVE_COLLECTION)
        return newCls.get_articles_by_date(kwargs)

    def get_articles_by_date(self, date):
        return self.query(kwargs=Q.DATE(date))

    def remove_from_archive_by_id(self, record_id):
        return self.remove_record(Q.ID(record_id))



