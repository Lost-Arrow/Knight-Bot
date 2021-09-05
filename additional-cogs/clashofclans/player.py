from common import (
    CocObject
)

class Player (CocObject):
    # noinspection PyTypeChecker
    def __init__ (
            self,
            data: dict
    ) -> None:

        self.tag: CocObject = None
        self.name: CocObject = None
        self.townHallLevel: CocObject = None
        self.expLevel: CocObject = None
        self.trophies: CocObject = None
        self.bestTrophies: CocObject = None
        self.warStars: CocObject = None
        self.attackWins: CocObject = None
        self.defenseWins: CocObject = None
        self.builderHallLevel: CocObject = None
        self.versusTrophies: CocObject = None
        self.bestVersusTrophies: CocObject = None
        self.versusBattleWins: CocObject = None
        self.role: CocObject = None
        self.donations: CocObject = None
        self.donationsReceived: CocObject = None
        self.clan: CocObject = None
        self.league: CocObject = None
        self.achievements: CocObject = None
        self.versusBattleWinCount: CocObject = None
        self.labels: CocObject = None
        self.troops: CocObject = None
        self.heroes: CocObject = None
        self.spells: CocObject = None

        super().__init__(data)
