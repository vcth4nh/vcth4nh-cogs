from typing import List
import discord

class GeneralButton(discord.ui.View):
    def __init__(self,timeout=3600):
        super().__init__(timeout=timeout)

class PaginationBtn(GeneralButton):
    def __init__(self, embed_list: List[discord.Embed]):
        super().__init__()
        print(embed_list)
        self.total_page = len(embed_list)
        self.current_page = 0
        self.change_page(page=0)

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def prev_btn(self, ctx: discord.Interaction, btn: discord.ui.Button):
        self.change_page(page=self.current_page - 1)

        await ctx.message.edit(embed=self.embed_list[self.current_page], view=self)

    @discord.ui.button(style=discord.ButtonStyle.grey, disabled=True)
    async def page_number(self):
        pass

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next_btn(self, ctx: discord.Interaction, btn: discord.ui.Button):
        self.change_page(page=self.current_page + 1)

        await ctx.message.edit(embed=self.embed_list[self.current_page], view=self)

    def change_page(self, page: int):
        if page < 0:
            self.current_page = 0
            self.page_number.label = f"1/{self.total_page}"
        if page >= self.total_page:
            self.current_page = self.total_page - 1
            self.page_number.label = f"{self.total_page}/{self.total_page}"

        self.current_page = page
        self.page_number.label = f"{str(self.current_page + 1)}/{self.total_page}"
        if self.current_page == 0:
            self.prev_btn.disabled = True
        elif self.current_page == self.total_page - 1:
            self.next_btn.disabled = True
