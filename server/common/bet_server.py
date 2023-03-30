import logging
import multiprocessing as mp
import multiprocessing.connection
from common.storage import Storage

from common.utils import has_won, load_bets, store_bets


class BetServer:
    def __init__(self, quit_pipe=None):
        self.storage = Storage(open_agencies={i for i in range(1, 6)}, winners=None)
        self._peers = []
        self.quit_pipe = quit_pipe
        if quit_pipe:
            self._peers.append(quit_pipe)

    def add_peer(self, peer):
        self._peers.append(peer.get_pipe())

    def run(self):
        while True:
            logging.info("BETSERVER waiting for peer connections")
            ready_peers = multiprocessing.connection.wait(self._peers)
            logging.info("BETSERVER waiting for peer connections")
            for peer in ready_peers:
                if peer == self.quit_pipe:
                    return
                self._handle_peer_request(peer)

    def _handle_peer_request(self, peer):
        logging.info("got request")
        cmd = peer.recv()
        response = cmd.apply(self)
        logging.info("sent response")
        peer.send(response)

    def store_bets(self, bets):
        return store_bets(bets)

    def winners(self):
        if self.storage.winners is not None:
            return self.storage.winners

        if len(self.storage.open_agencies) > 0:
            return None

        bets = load_bets()
        winners = [bet.document for bet in filter(has_won, bets)]
        self.storage.winners = winners
        return self.storage.winners

    def eof(self, agency_id):
        self.storage.open_agencies.discard(agency_id)


class BetStoreBatchCmd:
    def __init__(self, bets):
        self.bets = bets

    def apply(self, bs):
        return bs.store_bets(self.bets)


class BetWinnersCmd:
    def apply(self, bs):
        return bs.winners()


class BetEofCmd:
    def __init__(self, agency_id):
        self.agency_id = agency_id

    def apply(self, bs):
        return bs.eof(self.agency_id)


class BetQuitCmd:
    def apply(self, Bet_server):
        Bet_server.quit = True
