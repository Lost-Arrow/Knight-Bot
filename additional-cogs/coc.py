import asyncio

from discord.ext.commands import (
    Cog
)
from knightbot import (
    INFO,
    Knight
)

class ClashOfClans (Cog):
    def __init__ (self, bot: Knight):
        self.bot = bot
        asyncio.gather(self.bot.common_logger.log(INFO, '```\nClashOfClans Cog loaded!```'))

def setup (bot: Knight):
    bot.add_cog(ClashOfClans(bot))
