from typing import List
import discord


class GeneralEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def init_attr(
        self,
        title=None,
        description=None,
        color=0xFCBA03,
        embed_fields: List[List] = None,
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
        for item in embed_fields:
            self.add_field(name=item[0], value=item[1], inline=False)


def paginate_embed(title: str, color: int, embed_fields: List, per_page: int, **kwargs):
    embed_list = []
    for i in range(0, len(embed_fields), per_page):
        embed = GeneralEmbed()
        embed.init_attr(
            title=title,
            color=color,
            embed_fields=embed_fields[i : i + per_page],
            **kwargs
        )
        embed_list.append(embed)
    return embed_list
