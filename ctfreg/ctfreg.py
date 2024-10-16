from typing import Literal
import discord
from redbot.core import Config, commands, app_commands

from .response_embeded import *
from . import ctftime


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

    # @commands.hybrid_group(name="ctf-reg", description="CTFTime contest registration")
    # async def reg_commands(self, ctx: commands.Context):
    #     # if ctx.invoked_subcommand is None:
    #     #     await ctx.send_help(ctx.command)
    #     pass
    #
    # @commands.hybrid_group(name="ctf-info", description="CTFTime contest info")
    # async def info_commands(self, ctx: commands.Context):
    #     # if ctx.invoked_subcommand is None:
    #     #     await ctx.send_help(ctx.command)
    #     pass

    # TODO: use search_id and search_text var
    @info_commands.command(name="find")
    async def ctf_info_find(self, ctx: discord.Interaction, search_key: str):
        """[CTFTime] Tìm thông tin giải CTF"""
        await ctx.response.send_message(embed=LoadingEmbed())

        # if numeric then search by id
        if search_key.isnumeric():
            ctftime_id = int(search_key)
        else:
            ctftime_id = ctftime.find_ctf_by_text(search_key)

        # GET info
        embed_var = SearchContestEmbed(ctftime_id)
        ctx.edit_original_response(embed=embed_var)

    @info_commands.command(name="ongo")
    async def ctf_info_ongo(self, ctx: discord.Interaction):
        """[CTFTime] Xem các CTF đang diễn ra"""
        await ctx.response.send_message(embed=LoadingEmbed())

    @info_commands.command(name="upcom")
    async def ctf_info_upcom(self, ctx: discord.Interaction):
        """[CTFTime] Xem các CTF sắp diễn ra"""
        await ctx.response.send_message(embed=LoadingEmbed())

    @info_commands.command(name="past")
    async def ctf_info_past(self, ctx: discord.Interaction):
        """[CTFTime] Xem các CTF đã kết thúc"""
        await ctx.response.send_message(embed=LoadingEmbed())

    @reg_commands.command(name="reg")
    async def ctf_reg_register(self, ctx: discord.Interaction, ctf_id: int):
        """[CTFTime] Đăng ký tham gia CTF"""
        await ctx.response.send_message(embed=LoadingEmbed())

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
        await ctx.response.send_message(embed=LoadingEmbed())

    @reg_commands.command(name="unreg")
    async def ctf_reg_unregister(self, ctx: discord.Interaction, ctf_id: int):
        """[CTFTime] Hủy đăng ký tham gia CTF"""
        await ctx.response.send_message(embed=LoadingEmbed())

    @reg_commands.command(name="edit-cred")
    async def ctf_reg_add_cred(
        self, ctx: discord.Interaction, uname: str, password: str
    ):
        """[CTFTime] Thêm thông tin đăng nhập"""
        await ctx.response.send_message(embed=LoadingEmbed())

    @server_commands.command(name="list")
    async def ctf_server_list(
        self, ctx: discord.Interaction, desc: bool = True, page: int = 1, step: int = 5
    ):
        """List tất cả các giải CTF trong server"""
        await ctx.response.send_message(embed=LoadingEmbed())

    @server_commands.command(name="show")
    async def ctf_server_show(self, ctx: discord.Interaction, ctf_id: int):
        """Xem thông tin giải CTF trong server"""
        await ctx.response.send_message(embed=LoadingEmbed())

    @admin_commands.command(name="hide")
    async def ctf_admin_hide(self, ctx: discord.Interaction, ctf_id: int):
        """Ẩn thông tin giải CTF trong server ngay lập tức"""
        await ctx.response.send_message(embed=LoadingEmbed())

    @admin_commands.command(name="hide-all")
    async def ctf_admin_hide_all(self, ctx: discord.Interaction):
        """Ẩn thông tin tất cả giải CTF trong server ngay lập tức"""
        await ctx.response.send_message(embed=LoadingEmbed())

    @admin_commands.command(name="show")
    async def ctf_admin_show(self, ctx: discord.Interaction, ctf_id: int):
        """Hiện thông tin giải CTF trong server ngay lập tức"""
        await ctx.response.send_message(embed=LoadingEmbed())

    @admin_commands.command(name="show-all")
    async def ctf_admin_show_all(self, ctx: discord.Interaction):
        """Hiện thông tin tất cả giải CTF trong server ngay lập tức"""
        await ctx.response.send_message(embed=LoadingEmbed())

    @admin_commands.command(name="edit")
    async def ctf_admin_edit(
        self,
        ctx: discord.Interaction,
        ctf_id: int,
        field: Literal["name", "desc", "time", "link", "cred"],
        value: str,
    ):
        """Chỉnh sửa thông tin giải CTF trong server"""
        await ctx.response.send_message(embed=LoadingEmbed())

    @admin_commands.command(name="reg")
    async def ctf_admin_reg(
        self, ctx: discord.Interaction, ctf_id: int, role: discord.Role
    ):
        """[CTFTime] Đăng ký tham gia CTF và quản lý role"""
        await ctx.response.send_message(embed=LoadingEmbed())

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
        await ctx.response.send_message(embed=LoadingEmbed())

    @admin_commands.command(name="delete")
    async def ctf_admin_delete(self, ctx: discord.Interaction, ctf_id: int):
        """Xóa thông tin giải CTF trong server"""
        await ctx.response.send_message(embed=LoadingEmbed())