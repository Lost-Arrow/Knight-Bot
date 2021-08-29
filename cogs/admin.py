import asyncio
import json
import os

from discord import (
    Color,
    Embed
)
from discord.ext.commands import (
    Cog,
    Context,
    command,
    group,
    is_owner
)
from knightbot import (
    INFO,
    Knight,
    get_current_time
)

class cd:
    def __init__ (self, new_path: str):
        self.path = new_path

    def __enter__ (self):
        self.saved_path = os.getcwd()
        os.chdir(self.path)
        return self

    def __exit__ (self, exc_type, exc_val, exc_tb):
        os.chdir(self.saved_path)

class Admin (Cog):
    """Admin Cog for Knight"""

    def __init__ (self, bot: Knight):
        self.bot = bot
        asyncio.gather(self.bot.common_logger.log(INFO, '```Admin Cog loaded!```'))

    @command(brief = 'Displays cache')
    @is_owner()
    async def cache (self, ctx: Context):
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
    async def load (self, ctx: Context, extension: str):
        """Loads a Cog extension"""
        self.bot.load_extension(f'cogs.{extension}')

    @command(brief = 'Reloads a Cog')
    @is_owner()
    async def reload (self, ctx: Context, extension: str):
        """Reloads a Cog extension by unloading the cog and loading it again"""
        await self.unload(ctx, extension)
        await self.load(ctx, extension)

    @command(brief = 'Unloads a Cog')
    @is_owner()
    async def unload (self, ctx: Context, extension: str):
        """Unloads a Cog extension"""
        self.bot.unload_extension(f'cogs.{extension}')

    @group(pass_context = True, brief = 'Cog utility commands')
    @is_owner()
    async def cogs (self, ctx: Context):
        """Utility commands for cogs"""

        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid subcommand!')

    @cogs.command(pass_context = True, brief = 'Lists available cogs')
    async def available (self, ctx: Context):
        """Lists all available Cogs that can be added

        They are the *.py files present in the 'Knight Bot/cogs/' directory
        """

        with cd('../../cogs'):
            (_, _, files) = next(os.walk(os.getcwd()))
        cogs = '\n'.join(sorted([file[:-3] for file in files if file.endswith('.py')]))

        embed = Embed(color       = Color.default(),
                      description = f'```\n{cogs}```',
                      timestamp   = get_current_time(),
                      type        = 'rich')

        await ctx.send(embed = embed)

    @cogs.command(pass_context = True, brief = 'Lists loaded cogs')
    async def loaded (self, ctx: Context):
        """Lists all loaded Cogs"""
        cogs = '\n'.join([*self.bot.cogs.keys()])

        embed = Embed(color       = Color.default(),
                      description = f'```\n{cogs}```',
                      timestamp   = get_current_time(),
                      type        = 'rich')

        await ctx.send(embed = embed)

    @command(brief = 'Logs out the bot')
    @is_owner()
    async def logout (self, ctx: Context):
        """Logs out the bot i.e. bot goes offline"""
        await self.bot.common_logger.log(INFO, '```Logged out!```')
        self.bot.update_cache_file()
        await self.bot.close()

def setup (bot: Knight):
    bot.add_cog(Admin(bot))
