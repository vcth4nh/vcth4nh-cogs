from typing import List
from .utils import *
from thefuzz import fuzz, process

EVENT_URL = "https://ctftime.org/api/v1/events/"


def find_ctf_by_id(ctftime_id: int):
    return fetch_safe(f"{EVENT_URL}{str(ctftime_id)}/", all=True)


def find_ctf_by_text(search_key: str) -> List:
    param = Filter(limit=1000, days=365)
    data = fetch_safe(EVENT_URL, all=True)
    if not data:
        return

    # title_list = [x["organizers"][] + ' ' + x["title"] for x in data]
    search_list=[]
    for x in data:
        organizers_list = []
        for org in x["organizers"]:
            organizers_list.append(org["name"])
        organizers = ' '.join(organizers_list)
        search_list.append(organizers + ' ' + x["title"])
        
    result = process.extract(
        query=search_key, choices=search_list, scorer=fuzz.token_set_ratio, limit=5
    )
    return [data[search_list.index(x[0])] for x in result]


def get_ongoing_ctfs(
    all=False,
    limit: int = 100,
):
    data = fetch_safe(EVENT_URL, Filter(limit=limit), all)
    if not data:
        return
    return [x for x in data if time_within(x["start"], x["finish"])]


def get_upcoming_ctfs(
    all=False,
    limit: int = 100,
    weeks: int = 2,
):
    start = time_now_utc()
    finish = int(
        (datetime.now() + timedelta(weeks=weeks)).astimezone(timezone.utc).timestamp()
    )
    filter = Filter(limit=limit, start=start, finish=finish)

    data = fetch_safe(EVENT_URL, filter, all)
    return data


def get_past_ctfs(
    all=False,
    limit: int = 100,
    weeks: int = 2,
):
    start = int(
        (datetime.now() - timedelta(weeks=weeks)).astimezone(timezone.utc).timestamp()
    )
    finish = time_now_utc()
    filter = Filter(limit=limit, start=start, finish=finish)

    data = fetch_safe(EVENT_URL, filter, all)
    data.reverse()
    return data
