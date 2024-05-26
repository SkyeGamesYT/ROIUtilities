import discord
from discord import ui, ButtonStyle
import os
import asyncio
import datetime
from discord import client
from discord import member
from discord.utils import get
from discord.app_commands.commands import describe
from discord.ext import commands
import sqlite3
import random
import aiohttp
import roblox
from roblox import Client, utilities, thumbnails
from roblox import groups
from roblox import members
from roblox.thumbnails import AvatarThumbnailType
import roblox.thumbnails
from typing import Optional
from key_generator.key_generator import generate
from wonderwords import RandomSentence
from static import buttons

connection = sqlite3.connect("database.sqlite")
cursor = connection.cursor()
roblox = Client()

class MainCog(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot


  @commands.command()
  async def slap(ctx, member:discord.User):
    await ctx.send(f"{ctx.message.author.mention} slaps {member.mention}!") 


  @commands.command()
  async def echo(self,ctx,*, args):
    sentence = str(args)
    await ctx.send(args)
  
  @commands.command(name="debug")
  async def debug(self, ctx):
    if ctx.author.id == 789969566695424020:
      cursor.execute("SELECT * FROM warningsdb")
      result = cursor.fetchall()
      print(result)
      cursor.execute("SELECT * FROM accounts")
      result = cursor.fetchall()
      print(result)
      
  @commands.command(name="annoy_defy")
  async def annoy_defy(self, ctx):
    if ctx.author.id == 789969566695424020:
      times = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
      defy = await self.bot.fetch_user(733024205712523314)
      dm = self.bot.create_dm(defy)
      for i in times:
        await dm.send("HAI DEFY")
    else:
      await ctx.reply("Nuh uh")
        

  @commands.command(name="getrole")
  async def getrole(self, ctx, *, args):
    bot = self.bot
    role = str(args)
    guild = bot.get_guild(1233976552623181834)
    user = ctx.message.author
    choosable_roles = ["giveaway", "announcement", "sneakpeek", "dev", "codes"]
    if role and role in choosable_roles:
      if role == "giveaway":
        role = get(guild.roles, name="Giveaway Pings")
        if role in ctx.message.author.roles:
            await ctx.message.author.remove_roles(role)
            await ctx.reply("Removed role Giveaway Pings")
        else:
          await ctx.message.author.add_roles(role)
          await ctx.reply("Added role Giveaway Pings")
      elif role == "announcement":
        role = get(guild.roles, name="Announcement Pings")
        if role in ctx.message.author.roles:
          await ctx.message.author.remove_roles(role)
          await ctx.reply("Removed role Announcement Pings")
        else:
          await ctx.message.author.add_roles(role)
          await ctx.reply("Added role Announcement Pings")
      elif role == "sneakpeek":
        role = get(guild.roles, name="Sneakpeek Pings")
        if role in ctx.message.author.roles:
          await ctx.message.author.remove_roles(role)
          await ctx.reply("Removed role Sneakpeek Pings")
        else:
          await ctx.message.author.add_roles(role)
          await ctx.reply("Added role Sneakpeek Pings")
      elif role == "codes":
        role = get(guild.roles, name="Code Pings")
        if role in ctx.message.author.roles:
          await ctx.message.author.remove_roles(role)
          await ctx.reply("Removed role Code Pings")
        else:
          await ctx.message.author.add_roles(role)
          await ctx.reply("Added role Code Pings")
      elif role == "dev":
        role = get(guild.roles, name="Developer Pings")
        if role in ctx.message.author.roles:
          await ctx.message.author.remove_roles(role)
          await ctx.reply("Removed role Developer Pings")
        else:
          await ctx.message.author.add_roles(role)
          await ctx.reply("Added role Developer Pings")
    else:
      await ctx.reply("Role is not a valid role, please use one of these: giveaway, codes, announcement, sneakpeek, dev")
      



async def setup(bot: commands.Bot):
  await bot.add_cog(MainCog(bot))
  
