import logging
import struct

from dataclasses import dataclass
from typing import List

from protocol.command import RawCommand
from protocol.store_bet import StoreBetCommand


@dataclass
class SendBatchCommand:
    @staticmethod
    def from_raw(command: RawCommand):
        n_bets = struct.unpack(">H", command.payload[:2])[0]
        payload = command.payload[2:]
        bets = []
        for _ in range(n_bets):
            remaining_bytes, bet = StoreBetCommand.from_batch(payload)
            logging.info("action: got bet | result: success | bet: %r", bet)
            payload = remaining_bytes
            bets.append(bet)

        return SendBatchCommand(bets)

    bets: List[StoreBetCommand]
