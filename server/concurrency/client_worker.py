import logging
import multiprocessing as mp
import os


from common.client_handler import ClientHandler


class ClientWorker:
    def __init__(self, input_queue, bet_server):
        self.input_queue = input_queue
        self.bet_server = bet_server
        self.worker = mp.Process(target=self.__run)

    def start(self):
        self.worker.start()

    def stop(self):
        self.worker.join()

    def __run(self):
        logging.info(f"[WORKER {os.getpid()}] action: start | result: success")
        while connection := self.input_queue.get(block=True):
            try:
                logging.info(
                    f"[WORKER {os.getpid()}] action: handle_client | result: in_progress"
                )
                handler = ClientHandler(connection, self.bet_server)
                handler.run()
                logging.info(
                    f"[WORKER {os.getpid()}] action: handle_client | result: success"
                )
            except OSError as e:
                logging.error(
                    f"[WORKER {os.getpid()}] action: handle_client | result: fail | error: {e}"
                )
            finally:
                connection.close()

        logging.info(f"[WORKER {os.getpid()}] action: shutdown | result: success")
