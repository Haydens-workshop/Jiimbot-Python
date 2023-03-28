from logging import exception
import discord
from discord.ext import commands
import json
import requests

class Crypto(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    async def coinmarket(self,ctx,*,args:str = None):
        if not args:
            await ctx.send('not enough arguments!')
            return
        else:
            message = await ctx.send('Loading......')
            tp = ''.join(args).lower()
            tp = tp.replace(" ",",")
            try:
                tp = tp.split(',')
            except:
                tp = list(tp)
            
            embed = discord.Embed(color = discord.Color.random())
            for tp in tp:
                api = ''
                url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?convert=USD&slug={tp}'

                headers = {'X-CMC_PRO_API_KEY': api}
                r = requests.get(url,headers = headers)
                data = json.loads(r.content)

                for x in data['data']:
                    price = data['data'][x]['quote']['USD']['price']
                    name = data['data'][x]['name']
                    symbol = data['data'][x]['symbol']
                    embed.add_field(name = f'{name} | {symbol}',value = f"{price}$",inline = False)
                    break

            await message.edit(embed = embed)
            await message.edit(content = '')
            
async def setup(bot: commands.Bot):
    await bot.add_cog(Crypto(bot))
