import multiprocessing as mp
import os
import signal
import socket
import logging

from concurrency.bet_worker import BetWorker
from concurrency.client_worker import ClientWorker


class Server:
    def __init__(self, port, listen_backlog, n_workers=0):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(("", port))
        self._server_socket.listen(listen_backlog)
        self._graceful_quit = False
        if n_workers <= 0:
            self.n_workers = os.cpu_count()
        else:
            self.n_workers = n_workers
        self.input_queue = mp.Queue()
        self.bet_worker = BetWorker()
        self.workers = [
            ClientWorker(self.input_queue, self.bet_worker.get_client())
            for _ in range(self.n_workers)
        ]
        signal.signal(signal.SIGTERM, self.__handle_sigterm)

    def _start_workers(self):
        for worker in self.workers:
            worker.start()

    def _stop_workers(self):
        for _ in self.workers:
            self.input_queue.put(None)

        for worker in self.workers:
            worker.stop()

    def run(self):
        """
        Server loop.

        Waits for new connections and handles clients sequentially.
        """
        self.bet_worker.start()
        self._start_workers()

        while not self._graceful_quit:
            try:
                client_sock = self.__accept_new_connection()
                logging.info(f"[SERVER] action: new_connection | result: success")
                self.input_queue.put(client_sock)
            except OSError:
                if self._graceful_quit:
                    logging.info(f"[SERVER] action: graceful_quit | result: success")
                    break

                # If we're not in the middle of a graceful shutdown then
                # something bad may have happened -- rethrow exception.
                raise

        logging.info("[SERVER] terminating workers...")
        self._stop_workers()
        logging.info("[SERVER] terminating Bet worker...")
        self.bet_worker.stop()
        logging.info("[SERVER] finished")

    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        logging.info("[SERVER] action: accept_connections | result: in_progress")
        c, addr = self._server_socket.accept()
        logging.info(f"[SERVER] action: accept_connections | result: success | ip: {addr[0]}")
        return c

    def __handle_sigterm(self, *_):
        logging.info(f"[SERVER] action: sigterm | result: success")
        self._graceful_quit = True
        self._server_socket.close()
