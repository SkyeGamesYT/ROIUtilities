import discord
from discord import ui, ButtonStyle
import os
import asyncio
import datetime
from discord import client
from discord import member
from discord.app_commands.commands import describe
from discord.ext import commands
import sqlite3
import random
import aiohttp
import roblox
from roblox import utilities, thumbnails
from roblox import groups
from roblox import members
from roblox.thumbnails import AvatarThumbnailType
import roblox.thumbnails
from typing import Optional
from key_generator.key_generator import generate
from wonderwords import RandomSentence
from static import buttons


group_id = 16564777
rblx = roblox.Client()
connection = sqlite3.connect("database.sqlite")
cursor = connection.cursor()


class roblox(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    


    @commands.command(name="whois", breif="Get a user's information from username", description="Usage: -whois <username>")
    async def whois(self, ctx, *, username: str):
        try:
            user = await rblx.get_user_by_username(username)
            embed = discord.Embed(title=f"Info for {user.name}")

            description = user.description if hasattr(user, 'description') else "No Description Provided"
            embed.add_field(name="Username", value=f"`{user.name}`")
            embed.add_field(name="Display Name", value=f"`{user.display_name}`")
            embed.add_field(name="User ID", value=f"`{user.id}`")
            embed.add_field(name="Description", value=f"```{description}```")

            avatar_images = await rblx.thumbnails.get_user_avatar_thumbnails(
            users=[user],
            type=AvatarThumbnailType.headshot,
            size=(420, 420),
            is_circular=False
            )

            if avatar_images:
                avatar_image_url = avatar_images[0]
            embed.set_thumbnail(url=avatar_images[0].image_url)
            await ctx.send(embed=embed)

        except Exception as error:
            print(f"An error occurred: {error}")
            await ctx.send("An error occurred while fetching user information.")


    @commands.command(name="creatorify", breif="Rank a user to Content Creator within the group", description="Usage: -creatorify <username>")
    @commands.has_permissions(manage_guild=True)  # Guild managers only.
    async def promote(self, ctx, username):
        group = await rblx.get_group(16564777)  # Group ID here
        member = await group.get_member_by_username(username)
        await group.set_rank(member, 2)
        await ctx.send("Managed user.")

    @commands.command(name="memberify", description="Usage: -memberify <username>", breif="Set's a member's rank to Member (Rank 1)")
    @commands.has_permissions(manage_guild=True)  # Guild managers only.
    async def demote(self, ctx, username):
        group = await rblx.get_group(16564777)  # Group ID here
        member = await group.get_member_by_username(username)
        await group.set_rank(member, 1)
        await ctx.send("Managed user.")


    @commands.command(name="setrank", breif="Set a user's rank in group", description="Usage: -setrank <username> <rank number>, example: -setrank 5kye_II 3 (Sets 5kye_II's group rank to Content Creator)")
    @commands.has_permissions(manage_guild=True)  # Guild managers only.
    async def setrank(self, ctx, username, rank: int):
        if 253 >= rank >= 1:  # Make sure rank is in allowed range
            group = await rblx.get_group(group_id)  # Group ID here
            member = await group.get_member_by_username(username)
            await group.set_rank(member, rank)  # Sets the rank
            await ctx.send("Promoted user.")
        else:
            await ctx.send("Rank must be at least 1 and at most 253.")
            
            












    @commands.command(name="shout", breif="Post a message on the group shout", description="Usage: -shout <message>")
    @commands.has_permissions(manage_guild=True)  # Guild managers only.
    async def shout(self, ctx, *shout_text):
        group_id = 16564777  # Group ID here
        try:
        # Make a request to the Roblox API to send a message to the group
        # Replace the following code with the actual API request to send a message
        # Example: response = requests.post(f"https://groups.roblox.com/v1/groups/{group_id}/wall/posts", json={"body": shout_text})

        # Check the response status and send a message based on the result
        # Example: if response.status_code == 200:
        #             await ctx.send("Sent shout.")
        #         else:
        #             await ctx.send("Error: Failed to send shout.")
            group = await rblx.get_group(group_id)
            await group.update_shout(shout_text)
            await ctx.send("Sent shout.")  # Placeholder response

        except Exception as e:
            await ctx.send("An error occurred while trying to shout.")
            print(f"Error: {e}")

    @commands.command(name="verify")
    async def verify(self, ctx, username: str):
        discordId = ctx.author.id
        r = RandomSentence()
        randSentence = r.simple_sentence()
        username_str = str(username)
        randSent_str = str(randSentence)
        if username == None:
            ctx.reply("Please use -verify <username>")
        else:
            user = await rblx.get_user_by_username(username)
            if user:
                cursor.execute("INSERT INTO verifysentence VALUES(?, ?, ?)",(discordId, username_str, randSent_str))
                connection.commit()
                button = buttons.verify1()
                view = discord.ui.View()
                embed = discord.Embed(title="Verify", description="Press the button to verify", color=0x2ecc71)
                view.add_item(item=button)
                await ctx.send(embed=embed, view=view)
            else:
                ctx.reply("No roblox user found.")

    @commands.command(name="new_verification")
    async def new_verification(self, ctx):
        button = buttons.newverify()
        view = discord.ui.View()
        embed = discord.Embed(title="Regenerate Sentence", description="Press the button below to regenerate if an issue occurs.", color=0x2ecc71)
        view.add_item(item=button)
        await ctx.send(embed=embed, view=view)
    
    
    @commands.command(name="update")
    async def update(self, ctx):
        button = buttons.updateUser()
        view = discord.ui.View()
        embed = discord.Embed(title="Test")
        view.add_item(item=button)
        await ctx.send(embed=embed, view=view)
        

    @commands.command(name="unlink")
    async def unlink(self, ctx):
        cursor.execute(f"DELETE FROM accounts WHERE discord_id = {ctx.author.id}")
        connection.commit()
        embed = discord.Embed(title="Account unlinked", description="You have successfully unlinked your Roblox account.", color=0x2ecc71)
        await ctx.reply(embed=embed)





async def setup(bot: commands.Bot):
    await bot.add_cog(roblox(bot))