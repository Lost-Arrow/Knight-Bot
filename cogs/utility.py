from discord import (
    Color,
    Embed
)
from discord.ext.commands import (
    Cog,
    command,
    ColorConverter
)
from knightbot import (
    INFO,
    Knight,
    get_current_time
)

class Utility (Cog):
    def __init__(self, bot: Knight):
        self.bot = bot

    @Cog.listener()
    async def on_ready (self):
        await self.bot.common_logger.log(INFO, '```Utility Cog loaded!```')

    @command(brief = 'Lists all commands')
    async def commands (self, ctx):
        """Replies with a list of all usable commands"""

        embed = Embed(color       = Color.green(),
                      description = '```{cmd}```'.format(cmd = "\n".join(sorted(cmd.name for cmd in self.bot.commands))),
                      timestamp   = get_current_time(),
                      title       = 'Commands :scroll:',
                      type        = 'rich')

        await ctx.send(embed = embed)

    @command(brief = 'Pong!')
    async def ping (self, ctx):
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

    @command(brief = 'Say a message through the bot')
    async def say (self, ctx, *, message = ''):
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

    @command(brief = 'Uptime')
    async def uptime (self, ctx):
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

def setup (bot: Knight) -> None:
    bot.add_cog(Utility(bot))
