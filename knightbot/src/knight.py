"""
knight.py
"""

import aioshutil
import constants
import datetime
import json
import os
import traceback

from discord import (
    CategoryChannel,
    Color,
    Embed,
    Guild,
    Intents,
    Invite,
    Message,
    utils
)
from discord.ext.commands import (
    Bot
)
from discord.ext.tasks import (
    loop
)
from logger import (
    DEBUG,
    ERROR,
    INFO,
    FileLogger,
    ChannelLogger,
    CommonLogger
)

async def _command_prefix_callback (bot: Bot, message: Message) -> [str]:
    user_id = bot.user.id
    guild: Guild = message.guild

    prefixes = [f'<@!{user_id}>', f'<@{user_id}>']

    # Only allows custom prefixes in guilds
    if guild is not None:
        prefixes.extend(constants.get_custom_prefix().get(guild.id, constants.get_default_prefix()))
    else:
        prefixes.extend([constants.get_default_prefix()])

    return prefixes

class Knight (Bot):
    _cache_directory        = '../resources/cache'
    _cache_backup_directory = '../resources/cache_backup'

    _log_file = os.path.join(constants.get_log_directory(), 'logs.txt')

    def __init__ (self):
        super().__init__(command_prefix     = _command_prefix_callback,
                         description        = f'{constants.get_name()} is a Multipurpose Discord Bot',
                         intents            = Intents.all(),
                         owner_id           = constants.get_owner(),
                         case_insensitive   = True,
                         strip_after_prefix = True)

        self.file_logger    = FileLogger(self, self._log_file)
        self.channel_logger = ChannelLogger(self)
        self.common_logger  = CommonLogger(self.file_logger, self.channel_logger)

        self.start_time = datetime.datetime.utcnow().replace(microsecond = 0)

        self.cache_files = [
            # Channel IDs for Knight Admin and Knight Log for every guild
            'admin.json'
        ]

        self.cache = {}
        self.initialise_cache()

    async def on_ready (self) -> None:
        self.backup_cache.start()
        self.update_cache.start()

        await self.common_logger.log(INFO, f'```Logged in as {self.user.name} ({self.user.id})```')

        # Change bot name to the name set by the user during setup.py
        required_name = constants.get_name()
        if self.user.name != required_name:
            await self.common_logger.log(INFO, f'```Changing username from {self.user.name} to {required_name}```')
            await self.user.edit(username = required_name)

    async def on_command_error (self, ctx, exception):
        _pretty_exception = f'```{"".join(traceback.format_exception(type(exception), exception, exception.__traceback__))}```'
        await self.common_logger.log(ERROR, _pretty_exception)

    async def on_guild_join (self, guild: Guild):
        await self.update_cache()

    async def on_guild_remove (self, guild: Guild):
        if str(guild.id) in self.cache['admin.json'].keys():
            self.cache['admin.json'].pop(str(guild.id))
        await self.update_cache()

    async def on_invite_create (self, invite: Invite):
        embed = Embed(color     = Color.green(),
                      title     = 'New Invite!',
                      type      = 'rich',
                      timestamp = invite.created_at)

        embed.set_author(name      = invite.inviter.name,
                         icon_url  = invite.inviter.avatar_url)

        embed.set_thumbnail(url = invite.guild.icon_url)

        embed.add_field(name   = 'Channel',
                        value  = invite.channel.mention,
                        inline = False)

        embed.add_field(name   = 'Invite Link',
                        value  = invite.url,
                        inline = False)

        embed.add_field(name   = 'Duration',
                        value  = 'Unlimited' if invite.max_age == 0 else f'{invite.max_age}s',
                        inline = False)

        embed.add_field(name   = 'Max Uses',
                        value  = 'Unlimited' if invite.max_uses == 0 else invite.max_uses,
                        inline = False)

        embed.add_field(name   = 'Temporary Membership',
                        value  = invite.temporary,
                        inline = False)

        log_channel = int(self.cache['admin.json'][str(invite.guild.id)]['log'])
        channel = utils.find(lambda c: c.id == log_channel, invite.guild.channels)
        await channel.send(embed = embed)

    async def on_message_delete (self, message: Message):
        embed = Embed(title       = 'Message Deleted!',
                      description = message.content,
                      timestamp   = constants.get_current_time(),
                      type        = 'rich')

        embed.set_author(name     = message.author.name,
                         icon_url = message.author.avatar_url)

        embed.set_footer(text = message.id)

        log_channel = int(self.cache['admin.json'][str(message.guild.id)]['log'])
        channel = utils.find(lambda c: c.id == log_channel, message.guild.channels)
        await channel.send(embed = embed)

    @property
    def latency_ms (self) -> str:
        """Returns the latency of the bot in milliseconds"""
        return str(int(self.latency * 1000)) + 'ms'

    @property
    def uptime (self) -> str:
        """Returns the duration for how long the bot has been online"""

        return str(constants.get_current_time() - self.start_time)

    def initialise_cache (self) -> None:
        """Reads the cache files and initialises bot cache"""

        for file in self.cache_files:
            _cache_file = os.path.join(self._cache_directory, file)

            if not os.path.exists(_cache_file):
                with open(_cache_file, 'w', encoding = 'utf-8') as f:
                    f.write('{}')

            with open(_cache_file, 'r', encoding = 'utf-8') as f:
                content = json.loads(f.read())

            self.cache[file] = content

    def update_cache_file (self) -> None:
        """Updates the cache files"""

        for file in self.cache_files:
            _cache_file = os.path.join(self._cache_directory, file)

            with open(_cache_file, 'w', encoding = 'utf-8') as f:
                f.write(json.dumps(self.cache[file], indent = 4))

    @loop(hours = 24)
    async def backup_cache (self) -> None:
        """Creates a backup of cache files"""

        await aioshutil.copytree(src = self._cache_directory,
                                 dst = self._cache_backup_directory,
                                 dirs_exist_ok = True)

        await self.common_logger.log(INFO, '```Periodic cache backup complete!```')

    @loop(hours = 24)
    async def update_cache (self):
        await self.update_cache_admin()
        await self.common_logger.log(INFO, '```Cache update complete!```')

        self.update_cache_file()

    async def update_cache_admin (self):
        for guild in self.guilds:
            guild: Guild = guild

            knight_category: CategoryChannel = utils.find(lambda category: category.name == 'KNIGHT BOT', guild.categories)

            if knight_category is None:
                knight_category: CategoryChannel = await guild.create_category(name     = 'KNIGHT BOT',
                                                                               reason   = 'Knight Bot Admin and Log channels required',
                                                                               position = len(guild.categories))
                await knight_category.set_permissions(guild.default_role, read_messages = False)

            if str(guild.id) in self.cache['admin.json'].keys():
                _admin = self.cache['admin.json'][str(guild.id)]['admin']
                _log   = self.cache['admin.json'][str(guild.id)]['log']
            else:
                _admin = await knight_category.create_text_channel(name   = 'knightbot-admin',
                                                                   topic  = 'Admin channel for Knight Bot',
                                                                   reason = 'Channel for admin control of Knight Bot')

                _log = await knight_category.create_text_channel(name   = 'knightbot-log',
                                                                 topic  = 'Logging channel for Knight Bot',
                                                                 reason = 'Channel for logging Knight Bot logs')

                self.cache['admin.json'][str(guild.id)] = {
                    "admin": str(_admin.id),
                    "log": str(_log.id)
                }

        await self.common_logger.log(INFO, '```Cache update for admin.json complete!```')
