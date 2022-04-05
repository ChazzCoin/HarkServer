from bson.objectid import ObjectId
from pymongo import cursor
import Mongo
from Mongo.MCore import MCore
from rsLogger import Log

Log = Log("mQuery")


class F:
    THIS = lambda field: f"this.{field}"
    ID = "_id"
    DATE = "date"
    COUNT = "count"
    TITLE = "title"
    BODY = "body"
    DESCRIPTION = "description"
    SOURCE = "source"
    PUBLISHED_DATE = "published_date"
    URL = "url"
    URLS = "urls"
    CATEGORY = "category"


class R:
    SEARCH = lambda search_term: fr'.*{search_term}.*'
    SEARCH_STRICT = lambda search_term: fr'\b{search_term}\b'


class O:
    REGEX = "$regex"
    SEARCH = "$search"
    SET = "$set"
    PULL = "$pull"
    PUll_ALL = "$pullAll"
    OR = "$or"
    NOR = "$nor"
    AND = "$and"
    IN = "$in"
    WHERE = "$where"
    ADD_TO_SET = "$addToSet"
    EACH = "$each"
    TYPE = "$type"
    EQUALS = "$eq"
    EXISTS = "$exists"
    NOT = "$not"
    SIZE = "$size"
    OPTIONS = '$options'
    i_OPTION = 'i'
    GREATER_THAN_OR_EQUAL = "$gte"
    LESS_THAN_OR_EQUAL = "$lte"


class Q:
    BASE = lambda key, value: {key: value}
    BASE_TWO = lambda key1, value1, key2, value2: {key1: value1, key2: value2}
    OR = lambda list_of_queries: {O.OR: list_of_queries}
    AND = lambda list_of_queries: {O.AND: list_of_queries}
    REGEX = lambda search_term: Q.BASE_TWO(O.REGEX, R.SEARCH(search_term), O.OPTIONS, 'i')
    REGEX_STRICT = lambda search_term: Q.BASE_TWO(O.REGEX, R.SEARCH_STRICT(search_term), O.OPTIONS, 'i')
    SEARCH = lambda field, search_term: Q.BASE(field, Q.REGEX(search_term))
    SEARCH_STRICT = lambda field, search_term: Q.BASE(field, Q.REGEX_STRICT(search_term))
    LTE = lambda value: Q.BASE(O.LESS_THAN_OR_EQUAL, value)
    COUNT = lambda value: Q.BASE(F.COUNT, value)
    SIZE = lambda value: Q.BASE(O.SET, value)
    EQUALS = lambda value: Q.BASE(O.EQUALS, value)
    ID = lambda value: Q.BASE(F.ID, value if type(value) == ObjectId else ObjectId(value))
    DATE = lambda value: Q.BASE(F.DATE, value)
    PUBLISHED_DATE = lambda value: Q.BASE(F.PUBLISHED_DATE, value)
    SET = lambda field, list_value: Q.BASE(O.SET, Q.BASE(field, list_value))
    PULL = lambda value: Q.BASE(O.PULL, value)
    ADD_TO_SET = lambda field, list_value: Q.BASE(O.ADD_TO_SET, Q.BASE(field, Q.BASE(O.EACH, list_value)))
    FILTER_BY_FIELD = lambda field, value: Q.BASE(F.THIS(field), value)
    FILTER_BY_CATEGORY = lambda value: Q.BASE(F.THIS(F.CATEGORY), value)
    LESS_THAN_OR_EQUAL = lambda value: Q.BASE(O.LESS_THAN_OR_EQUAL, value)
    GREATER_THAN_OR_EQUAL = lambda value: Q.BASE(O.GREATER_THAN_OR_EQUAL, value)


