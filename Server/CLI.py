from FAIR import Regex
from FAIR.Logger import Log, LogColors
from Mongo.mArticles import mArticles

Log = Log("Search", log_level=4)
db = mArticles.constructor()

WELCOME = f"\n{LogColors.HEADER}Welcome to Jarticle Command Line!"
ENTER_SEARCH = "Enter Search Term:"
SEARCHING = lambda search_term: f"Searching for: [ {search_term} ]"

def perform_search(search_term):
    Log.i(f"{SEARCHING(search_term=search_term)}")
    records = db.Find.search_unlimited(search_term=search_term)
    if records:
        main_loop(records)
    else:
        Log.e("No Results Found.")
        seearc_request = user_request(ENTER_SEARCH)
        perform_search(seearc_request)


def main_loop(records):
    count = len(records)
    Log.w(f"{count} Articles Found!")
    total_pages = count / 10
    art_count = 1
    current_page = 0
    processing = True
    while processing:
        if current_page >= total_pages:
            processing = False
            continue
        Log.w(f"Page {current_page + 1} of {total_pages}:")
        page_records = get_page(records, current_page)
        for i in page_records:
            Log.print_article(art_count, i)
            art_count += 1
        if current_page >= total_pages:
            user_in = user_request("\nNo More Pages - 2. New Search - 3. Exit\n")
            handle_input(user_in, False)
            return
        else:
            user_in = user_request("\n1. Next Page - 2. New Search - 3. Exit\n")
        if handle_input(user_in, True):
            current_page += 1

def handle_input(user_in, newPage=False):
    if newPage and Regex.contains_any(["1", "next", "page"], user_in):
        return True
    if Regex.contains_any(["2", "new", "search"], user_in):
        user_search = user_request(ENTER_SEARCH)
        perform_search(user_search)
        return False
    if Regex.contains_any(["3", "exit", "quit"], user_in):
        exit()
    return True

def get_page(records, page):
    end_temp = page + 1
    end = end_temp * 10
    start = page * 10
    return records[start:end]

def user_request(request):
    return input(f"\n{LogColors.HEADER}{request}")


if __name__ == '__main__':
    print(WELCOME)
    search_term = user_request(ENTER_SEARCH)
    perform_search(search_term)