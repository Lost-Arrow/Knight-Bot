import asyncio
import aiohttp
import json
import requests

from common import (
    requestmethod,
    handle_coc_json_errors
)
from clan import (
    Clan,
    ClanWarLeagueGroup,
    ClanWarLeagueWar,
    ClanWar,
    ClanWarLog,
    ClanMembers
)
from player import (
    Player
)

class Throttler:
    """Class that manages rate limits for interaction with Clash of Clans API"""

    def __init__ (
            self,
            rate_limit: int,
            retry_interval: float
    ) -> None:
        """
        :param: rate_limit
            number of requests per seconds
        :param: retry_interval
            number of seconds to wait retrying in case of failure
        """

        self.rate_limit = rate_limit
        self.retry_interval = retry_interval
        self.lock = asyncio.Lock()

        self._tasks_counter = 0

    async def __aenter__(
            self
    ) -> 'Throttler':

        async with self.lock:
            while True:
                if self._tasks_counter < self.rate_limit:
                    break
                else:
                    await asyncio.sleep(self.retry_interval)
            self._tasks_counter += 1
        return self

    async def __aexit__(
            self,
            exc_type,
            exc_val,
            exc_tb
    ) -> None:
        self._tasks_counter -= 1

class CocRoute:
    base = 'https://api.clashofclans.com/v1'

    def __init__ (self, route: str):
        self.url = self.base + route
        self.url = self.url.replace('#', '%23')

class CocAPIRequestHandler:
    """Clash of Clans API Request Handler"""

    def __init__ (self, method: str, route: str, coroutine):
        self.method = method
        self.route = route
        self.coroutine = coroutine

    @requestmethod
    async def __call__ (self, client: 'CocHTTPClient', *args, **kwargs):
        url = CocRoute(self.route.format(**kwargs)).url
        async with client.throttler:
            async with getattr(client.session, self.method)(
                url = url,
                headers = {
                    'Authorization': f'Bearer {client.token}',
                },
                data = kwargs['data'] if 'data' in kwargs.keys() else {}
            ) as request:
                json_content = await request.json()

            kwargs.update({'url': url,
                           'json': json_content})

            return await self.coroutine(*args, **kwargs)

def coc_request (method, route):
    def get_coroutine (coroutine):
        return CocAPIRequestHandler(method, route, coroutine)
    return get_coroutine

