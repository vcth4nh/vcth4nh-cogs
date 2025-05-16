from typing import List, Dict
import discord
import logging

logger = logging.getLogger(__name__)

class GeneralEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def init_attr(
        self,
        title=None,
        description=None,
        color=0xFCBA03,
        embed_fields: List[Dict] = None,
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
            logger.debug("-"*30)
            logger.debug(item)
            logger.debug("-"*30)
            self.add_field(**item)
        return self

# Insert an item between each element of a list.
def intersperse(lst, item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

def paginate_embed(title: str, color: int, embed_fields: List, per_page: int, **kwargs):
    embed_list = []
    for i in range(0, len(embed_fields), per_page):
        embed_fields_list = embed_fields[i : i + per_page]
        embed_fields_list = intersperse(embed_fields_list, {'name': '\u200B', 'value': '\u200B'})

        embed = GeneralEmbed().init_attr(
            title=title,
            color=color,
            embed_fields=embed_fields_list,
            **kwargs
        )
        embed_list.append(embed)
    return embed_list
