from typing import Literal
import discord
from discord import Permissions
import traceback
from redbot.core import Config, commands, app_commands
from redbot.core.bot import Red

from .response import *
from .perm_check import *
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


# TODO: split commands into multiple files
class CtfReg(commands.Cog):

    def __init__(self, bot: Red, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=9854905156701, force_registration=True
        )
        self.config.register_guild(
            ctf_list={},
            ctf_player_role_id=None,
            # all ctf will be created below this category
            ctf_category_location_id=None,
            ctf_quick_contest_category_id=None,
        )


    info_commands = app_commands.Group(
        name="ctf-info", description="CTFTime contest info"
    )
    reg_commands = app_commands.Group(
        name="ctf-reg", description="CTFTime contest registration"
    )
    server_commands = app_commands.Group(
        name="ctf-server", description="This server CTF registration info"
    )
    admin_commands = app_commands.Group(name="ctf-admin", description="Admin commands")
    conf_commands = app_commands.Group(name="ctf-conf", description="Server configuration")

    # dev only
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(name="mass-del")
    async def ctf_mass_del(self, ctx: discord.Interaction):
        """Xóa tất cả thông tin giải CTF trong server"""
        if not ctx.guild.id == 990081200414687314:
            await ctx.response.send_message("This command is only available in the development server")
            return

        list=ctx.guild.categories
        # await ctx.response.defer()
        await ctx.response.send_message(content="Đang xóa tất cả thông tin giải CTF trong server")

        for cate in list:
            if "CTF" in cate.name:
                for ch in cate.channels:
                    await ch.delete()
                await cate.delete()
        for role in ctx.guild.roles:
            if "CTF" in role.name:
                await role.delete()
        await self.config.guild(ctx.guild).ctf_list.clear()

    @conf_commands.command(name="set-ctf-player-role")
    async def ctf_conf_set_ctf_player_role(self, ctx: discord.Interaction, role: discord.Role):
        """Set the role for CTF players"""
        # should use a Response object
        await self.config.guild(ctx.guild).ctf_player_role_id.set(role.id)
        await ctx.response.send_message(f"Set the role for CTF players to <@&{role.id}>")

    @conf_commands.command(name="set-ctf-category-location")
    async def ctf_conf_set_ctf_category_location(self, ctx: discord.Interaction, category: discord.CategoryChannel):
        """Set the location for new CTF categories"""
        await self.config.guild(ctx.guild).ctf_category_location_id.set(category.id)
        await ctx.response.send_message(f"CTF categories will be created below <#{category.id}>")

    @conf_commands.command(name="set-ctf-quick-contest-category")
    async def ctf_conf_set_ctf_quick_contest_category(self, ctx: discord.Interaction, category: discord.CategoryChannel = None):
        """Set the category for quick CTF contests"""
        if category is None:
            category = await ctx.guild.create_category(name="Quick CTF contests")
        
        await self.config.guild(ctx.guild).ctf_quick_contest_category_id.set(category.id)
        await ctx.response.send_message(f"Quick CTF contests will be created in <#{category.id}>")

    @info_commands.command(name="find-id")
    async def ctf_info_find(self, ctx: discord.Interaction, ctftime_id: int):
        """[CTFTime] Tìm thông tin giải CTF theo ID"""
        await try_catch_wrapper(ctx, SearchIdContestResponse, ctftime_id=ctftime_id)

    @info_commands.command(name="find")
    async def ctf_info_find_text(self, ctx: discord.Interaction, ctftime_text: str):
        """[CTFTime] Tìm thông tin giải CTF theo tên"""
        await try_catch_wrapper(
            ctx, SearchTextContestResponse, ctftime_text=ctftime_text
        )

    @info_commands.command(name="ongo")
    async def ctf_info_ongo(
        self, ctx: discord.Interaction, per_page: int = 4, all: bool = False, prize: bool = False
    ):
        """[CTFTime] Xem các CTF đang diễn ra"""
        await try_catch_wrapper(ctx, OngoingContestResponse, per_page=per_page, all=all, prize=prize)

    @info_commands.command(name="upcom")
    async def ctf_info_upcom(
        self,
        ctx: discord.Interaction,
        week: int = 2,
        per_page: int = 4,
        all: bool = False,
        prize: bool = False,
    ):
        """[CTFTime] Xem các CTF sắp diễn ra"""
        await try_catch_wrapper(
            ctx, UpcomingContestResponse, week=week, per_page=per_page, all=all, prize=prize
        )

    @info_commands.command(name="past")
    async def ctf_info_past(
        self,
        ctx: discord.Interaction,
        week: int = 2,
        per_page: int = 4,
        all: bool = False,
        prize: bool = False,
    ):
        """[CTFTime] Xem các CTF đã kết thúc"""
        await try_catch_wrapper(
            ctx, PastContestResponse, week=week, per_page=per_page, all=all, prize=prize
        )

    @reg_commands.command(name="reg")
    @app_commands.checks.bot_has_permissions(manage_channels=True, manage_roles=True)
    @app_commands.check(guild_only)
    async def ctf_reg_register(
        self,
        ctx: discord.Interaction,
        ctf_id: int,
        username: str = None,
        password: str = None,
        url: str = None,
    ):
        """[CTFTime] Đăng ký tham gia CTF"""
        await try_catch_wrapper(
            ctx=ctx,
            func=RegisterContestResponse,
            bot_id=self.bot.application_id,
            ctftime_id=ctf_id,
            username=username,
            password=password,
            url=url,
            conf=await self.get_guild_conf(ctx),
        )

    @reg_commands.command(name="edit-cred")
    @app_commands.check(guild_only)
    async def ctf_reg_edit_cred(
        self,
        ctx: discord.Interaction,
        username: str = None,
        password: str = None,
        url: str = None,
    ):
        """[CTFTime] Chỉnh sửa thông tin đăng nhập"""
        await try_catch_wrapper(
            ctx=ctx,
            func=EditCredResponse,
            bot_id=self.bot.application_id,
            username=username,
            password=password,
            url=url,
            conf=await self.get_guild_conf(ctx),
        )

    @reg_commands.command(name="reg-special")
    async def ctf_reg_register(
        self,
        ctx: discord.Interaction,
        ctf_id: int,
        role: discord.Role,
        name: str,
        url: str,
        uname: str,
        password: str,
    ):
        """Đăng ký tham gia CTF không có trên CTFTime"""
        await Not_Implemented_Response.send(ctx)

    @reg_commands.command(name="unreg")
    async def ctf_reg_unregister(self, ctx: discord.Interaction, ctf_id: int):
        """[CTFTime] Hủy đăng ký tham gia CTF"""
        await Not_Implemented_Response.send(ctx)

    @server_commands.command(name="list")
    async def ctf_server_list(
        self, ctx: discord.Interaction, desc: bool = True, page: int = 1, step: int = 5
    ):
        """List tất cả các giải CTF trong server"""
        await Not_Implemented_Response.send(ctx)

    @server_commands.command(name="show")
    async def ctf_server_show(self, ctx: discord.Interaction, ctf_id: int):
        """Xem thông tin giải CTF trong server"""
        await Not_Implemented_Response.send(ctx)

    @admin_commands.command(name="hide")
    async def ctf_admin_hide(self, ctx: discord.Interaction, ctf_id: int):
        """Ẩn thông tin giải CTF trong server ngay lập tức"""
        await Not_Implemented_Response.send(ctx)

    @admin_commands.command(name="hide-all")
    async def ctf_admin_hide_all(self, ctx: discord.Interaction):
        """Ẩn thông tin tất cả giải CTF trong server ngay lập tức"""
        await Not_Implemented_Response.send(ctx)

    @admin_commands.command(name="show")
    async def ctf_admin_show(self, ctx: discord.Interaction, ctf_id: int):
        """Hiện thông tin giải CTF trong server ngay lập tức"""
        await Not_Implemented_Response.send(ctx)

    @admin_commands.command(name="show-all")
    async def ctf_admin_show_all(self, ctx: discord.Interaction):
        """Hiện thông tin tất cả giải CTF trong server ngay lập tức"""
        await Not_Implemented_Response.send(ctx)

    @admin_commands.command(name="edit")
    async def ctf_admin_edit(
        self,
        ctx: discord.Interaction,
        ctf_id: int,
        field: Literal["name", "desc", "time", "link", "cred"],
        value: str,
    ):
        """Chỉnh sửa thông tin giải CTF trong server"""
        await Not_Implemented_Response.send(ctx)

    @admin_commands.command(name="reg")
    async def ctf_admin_reg(
        self, ctx: discord.Interaction, ctf_id: int, role: discord.Role
    ):
        """[CTFTime] Đăng ký tham gia CTF và quản lý role"""
        await Not_Implemented_Response.send(ctx)

    @admin_commands.command(name="reg-special")
    async def ctf_admin_reg(
        self,
        ctx: discord.Interaction,
        ctf_id: int,
        role: discord.Role,
        name: str,
        url: str,
        uname: str,
        password: str,
    ):
        """Đăng ký tham gia CTF không có trên CTFTime và quản lý role"""
        await Not_Implemented_Response.send(ctx)

    @admin_commands.command(name="delete")
    async def ctf_admin_delete(self, ctx: discord.Interaction, ctf_id: int):
        """Xóa thông tin giải CTF trong server"""
        await Not_Implemented_Response.send(ctx)

    async def get_guild_conf(self, ctx: discord.Interaction):
        return self.config.guild(ctx.guild)


async def try_catch_wrapper(ctx: discord.Interaction, func: callable, **kwargs):
    await Loading_Response.send(ctx)
    try:
        await func(**kwargs).send(ctx)
    except EmptyResultExeption:
        await EmptyResponse().send(ctx)
