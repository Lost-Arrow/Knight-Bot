import json

from discord import (
    Color,
    Embed
)
from discord.ext.commands import (
    Cog,
    command,
    is_owner
)
from knightbot import (
    INFO,
    Knight,
    get_current_time
)

class Admin (Cog):
    def __init__ (self, bot: Knight):
        self.bot = bot

    @Cog.listener()
    async def on_ready (self):
        await self.bot.common_logger.log(INFO, '```Admin Cog loaded!```')

    @command(brief = 'Displays cache')
    @is_owner()
    async def cache (self, ctx):
        """Displays cache"""

        embed = Embed(color       = Color.green(),
                      description = f'```{json.dumps(self.bot.cache, indent = 4)}```',
                      timestamp   = get_current_time(),
                      type        = 'rich')
        embed.set_author(name     = self.bot.user.name,
                         icon_url = self.bot.user.avatar_url)

        await ctx.send(embed = embed)

    @command(brief = 'Loads a Cog')
    @is_owner()
    async def load (self, ctx, extension: str):
        """Loads a Cog extension"""
        self.bot.load_extension(f'knightbot.cogs.{extension}')

    @command(brief = 'Reloads a Cog')
    @is_owner()
    async def reload (self, ctx, extension: str):
        """Reloads a Cog extension by unloading the cog and loading it again"""
        await self.unload(ctx, extension)
        await self.load(ctx, extension)

    @command(brief = 'Unloads a Cog')
    @is_owner()
    async def unload (self, ctx, extension: str):
        """Unloads a Cog extension"""
        self.bot.unload_extension(f'knightbot.cogs.{extension}')

    @command(brief = 'Log off')
    @is_owner()
    async def logout (self, ctx):
        """Logs out the bot i.e. bot goes offline"""
        await self.bot.common_logger.log(INFO, '```Logged out!```')
        self.bot.update_cache_file()
        await self.bot.close()

def setup (bot: Knight):
    bot.add_cog(Admin(bot))
