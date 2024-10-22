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
    data = fetch_safe(EVENT_URL, {"limit": limit}, all)
    if not data:
        return
    return [x for x in data if time_within(x["start"], x["finish"])]
