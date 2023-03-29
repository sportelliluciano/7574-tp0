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

        name_len = command.payload[fixed_part_size:].index(b"\0")
        name = str(
            command.payload[fixed_part_size : fixed_part_size + name_len], "utf-8"
        )
        last_name = str(command.payload[fixed_part_size + name_len + 1 : -1], "utf-8")
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

    agency: int
    name: str
    last_name: str
    id: int
    birth_year: int
    birth_month: int
    birth_day: int
    number_to_bet: int
