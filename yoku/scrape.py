import re
from urllib import parse
from bs4 import BeautifulSoup
import requests

from yoku.consts import KEY_TITLE, KEY_BUYNOW_PRICE, KEY_CURRENT_PRICE, KEY_END_TIMESTAMP, KEY_IMAGE, KEY_ITEM_ID, KEY_POST_TIMESTAMP, KEY_START_PRICE, KEY_START_TIMESTAMP, KEY_URL

# Always search sorted by new in descending order
YAHUOKU_SEARCH_TEMPLATE = r"https://auctions.yahoo.co.jp/search/search?p={query}&b={start}&n={count}&s1=new&o1=d"

POST_TIMESTAMP_REGEX = r"^.*i-img\d+x\d+-(\d{10}).*$"
AUCTION_TIMESTAMP_REGEX = r"^.*etm=(\d{10}),stm=(\d{10}).*$"


def get_raw_results(query: str):
    """
    Return raw html page content of the results from the search query
    """

    # start cannot be more than 15000
    url = YAHUOKU_SEARCH_TEMPLATE.format(query=parse.quote_plus(query), start=1, count=100)
    print(f"[GET] {url}")

    r = requests.get(url)

    return r.text


def parse_raw_results(raw: str):
    """
    Parse a raw html page of search results and return a list of result dicts
    """

    results = []
    soup = BeautifulSoup(raw, "lxml")

    product_details = soup.find_all("div", class_="Product__detail")
    for product_detail in product_details:
        product_bonuses = product_detail.find_all(
            "div", class_="Product__bonus")
        product_titlelinks = product_detail.find_all(
            "a", class_="Product__titleLink")

        if not product_bonuses or not product_titlelinks:
            continue

        product_bonus = product_bonuses[0]
        product_titlelink = product_titlelinks[0]

        auction_title = product_titlelink["data-auction-title"]
        auction_img = product_titlelink["data-auction-img"]
        href = product_titlelink["href"]
        cl_params = product_titlelink["data-cl-params"]

        match = re.match(POST_TIMESTAMP_REGEX, auction_img)
        if not match:
            continue

        post_timestamp = int(match.group(1))

        match = re.match(AUCTION_TIMESTAMP_REGEX, cl_params)
        if not match:
            continue

        end_timestamp = int(match.group(1))
        start_timestamp = int(match.group(2))

        auction_id = product_bonus["data-auction-id"]
        auction_buynowprice = product_bonus["data-auction-buynowprice"]
        auction_price = product_bonus["data-auction-price"]
        auction_startprice = product_bonus["data-auction-startprice"]

        result = {
            KEY_TITLE: auction_title,
            KEY_IMAGE: auction_img,
            KEY_URL: href,

            KEY_POST_TIMESTAMP: post_timestamp,
            KEY_END_TIMESTAMP: end_timestamp,
            KEY_START_TIMESTAMP: start_timestamp,

            KEY_ITEM_ID: auction_id,
            KEY_BUYNOW_PRICE: auction_buynowprice,
            KEY_CURRENT_PRICE: auction_price,
            KEY_START_PRICE: auction_startprice,
        }

        results.append(result)

    return results


def search(query: str):
    """
    Search for query and return a list of result dicts
    """

    raw = get_raw_results(query)

    return parse_raw_results(raw)
