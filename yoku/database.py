from pathlib import Path
from tinydb import TinyDB, Query
from threading import Lock

from yoku.consts import KEY_ITEM_ID, KEY_CHAT_ID
from yoku.scrape import search
from yoku.botutils import notify

DB_PATH = Path.cwd() / "db.json"

TABLE_QUERIES = "queries"
KEY_QUERY = "query"


lock = Lock()

db = TinyDB(str(DB_PATH))


def add_query(chat_id, query):
    """
    Add a user query to the database
    """

    with lock:
        queries_table = db.table(TABLE_QUERIES)
        Item = Query()

        # Skip if already exists
        if queries_table.search((Item[KEY_QUERY] == query) & (Item[KEY_CHAT_ID] == chat_id)):
            return

        queries_table.insert({KEY_QUERY: query, KEY_CHAT_ID: chat_id})


def remove_query(chat_id, query):
    """
    Remove a user query from the database
    """

    with lock:
        queries_table = db.table(TABLE_QUERIES)
        Item = Query()

        queries_table.remove((Item[KEY_QUERY] == query)
                            & (Item[KEY_CHAT_ID] == chat_id))


def list_queries(chat_id):
    with lock:
        queries_table = db.table(TABLE_QUERIES)
        Item = Query()

        queries = queries_table.search(Item[KEY_CHAT_ID] == chat_id)

        return [x[KEY_QUERY] for x in queries]


def search_and_notify(bot):
    """
    Iterate through saved queries and perform search
    Cache results and notify users of new results
    """

    with lock:
        queries_table = db.table(TABLE_QUERIES)

        for row in queries_table:
            chat_id = row[KEY_CHAT_ID]
            query = row[KEY_QUERY]

            results = search(query)
            cache_table = db.table(chat_id)

            for result in results:
                item_id = result[KEY_ITEM_ID]

                Item = Query()
                if not cache_table.search(Item[KEY_ITEM_ID] == item_id):
                    notify(chat_id, result, bot)

                cache_table.upsert(result, Item[KEY_ITEM_ID] == item_id)