class CocHTTPClient:
    """Class that manages all HTTP interactions with the Clash of Clans API

    Clash of Clans API: https://developer.clashofclans.com/
    """

    # noinspection PyTypeChecker
    def __init__(
            self,
            email: str,
            password: str,
            throttler: Throttler,
            key_name: str = 'Clash of Clans',
            key_description: str = 'Clash of Clans API Key',
            key_scopes: str = 'clash'
    ) -> None:
        self._api_key = None
        self.api_keys = {}
        self.email = email
        self.ip: str = None
        self.password = password
        self.session: aiohttp.ClientSession = None
        self.token = None
        self.throttler = throttler
        self.key_name = key_name
        self.key_description = key_description
        self.key_scopes = key_scopes

        self._login_response = {}
        self._session_cookie = {}

        asyncio.ensure_future(self.async_init())

    async def async_init (
            self
    ) -> None:
        self.session = aiohttp.ClientSession()
        self._set_ip()

    async def __aenter__ (
            self
    ) -> 'CocHTTPClient':
        return self

    async def __aexit__(
            self,
            exc_type,
            exc_val,
            exc_tb
    ) -> None:
        pass

    async def _set_token (
            self
    ) -> None:
        all_ips = set([ip for key in self.api_keys for ip in key['cidrRanges']])

        if self.ip not in all_ips:
            raise KeyError(f'No API Key could be found for your currently used IP Address {self.ip}!\nPlease create a new key!')
            # print(f'No API Key could be found for your currently used IP Address {self.ip}!\nCreating new key!')
            # all_ips.add(self.ip)
            # self.token = await self.create_key(all_ips)
        else:
            for key in self.api_keys:
                if self.ip in key['cidrRanges']:
                    self.token = key['key']
                    break

    @requestmethod
    def _set_ip (
            self
    ) -> None:
        with requests.get(
                url = 'https://httpbin.org/ip'
        ) as request:
            self.ip = request.json()['origin']

    @requestmethod
    async def _get_api_keys (
            self
    ) -> dict:
        async with self.session.post(
            url  = 'https://developer.clashofclans.com/api/apikey/list',
            json = {},

        ) as request:
            _api_keys = await request.json()
            handle_coc_json_errors(_api_keys)
            self.api_keys = _api_keys['keys']
        return self.api_keys

    # @requestmethod
    # async def create_key (
    #         self,
    #         ips: set
    # ):
    #     async with self.session.post(
    #         url = 'https://developer.clashofclans.com/api/apikey/create',
    #         headers = {
    #             'cookie': f'session={self._session_cookie};'
    #                       f'game-api-url={self._login_response["swaggerUrl"]};'
    #                       f'game-api-token={self._login_response["temporaryAPIToken"]}',
    #             'content-type': 'application/json'
    #         },
    #         data = {
    #             'name': self.key_name,
    #             'description': self.key_description,
    #             'scopes': self.key_scopes,
    #             'cidrRanges': [self.ip]
    #         }
    #     ) as request:
    #         content = await request.json()
    #     return content['key']['key']

    @requestmethod
    async def login (
            self
    ) -> dict:

        async with self.session.post(
            url  = 'https://developer.clashofclans.com/api/login',
            json = {
                "email": self.email,
                "password": self.password
            }
        ) as request:
            self._login_response = await request.json()
            handle_coc_json_errors(self._login_response)
            self._session_cookie = request.cookies.get('session').value

        await self._get_api_keys()
        await self._set_token()

        return self._login_response

    async def logout (
            self
    ) -> None:
        await self.session.close()

    # ------- Player Methods -------- #

    # noinspection PyUnusedLocal
    @staticmethod
    @coc_request(
        method = 'get',
        route = '/players/{player_tag}'
    )
    async def get_player (
            *args,
            **kwargs
    ) -> Player:
        return Player(kwargs['json'])

    # @staticmethod
    # @coc_request(method = 'post', route = '/players/{player_tag}/verifytoken)')
    # async def verify_player (*args, **kwargs):
    #     print(kwargs['json'])

    # ------- Clan Methods -------- #

    # noinspection PyUnusedLocal
    @staticmethod
    @coc_request(
        method = 'get',
        route = '/clans/{clan_tag}/currentwar/leaguegroup'
    )
    async def get_clan_war_league_group (
            *args,
            clan_tag: str,
            **kwargs
    ) -> ClanWarLeagueGroup:
        return ClanWarLeagueGroup(kwargs['json'])

    # noinspection PyUnusedLocal
    @staticmethod
    @coc_request(
        method = 'get',
        route = '/clanwarleagues/wars/{war_tag}'
    )
    async def get_clan_war_league_war (
            *args,
            war_tag: str,
            **kwargs
    ) -> ClanWarLeagueWar:
        return ClanWarLeagueWar(kwargs['json'])

    # noinspection PyUnusedLocal
    @staticmethod
    @coc_request(
        method = 'get',
        route = '/clans/{clan_tag}/warlog')
    async def get_clan_war_log (
            *args,
            clan_tag: str,
            **kwargs
    ) -> ClanWarLog:
        return ClanWarLog(kwargs['json'])

    # noinspection PyUnusedLocal
    @staticmethod
    @coc_request(
        method = 'get',
        route = '/clans/{clan_tag}/currentwar'
    )
    async def get_clan_current_war (
            *args,
            clan_tag: str,
            **kwargs
    ) -> ClanWar:
        return ClanWar(kwargs['json'])

    # noinspection PyUnusedLocal
    @staticmethod
    @coc_request(
        method = 'get',
        route = '/clans/{clan_tag}'
    )
    async def get_clan (
            *args,
            clan_tag: str,
            **kwargs
    ) -> Clan:
        return Clan(kwargs['json'])

    # noinspection PyUnusedLocal
    @staticmethod
    @coc_request(
        method = 'get',
        route =  '/clans/{clan_tag}/members'
    )
    async def get_clan_members (
            *args,
            clan_tag: str,
            **kwargs
    ) -> ClanMembers:
        return ClanMembers(kwargs['json'])
