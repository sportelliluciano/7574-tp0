import logging
import multiprocessing as mp
import multiprocessing.connection

from common.bet_server import BetServer
from .bet_server_proxy import BetServerProxy


class BetWorker:
    def __init__(self):
        self.server = BetServer()
        self._peers = []
        quit_pipe_rx, quit_pipe_tx = mp.Pipe()
        self._peers.append(quit_pipe_rx)
        self.quit_pipe = quit_pipe_tx
        self.worker = mp.Process(target=self.__run)

    def get_client(self):
        client = BetServerProxy()
        self._peers.append(client.get_pipe())
        return client

    def start(self):
        self.worker.start()

    def stop(self):
        self.quit_pipe.send(None)
        self.worker.join()

    def __run(self):
        logging.info("[BET WORKER] started")
        quit_signal = False
        while not quit_signal:
            logging.info("[BET WORKER] waiting for peer")
            ready_peers = multiprocessing.connection.wait(self._peers)
            for peer in ready_peers:
                logging.info("[BET WORKER] new peer received")
                cmd = peer.recv()
                if not cmd:
                    logging.info(
                        "[BET WORKER] quit signal -- finishing requests and closing"
                    )
                    quit_signal = True
                    continue
                response = cmd.apply(self.server)
                peer.send(response)
