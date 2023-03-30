import multiprocessing as mp
import signal
import socket
import logging
from common.bet_server import BetServer
from common.bet_server_facade import BetServerFacade

from common.client_handler import ClientHandler


N_WORKERS = 8


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(("", port))
        self._server_socket.listen(listen_backlog)
        self._graceful_quit = False
        signal.signal(signal.SIGTERM, self.__handle_sigterm)

    def run(self):
        """
        Server loop.

        Waits for new connections and handles clients sequentially.
        """
        bets_worker_quit, bwq_rx = mp.Pipe()
        bet_server = BetServer(bwq_rx)
        clients_queue = mp.Queue()
        bets_facades = [BetServerFacade() for _ in range(N_WORKERS)]
        for bets in bets_facades:
            bet_server.add_peer(bets)

        workers = [
            mp.Process(target=worker_main, args=(clients_queue, bets))
            for bets in bets_facades
        ]

        bets_worker = mp.Process(target=bet_server.run)
        bets_worker.start()

        for worker in workers:
            worker.start()

        while not self._graceful_quit:
            try:
                client_sock = self.__accept_new_connection()
                logging.info(f"action: new_connection | result: success")
                clients_queue.put(client_sock)
            except OSError:
                if self._graceful_quit:
                    logging.info(f"action: graceful_quit | result: success")
                    break

                # If we're not in the middle of a graceful shutdown then
                # something bad may have happened -- rethrow exception.
                raise

        logging.info("Terminating workers...")
        for worker in workers:
            clients_queue.put(None)
            worker.join()

        logging.info("Terminating Bet server...")
        bets_worker_quit.send(None)
        bets_worker.join()
        logging.info("Finished")

    def __accept_new_connection(self):
        """
        Accept new connections

        Function blocks until a connection to a client is made.
        Then connection created is printed and returned
        """

        # Connection arrived
        logging.info("action: accept_connections | result: in_progress")
        c, addr = self._server_socket.accept()
        logging.info(f"action: accept_connections | result: success | ip: {addr[0]}")
        return c

    def __handle_sigterm(self, *_):
        logging.info(f"action: sigterm | result: success")
        self._graceful_quit = True
        self._server_socket.close()


def worker_main(clients_queue, bets):
    """
    Read message from a specific client socket and closes the socket

    If a problem arises in the communication with the client, the
    client socket will also be closed
    """
    while True:
        client_sock = clients_queue.get(block=True)
        if client_sock is None:
            break

        try:
            logging.info("action: client_handler | result: in_progress")
            handler = ClientHandler(client_sock, bets)
            handler.run()
            logging.info("action: client_handler | result: success")
        except OSError as e:
            logging.error(f"action: client_handler | result: fail | error: {e}")
        finally:
            client_sock.close()

    logging.info("worker finished")
