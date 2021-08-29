import asyncio
import platform
import constants

from knight import (
    Knight
)

# When Knight tries to log off, there seems to be an exception being raised
# Magicians at StackOverflow and Discord.py suggested this would fix the issue /shrug
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

default_cogs = [
    'admin',
    'moderation',
    'utility'
]

knight = Knight()

for cog in default_cogs:
    knight.load_extension(f'cogs.{cog}')

knight.run(constants.get_token())
