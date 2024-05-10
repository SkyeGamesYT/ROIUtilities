from discord.ext import commands
import discord

class MainCog:
  def __init__(self, bot):
    self.bot = bot


  @commands.command(pass_context=True)
  async def slap(ctx, member:discord.User):
    await ctx.send(f"{ctx.message.author.mention} slaps {member.mention}!") 
  async def echo(ctx, *,args):
    if ctx.author.id >= 0:
        await ctx.send(args)
      

  def setup(bot):
    bot.add_cog(MainCog(bot))
  
