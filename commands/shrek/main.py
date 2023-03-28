from discord.ext import commands


class Shrek(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def letswatchshrek(self,ctx):
        await ctx.reply("https://cdn.discordapp.com/attachments/442850936008867870/711567408393093120/Shrek.webm")
    

async def setup(bot: commands.Bot):
    await bot.add_cog(Shrek(bot))
