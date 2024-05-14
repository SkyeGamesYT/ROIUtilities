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




connection = sqlite3.connect("database.sqlite")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS warningsdb (user_id INTEGER, reason TEXT, moderator TEXT, warn_id TEXT)")
connection.commit()
cursor.execute("CREATE TABLE IF NOT EXISTS accounts (discord_id INTEGER, roblox_username TEXT)")
connection.commit()
cursor.execute("CREATE TABLE IF NOT EXISTS verifysentence (discord_id INTEGER, roblox_username TEXT, sentence TEXT)")
connection.commit()


help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)




bot = commands.Bot(
        command_prefix="r-" 
        intents = discord.Intents.all(), 
        help_command=help_command,
        activity=discord.Activity(type=discord.activity.ActivityType.watching, name="The Realm of Imagination",status=discord.Status.idle),
        )


@bot.event
async def setup_hook():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"Loaded Cog: {filename[:-3]}")
        else:
            print("Unable to load pycache folder.")





@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.run("TOKEN")