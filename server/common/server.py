import signal
import socket
import logging

from common.client_handler import ClientHandler
from common.storage import Storage


class Server:
    def __init__(self, port, listen_backlog):
        # Initialize server socket
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(("", port))
        self._server_socket.listen(listen_backlog)
        self._graceful_quit = False
        signal.signal(signal.SIGTERM, self.__handle_sigterm)
        self._storage = Storage(open_agencies={i for i in range(1, 6)}, winners=None)

    def run(self):
        """
        Server loop.

        Waits for new connections and handles clients sequentially.
        """
        while not self._graceful_quit:
            try:
                client_sock = self.__accept_new_connection()
                self.__handle_client_connection(client_sock)
            except OSError:
                if self._graceful_quit:
                    logging.info(f"action: graceful_quit | result: success")
                    return

                # If we're not in the middle of a graceful shutdown then
                # something bad may have happened -- rethrow exception.
                raise

    def __handle_client_connection(self, client_sock):
        """
        Read message from a specific client socket and closes the socket

        If a problem arises in the communication with the client, the
        client socket will also be closed
        """
        try:
            logging.info("action: client_handler | result: in_progress")
            handler = ClientHandler(client_sock, self._storage)
            handler.run()
            logging.info("action: client_handler | result: success")
        except OSError as e:
            logging.error(f"action: client_handler | result: fail | error: {e}")
        finally:
            client_sock.close()

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
