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
import buttons




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
    command_prefix="-",  # - will be bot's prefix
    case_insensitive=True,
  intents=discord.Intents.all(),
  help_command=help_command,
  activity=discord.Activity(type=discord.activity.ActivityType.watching, name="The Realm of Imagination",status=discord.Status.idle)
)


roblox = Client(os.getenv("ROBLOXTOKEN"))



@bot.event
async def on_ready():
  print(f"Logged in as {bot.user}")









@bot.command(name="whois", breif="Get a user's information from username", description="Usage: -whois <username>")
async def whois(ctx, *, username: str):
    try:
        user = await roblox.get_user_by_username(username)
        embed = discord.Embed(title=f"Info for {user.name}")

        description = user.description if hasattr(user, 'description') else "No Description Provided"
        embed.add_field(name="Username", value=f"`{user.name}`")
        embed.add_field(name="Display Name", value=f"`{user.display_name}`")
        embed.add_field(name="User ID", value=f"`{user.id}`")
        embed.add_field(name="Description", value=f"```{description}```")

        avatar_images = await roblox.thumbnails.get_user_avatar_thumbnails(
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


@bot.command(name="creatorify", breif="Rank a user to Content Creator within the group", description="Usage: -creatorify <username>")
@commands.has_permissions(manage_guild=True)  # Guild managers only.
async def promote(ctx, username):
    group = await roblox.get_group(16564777)  # Group ID here
    member = await group.get_member_by_username(username)
    await group.set_rank(member, 2)
    await ctx.send("Managed user.")

@bot.command(name="memberify", description="Usage: -memberify <username>", breif="Set's a member's rank to Member (Rank 1)")
@commands.has_permissions(manage_guild=True)  # Guild managers only.
async def demote(ctx, username):
    group = await roblox.get_group(16564777)  # Group ID here
    member = await group.get_member_by_username(username)
    await group.set_rank(member, 1)
    await ctx.send("Managed user.")


@bot.command(name="setrank", breif="Set a user's rank in group", description="Usage: -setrank <username> <rank number>, example: -setrank 5kye_II 3 (Sets 5kye_II's group rank to Content Creator)")
@commands.has_permissions(manage_guild=True)  # Guild managers only.
async def setrank(ctx, username, rank: int):
    if 253 >= rank >= 1:  # Make sure rank is in allowed range
        group = await roblox.get_group(16564777)  # Group ID here
        member = await group.get_member_by_username(username)
        await group.set_rank(member, rank)  # Sets the rank
        await ctx.send("Promoted user.")
    else:
        await ctx.send("Rank must be at least 1 and at most 253.")

@bot.command(name="echo", description="Usage: -echo <message>")
async def echo(ctx, *,args):
    if ctx.author.id >= 0:
        await ctx.send(args)

@bot.command(name="slap", description="Usage: -slap <mention>")
async def slap(ctx, member:discord.User):
  await ctx.send(f"{ctx.message.author.mention} slaps {member.mention}!") 


@bot.command(name="ban", description="Usage: -ban <mention> <reason>")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason = None):
    await member.send(f"You were banned from {ctx.guild} for {reason} by {ctx.author}")
    await member.ban(reason = reason)
    embedVar = discord.Embed(title="Banned User", description=f"{member} was banned by {ctx.author} for {reason}", color=00000)
    await ctx.send(embed=embedVar)

@bot.command(name='unban', description="Usage: -unban <user id> <reason>")
@commands.has_permissions(ban_members=True)
async def _unban(ctx, id: int, *, reason = None):
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user, reason = reason)
    embedVar = discord.Embed(title="Unbanned User", description=f"{user} was unbanned by {ctx.author} for {reason}", color=0x00ff00)
    await ctx.send(embed=embedVar)


@bot.command(name="mute", description="Usage: -mute <mention> <reason>")
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, reason = None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")  # Assuming you have a role named "Muted"

    if not role:
        # The "Muted" role does not exist, so create it
        role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            # Disallow the "Muted" role to send messages in all channels
            await channel.set_permissions(role, send_messages=False)

    await member.add_roles(role)
    embedVar = discord.Embed(title="User Muted", description=f"{member} was muted by {ctx.author} for {reason}", color=0x00ff00)
    await ctx.send(embed=embedVar)



@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a member to mute.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    else:
        await ctx.send("An error occurred while executing this command.")


@bot.command(name="unmute", description="Usage: -unmute <mention>")
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")  # Assuming you have a role named "muted"

    if role in member.roles:
        await member.remove_roles(role)
        embedVar = discord.Embed(title="User Unmuted", description=f"{member} was unmuted by {ctx.author}", color=0x00ff00)
        await ctx.send(embed=embedVar)
    else:
        await ctx.send(f"{member.mention} is not muted.")




