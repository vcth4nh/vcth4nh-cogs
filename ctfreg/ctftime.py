from .utils import *

EVENT_URL = "https://ctftime.org/api/v1/events/"


def find_ctf_by_id(ctftime_id: int):
    return fetch_safe(f"{EVENT_URL}{str(ctftime_id)}/", all=True)


# TODO: return list of contests insead of single contest id
def find_ctf_by_text(search_key, all=False):
    json = fetch_safe(EVENT_URL, all)
    if not json:
        return 0
    for ctf in json:
        if "".join(search_key.split()).lower() in "".join(ctf["title"].split()).lower():
            return ctf["id"]
    return 0


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
    return data
