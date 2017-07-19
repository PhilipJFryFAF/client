from PyQt5.QtCore import QObject, pyqtSignal

class Player(QObject):
    updated = pyqtSignal(object)

    """
    Represents a player the client knows about, mirrors the similar class in the server.
    Needs to be constructed using a player_info message sent from the server.
    """
    def __init__(self,
                 id_,
                 login,
                 global_rating=None,
                 ladder_rating=None,
                 number_of_games=None,
                 avatar=None,
                 country=None,
                 clan=None,
                 league=None):
        QObject.__init__(self)
        """
        Initialize a Player
        """
        # Required fields
        self.id = int(id_)
        self.login = login

        self.global_rating = (1500, 500)
        self.ladder_rating = (1500, 500)
        self.number_of_games = 0
        self.avatar = None
        self.country = None
        self.clan = None
        self.league = None

        self.update(id_, login, global_rating, ladder_rating, number_of_games,
                    avatar, country, clan, league)

    def update(self,
               id_=None,
               login=None,
               global_rating=None,
               ladder_rating=None,
               number_of_games=None,
               avatar=None,
               country=None,
               clan=None,
               league=None):

        # Ignore id and login (they are be immutable)
        # Login should be mutable, but we look up things by login right now
        if global_rating:
            self.global_rating = global_rating
        if ladder_rating:
            self.ladder_rating = ladder_rating
        if number_of_games:
            self.number_of_games = number_of_games
        if avatar:
            self.avatar = avatar
        if country:
            self.country = country
        if clan:
            self.clan = clan
        if league:
            self.league = league

        self.updated.emit(self)

    def __hash__(self):
        """
        Index by id
        """
        return self.id.__hash__()

    def __index__(self):
        return self.id

    def __eq__(self, other):
        """
        Equality by id

        :param other: player object to compare with
        """
        if not isinstance(other, Player):
            return False
        return other.id == self.id

    def rounded_rating_estimate(self):
        """
        Get the conservative estimate of the players global trueskill rating, rounded to nearest 100
        """
        return round((self.rating_estimate()/100))*100

    def rating_estimate(self):
        """
        Get the conservative estimate of the players global trueskill rating
        """
        return int(max(0, (self.global_rating[0] - 3 * self.global_rating[1])))

    def ladder_estimate(self):
        """
        Get the conservative estimate of the players ladder trueskill rating
        """
        return int(max(0, (self.ladder_rating[0] - 3 * self.ladder_rating[1])))

    @property
    def rating_mean(self):
        return self.global_rating[0]

    @property
    def rating_deviation(self):
        return self.global_rating[1]

    @property
    def ladder_rating_mean(self):
        return self.ladder_rating[0]

    @property
    def ladder_rating_deviation(self):
        return self.ladder_rating[1]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "Player(id={}, login={}, global_rating={}, ladder_rating={})".format(
            self.id,
            self.login,
            self.global_rating,
            self.ladder_rating
        )