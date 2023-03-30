import struct

from dataclasses import dataclass

from protocol.command import RawCommand


@dataclass
class StoreBetCommand:
    PAYLOAD_FMT = ">BHIHBB"

    @staticmethod
    def from_raw(command: RawCommand):
        fixed_part_size = struct.calcsize(StoreBetCommand.PAYLOAD_FMT)
        agency, bet, id, birth_year, birth_month, birth_day = struct.unpack(
            StoreBetCommand.PAYLOAD_FMT, command.payload[:fixed_part_size]
        )

        name_start = fixed_part_size
        name_len = command.payload[name_start:].index(b"\0")
        name_end = name_start + name_len
        name = str(command.payload[name_start:name_end], "utf-8")

        last_name_start = name_end + 1
        last_name_len = command.payload[last_name_start:].index(b"\0")
        last_name_end = last_name_start + last_name_len
        last_name = str(command.payload[last_name_start:last_name_end], "utf-8")

        return StoreBetCommand(
            agency=agency,
            name=name,
            last_name=last_name,
            id=id,
            birth_year=birth_year,
            birth_month=birth_month,
            birth_day=birth_day,
            number_to_bet=bet,
        )

    @staticmethod
    def from_batch(payload: bytes):
        fixed_part_size = struct.calcsize(StoreBetCommand.PAYLOAD_FMT)
        agency, bet, id, birth_year, birth_month, birth_day = struct.unpack(
            StoreBetCommand.PAYLOAD_FMT, payload[:fixed_part_size]
        )

        name_start = fixed_part_size
        name_len = payload[name_start:].index(b"\0")
        name_end = name_start + name_len
        name = str(payload[name_start:name_end], "utf-8")

        last_name_start = name_end + 1
        last_name_len = payload[last_name_start:].index(b"\0")
        last_name_end = last_name_start + last_name_len
        last_name = str(payload[last_name_start:last_name_end], "utf-8")

        return payload[last_name_end + 1 :], StoreBetCommand(
            agency=agency,
            name=name,
            last_name=last_name,
            id=id,
            birth_year=birth_year,
            birth_month=birth_month,
            birth_day=birth_day,
            number_to_bet=bet,
        )

    agency: int
    name: str
    last_name: str
    id: int
    birth_year: int
    birth_month: int
    birth_day: int
    number_to_bet: int