@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention a member to unmute.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to use this command.")
    else:
        await ctx.send("An error occurred while executing this command.")



@bot.command(name="warn")
@commands.has_permissions(ban_members=True)
async def warn(ctx, id: int, reason="No reason Specified"):
  moderator = str(ctx.author.name)
  member = await bot.fetch_user(id)
  print(member)
  key = generate()
  warnid = key.get_key()
  print(warnid)
  cursor.execute("INSERT INTO warningsdb VALUES (?, ?, ?, ?)",
                 (id, reason, moderator, warnid))
  connection.commit()
  embedVar = discord.Embed(
      title="User Warned",
      description=f"{member} has been warned by {moderator} for {reason}", color=0x2ecc71)
  await ctx.send(embed=embedVar)
  channel = await member.create_dm()
  embedDM = discord.Embed(
      title="Warning",
      description=f"You have been warned by {moderator} for {reason}",
      color=0xe74c3c)
  await channel.send(embed=embedDM)



@bot.command(name="warnings")
@commands.has_permissions(manage_roles=True)
async def warnings(ctx, id: int):
  member = ctx.guild.get_member(id)
  cursor.execute("SELECT * FROM warningsdb WHERE user_id = ?", (id, ))
  result = cursor.fetchall()

  if result:
    embedVar = discord.Embed(title=f"Warnings for {member}",
                             description="Warnings",
                             color=0x2ecc71)
    for row in result:
      moduser = row[2]  # Extract moderator from each row
      warningNumber = row[3]  # Extract warning number from each row
      embedVar.add_field(
          name=f"Reason: {row[1]}",
          value=f"Moderator: {moduser}, Warning Number: {warningNumber}",
          inline=False)
    await ctx.send(embed=embedVar)
  else:
    await ctx.send("No warnings found for the member.")


@bot.command(name="delwarn")
@commands.has_permissions(manage_roles=True)
async def delwarn(ctx, id: int, warnNumb: str):
  member = ctx.guild.get_member(id)

  if member:
    cursor.execute("select warn_id FROM warningsdb WHERE user_id = ?", (id, ))
    warnings = cursor.fetchall()
    print("warnings:", warnings)  # add this line for debugging
    found = False
    for warning in warnings:
      print("warning id:", warning)  # add this line for debugging
      if warnNumb == warning[0]:
        cursor.execute(f"DELETE FROM warningsdb WHERE warn_id = ?", (warnNumb, ))
        connection.commit()
        embed_var = discord.Embed(
            title="Warning Deleted",
            description=f"Warning #{warnNumb} was deleted by {ctx.author}", color=0x2ecc71)
        await ctx.send(embed=embed_var)
        found = True
        break
    if not found:
        await ctx.send("Warning number not found.")
    else:
        await ctx.send("Member not found.")













@bot.command(name="shout", breif="Post a message on the group shout", description="Usage: -shout <message>")
@commands.has_permissions(manage_guild=True)  # Guild managers only.
async def shout(ctx, *, shout_text: str):
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
      group = await roblox.get_group(group_id)
      await group.update_shout(shout_text)
      await ctx.send("Sent shout.")  # Placeholder response

    except Exception as e:
        await ctx.send("An error occurred while trying to shout.")
        print(f"Error: {e}")

@bot.command(name="verify")
async def verify(ctx, username: str):
    discordId = ctx.author.id
    r = RandomSentence()
    randSentence = r.simple_sentence()
    username_str = str(username)
    randSent_str = str(randSentence)
    if username == None:
        ctx.reply("Please use -verify <username>")
    else:
        user = await roblox.get_user_by_username(username)
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

@bot.command(name="new_verification")
async def new_verification(ctx):
    button = buttons.newverify()
    view = discord.ui.View()
    embed = discord.Embed(title="Regenerate Sentence", description="Press the button below to regenerate if an issue occurs.", color=0x2ecc71)
    view.add_item(item=button)
    await ctx.send(embed=embed, view=view)

@bot.command()
async def test(ctx):
    randomsent = RandomSentence()
    await ctx.reply(randomsent.sentence())


@bot.command(name="unlink")
async def unlink(ctx):
    cursor.execute(f"DELETE FROM accounts WHERE discord_id = {ctx.author.id}")
    connection.commit()
    embed = discord.Embed(title="Account unlinked", description="You have successfully unlinked your Roblox account.", color=0x2ecc71)
    await ctx.reply(embed=embed)






bot.run(os.environ["DISCORDTOKEN"])  # Grab the DISCORDTOKEN env from our .env file
