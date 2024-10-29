from typing import Literal, ClassVar
import discord
import traceback
from redbot.core import Config, commands, app_commands

from .response import *

Loading_Response = LoadingResponse()


# TODO: split commands into multiple files
class CtfReg(commands.Cog):

    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=985490701, force_registration=True
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
        self, ctx: discord.Interaction, per_page: int = 5, all: bool = False
    ):
        """[CTFTime] Xem các CTF đang diễn ra"""
        await try_catch_wrapper(ctx, OngoingContestResponse, per_page=per_page, all=all)

    @info_commands.command(name="upcom")
    async def ctf_info_upcom(
        self,
        ctx: discord.Interaction,
        week: int = 2,
        per_page: int = 5,
        all: bool = False,
    ):
        """[CTFTime] Xem các CTF sắp diễn ra"""
        await try_catch_wrapper(
            ctx, UpcomingContestResponse, week=week, per_page=per_page, all=all
        )

    @info_commands.command(name="past")
    async def ctf_info_past(
        self,
        ctx: discord.Interaction,
        week: int = 2,
        per_page: int = 5,
        all: bool = False,
    ):
        """[CTFTime] Xem các CTF đã kết thúc"""
        await try_catch_wrapper(
            ctx, PastContestResponse, week=week, per_page=per_page, all=all
        )

    @reg_commands.command(name="reg")
    async def ctf_reg_register(
        self,
        ctx: discord.Interaction,
        ctf_id: int,
        username: str = None,
        password: str = None,
    ):
        """[CTFTime] Đăng ký tham gia CTF"""
        await try_catch_wrapper(
            ctx,
            RegisterContestResponse,
            ctftime_id=ctf_id,
            username=username,
            password=password,
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
        await Loading_Response.send(ctx)

    @reg_commands.command(name="unreg")
    async def ctf_reg_unregister(self, ctx: discord.Interaction, ctf_id: int):
        """[CTFTime] Hủy đăng ký tham gia CTF"""
        await Loading_Response.send(ctx)

    @reg_commands.command(name="edit-cred")
    async def ctf_reg_add_cred(
        self, ctx: discord.Interaction, uname: str, password: str
    ):
        """[CTFTime] Thêm thông tin đăng nhập"""
        await Loading_Response.send(ctx)

    @server_commands.command(name="list")
    async def ctf_server_list(
        self, ctx: discord.Interaction, desc: bool = True, page: int = 1, step: int = 5
    ):
        """List tất cả các giải CTF trong server"""
        await Loading_Response.send(ctx)

    @server_commands.command(name="show")
    async def ctf_server_show(self, ctx: discord.Interaction, ctf_id: int):
        """Xem thông tin giải CTF trong server"""
        await Loading_Response.send(ctx)

    @admin_commands.command(name="hide")
    async def ctf_admin_hide(self, ctx: discord.Interaction, ctf_id: int):
        """Ẩn thông tin giải CTF trong server ngay lập tức"""
        await Loading_Response.send(ctx)

    @admin_commands.command(name="hide-all")
    async def ctf_admin_hide_all(self, ctx: discord.Interaction):
        """Ẩn thông tin tất cả giải CTF trong server ngay lập tức"""
        await Loading_Response.send(ctx)

    @admin_commands.command(name="show")
    async def ctf_admin_show(self, ctx: discord.Interaction, ctf_id: int):
        """Hiện thông tin giải CTF trong server ngay lập tức"""
        await Loading_Response.send(ctx)

    @admin_commands.command(name="show-all")
    async def ctf_admin_show_all(self, ctx: discord.Interaction):
        """Hiện thông tin tất cả giải CTF trong server ngay lập tức"""
        await Loading_Response.send(ctx)

    @admin_commands.command(name="edit")
    async def ctf_admin_edit(
        self,
        ctx: discord.Interaction,
        ctf_id: int,
        field: Literal["name", "desc", "time", "link", "cred"],
        value: str,
    ):
        """Chỉnh sửa thông tin giải CTF trong server"""
        await Loading_Response.send(ctx)

    @admin_commands.command(name="reg")
    async def ctf_admin_reg(
        self, ctx: discord.Interaction, ctf_id: int, role: discord.Role
    ):
        """[CTFTime] Đăng ký tham gia CTF và quản lý role"""
        await Loading_Response.send(ctx)

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
        await Loading_Response.send(ctx)

    @admin_commands.command(name="delete")
    async def ctf_admin_delete(self, ctx: discord.Interaction, ctf_id: int):
        """Xóa thông tin giải CTF trong server"""
        await Loading_Response.send(ctx)


async def try_catch_wrapper(ctx: discord.Interaction, func: callable, **kwargs):

    await Loading_Response.send(ctx)
    try:
        await func(**kwargs).send(ctx)
    except EmptyResultExeption:
        traceback.print_exc()
        await EmptyResponse().send(ctx)
