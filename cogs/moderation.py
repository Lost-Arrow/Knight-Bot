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
    has_permissions
)

from knightbot import (
    INFO,
    Knight,
    get_current_time
)

class Moderation (Cog):
    """Moderation Cog for Knight"""

    def __init__ (self, bot: Knight):
        self.bot = bot
        asyncio.gather(self.bot.common_logger.log(INFO, '```Moderation Cog loaded!```'))

    @command(brief = 'Kicks a user')
    @has_permissions(kick_members = True)
    async def kick (self, ctx: Context, user: Member, *, reason: str = 'No reason provided'):
        """Kicks a user from a guild"""

        embed = Embed(color     = Color.red(),
                      title     = f'Kicked {user.display_name}#{user.discriminator} :boot:',
                      timestamp = get_current_time(),
                      type      = 'rich')

        embed.set_author(name     = f'{ctx.author.name}#{ctx.author.discriminator}',
                         icon_url = ctx.author.avatar_url)

        embed.set_thumbnail(url = user.avatar_url)

        embed.add_field(name   = 'Nick',
                        value  = user.nick,
                        inline = False)

        embed.add_field(name   = 'Reason',
                        value  = f'```\n{reason}```',
                        inline = False)

        message = f'```\n{ctx.author.name}#{ctx.author.discriminator} kicked {user.name}#{user.discriminator}\n\nReason:\n\n{reason}```'

        await user.kick(reason = reason)
        await ctx.message.delete()
        await ctx.send(embed = embed)
        await self.bot.common_logger.guild_specific_log(ctx.guild, INFO, message)

    @command(brief = 'Bans a user')
    @has_permissions(ban_members = True)
    async def ban (self, ctx: Context, user: Member, *, reason: str = 'No reason provided'):
        """Bans a user from a guild"""

        embed = Embed(color     = Color.red(),
                      title     = f'Banned {user.display_name}#{user.discriminator} :boot:',
                      timestamp = get_current_time(),
                      type      = 'rich')

        embed.set_author(name     = f'{ctx.author.name}#{ctx.author.discriminator}',
                         icon_url = ctx.author.avatar_url)

        embed.set_thumbnail(url = user.avatar_url)

        embed.add_field(name   = 'Nick',
                        value  = user.nick,
                        inline = False)

        embed.add_field(name   = 'Reason',
                        value  = f'```\n{reason}```',
                        inline = False)

        message = f'```\n{ctx.author.name}#{ctx.author.discriminator} banned {user.name}#{user.discriminator}\n\nReason:\n\n{reason}```'

        await user.ban(reason = reason)
        await ctx.message.delete()
        await ctx.send(embed = embed)
        await self.bot.common_logger.guild_specific_log(ctx.guild, INFO, message)

    @command(brief = 'Bulk deletes messages')
    @has_permissions(manage_messages = True)
    async def purge (self, ctx: Context, limit: int, *, reason = 'No reason provided'):
        """Bulk deletes messages without a cached copy to review in future"""

        message = f'```\n{ctx.author.name}#{ctx.author.discriminator} purged {limit} messages\n\nReason:\n\n{reason}```'

        # limit + 1 to delete invoking command message too
        await ctx.channel.purge(limit = limit + 1)
        await self.bot.common_logger.guild_specific_log(ctx.guild, INFO, message)
        await ctx.send(message)

    @command(brief = 'Bulk deletes messages')
    @has_permissions(manage_messages = True)
    async def cachedpurge (self, ctx: Context, limit: int, *, reason = 'No reason provided'):
        """Bulk deletes messages with a cached copy to review in future"""

        message = f'```\n{ctx.author.name}#{ctx.author.discriminator} purged {limit} messages\n\nReason:\n\n{reason}```'

        # limit + 1 to delete invoking command message too
        purged_messages = await ctx.channel.purge(limit = limit + 1)
        await self.bot.common_logger.log(INFO, message)
        await ctx.send(message)

        content = f'{message}\n\n'

        for index, message in enumerate(purged_messages, start = 1):
            content += f'```\n{index}\n```{message.content}\n\n'

        await self.bot.common_logger.guild_specific_log(ctx.guild, INFO, content)

def setup (bot: Knight):
    bot.add_cog(Moderation(bot))
