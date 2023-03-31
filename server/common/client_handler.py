import logging

from common.net_reader_writer import NetReaderWriter
from common.utils import Bet, has_won, load_bets, store_bets
from protocol.command import CommandTag
from protocol.eof import EofCommand
from protocol.lottery_stream import LotteryStream
from protocol.response import Response
from protocol.store_bet import StoreBetCommand
from protocol.send_batch import SendBatchCommand
from protocol.winners import WinnersCommand, WinnersResponse


class ClientHandler:
    def __init__(self, connection, storage):
        self.stream = LotteryStream(NetReaderWriter(connection))
        self.commands = {
            CommandTag.STORE_BET: self._store_bet,
            CommandTag.SEND_BATCH: self._send_batch,
            CommandTag.EOF: self._eof,
            CommandTag.WINNERS: self._winners,
        }
        self.storage = storage

    def run(self):
        logging.info("action: read_command | result: in_progress")
        command = self.stream.read_command()
        logging.info("action: read_command | result: success | command: %r", command)
        controller = self.commands.get(command.header.tag, None)
        if controller:
            logging.info(
                "action: get_controller | result: success | tag: %r | length: %r",
                command.header.tag,
                command.header.length,
            )
            response = controller(command)
            logging.info(
                "action: send_response | result: success | response: %r",
                response,
            )
            self.stream.write_response(response)
        else:
            logging.info(
                "action: get_controller | result: fail | tag: %r | length: %r",
                command.header.tag,
                command.header.length,
            )
            self.stream.write_response(Response.error("Invalid tag"))

    def _store_bet(self, raw_command):
        store_bet_data = StoreBetCommand.from_raw(raw_command)
        logging.info("action: store_bet | result: success | bet: %r", store_bet_data)
        bet = self.__create_bet(store_bet_data)
        logging.info("action: construct_bet | result: success | bet: %r", bet)
        store_bets([bet])
        return Response.ok()

    def _send_batch(self, raw_command):
        batch = SendBatchCommand.from_raw(raw_command)
        logging.info("action: store_batch | result: in_progress")
        store_bets([self.__create_bet(store_bet_data) for store_bet_data in batch.bets])
        logging.info("action: store_batch | result: success")
        return Response.ok()

    def _eof(self, raw_command):
        eof = EofCommand.from_raw(raw_command)
        self.storage.open_agencies.discard(eof.agency)
        logging.info(
            "action: agency_eof | result: success | agency_id: %d",
            eof.agency,
        )
        return Response.ok()

    def _winners(self, raw_command):
        cmd = WinnersCommand.from_raw(raw_command)
        if len(self.storage.open_agencies) != 0:
            return WinnersResponse.error("No results yet.")

        if self.storage.winners is None:
            logging.info("action: sorteo | result: success")
            bets = load_bets()
            self.storage.winners = {}
            for bet in filter(has_won, bets):
                winners = self.storage.winners.get(bet.agency, [])
                winners.append(bet.document)
                self.storage.winners[bet.agency] = winners

        logging.info(
            "action: winners | result: success | winners: %d", len(self.storage.winners.get(cmd.agency_id, []))
        )
        return WinnersResponse.ok(self.storage.winners.get(cmd.agency_id, []))

    def __create_bet(self, store_bet_data):
        return Bet(
            agency=store_bet_data.agency,
            first_name=store_bet_data.name,
            last_name=store_bet_data.last_name,
            document=store_bet_data.id,
            birthdate=f"{store_bet_data.birth_year:04}-{store_bet_data.birth_month:02}-{store_bet_data.birth_day:02}",
            number=store_bet_data.number_to_bet,
        )