class JQ:
    search_or_list = lambda search_term: [Q.BASE(F.BODY, Q.REGEX(search_term)),
                                          Q.BASE(F.TITLE, Q.REGEX(search_term)),
                                          Q.BASE(F.DESCRIPTION, Q.REGEX(search_term)),
                                          Q.BASE(F.SOURCE, Q.REGEX(search_term))]
    DATE = lambda dateStr: Q.OR([Q.DATE(dateStr), Q.PUBLISHED_DATE(dateStr)])
    DATE_LESS_THAN = lambda dateStr: JQ.DATE(Q.LESS_THAN_OR_EQUAL(dateStr))
    DATE_GREATER_THAN = lambda dateStr: Q.DATE(Q.GREATER_THAN_OR_EQUAL(dateStr))
    PUBLISHED_DATE_AND_URL = lambda date, url: Q.BASE_TWO(F.PUBLISHED_DATE, date, F.URL, url)
    SEARCH_FIELD_BY_DATE = lambda date, field, source_term: Q.BASE_TWO(F.PUBLISHED_DATE, date, field,
                                                                       Q.REGEX(source_term))
    SEARCH_FIELD_BY_DATE_GTE = lambda date, field, source_term: Q.BASE_TWO(F.PUBLISHED_DATE,
                                                                           Q.GREATER_THAN_OR_EQUAL(date),
                                                                           field, Q.REGEX(source_term))
    SEARCH_FIELD_BY_DATE_LTE = lambda date, field, source_term: Q.BASE_TWO(F.PUBLISHED_DATE, Q.LESS_THAN_OR_EQUAL(date),
                                                                           field, Q.REGEX(source_term))

    SEARCH_ALL = lambda search_term: Q.OR([Q.BASE(F.BODY, Q.REGEX(search_term)),
                                            Q.BASE(F.TITLE, Q.REGEX(search_term)),
                                            Q.BASE(F.DESCRIPTION, Q.REGEX(search_term)),
                                            Q.BASE(F.SOURCE, Q.REGEX(search_term))])
    SEARCH_ALL_STRICT = lambda search_term: Q.OR([Q.BASE(F.BODY, Q.REGEX_STRICT(search_term)),
                                                   Q.BASE(F.TITLE, Q.REGEX_STRICT(search_term)),
                                                   Q.BASE(F.DESCRIPTION, Q.REGEX_STRICT(search_term)),
                                                   Q.BASE(F.SOURCE, Q.REGEX_STRICT(search_term))])

    SEARCH_ALL_BY_DATE_GTE = lambda search_term, date: Q.AND([JQ.DATE_GREATER_THAN(date), JQ.SEARCH_ALL(search_term)])
    SEARCH_ALL_BY_DATE_LTE = lambda search_term, date: Q.AND([JQ.DATE_LESS_THAN(date), JQ.SEARCH_ALL(search_term)])

class Find:
    collection = None

    def __init__(self, collection_or_name):
        if type(collection_or_name) == str:
            self.collection = Mongo.GET_COLLECTION(collection_or_name)
        else:
            self.collection = collection_or_name

    def base_query(self, kwargs, page=0, limit=100):
        if limit:
            results = self.collection.find(kwargs).skip(page).limit(limit)
        else:
            results = self.collection.find(kwargs)
        results = MCore.to_list(results)
        if results and len(results) > 0:
            return results

        return False

    def search_field(self, search_term, field_name, page=0, limit=100):
        return self.base_query(kwargs=Q.SEARCH(field_name, search_term), page=page, limit=limit)

    def search_all(self, search_term, page=0, limit=100, strict=False):
        if strict:
            return self.base_query(kwargs=JQ.SEARCH_ALL_STRICT(search_term), page=page, limit=limit)
        return self.base_query(kwargs=JQ.SEARCH_ALL(search_term), page=page, limit=limit)

    def search_unlimited(self, search_term):
        return self.base_query(kwargs=JQ.SEARCH_ALL(search_term), page=False, limit=False)

    def search_before_or_after_date(self, search_term, date, page=0, limit=100, before=False):
        if before:
            return self.base_query(kwargs=JQ.SEARCH_ALL_BY_DATE_LTE(search_term, date), page=page, limit=limit)
        return self.base_query(kwargs=JQ.SEARCH_ALL_BY_DATE_GTE(search_term, date), page=page, limit=limit)

    def search_field_by_date(self, date, search_term, field_name):
        return self.base_query(kwargs=JQ.SEARCH_FIELD_BY_DATE(date, field_name, search_term))

    def find_records_where_date(self, date: str, toDict=False) -> cursor or dict:
        """ -> RETURN Cursor of all Records for Date. <- """
        result = self.collection.query(Q.DATE(date))
        if toDict:
            return MCore.to_counted_dict(result)
        else:
            return result

    def find_records_where_count(self, date: str, limit=1000, toDict=False) -> list or dict:
        """ -> RETURN List/Dict of all Records for Date with count under limit. <- """
        result = self.base_query({F.DATE: date, F.COUNT: Q.LTE(limit)})
        if toDict:
            _result = MCore.to_counted_dict(result)
        else:
            _result = list(result)
        return _result


if __name__ == '__main__':
    results1 = Find("archive").base_query(Q.DATE("December 27 2021"))
    if results1 and len(list(results1)) > 0:
        for item in list(results1):
            print(item)
