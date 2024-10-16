import requests

from .error import *


def fetch(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36"
    }
    data = requests.get(url, headers=headers)
    if data.status_code == 404:
        raise ApiNotFound()
    try:
        return data.json()
    except:
        raise DataNotJson()


def find_ctf_by_id(ctftime_id: int):
    try:
        return fetch(f"https://ctftime.org/api/v1/events/{str(ctftime_id)}/")
    except ApiNotFound:
        return

def find_ctf_by_text(search_key):
    json = fetch("https://ctftime.org/api/v1/events/?limit=1000")
    if not json:
        return 0
    for ctf in json:
        if "".join(search_key.split()).lower() in "".join(ctf["title"].split()).lower():
            return ctf["id"]
    return 0
