from typing import List
import discord
from .response_embeded import GeneralEmbed


class GeneralButton(discord.ui.View):
    def __init__(self, timeout=3600):
        super().__init__(timeout=timeout)


class PaginationBtn(GeneralButton):
    def __init__(self, embed_list: List[discord.Embed]):
        super().__init__()
        self.embed_list = embed_list
        self.total_page = len(embed_list)
        self.current_page = 0
        if self.total_page == 1:
            self.prev_btn.disabled = True
            self.next_btn.disabled = True

        self.change_page(page=0)

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def prev_btn(self, ctx: discord.Interaction, btn: discord.ui.Button):
        self.change_page(page=self.current_page - 1)
        await ctx.response.edit_message(
            embed=self.embed_list[self.current_page], view=self
        )

    @discord.ui.button(label="0/0", style=discord.ButtonStyle.grey, disabled=True)
    async def page_number(self):
        pass

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next_btn(self, ctx: discord.Interaction, btn: discord.ui.Button):
        self.change_page(page=self.current_page + 1)
        await ctx.response.edit_message(
            embed=self.embed_list[self.current_page], view=self
        )

    def change_page(self, page: int):
        if page < 0:
            self.current_page = 0
        elif page >= self.total_page:
            self.current_page = self.total_page
        else:
            self.current_page = page

        if self.current_page <= 0:
            self.prev_btn.disabled = True
            self.next_btn.disabled = False
        elif self.current_page >= self.total_page - 1:
            self.prev_btn.disabled = False
            self.next_btn.disabled = True
        else:
            self.prev_btn.disabled = False
            self.next_btn.disabled = False

        self.page_number.label = self.get_cur_page()

    def get_cur_page(self):
        return f"{self.current_page+1}/{self.total_page}"
