from common import (
    CocObject
)

class Clan (CocObject):
    def __init__(self, data):
        self.tag: CocObject = None
        self.name: CocObject = None
        self.type: CocObject = None
        self.description: CocObject = None
        self.location: CocObject = None
        self.badgeUrls: CocObject = None
        self.clanLevel: CocObject = None
        self.clanPoints: CocObject = None
        self.clanVersusPoints: CocObject = None
        self.requiredTrophies: CocObject = None
        self.warFrequency: CocObject = None
        self.warWinStreak: CocObject = None
        self.warWins: CocObject = None
        self.warTies: CocObject = None
        self.warLosses: CocObject = None
        self.isWarLogPublic: CocObject = None
        self.warLeague: CocObject = None
        self.members: CocObject = None
        self.memberList: CocObject = None
        self.labels: CocObject = None
        self.chatLanguage: CocObject = None
        self.requiredVersusTrophies: CocObject = None
        self.requiredTownhallLevel: CocObject = None

        super().__init__(data)

class ClanWarLeagueGroup (CocObject):
    def __init__ (self, data):
        self.state: CocObject = None
        self.season: CocObject = None
        self.clans: CocObject = None
        self.rounds: CocObject = None

        super().__init__(data)

class ClanWarLeagueWar (CocObject):
    def __init__ (self, data):
        self.state: CocObject = None
        self.teamSize: CocObject = None
        self.preparationStartTime: CocObject = None
        self.startTime: CocObject = None
        self.endTime: CocObject = None
        self.clan: CocObject = None
        self.opponent: CocObject = None
        self.warStartTime: CocObject = None

        super().__init__(data)

class ClanWar (CocObject):
    def __init__ (self, data):
        self.state: CocObject = None
        self.clan: CocObject = None
        self.opponent: CocObject = None

        super().__init__(data)

class ClanWarLog (CocObject):
    def __init__(self, data):
        self.items: CocObject = None
        self.paging: CocObject = None

        super().__init__(data)

class ClanMembers (CocObject):
    def __init__ (self, data):
        self.items: CocObject = None
        self.paging: CocObject = None

        super().__init__(data)
