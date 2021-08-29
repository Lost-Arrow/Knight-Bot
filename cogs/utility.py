import asyncio

from discord import (
    Color,
    Embed,
    Member
)
from discord.ext.commands import (
    Cog,
    Context,
    command,
    errors,
    group,
    ColorConverter
)
from knightbot import (
    DEBUG,
    INFO,
    Knight,
    get_current_time
)

class Utility (Cog):
    """Utility Cog for Knight"""

    def __init__(self, bot: Knight):
        self.bot = bot
        asyncio.gather(self.bot.common_logger.log(INFO, '```Utility Cog loaded!```'))

    @command(brief = 'Lists all commands')
    async def commands (self, ctx: Context):
        """Replies with a list of all usable commands"""

        embed = Embed(color       = Color.green(),
                      description = '```\n{cmd}```'.format(cmd = "\n".join(sorted(cmd.name for cmd in self.bot.commands))),
                      timestamp   = get_current_time(),
                      title       = 'Commands :scroll:',
                      type        = 'rich')

        await ctx.send(embed = embed)

    @command(brief = 'Pong!')
    async def ping (self, ctx: Context):
        """Replies with latency and uptime"""

        content = """
```
Latency: {latency}
 Uptime: {uptime}
```
        """.format(latency = self.bot.latency_ms,
                   uptime  = self.bot.uptime)

        embed = Embed(color       = Color.green(),
                      description = content,
                      timestamp   = get_current_time(),
                      title       = 'Pong :ping_pong:',
                      type        = 'rich')

        await ctx.send(embed = embed)

    @command(brief = 'Makes the bot say a message')
    async def say (self, ctx: Context, *, message = ''):
        """Replies with an embed containing the message you want it to say

        Expected format: say message
                         say message embed_color
        """

        if message == '':
            await ctx.send('Message not provided!')
            return

        try:
            _str_color = message.split()[-1]
            _message   = message[:-len(_str_color)]
            _color     = await ColorConverter().convert(None, _str_color)
        except:
            _color   = Color.gold()
            _message = message

        embed = Embed(color       = _color,
                      description = _message,
                      timestamp   = get_current_time(),
                      type        = 'rich')

        embed.set_author(name     = self.bot.user.name,
                         icon_url = self.bot.user.avatar_url)

        await ctx.send(embed = embed)
        await self.bot.common_logger.guild_specific_log(ctx.guild, DEBUG, f'Message by {ctx.author.name}#{ctx.author.discriminator}:\n\n{message}')
        await ctx.message.delete()

    @command(brief = 'Uptime')
    async def uptime (self, ctx: Context):
        """The time duration for which the bot has been online"""

        content = """
```
Started at: {starttime}
    Uptime: {uptime}
```
        """.format(starttime = self.bot.start_time,
                      uptime = self.bot.uptime)

        embed = Embed(color       = Color.green(),
                      description = content,
                      timestamp   = get_current_time(),
                      title       = 'Pong :ping_pong:',
                      type        = 'rich')

        await ctx.send(embed = embed)

    @group(pass_context = True, brief = 'Displays avatars')
    async def avatar (self, ctx: Context):
        if ctx.invoked_subcommand is None:
            user = ctx.author

            embed = Embed(color     = Color.blurple(),
                          title     = f'{user.name}#{user.discriminator}\'s Avatar',
                          timestamp = get_current_time())

            embed.set_image(url = user.avatar_url)

            await ctx.send(embed = embed)

    @avatar.group(pass_context = True, brief = 'Displays server avatar')
    async def server (self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await self.icon(ctx)

    @server.command(pass_context = True, brief = 'Displays server icon')
    async def icon (self, ctx: Context):
        """Displays server icon"""

        embed = Embed(color     = Color.blurple(),
                      title     = 'Server Icon',
                      timestamp = get_current_time())

        embed.set_image(url = ctx.guild.icon_url)

        await ctx.send(embed = embed)

    @server.command(pass_context = True, brief = 'Displays server banner')
    async def banner (self, ctx: Context):
        """Displays server banner"""

        embed = Embed(color     = Color.blurple(),
                      title     = 'Server Banner',
                      timestamp = get_current_time())

        embed.set_image(url = ctx.guild.banner_url)

        await ctx.send(embed = embed)

    @avatar.command(pass_context = True, brief = 'Displays user avatar')
    async def user (self, ctx: Context, *, user: Member):
        """Displays user avatar"""

        embed = Embed(color     = Color.blurple(),
                      title     = f'{user.name}#{user.discriminator}\'s Avatar',
                      timestamp = get_current_time())

        embed.set_image(url = user.avatar_url)

        embed.set_footer(text     = f'Requested by {ctx.author.name}#{ctx.author.discriminator}',
                         icon_url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    @user.error
    async def user_error (self, ctx: Context, error):
        if isinstance(error, errors.MemberNotFound):
            # Extract name from error message
            name = error.args[0].split()[1].strip('"').lower()
            for member in ctx.guild.members:
                if member.name.lower().startswith(name) or member.display_name.lower().startswith(name):
                    await self.user(ctx, user = member)
                    return

def setup (bot: Knight) -> None:
    bot.add_cog(Utility(bot))
