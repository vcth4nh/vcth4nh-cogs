from datetime import datetime, timedelta
import re

import pytz
from typing import List, Dict


"""Example data:
{
    "organizers": [
        {
            "id": 127017,
            "name": "Cyber Hacktics"
        }
    ],
    "ctftime_url": "https://ctftime.org/event/2443/",
    "ctf_id": 487,
    "weight": 38.7,
    "duration": {
        "hours": 10,
        "days": 1
    },
    "live_feed": "https://ctftime.org/live/2443/",
    "logo": "https://ctftime.org/media/events/logo_deadface_ctf_2024.png",
    "id": 2443,
    "title": "DEADFACE CTF 2024",
    "start": "2024-10-18T14:00:00+00:00",
    "participants": 189,
    "location": "",
    "finish": "2024-10-20T00:00:00+00:00",
    "description": "Welcome to the electrifying world of DEADFACE CTF, where cybersecurity enthusiasts and professionals converge to test their skills individually or as a team and face off against a formidable adversary known as DEADFACE. Organized by Cyber Hacktics, a registered non-profit organization, DEADFACE CTF stands out as a premier Capture-the-Flag competition that goes beyond the ordinary. With thrilling challenges, enticing prizes, and a mission to cultivate cybersecurity excellence, this event is a must-attend for anyone seeking to immerse themselves in the dynamic realm of cyber warfare.",
    "format": "Jeopardy",
    "is_votable_now": false,
    "prizes": "First Place Team: $300 USD\r\nSecond Place Team: $200 USD\r\nThird Place Team: $100 USD",
    "format_id": 1,
    "onsite": false,
    "restrictions": "Open",
    "url": "https://ctf.deadface.io/",
    "public_votable": false
}
"""


def parse_ctftime_json_long(data, list_fn: List[callable]) -> List[List]:
    if isinstance(data, dict):
        data = [data]
    embed_fields_list = []
    for ctf in data:
        embed_fields = []
        for fn in list_fn:
            fn(embed_fields, ctf)
        embed_fields_list.append(embed_fields)

    return embed_fields_list


def parse_ctftime_json_long_upgraded(data) -> List[List]:
    if isinstance(data, dict):
        data = [data]
    embed_fields_list = []
    
    for ctf_data in data:
        embed_fields = []
        embed_fields.append(["Time", ctftime_date(data=ctf_data)])    
        embed_fields.append(["Rating weight", ctftime_rating(data=ctf_data)])
        embed_fields.append(["Format", ctftime_format(data=ctf_data)])
        embed_fields.append(["Discord", ctftime_discord_link(data=ctf_data)])
        embed_fields.append(["Credentials", ctftime_cred(data=ctf_data)])
        embed_fields_list.append(embed_fields)

    return embed_fields_list


def parse_ctftime_json_inline(data_list: List, list_fn: List[callable]):
    embed_fields = []
    for data in data_list:
        field_value = ""
        for fn in list_fn:
            field_value += fn(data=data) + "\n"
        fmt = ctftime_format_short(data)
        embed_fields.append([data["title"] + f" {fmt}", field_value])
    return embed_fields


def parse_ctftime_data_1(data: Dict) -> List[List]:
    embed_fields = []
    embed_fields.append(["Time", ctftime_date(data)])    
    embed_fields.append(["Rating weight", ctftime_rating(data=data)])
    embed_fields.append(["Format", ctftime_format(data=data)])
    embed_fields.append(["Discord", ctftime_discord_link(data=data)])
    return embed_fields


def ctftime_cred(data: Dict = None):
    return f"Username: {data['username']}\nPassword: {data['password']}"


def ctftime_date(data: Dict = None):
    start_time = int(datetime.fromisoformat(data["start"]).timestamp())
    finish_time = int(datetime.fromisoformat(data["finish"]).timestamp())

    discord_start_time=f"<t:{start_time}:F>"
    discord_start_time_remaining=f"<t:{start_time}:R>"
    discord_finish_time=f"<t:{finish_time}:F>"
    discord_finish_time_remaining=f"<t:{finish_time}:R>"
    res = f"Start: {discord_start_time} ({discord_start_time_remaining})\nEnd: {discord_finish_time} ({discord_finish_time_remaining})"
    return res


def ctftime_rating(data: Dict = None):
    return data["weight"]


def ctftime_format(data: Dict = None):
    fmat = data["format"]
    if fmat == "Attack-Defense":
        fmat += " ⚔"
    elif fmat == "Hack quest":
        fmat += " 🌄"
    elif fmat == "Jeopardy":
        fmat += " 🎯"

    if data["onsite"] == True:
        fmat += "\nOn-site ✈️: " + data["location"]
    if data["restrictions"] != "Open":
        fmat += "\nRestricted 🔒: " + data["restrictions"]

    return fmat


def ctftime_format_short(data: dict):
    fmat = data["format"]
    if fmat == "Attack-Defense":
        fmat = "⚔"
    elif fmat == "Hack quest":
        fmat = "🌄"
    elif fmat == "Jeopardy":
        fmat = "🎯"

    if data["onsite"] == True:
        fmat += "✈️"
    if data["restrictions"] != "Open":
        fmat += "🔒"

    return fmat


def ctftime_discord_link(data: Dict = None):
    invite_link = re.findall(r"(https://discord.gg/\S+)", data["description"])
    if len(invite_link) != 0:
        return invite_link[0]


def ctftime_contest_name(data: Dict = None):
    return data["title"]


def ctftime_organizers(data: Dict = None):
    orgs = []
    for org in data["organizers"]:
        orgs.append(f"[{org['name']}](https://ctftime.org/team/{org['id']})")
    orgs = ", ".join(orgs)
    return orgs


def ctftime_id(data: Dict = None):
    id_url = f"[{data['id']}]({data['ctftime_url']})"
    return id_url
