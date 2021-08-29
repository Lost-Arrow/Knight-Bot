import constants

from abc import (
    abstractmethod
)
from discord import (
    Color,
    Embed,
    Guild,
    utils
)

_log_directory = '../resources/logs'

class _LoggerCategory:
    """Base class for different Logger Types"""

    @property
    def color (self):
        return None

    @property
    def name (self):
        """Returns the class name"""
        return self.__class__.__name__.upper()

class Debug (_LoggerCategory):
    @property
    def color (self):
        return Color.blue()

class Error (_LoggerCategory):
    @property
    def color (self):
        return Color.red()

class Info (_LoggerCategory):
    @property
    def color (self):
        return Color.green()

class _Logger:
    @staticmethod
    def pretty (category: _LoggerCategory, message: str) -> str:
        return f'[{category.name} - {constants.get_current_time()}]: {message}\n'

    @abstractmethod
    async def log (self, category: _LoggerCategory, message: str) -> None:
        raise Exception('Implementation of _Logger.log() not found')

class FileLogger (_Logger):
    """Logger that writes its output to files"""

    def __init__ (self, bot, file: str):
        self.bot  = bot
        self.file = file

    def set_file (self, file: str) -> None:
        self.file = file

    async def log (self, category: _LoggerCategory, message: str) -> None:
        # Log to file
        with open(self.file, 'a', encoding = 'utf-8') as file:
            print(self.pretty(category, message), file = file)

class ChannelLogger (_Logger):
    """Logger that writes its output to a Discord TextChannel"""

    def __init__ (self, bot, channel: int = None):
        self.bot     = bot
        self.channel = channel

    def set_channel (self, channel: int) -> None:
        self.channel = int(channel)

    async def log (self, category: _LoggerCategory, message: str) -> None:
        await self.bot.wait_until_ready()

        if self.channel is None:
            # Log message in all log channels
            for channel in self.bot.cache['admin.json'].values():
                await ChannelLogger(self.bot, int(channel['log'])).log(category, message)
        else:
            # Log message in the channel that has been set
            channel = utils.get(self.bot.get_all_channels(), id = self.channel)

            if channel is None:
                print(f'[Channel has not been set] - {self.pretty(category, message)}')
            else:
                embed = Embed(color       = category.color,
                              description = message,
                              timestamp   = constants.get_current_time(),
                              title       = category.name.upper(),
                              type        = 'rich')
                embed.set_author(name     = self.bot.user.name,
                                 icon_url = self.bot.user.avatar_url)
                await channel.send(embed = embed)

class CommonLogger:
    def __init__ (self, file_logger: FileLogger, channel_logger: ChannelLogger):
        self.file_logger    = file_logger
        self.channel_logger = channel_logger

    async def log (self, category: _LoggerCategory, message: str) -> None:
        await self.file_logger.log(category, message)
        await self.channel_logger.log(category, message)

    async def guild_specific_log(self, guild: Guild, category: _LoggerCategory, message: str):
        channel_id = int(self.channel_logger.bot.cache['admin.json'][str(guild.id)]['log'])
        await ChannelLogger(self.channel_logger.bot, channel_id).log(category, message)

DEBUG = Debug()
ERROR = Error()
INFO  = Info()
