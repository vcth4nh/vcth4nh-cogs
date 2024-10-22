from datetime import datetime, timedelta, timezone
import requests
import pytz

from .error import ApiNotFound, DataNotJson


class Filter:
    def __init__(
        self,
        limit: int = 1000,
        start: int = 0,
        finish: int = 0,
        days: int = 0,
        weeks: int = 0,
        months: int = 0,
    ):
        if not (days or weeks or months):
            days = 30
        
        if days or weeks or months:
            start = int(
                (datetime.now() - timedelta(days=days + 30 * months, weeks=weeks))
                .astimezone(timezone.utc)
                .timestamp()
            )
            finish = int(
                (datetime.now() + timedelta(days=days + 30 * months, weeks=weeks))
                .astimezone(timezone.utc)
                .timestamp()
            )
        self.limit = min(limit, 1000)
        self.start = start
        self.finish = finish

    def to_dict(self):
        return {
            "limit": self.limit,
            "start": self.start,
            "finish": self.finish,
        }


def fetch(url, params: Filter = None):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36"
    }

    if params is None:
        params = Filter()
    data = requests.get(url, headers=headers, params=params.to_dict())
    if data.status_code == 404:
        raise ApiNotFound()
    try:
        return data.json()
    except:
        raise DataNotJson()


def fetch_safe(url, params: Filter = None, all=False):
    if params is None:
        params = Filter()
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


def time_now_utc():
    return int(datetime.now().astimezone(tz=timezone.utc).timestamp())
