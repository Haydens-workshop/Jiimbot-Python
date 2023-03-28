import logging
import discord
from discord.ext import commands
import os

import asyncio
from logger import SetupLogging


log = logging.getLogger('main')


class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix='.', intents=discord.Intents.all(), help_command=None)

    async def on_ready(self):
        log.info('-------- GOLIATH ONLINE --------')

    async def setup_hook(self) -> None:
        for files in os.listdir('./Commands'):
            for filename in os.listdir("./Commands/"+files):
                if filename.endswith('.py'):
                    await self.load_extension(f'Commands.{files}.{filename[:-3]}')


bot = Bot()


async def main() -> None:
    with SetupLogging():
        await bot.start('')


if __name__ == '__main__':
    asyncio.run(main())
