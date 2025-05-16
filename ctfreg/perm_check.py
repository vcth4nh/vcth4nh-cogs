import discord
import logging

logger = logging.getLogger(__name__)

def guild_only(interaction: discord.Interaction):

    logger.debug(f"interaction.guild_id: {interaction.guild_id}")
    return interaction.guild_id is not None
