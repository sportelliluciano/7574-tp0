import struct

from dataclasses import dataclass

from protocol.command import RawCommand


@dataclass
class EofCommand:
    PAYLOAD_FMT = ">B"

    @staticmethod
    def from_raw(command: RawCommand):
        agency = struct.unpack(EofCommand.PAYLOAD_FMT, command.payload)[0]
        return EofCommand(
            agency=agency,
        )

    agency: int
