from PyQt5.QtCore import QTimer
from model.game import GameState

from fa import maps


class GameAnnouncer:
    ANOUNCE_DELAY_SECS = 35

    def __init__(self, gameset, me, colors, client):
        self._gameset = gameset
        self._me = me
        self._colors = colors
        self._client = client

        self._gameset.newLobby.connect(self._announceHosting)
        self._gameset.newLiveReplay.connect(self._announceReplay)

        self.announce_games = True
        self.announce_replays = True
        self._delayed_host_list = []

    def _is_friend_host(self, game):
        return (game.host_player is not None
                and self._me.isFriend(game.host_player.id))

    def _announceHosting(self, game):
        if not self._is_friend_host(game) or not self.announce_games:
            return
        announce_delay = QTimer()
        announce_delay.setSingleShot(True)
        announce_delay.setInterval(self.ANNOUNCE_DELAY_SECS * 1000)
        announce_delay.timeout.connect(self._delayed_announce_hosting)
        announce_delay.start()
        self._delayed_host_list.append((announce_delay, game))

    def _delayed_announce_hosting(self):
        timer, game = self._delayed_host_list.pop(0)

        if (not self._is_friend_host(game) or
           not self.announce_games or
           game.state != GameState.PLAYING):
            return
        self._announce(game, "hosting")

    def _announceReplay(self, game):
        if not self._is_friend_host(game) or not self.announce_replays:
            return
        self._announce(game, "playing live")

    def _announce(self, game, activity):
        url = game.url(game.host_player.id)
        url_color = self._colors.getColor("url")
        mapname = maps.getDisplayName(game.mapname)
        fmt = 'is {} {}<a style="color:{}" href="{}">{}</a> (on {})'
        if game.featured_mod == "faf":
            modname = ""
        else:
            modname = game.featured_mod + " "
        msg = fmt.format(activity, modname, url_color, url, mapname)
        self._client.forwardLocalBroadcast(game.host, msg)
