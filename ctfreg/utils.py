from datetime import datetime, timedelta, timezone
import requests
from json import dumps
import discord
from redbot.core import Config
from .error import ApiNotFoundExeption, DataNotJsonExeption


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
        if not (days or weeks or months or start or finish):
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
        raise ApiNotFoundExeption()
    try:
        return data.json()
    except:
        raise DataNotJsonExeption()


def fetch_safe(url, params: Filter = None, all=False):
    if params is None:
        params = Filter()
    try:
        data_list = fetch(url, params)
    # TODO: handle more exceptions
    except ApiNotFoundExeption as e:
        print(e.__traceback__)
        return
    except DataNotJsonExeption as e:
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


class CTFRegData:
    id: int = None
    """
     {
       "ctftimeid": 1856,
       "role": 1099364079065370716,
       "cate": 1099364081250619392,
       "name": "Space Heroes CTF",
       "info_msg": 1099364086438969435,
       "info_ch": 1099364085184872479,
       "finish": 1683493200,
       "archived": true
    }
    """

    def __init__(
        self,
        role: int,
        cate: int,
        name: str,
        info_msg: int,
        info_ch: int,
        finish: int,
        archived: bool,
        id: int = None,
    ):  
        if id is not None:
            self.id: int = id
        else :
            self.id: int = time_now()
        
        self.role: int = role
        self.cate: int = cate
        self.name: str = name
        self.infom: int = info_msg
        self.channel: int = info_ch
        self.finish: int = finish
        self.archived: bool = archived

    def generate(self):
        return {
            self.id: {
                "role": self.role,
                "cate": self.cate,
                "name": self.name,
                "infom": self.infom,
                "channel": self.channel,
                "endtime": self.finish,
                "archived": self.archived,
            }
        }
