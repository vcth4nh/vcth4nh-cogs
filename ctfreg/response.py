from typing import Any
import discord

from .ctftime_parser import *
from . import ctftime
from .response_embeded import GeneralEmbed, paginate_embed
from .response_button import *


class GeneralResponse:
    def __init__(self):
        self.embed: GeneralEmbed | List[GeneralEmbed] = discord.utils.MISSING
        self.view: discord.ui.View = discord.utils.MISSING
        # self.completed: bool = False
        self.kwargs: dict[str, Any] = {}

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


class SearchContestResponse(GeneralResponse):
    def __init__(self, ctftime_id: int):
        super().__init__()
        data = ctftime.find_ctf_by_id(ctftime_id)
        # TODO: Wrong
        # if not data:
        #     return ErrorNotFoundResponse()
        self.embed = GeneralEmbed()

        list_fields = [ctftime_date, ctftime_format, ctftime_ivlink]
        embed_fields = parse_ctftime_json_long(data, list_fields)

        self.embed.init_attr(
            title=data["title"],
            description=data["url"],
            embed_fields=embed_fields,
            footer=data["ctftime_url"],
            thumbnail=data["logo"],
            color=0xD50000,
        )


class OngoingContestResponse(GeneralResponse):
    def __init__(self, per_page: int = 5, all: bool = False):
        super().__init__()
        data = ctftime.get_ongoing_ctfs(all=all)
        # TODO: Wrong
        # if not data:
        #     return ErrorNotFoundResponse()
        list_fields = [ctftime_date, ctftime_format]
        embed_fields = parse_ctftime_json_inline(data, list_fields)

        self.embed = paginate_embed(
            title="Ongoing contests",
            color=0x000000,
            embed_fields=embed_fields,
            per_page=per_page,
        )

        print(self.embed)
        self.view = PaginationBtn(self.embed)


class UpOrPastContestResponse(GeneralResponse):
    def __init__(self, title: str, per_page: int = 5):
        super().__init__()
        self.embed_title = title
        self.per_page = per_page
        self.data = None

    def init(self):
        list_fields = [ctftime_date, ctftime_organizers]
        embed_fields = parse_ctftime_json_inline(self.data, list_fields)
        self.embed = paginate_embed(
            title=self.embed_title,
            color=0x000000,
            embed_fields=embed_fields,
            per_page=self.per_page,
        )
        print(self.embed)
        self.view = PaginationBtn(self.embed)


class UpcomingContestResponse(UpOrPastContestResponse):
    def __init__(self, week: int = 2, per_page: int = 5, all: bool = False):
        super().__init__(title="Upcomming contests", per_page=per_page)
        self.data = ctftime.get_upcoming_ctfs(weeks=week, all=all)
        self.init()

class PastContestResponse(UpOrPastContestResponse):
    def __init__(self, week: int = 2, per_page: int = 5, all: bool = False):
        super().__init__(title="Past contests", per_page=per_page)
        self.data = ctftime.get_past_ctfs(weeks=week, all=all)
        self.init()


class LoadingResponse(GeneralResponse):
    def __init__(self):
        super().__init__()
        self.embed = GeneralEmbed(title="Đợi chút ...", color=0x000000)


class EmptyResponse(GeneralResponse):
    def __init__(self, **kwargs):
        super().__init__()
        self.embed = GeneralEmbed(title="Empty", color=0x000000)
        if kwargs:
            self.embed.init_attr(**kwargs)


class ErrorResponse(GeneralResponse):
    def __init__(self, **kwargs):
        super().__init__()
        self.embed = GeneralEmbed(
            title=kwargs.get("title", "Error"),
            description=kwargs.get("description", "Some error occurred"),
            color=kwargs.get("color", 0x000000),
        )


class ErrorNotFoundResponse(ErrorResponse):
    def __init__(self):
        super().__init__(title="Error", description="Không thấy j hết...")
