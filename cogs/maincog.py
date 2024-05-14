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
from roblox import Client, utilities, thumbnails
from roblox import groups
from roblox import members
from roblox.thumbnails import AvatarThumbnailType
import roblox.thumbnails
from typing import Optional
from key_generator.key_generator import generate
from wonderwords import RandomSentence
from static import buttons


roblox = Client("")

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
      



async def setup(bot: commands.Bot):
  await bot.add_cog(MainCog(bot))
  
