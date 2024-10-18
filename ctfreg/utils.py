from datetime import datetime, timedelta
import requests

from ctfreg.error import ApiNotFound, DataNotJson


def fetch(url, params: dict = None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36"
    }
    if params is None:
        params = {}

    limit = min(1000, params.get("limit", 1000))
    start = params.get("start", datetime.now() - timedelta(days=30))
    end = params.get("end", datetime.now() + timedelta(days=30))

    params["limit"] = limit
    params["start"] = start
    params["end"] = end

    data = requests.get(url, headers=headers, params=params)
    if data.status_code == 404:
        raise ApiNotFound()
    try:
        return data.json()
    except:
        raise DataNotJson()


def fetch_safe(url, params: dict = None, all=False):
    if params is None:
        params = {"limit": 1000}
    try:
        data = fetch(url, params)
        return (
            data
            if all
            else [
                _ for _ in data if _["onsite"] == False and _["restrictions"] == "open"
            ]
        )
    except:
        return


def time_within(start_time: str, end_time: str, now_time: str = None):
    """convert to unix timestamp and compare"""
    start_time = datetime.datetime.fromisoformat(start_time)
    end_time = datetime.datetime.fromisoformat(end_time)
    if now_time is None:
        now_time = datetime.datetime.now()
    else:
        now_time = datetime.datetime.fromisoformat(now_time)
    return start_time < now_time < end_time


def time_now():
    return int(datetime.now().timestamp())
