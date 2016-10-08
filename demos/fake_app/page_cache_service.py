# encoding=utf-8
import urlparse


def cache_request(conn, request, callback):
    if not can_cache(conn, request):
        return callback(request)
    page_key = 'cache:' + hash_request(request)
    content = conn.get(page_key)
    if not content:
        content = callback(request)
        conn.setex(page_key, content, 300)
    return content


# <start id="_1311_14471_8289"/>
def can_cache(conn, request):
    item_id = extract_item_id(request)          #A
    if not item_id or is_dynamic(request):      #B
        return False
    rank = conn.zrank('viewed:', item_id)       #C
    return rank is not None and rank < 10000    #D
# <end id="_1311_14471_8289"/>
#A Get the item id for the page, if any
#B Check whether the page can be statically cached, and whether this is an item page
#C Get the rank of the item
#D Return whether the item has a high enough view count to be cached
#END


def extract_item_id(request):
    parsed = urlparse.urlparse(request)
    query = urlparse.parse_qs(parsed.query)
    return (query.get('item') or [None])[0]


def is_dynamic(request):
    parsed = urlparse.urlparse(request)
    query = urlparse.parse_qs(parsed.query)
    return '_' in query


def hash_request(request):
    return str(hash(request))
