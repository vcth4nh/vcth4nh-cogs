from datetime import datetime, timedelta, timezone
import requests
import pytz

from .error import ApiNotFound, DataNotJson


def fetch(url, params: dict = None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36"
    }
    if params is None:
        params = {}

    limit = min(1000, params.get("limit", 1000))
    start = params.get(
        "start",
        int((datetime.now() - timedelta(days=30)).astimezone(timezone.utc).timestamp()),
    )
    end = params.get(
        "end",
        int((datetime.now() + timedelta(days=30)).astimezone(timezone.utc).timestamp()),
    )

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
        data_list = fetch(url, params)
    # TODO: handle more exceptions
    except ApiNotFound as e:
        print(e.__traceback__)
        return

    return (
        data_list
        if all
        else [
            data
            for data in data_list
            if data["onsite"] == False and data["restrictions"] == "Open"
        ]
    )


def time_within(start_time: str, end_time: str, now_time: str = None):
    """convert to unix timestamp and compare"""
    start_time = datetime.fromisoformat(start_time)
    end_time = datetime.fromisoformat(end_time)
    if now_time is None:
        now_time = datetime.now().astimezone(tz=timezone.utc)
    else:
        now_time = datetime.fromisoformat(now_time)
    return start_time < now_time < end_time


def time_now():
    return int(datetime.now().timestamp())
