import json, datetime
from math import ceil
import requests

from response_embeded import GeneralEmbed
from utils import parse_ctftime_json


def find_ctf_by_id(ctftime_id, creating=False, username=None, password=None):
    data = requests.get(f"https://ctftime.org/api/v1/events/{str(ctftime_id)}/")
    if data.status_code == 404:
        if creating:
            return False, False, False
        else:
            return False

    return parse_ctftime_json(data.json(), creating, username, password)


def find_ctf_by_text(search_key):
    data = requests.get('https://ctftime.org/api/v1/events/?limit=1000')
    if data.status_code == 404:
        return 0
    data = data.json()

    for ctf in data:
        if "".join(search_key.split()).lower() in "".join(ctf['title'].split()).lower():
            return ctf['id']
    return 0
