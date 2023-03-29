import struct

from enum import Enum
from dataclasses import dataclass


class CommandTag(Enum):
    STORE_BET = 0b001


@dataclass
class CommandHeader:
    PAYLOAD_FMT = ">H"

    @staticmethod
    def byte_length():
        return struct.calcsize(CommandHeader.PAYLOAD_FMT)

    @staticmethod
    def from_bytes(payload):
        tag_and_length = struct.unpack(CommandHeader.PAYLOAD_FMT, payload)[0]
        tag = CommandTag(tag_and_length >> 13)
        length = tag_and_length & 0b0001_1111_1111_1111
        return CommandHeader(tag, length)

    tag: CommandTag
    length: int


@dataclass
class RawCommand:
    header: CommandHeader
    payload: bytes
