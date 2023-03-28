from discord.ext import commands
import json
import requests

song_queue = []
class Eq2u(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def eq2u(self,ctx,*,args:str = None):
        msg = await ctx.send('Loading....')
        try:
            if args:
                r = requests.get(f"http://census.daybreakgames.com/json/get/eq2/character?name.first={args}")
                data = json.loads(r.content)
                id = data['character_list'][0]['id']
                await msg.edit(content = f"https://u.eq2wire.com/soe/character_detail/{id}")
            else:
                await msg.edit(content = "Uh uh... Unknown character...")

        except Exception as e:
            await msg.edit(content = "Uh uh... Unknown character...")

async def setup(bot: commands.Bot):
    await bot.add_cog(Eq2u(bot))
