import logging
import multiprocessing as mp


from .bet_command import BetEofCmd, BetStoreBatchCmd, BetWinnersCmd


class BetServerProxy:
    def __init__(self):
        rx, peer = mp.Pipe(duplex=True)
        self.rx = rx
        self.peer = peer

    def get_pipe(self):
        rx = self.rx
        self.rx = None
        return rx

    def _send_cmd(self, cmd):
        logging.info("sending cmd %r", cmd)
        self.peer.send(cmd)
        logging.info("sent")
        return self.peer.recv()

    def store_bets(self, bets):
        return self._send_cmd(BetStoreBatchCmd(bets))

    def winners(self):
        return self._send_cmd(BetWinnersCmd())

    def eof(self, agency_id):
        return self._send_cmd(BetEofCmd(agency_id))
