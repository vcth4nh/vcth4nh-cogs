from typing import Any, Dict
from redbot.core import Config
import discord

from .ctftime_parser import *
from . import ctftime
from .response_embeded import GeneralEmbed, paginate_embed
from .response_button import *
from .error import *


class GeneralResponse:
    def __init__(self):
        self.embed: GeneralEmbed | List[GeneralEmbed] = discord.utils.MISSING
        self.view: discord.ui.View = discord.utils.MISSING
        # self.completed: bool = False
        self.kwargs: Dict[str, Any] = {}

    async def send(self, ctx: discord.Interaction):
        if type(self.embed) == list:
            embed = self.embed[0]
        else:
            embed = self.embed

        if ctx.response.is_done():
            await ctx.edit_original_response(embed=embed, view=self.view, **self.kwargs)
        else:
            await ctx.response.send_message(embed=embed, view=self.view, **self.kwargs)
        # self.completed = True

    # def __del__(self):
    #     if not self.completed:
    #         ErrorResponse().send()


class SearchIdContestResponse(GeneralResponse):
    def __init__(self, ctftime_id: int):
        super().__init__()

        data = ctftime.find_ctf_by_id(ctftime_id)
        if not data:
            raise EmptyResultExeption()

        list_fields = [ctftime_date, ctftime_format, ctftime_ivlink]
        embed_fields = parse_ctftime_json_long(data, list_fields)[0]

        self.embed = GeneralEmbed().init_attr(
            title=data["title"],
            description=data["url"],
            embed_fields=embed_fields,
            footer=data["ctftime_url"],
            thumbnail=data["logo"],
            color=0xD50000,
        )


class SearchTextContestResponse(GeneralResponse):
    def __init__(self, ctftime_text: str):
        super().__init__()

        data_list = ctftime.find_ctf_by_text(ctftime_text)
        if not data_list:
            raise EmptyResultExeption()

        list_fields = [ctftime_date, ctftime_format, ctftime_ivlink]
        embed_fields_list = parse_ctftime_json_long(data_list, list_fields)

        assert len(data_list) == len(embed_fields_list)
        self.embed = self.paginate(data_list, embed_fields_list)
        self.view = PaginationBtn(self.embed)

    def paginate(self, data_list, embed_fields_list):
        result = []
        for i in range(len(data_list)):
            data = data_list[i]
            embed_fields = embed_fields_list[i]
            result.append(
                GeneralEmbed().init_attr(
                    title=data["title"],
                    description=data["url"],
                    embed_fields=embed_fields,
                    footer=data["ctftime_url"],
                    thumbnail=data["logo"],
                    color=0xD50000,
                )
            )
        return result


class UpOngPastContestResponse(GeneralResponse):
    def __init__(self, title: str, per_page: int = 5):
        super().__init__()
        self.embed_title = title
        self.per_page = per_page
        self.data = None

    def init(self):
        if not self.data:
            raise EmptyResultExeption()
        list_fields = [ctftime_organizers, ctftime_date, ctftime_id]
        embed_fields = parse_ctftime_json_inline(self.data, list_fields)
        self.embed = paginate_embed(
            title=self.embed_title,
            color=0x000000,
            embed_fields=embed_fields,
            per_page=self.per_page,
        )
        self.view = PaginationBtn(self.embed)


class OngoingContestResponse(UpOngPastContestResponse):
    def __init__(self, per_page: int = 5, all: bool = False):
        super().__init__(title="Ongoing contests", per_page=per_page)
        self.data = ctftime.get_ongoing_ctfs(all=all)
        self.init()


class UpcomingContestResponse(UpOngPastContestResponse):
    def __init__(self, week: int = 2, per_page: int = 5, all: bool = False):
        super().__init__(title="Upcomming contests", per_page=per_page)
        self.data = ctftime.get_upcoming_ctfs(weeks=week, all=all)
        self.init()


class PastContestResponse(UpOngPastContestResponse):
    def __init__(self, week: int = 2, per_page: int = 5, all: bool = False):
        super().__init__(title="Past contests", per_page=per_page)
        self.data = ctftime.get_past_ctfs(weeks=week, all=all)
        self.init()


class RegisterContestResponse(GeneralResponse):
    def __init__(self, ctftime_id: int, conf: Config):
        super().__init__()
        data = ctftime.find_ctf_by_id(ctftime_id)
        if not data:
            raise EmptyResultExeption()

        self.data = data
        self.embed = GeneralEmbed().init_attr(
            title=data["title"],
            description=data["url"],
            color=0x000000,
        )
        self.conf = conf

    def send(self, ctx: discord.Interaction):
        super().send(ctx)
        ctx.guild.create_role(name=self.data["title"], color=discord.Color.default())


class LoadingResponse(GeneralResponse):
    def __init__(self):
        super().__init__()
        self.embed = GeneralEmbed(title="Đợi chút...", color=0x000000)


class EmptyResponse(GeneralResponse):
    def __init__(self):
        super().__init__()
        self.embed = GeneralEmbed(
            title="Error", description="Không thấy j hết...", color=0x000000
        )


class ErrorResponse(GeneralResponse):
    def __init__(self, **kwargs):
        super().__init__()
        self.embed = GeneralEmbed(
            title=kwargs.get("title", "Error"),
            description=kwargs.get("description", "Some error occurred"),
            color=kwargs.get("color", 0x000000),
        )
