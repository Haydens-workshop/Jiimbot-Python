from discord.ext import commands
import requests
from bs4 import BeautifulSoup as bs
import discord


class Newegg(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def newegg(self, ctx, *, args: str = None):
        msg = await ctx.send('Loading.....')

        r = requests.get(f'https://www.newegg.com/p/pl?d={args}')
        data = r.content
        embed = discord.Embed(color=discord.Color.random())

        soup = bs(r.content, 'lxml')
        soup = soup.find_all('div', class_='item-container')
        iteration_num = 0

        for x in soup:
            if iteration_num >= 5:
                break
            try:

                tag = x.find('a')
                title = x.find('a')
                for img in title.find_all('img', alt=True):
                    title = img['title']

                link = (tag['href'], tag.get_text(strip=False))
                link = list(link)[0]
                embed.add_field(name=title, value=link, inline=False)
                iteration_num += 1

            except:
                continue

        await msg.edit(embed=embed)
        await msg.edit(content='')


async def setup(bot: commands.Bot):
    await bot.add_cog(Newegg(bot))
