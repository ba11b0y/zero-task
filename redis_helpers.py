import csv
import time
from redis.exceptions import ResponseError
from conf import redis_conn
from fetch_and_save import save_zip
from datetime import datetime as dt
import datetime
import os


def calculate_expiry():
    """
    Calculates expiry for a last_sync key in redis to check and update bhavcopy
    """
    date_tod = dt.now()
    hour = date_tod.hour
    if hour >= 16:
        expiry = datetime.timedelta(days=1).seconds
    else:
        expiry = (16 - hour)*3600
    return date_tod.__str__(), expiry


def parse_csv_and_seed(path: str = "temp.csv") -> None:
    """
    Uses redis hashes as the data structure to store details about each scrip.
    Additionally sets are used for search and sorting since hashes do not support searching/sorting.
    """

    if not os.path.exists(path):
        save_zip()
    with open(path) as f:
        reader = csv.DictReader(f)
        keys = []
        trades = {}
        with redis_conn.pipeline() as pipe:
            for row in reader:
                name = row["SC_NAME"].strip()
                custom_dict = {"SC_CODE": row["SC_CODE"], "OPEN": row["OPEN"],
                               "HIGH": row["HIGH"], "LOW": row["LOW"], "CLOSE": row["CLOSE"], "PREVCLOSE": row["PREVCLOSE"], "TRADES": row["NO_TRADES"]}
                pipe.hmset(name, custom_dict)
                keys.append(name)
                trades[f"{name}"] = float(row["NO_TRADES"])
            pipe.execute()
            redis_conn.sadd("names", *set(keys))
            redis_conn.zadd("trades", trades)
            last_sync, expiry = calculate_expiry()
            redis_conn.set("last_sync", last_sync, ex=expiry)
        print("Seeded sucrcessfully!")


def search_by_name(name: str) -> list:
    """
    Fetches suggestions by name
    """
    num_keys = redis_conn.dbsize()
    try:
        _, results = redis_conn.scan(
            0, match=name.upper() + '*', count=num_keys)
    except Exception as e:
        return [e]
    final_results = [res.decode("utf-8") for res in results]
    return final_results


def order_by_num_of_trades():
    """
    Fetches top 10 results by number of trades
    """
    _ten = redis_conn.zrevrange("trades", 0, -1)[0:10]
    top_ten = [_.decode("utf-8") for _ in _ten]
    return top_ten


def get_scrip_details(scrip_name: str) -> None:
    """
    Fetches scrip details for `scrip_name`
    """
    details = redis_conn.hgetall(scrip_name)
    return details
