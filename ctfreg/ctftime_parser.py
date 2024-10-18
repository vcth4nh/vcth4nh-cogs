import datetime
import re

import pytz
from typing import List


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


def parse_ctftime_json_long(data: dict, list_fn: List[callable]):
    if type(data) == dict:
        data = [data]

    embed_fields = []
    for fn in list_fn:
        fn(embed_fields, data)

    return embed_fields


def parse_ctftime_json_short(data: List, list_fn: List[callable]):
    if type(data) == dict:
        data = [data]

    embed_fields = []
    for item in data:
        field_value = ""
        for fn in list_fn:
            field_value += fn({}, item) + "\n"
        embed_fields.append({data["title"]: field_value})
    return embed_fields


def ctftime_cred(data):
    pass


def ctftime_date(embed_fields: List, data):
    start_time = datetime.datetime.fromisoformat(data["start"])
    start_time = start_time.astimezone(pytz.timezone("Asia/Bangkok"))
    end_time = start_time + datetime.timedelta(
        days=data["duration"]["days"], hours=data["duration"]["hours"]
    )

    formatted_start_time = start_time.strftime("%I:%M %p %m/%d/%Y %Z")
    formatted_end_time = end_time.strftime("%I:%M %p %m/%d/%Y %Z")

    res = f"Start: {formatted_start_time}\nEnd: {formatted_end_time}"
    embed_fields.append(["Time", res])
    return res


def ctftime_rating(embed_fields: List, data):
    embed_fields.append(["Rating weight", data["weight"]])
    return data["weight"]


def ctftime_format(embed_fields: List, data):
    fmat = data["format"]
    if fmat == "Attack-Defense":
        fmat += " ⚔"
    elif fmat == "Hack quest":
        fmat += " 🌄"
    elif fmat == "Jeopardy":
        fmat += " 🎯"

    if data["onsite"] == True:
        fmat += "\nOn-site: " + data["location"]
    if data["restrictions"] != "Open":
        fmat += "\nRestricted (" + data["restrictions"] + ")"

    embed_fields.append(["Format", fmat])
    return fmat


def ctftime_ivlink(embed_fields: List, data):
    invite_link = re.findall(r"(https://discord.gg/\S+)", data["description"])
    if len(invite_link) != 0:
        embed_fields.append(["Discord", invite_link[0]])
        return invite_link[0]


def ctftime_contest_name(embed_fields: List, data):
    embed_fields.append(["Contest name", data["title"]])
    return data["title"]
