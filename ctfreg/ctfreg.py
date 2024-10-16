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

    reg_commands = app_commands.Group(
        name="ctf-reg", description="CTFTime contest registration"
    )
    info_commands = app_commands.Group(
        name="ctf-info", description="CTFTime contest info"
    )

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
        if embed_var:
            await ctx.edit_original_response(embed=embed_var)
        else:
            await ctx.edit_original_response(embed=ErrorEmbed())

    # @info_commands.command(name="ongoing")
    # async def ctf_info_ongo(self, ctx: commands.Context):
    #     """[CTFTime] Xem các CTF đang diễn ra"""
    #     await ctx.send(embed=LoadingEmbed())
    #
    #     embed_var = ctftime.getOngoCTF(limit_EventDuration=True)
    #     if embed_var:
    #         await ctx.edit_original_response(
    #             embed=embed_var, view=Buttons.ShowOngoAll()
    #         )
    #     else:
    #         await ctx.edit_original_response(embed=ErrorEmbed())
    #
    # @info_commands.command(name="ongoing")
    # async def upco(self, ctx: commands.Context, page: int = 1, step: int = 3):
    #     """[CTFTime] Xem các CTF sắp diễn ra"""
    #     page -= 1
    #     await ctx.response.send_message(embed=LoadingEmbed())
    #     embed_var, npage = ctftime.getUpcoCTF(page=page, step=step)
    #     if embed_var:
    #         await ctx.edit_original_response(
    #             embed=embed_var,
    #             view=Buttons.ShowUpcoPages(page=page, step=step, npage=npage),
    #         )
    #     else:
    #         await ctx.edit_original_response(embed=ErrorEmbed())
