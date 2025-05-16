from typing import Any, Dict, List
from redbot.core.config import Group
import discord

from .ctftime_parser import *
from . import ctftime
from .response_embeded import GeneralEmbed, paginate_embed
from .response_button import *
from .error import *
from .utils import *

import logging
logger = logging.getLogger(__name__)


class GeneralResponse:
    def __init__(self):
        self.embed: GeneralEmbed | List[GeneralEmbed] = discord.utils.MISSING
        self.view: discord.ui.View = discord.utils.MISSING
        # self.completed: bool = False
        # self.kwargs: Dict[str, Any] = {}

    async def send(self, ctx: discord.Interaction):
        if ctx.response.is_done():
            await self.edit_message(ctx, self.embed, self.view)
        else:
            await self.send_message(ctx, self.embed, self.view)
        # self.completed = True

    async def send_message(
        self, ctx: discord.Interaction, embed: discord.Embed, view: discord.ui.View
    ):
        # TODO: clean up the code
        if type(embed) == list:
            await ctx.response.send_message(embed=embed[0], view=view)
        else:
            await ctx.response.send_message(embed=embed, view=view)

    async def edit_message(
        self, ctx: discord.Interaction, embed: discord.Embed, view: discord.ui.View
    ):
        if type(embed) == list:
            await ctx.edit_original_response(embed=embed[0], view=view)
        else:
            await ctx.edit_original_response(embed=embed, view=view)


class SearchIdContestResponse(GeneralResponse):
    def __init__(self, ctftime_id: int):
        super().__init__()

        data = ctftime.find_ctf_by_id(ctftime_id)
        if not data:
            raise EmptyResultExeption()

        embed_fields = parse_ctftime_data_search(data)

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

        embed_fields_list = []
        for data in data_list:
            embed_fields = parse_ctftime_data_search(data)
            embed_fields_list.append(embed_fields)

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
        # return make_chunks(result, 2)


class UpOngPastContestResponse(GeneralResponse):
    def __init__(self, title: str, per_page: int = 5, prize: bool = False):
        super().__init__()
        self.embed_title = title
        self.per_page = per_page
        self.data = None
        self.prize = prize

    def init(self):
        if not self.data:
            raise EmptyResultExeption()
        embed_fields = parse_ctftime_data_list(self.data, prize=self.prize)
        self.embed = paginate_embed(
            title=self.embed_title,
            color=0x000000,
            embed_fields=embed_fields,
            per_page=self.per_page,
        )
        self.view = PaginationBtn(self.embed)


class OngoingContestResponse(UpOngPastContestResponse):
    def __init__(self, per_page: int = 5, all: bool = True, prize: bool = False):
        super().__init__(title="Ongoing contests", per_page=per_page, prize=prize)
        self.data = ctftime.get_ongoing_ctfs(all=all)
        self.init()


class UpcomingContestResponse(UpOngPastContestResponse):
    def __init__(self, week: int = 2, per_page: int = 5, all: bool = True, prize: bool = False):
        super().__init__(title="Upcomming contests", per_page=per_page, prize=prize)
        self.data = ctftime.get_upcoming_ctfs(weeks=week, all=all)
        self.init()


class PastContestResponse(UpOngPastContestResponse):
    def __init__(self, week: int = 2, per_page: int = 5, all: bool = True, prize: bool = False):
        super().__init__(title="Past contests", per_page=per_page, prize=prize)
        self.data = ctftime.get_past_ctfs(weeks=week, all=all)
        self.init()


