from discord.ext import commands
import discord

class MainCog:
  def __init__(self, bot):
    self.bot = bot


  @commands.command(pass_context=True)
  async def slap(ctx, member:discord.User):
  await ctx.send(f"{ctx.message.author.mention} slaps {member.mention}!") 




  def setup(bot):
    bot.add_cog(MainCog(bot))
  
