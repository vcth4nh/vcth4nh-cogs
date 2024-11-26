import discord


def guild_only(interaction: discord.Interaction):
    print(interaction.guild_id)
    return interaction.guild_id is not None