class RegisterContestResponse(GeneralResponse):
    def __init__(
        self,
        conf: Group,
        ctftime_id: int,
        username: str = None,
        password: str = None,
        bot_id: int = None,
        url: str = None,
        quick: bool = False,
    ):
        super().__init__()
        self.quick = quick
        data = ctftime.find_ctf_by_id(ctftime_id)
        if not data:
            raise EmptyResultExeption()

        self.data = data
        self.conf = conf
        if url is not None:
            data["credentials"] = {
                "url": url
            }
        elif username is not None or password is not None:
            data["credentials"] = {
                "username": username,
                "password": password
            }
        self.bot_id = bot_id
        
        embed_fields = parse_ctftime_data_reg(data)
        logger.debug(f"embed_fields: {embed_fields}")
        self.ctf_data_embed = GeneralEmbed().init_attr(
            title=data["title"],
            description=data["url"],
            embed_fields=embed_fields,
            footer=data['ctftime_url'],
            thumbnail=data["logo"],
            color=0xD50000,
        )
        self.embed = Error_CTF_General_Response.embed

        logger.debug(f"self: {self.__dict__}")

    async def check_exist(self, ctf_list: dict):
        if ctf_list.get(str(self.data["id"])) is not None:
            logger.debug(f"ctf_list: {ctf_list}")
            self.embed = ErrorCTFRegExistResponse(ctf_list[str(self.data["id"])]["info_ch"]).embed
            raise CTFRegExistExeption()

    async def prepare_roles(self, ctx: discord.Interaction, role_id: int) -> List[discord.Role]:
        contest_role = await ctx.guild.create_role(
            name=f"CTF - {self.data['title']}", mentionable=True
        )
        if role_id:
            ctf_player_role = ctx.guild.get_role(role_id)
            return [contest_role, ctf_player_role]
        return [contest_role]

    async def edit_category_location(self, cate: discord.CategoryChannel, ctx: discord.Interaction):
        category_position = 0

        quick_ctf_category_id = await self.conf.ctf_quick_contest_category_id()
        if quick_ctf_category_id is not None:
            category_location : discord.CategoryChannel = ctx.guild.get_channel(quick_ctf_category_id)
        else:
            category_location_id = await self.conf.ctf_category_location_id()
            category_location : discord.CategoryChannel = ctx.guild.get_channel(category_location_id)
        
        if category_location is not None:
            category_position = category_location.position + 1

        logger.info(f"Moving category to {category_position}")    
        await cate.edit(position=category_position)



    async def create_category(self, roles: List[discord.Role], ctx: discord.Interaction):

        logger.info(f"Creating category {self.data['title']}")
        cate = await ctx.guild.create_category(name=self.data["title"])
        await self.edit_category_location(cate, ctx)

        logger.info(f"Setting permissions for {self.bot_id}")
        await cate.set_permissions(
            ctx.guild.get_member(self.bot_id),
            read_messages=True,
            send_messages=True,
        )

        logger.info(f"Setting default everyone permissions for {cate.name}")
        await cate.set_permissions(ctx.guild.default_role, read_messages=False)

        for role in roles:
            logger.info(f"Setting {role.name} permissions for {cate.name}")
            await cate.set_permissions(role, read_messages=True, send_messages=True)
        
        logger.info(f"Creating channels for {cate.name}")
        info = await cate.create_text_channel(name="info")
        info_msg = await info.send(embed=self.ctf_data_embed)
        await cate.create_text_channel(name="web")
        await cate.create_text_channel(name="crypto")
        await cate.create_text_channel(name="pwn")
        await cate.create_text_channel(name="rev")
        await cate.create_text_channel(name="misc")

        return cate, info, info_msg

    async def send(self, ctx: discord.Interaction):
        try:
            ctf_list: dict = await self.conf.ctf_list()
            await self.check_exist(ctf_list)
            logger.debug(f"ctf_list: {ctf_list}")
            logger.debug(f"self.data: {self.data}")
            if not self.quick:
                logger.info(f"Creating full category for {self.data['title']}")
                role_lists = await self.prepare_roles(ctx, await self.conf.ctf_player_role_id())
                cate, info, info_msg = await self.create_category(role_lists, ctx)
            else:
                logger.info(f"Creating channel in quick category for {self.data['title']}")
                quick_ctf_category_id = await self.conf.ctf_quick_contest_category_id()
                cate = ctx.guild.get_channel(quick_ctf_category_id)
                info = await cate.create_text_channel(name=self.data["title"][:60])
                await info.edit(position=0)
                info_msg = await info.send(embed=self.ctf_data_embed)

            if self.data['prizes']:
                await info.send(f"```{self.data['prizes']}```")
            ctf_data = CTFRegData(
                id=self.data["id"],
                # get the role that just created
                role=role_lists[0].id if not self.quick else None,
                cate=cate.id if not self.quick else None,
                name=self.data["title"],
                info_msg=info_msg.id,
                info_ch=info.id,
                finish=self.data["finish"],
                archived=False,
            )

            ctf_list.update(ctf_data.generate())
            await self.conf.ctf_list.set(ctf_list)

            self.embed = GeneralEmbed(
                title="Xong!",
                description=f'Đã tạo channel cho <***{self.data["title"]}***> ở <#{info.id}>',
                color=0x03AC13,
            )
        except CTFRegExistExeption:
            pass
        finally:
            await super().send(ctx)

class EditCredResponse(GeneralResponse):
    def __init__(
        self,
        conf: Group,
        username: str = None,
        password: str = None,
        url: str = None,
        bot_id: int = None,
    ):
        super().__init__()
        self.error = False
        if username is None and password is None and url is None:
            self.embed = ErrorResponse(title="Lỗi", description="Không có thông tin để chỉnh sửa").embed
            self.error = True
            return

        self.conf = conf
        self.username = username
        self.password = password
        self.url = url
        self.embed = Error_CTF_General_Response.embed
    
    async def send(self, ctx):
        if self.error:
            await super().send(ctx)
            return

        ctf_list: dict = await self.conf.ctf_list()
        target_ctf_id=search_ctf_info_ch_from_db(ctf_list, ctx.channel.id)

        if target_ctf_id is None:
            self.embed = Error_CTF_General_Response.embed
            await super().send(ctx)
            return
        
        self.embed = GeneralEmbed(
            title="Xong!",
            description=f'Đã cập nhật thông tin đăng nhập cho <***{ctf_list[target_ctf_id]["name"]}***>',
            color=0x03AC13,
        )

        msg = await ctx.channel.fetch_message(ctf_list[target_ctf_id]["info_msg"])
        embed=msg.embeds[0]
        logger.debug(f"embed: {id(embed)}")
        logger.debug(f"msg.embeds[0]: {id(msg.embeds[0])}")
        for i, field in enumerate(embed.fields):
            if field.name == "Credentials":
                embed.remove_field(i)
                break

        if self.url is not None:
            value=f"Team URL: {self.url}"
        else:
            value=f"Username: {self.username}\nPassword: {self.password}"

        embed.add_field(name="Credentials", value=value)

        await msg.edit(embed=embed)
        await super().send(ctx)

