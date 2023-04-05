class bobt:
  def __init__(self, bot):
    self.bot = bot

  async def loadcog(self, fn: str, conf: str):
    self.bot.load_extension(f'{conf}.{fn}')

  def run(self, token):
    self.bot.run(token)

from nextcord.ext import commands
from nextcord import Intents
import asyncio
from os import listdir, environ
bot = bobt(commands.Bot(command_prefix=['?'], intents=Intents.all(), help_command=None))
async def main():
  tasks: list = []
  for i in ['cogs']:
    for fn in listdir(i):
      if fn.endswith(".py"):
        tasks.append(asyncio.create_task(bot.loadcog(fn[:-3], i)))
  for i in tasks: await i
asyncio.run(main())
bot.run(environ['token'])
