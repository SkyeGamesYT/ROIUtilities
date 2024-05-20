import discord
from discord import ui, ButtonStyle
from discord import message
from discord.ui import button
from discord.app_commands.commands import describe
from discord.ext import commands
import roblox.members
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
from discord.utils import get

connection = sqlite3.connect("database.sqlite")
cursor = connection.cursor()
rblx = Client(os.getenv("ROBLOXTOKEN"))
verify_log_channel = 1237771705842270248
group_id = 16564777

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
            f"SELECT rblx_username FROM verifysentence WHERE discord_id = {interaction.user.id}"
        )
        result1 = cursor.fetchone()
        cursor.execute(
            f"SELECT rblx_username FROM accounts WHERE discord_id = {interaction.user.id}"
        )
        result2 = cursor.fetchone()
        cursor.execute(
            f"SELECT sentence FROM verifysentence WHERE discord_id = {interaction.user.id}"
        )
        result3 = cursor.fetchone()
        if result2:
            username = result1[0]
            user = await rblx.get_user_by_username(username)
            await interaction.response.send_message(
                f"Your account is already linked to {result1[0]}",
                ephemeral=True)
            embed = discord.Embed(title="User Verified")
            embed.add_field(name="User Verified as:", value=username)
            connection.commit()
            avatar_images = await rblx.thumbnails.get_user_avatar_thumbnails(
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
                user = await rblx.get_user_by_username(result1[0])
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
                        avatar_images = await rblx.thumbnails.get_user_avatar_thumbnails(
                            users=[user],
                            type=AvatarThumbnailType.headshot,
                            size=(420, 420),
                            is_circular=False)

                        if avatar_images:
                            avatar_image_url = avatar_images[0]
                        embed.set_thumbnail(url=avatar_images[0].image_url)
                    else:
                        await interaction.response.send_message(
                            f" Please put \" {result3[0]} \" in your rblx bio, then rerun this command.",
                            ephemeral=True)
class updateUser(ui.Button):
    def __init__(self):
        super().__init__(
            label="Update Roles",
            style=ButtonStyle.green,
        )
    async def callback(self, interaction: ...):
        cursor.execute(f"SELECT * FROM accounts WHERE discord_id = {interaction.user.id}")
        result = cursor.fetchall()
        print(result)
        if result:
            discord_user = bot.get_user(result[0][0])
            rblx_user = result[0][1]
            guild = bot.get_guild(1233976552623181834)
            user = await rblx.get_user_by_username(rblx_user)
            roles = await user.get_group_roles()
            role = None
            for test_role in roles:
                if test_role.group.id == group_id:
                    role = test_role
                    break
            print(role)
            if role.name == "Member":
                member_role = get(guild.roles, name="Member")
                await discord_user.add_roles(member_role)
                await interaction.response.send_message("Verified! Recieved roles: Member")
            elif role.name == "Tester":
                tester_role = get(guild.roles, name="Tester")
                await discord_user.add_roles(tester_role)
                await interaction.response.send_message("Verified! Recieved roles: Tester")
            elif role.name == "Content Creator":
                cc_role = get(guild.roles, name="Content Creator")
                await discord_user.author.add_roles(cc_role)
                await interaction.response.send_message("Verifed! Recieved roles: Content Creator")
            elif role.name == "Supervisor":
                supervisor_role = get(guild.roles, name="Supervisor")
                await discord_user.add_roles(supervisor_role)
                await interaction.response.send_message("Verified! Recieved roles: Supervisor")
            elif role.name == "Community Manager":
                cm_role = get(guild.roles, name="Community Manager")
                await discord_user.add_roles(cm_role)
                await interaction.response.send_message("Verified! Recieved roles: Community Manager")
            elif role.name == "Directorate":
                directorate_role = get(guild.roles, name="Directorate")
                await discord_user.add_roles(directorate_role)
                await interaction.response.send_message("Verified! Recieved roles: Directorate")
            elif role.name == "Founder":
                await interaction.response.send_message("Cannot update, Reason: Owner of group")
            else:
                await interaction.response.send_message("Cannot update, Reason: Unknown")
        else:
            await interaction.response.send_message("Your account is not linked, please run -verify <username> to link.")



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