class DeleteContestResponse(GeneralResponse):
    def __init__(self, conf: Group, ctftime_id: int):
        super().__init__()
        self.conf = conf
        self.ctftime_id = ctftime_id
    
    async def send(self, ctx):
        ctf_list: dict = await self.conf.ctf_list()
        print(f"ctf_list: {ctf_list}")
        if self.ctftime_id:
            logger.info(f"Searching for ctf_id {self.ctftime_id} in the database")
            target_ctf_id=search_ctf_id_from_db(ctf_list, self.ctftime_id)
        else:
            logger.info(f"Searching for ctf_id corresponding to channel {ctx.channel.id} in the database")
            cate_id=ctx.channel.category.id
            quick_ctf_category_id = await self.conf.ctf_quick_contest_category_id()
            print(type(quick_ctf_category_id))
            logger.info(f"quick_ctf_category_id: {quick_ctf_category_id}")
            logger.info(f"cate_id: {cate_id}")
            logger.info(f"str(cate_id) == str(quick_ctf_category_id): {cate_id == quick_ctf_category_id}")
            if quick_ctf_category_id is None or cate_id != quick_ctf_category_id:
                logger.info(f"Searching for ctf_id corresponding to category {cate_id} in the database")
                target_ctf_id=search_ctf_cate_id_from_db(ctf_list, cate_id)
            else:
                logger.info(f"Searching for ctf_id corresponding to channel {ctx.channel.id} in the database")
                target_ctf_id=search_ctf_info_ch_from_db(ctf_list, ctx.channel.id)

        logger.debug(f"target_ctf_id: {target_ctf_id}")
        if target_ctf_id is None:
            self.embed = Error_CTF_General_Response.embed
            await super().send(ctx)
            return
        


        if ctf_list[target_ctf_id]["cate"]:
            logger.info(f"Deleting category {ctf_list[target_ctf_id]['name']}")
            cate = ctx.guild.get_channel(ctf_list[target_ctf_id]["cate"])
            if cate is not None:
                for ch in cate.channels:
                    await ch.delete()
                await cate.delete()
            role = ctx.guild.get_role(ctf_list[target_ctf_id]["role"])
            if role is not None:
                await role.delete()
        else:
            logger.info(f"Deleting channel {ctf_list[target_ctf_id]['name']}")
            info_ch = ctx.guild.get_channel(ctf_list[target_ctf_id]["info_ch"])
            await info_ch.delete()
        
        logger.info(f"Deleting {target_ctf_id} from ctf_list")
        ctf_list.pop(target_ctf_id, None)
        await self.conf.ctf_list.set(ctf_list)
        logger.debug(f"ctf_list: {ctf_list}")


class LoadingResponse(GeneralResponse):
    def __init__(self):
        super().__init__()
        self.embed = GeneralEmbed(title="Đợi chút...", color=0x000000)


class ErrorResponse(GeneralResponse):
    def __init__(self, **kwargs):
        super().__init__()
        self.embed = GeneralEmbed(
            title=kwargs.get("title", "Error"),
            description=kwargs.get("description", "Some error occurred"),
            color=kwargs.get("color", discord.Color.red()),
        )


class EmptyResponse(GeneralResponse):
    def __init__(self):
        super().__init__()
        self.embed = GeneralEmbed(title="Không thấy kết quả", color=0x000000)


class ErrorCTFRegExistResponse(ErrorResponse):
    def __init__(self, channel_id:str):
        super().__init__(description=f"CTF đã được đăng ký ở <#{channel_id}>")


class ErrorCTFGeneralResponse(ErrorResponse):
    def __init__(self):
        super().__init__(description="Không thể hoàn thành reg CTF")

class NotImplementedResponse(ErrorResponse):
    def __init__(self):
        super().__init__()
        self.embed = GeneralEmbed(title="Chức năng chưa được triển khai...", color=0x000000)


Loading_Response = LoadingResponse()
Not_Implemented_Response = NotImplementedResponse()
# Error_CTF_Exist_Response = ErrorCTFRegExistResponse()
Error_CTF_General_Response = ErrorCTFGeneralResponse()
