import datetime
import re

import pytz
from typing import List


def parse_ctftime_json(data: dict = None, list_fn: List[callable] = None):
    embed_fields = {}
    for fn in list_fn:
        fn(embed_fields, data)

    return embed_fields


def ctftime_login(data):
    pass


def ctftime_date(embed_fields, data):
    start_time = datetime.datetime.fromisoformat(data["start"])
    start_time = start_time.astimezone(pytz.timezone("Asia/Bangkok"))
    end_time = start_time + datetime.timedelta(
        days=data["duration"]["days"], hours=data["duration"]["hours"]
    )

    formatted_start_time = start_time.strftime("%I:%M %p %m/%d/%Y %Z")
    formatted_end_time = end_time.strftime("%I:%M %p %m/%d/%Y %Z")

    embed_fields.update(
        {
            "Time": f"Start: {formatted_start_time}\nEnd: {formatted_end_time}",
            "Rating weight": data["weight"],
        }
    )


def ctftime_format(embed_fields, data):
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

    embed_fields["Format"] = fmat


def ctftime_ivlink(embed_fields, data):
    invite_link = re.findall(r"(https://discord.gg/\S+)", data["description"])
    if len(invite_link) != 0:
        embed_fields["Discord"] = invite_link[0]
