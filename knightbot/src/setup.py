"""
setup.py

Sets up basic requirements for running an instance of Knight Bot

You will be prompted for the following:
    Bot Token
    Instance Name
    Owner Discord ID
"""

import json
import os
import shutil

__author__  = 'Aryan V S'
__email__   = 'avs070518@gmail.com'
__discord__ = 'Arrow#1334'
__support__ = 'https://discord.gg/D4uzqpu2nr'

def setup () -> None:
    """
    Setup for Knight Bot
    
    You will be prompted for a few things that Knight must know about
    before it can be used on your servers
    """

    def create_dir (location: str) -> None:
        print(f'Creating directory: {location}')
        if not os.path.exists(location):
            os.mkdir(location)

    data = {
        'token'          : None,
        'name'           : 'Knight',
        'owner'          : None,
        'support'        : __support__
    }

    env_directory = '../resources/env'

    print()
    print('Hey, I am Knight - a Multipurpose Discord Bot!')
    print()
    print('I will be creating a few directories that I require for working')

    if os.path.exists('../resources'):
        shutil.rmtree('../resources')

    create_dir('../resources')
    create_dir('../resources/cache')
    create_dir('../resources/cache_backup')
    create_dir('../resources/env')
    create_dir('../resources/logs')

    print()
    print('Before you can run me on your favourite servers, I need to know some things that will be a secret between me and you...')
    print('I will ask you questions that you will have to answer correctly for me to run. Let\'s get started!')
    
    print()
    print('What is my token?')
    data['token'] = input('Token: ')
    
    print()
    print(f'Would you like to call me something other than "{data["name"]}"?')
    name = input('Enter name (Press Enter to keep default settings): ')
    if name != '':
        data['name'] = name
    
    print()
    print('What is your Discord ID?')
    data['owner'] = input('Owner ID: ')

    print()
    print('The default bot prefix is "!"')
    prefixes = {
        'default_prefix': '!',
        'custom_prefix': {}
    }
    prefixes_json = json.dumps(prefixes, indent = 4)
    prefix_path = os.path.join(env_directory, 'prefix.json')
    with open(file = prefix_path, mode = 'w', encoding = 'utf-8') as prefix_file:
        prefix_file.write(prefixes_json)

    print()
    print('You\'ve finished setting me up, thanks!')
    print('If everything has been done correctly, you can start using me on your servers now!')
    print('To start me, run bot.py')
    print('If I do not seem to be working, there may have been an error while setting me up')
    print('You can always re-run setup.py to reset to defaults or correct an error that was made')
    print()
    print(f'Author: {__author__} (Discord: {__discord__})')
    print(f'If you\'re stuck, feel free to join {__support__} for help!')
    print()

    data_json = json.dumps(data, indent = 4)
    env_path  = os.path.join(env_directory, 'env.json')
    with open(file = env_path, mode = 'w', encoding = 'utf-8') as env_file:
        env_file.write(data_json)

if __name__ == '__main__':
    setup()
