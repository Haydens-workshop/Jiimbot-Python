from typing import Text
import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def help(self,ctx):
        embed = discord.Embed(color = discord.Color.random())
        embed.add_field(name = "coinmarket [crypto name] [crypto name] [crypto name]",value = "Displays the current price of one or more crypto-currencies",inline = False)
        embed.add_field(name = "newegg [item name]",value = "Display the links to the first 5 articles corresponding to this search",inline = False)
        embed.add_field(name = "play [music name or link]",value = "Play a music",inline = False)
        embed.add_field(name = "stop",value = "End the music",inline = False)
        embed.add_field(name = "skip",value = "Skip the current played music",inline = False)
        embed.add_field(name = "queue",value = "Display the music queue",inline = False)
        embed.add_field(name = "get",value = "Gets Current Song",inline = False)
        embed.add_field(name = "pause",value = "Pauses Current Song",inline = False)
        embed.add_field(name = "resume",value = "Resumes Current Song",inline = False)
        embed.add_field(name = "seek",value = "Skips to TimeStamp",inline = False)
        embed.add_field(name = "donate",value = "Prints PayPal Donation Link",inline = False)
        embed.set_footer(text = "Jimbot",icon_url = self.bot.user.avatar.url)
        await ctx.send(embed = embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Help(bot))
