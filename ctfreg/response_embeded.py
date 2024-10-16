from discord import Embed

from . import ctftime
from .ctftime_parser import *


class GeneralEmbed(Embed):
    # TODO: change fields and values to dict
    def __init__(self):
        super().__init__()
        # self.init_attr()

    def init_attr(
        self,
        title=None,
        description=None,
        color=0xFCBA03,
        embed_fields: dict = None,
        timestamp=None,
        footer=None,
        thumbnail=None,
    ):
        self.title = title
        self.description = description
        self.color = color
        self.timestamp = timestamp
        if footer is not None:
            self.set_footer(text=footer)
        if thumbnail is not None:
            self.set_thumbnail(url=thumbnail)
        for name, value in embed_fields.items():
            self.add_field(name=name, value=value, inline=False)


class SearchContestEmbed(GeneralEmbed):
    def __init__(self, ctftime_id: int):
        super().__init__()
        data = ctftime.find_ctf_by_id(ctftime_id)
        if not data:
            return ErrorNotFoundEmbed()
        list_fields = [ctftime_date, ctftime_format, ctftime_ivlink]
        embed_fields = parse_ctftime_json(data, list_fields)
        self.init_attr(
            title=data["title"],
            description=data["url"],
            embed_fields=embed_fields,
            footer=data["ctftime_url"],
            thumbnail=data["logo"],
            color=0xD50000,
        )

class ListOngoingEmbed(GeneralEmbed):
    def __init__(self):
        super().__init__()
        

class ErrorNotFoundEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__()

        self.title = kwargs.get("title", "Error")
        self.description = kwargs.get("description", "Không thấy j hết...")
        self.color = kwargs.get("color", 0x000000)


class ErrorEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__()

        self.title = kwargs.get("title", "Error")
        self.description = kwargs.get("description", "Some error occurred")
        self.color = kwargs.get("color", 0x000000)


class LoadingEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__()

        self.title = kwargs.get("title", "Đợi chút...")
        self.color = kwargs.get("color", 0xFEE12B)
