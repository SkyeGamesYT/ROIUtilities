import discord
from discord import ui, ButtonStyle
from discord import message
from discord.ui import button
from discord.app_commands.commands import describe
from discord.ext import commands
from wonderwords import RandomSentence
import sqlite3
import roblox
from roblox import Client, utilities, thumbnails
from roblox import groups
from roblox import members
from roblox.thumbnails import AvatarThumbnailType
import roblox.thumbnails
import os
import aiohttp

connection = sqlite3.connect("database.sqlite")
cursor = connection.cursor()
roblox = Client("")
verify_log_channel = 0

bot = commands.Bot(intents=discord.Intents.all(), command_prefix="r-")


class MyButton(ui.Button):

    def __init__(self):
        super().__init__(label="Click me!", style=ButtonStyle.green)

    async def callback(self, interaction: ...):
        print("Nuh uh")


class verify1(ui.Button):

    def __init__(self):
        super().__init__(
            label="Click for verification!",
            style=ButtonStyle.green,
        )

    async def callback(self, interaction: ...):
        cursor.execute(
            f"SELECT roblox_username FROM verifysentence WHERE discord_id = {interaction.user.id}"
        )
        result1 = cursor.fetchone()
        cursor.execute(
            f"SELECT roblox_username FROM accounts WHERE discord_id = {interaction.user.id}"
        )
        result2 = cursor.fetchone()
        cursor.execute(
            f"SELECT sentence FROM verifysentence WHERE discord_id = {interaction.user.id}"
        )
        result3 = cursor.fetchone()
        if result2:
            username = result1[0]
            user = await roblox.get_user_by_username(username)
            await interaction.response.send_message(
                f"Your account is already linked to {result1[0]}",
                ephemeral=True)
            embed = discord.Embed(title="User Verified")
            embed.add_field(name="User Verified as:", value=username)
            connection.commit()
            avatar_images = await roblox.thumbnails.get_user_avatar_thumbnails(
                users=[user],
                type=AvatarThumbnailType.headshot,
                size=(420, 420),
                is_circular=False)

            if avatar_images:
                avatar_image_url = avatar_images[0]
            embed.set_thumbnail(url=avatar_images[0].image_url)
            channel = await bot.fetch_channel(verify_log_channel)
            await interaction.channel.send_message(embed=embed)
        else:
            if result1:
                print(result1)
                username = result1[0]
                print(username)
                user = await roblox.get_user_by_username(result1[0])
                if user:
                    print(f"Found user, {result1[0]}")
                    if user.description == result3[0]:
                        cursor.execute(f"INSERT INTO accounts VALUES (?, ?)",(interaction.user.id, username))
                        await interaction.response.send_message(
                            f"Verified as {result1[0]}")
                        embed = discord.Embed(title="User Verified")
                        embed.add_field(name="User Verified as:",
                                        value=username)
                        connection.commit()
                        avatar_images = await roblox.thumbnails.get_user_avatar_thumbnails(
                            users=[user],
                            type=AvatarThumbnailType.headshot,
                            size=(420, 420),
                            is_circular=False)

                        if avatar_images:
                            avatar_image_url = avatar_images[0]
                        embed.set_thumbnail(url=avatar_images[0].image_url)
                        channel = await bot.fetch_channel(verify_log_channel)
                        await channel.send(embed=embed)
                    else:
                        await interaction.response.send_message(
                            f" Please put \" {result3[0]} \" in your ROBLOX bio, then rerun this command.",
                            ephemeral=True)


class newverify(ui.Button):

    def __init__(self):
        super().__init__(label="Generate new verification sentence",style=ButtonStyle.green)

    async def callback(self, interaction: ...):
        r = RandomSentence()
        randSent = r.sentence()
        cursor.execute(
            f"UPDATE verifysentence SET sentence = ? WHERE discord_id = ?",
            (randSent, interaction.user.id))
        connection.commit()
        await interaction.response.send_message(
            f"Your new sentence is: \"{randSent}\"", ephemeral=True)
