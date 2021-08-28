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

knight = Knight()
knight.load_extension('knightbot.cogs.admin')

knight.run(constants.get_token())
