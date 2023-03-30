import struct


from dataclasses import dataclass
from enum import Enum


class StatusCode(Enum):
    Ok = 0b111
    Error = 0b110


@dataclass
class Response:
    status: StatusCode
    payload: bytes

    @staticmethod
    def ok():
        return Response(StatusCode.Ok, bytes())

    @staticmethod
    def error(message: str):
        return Response(StatusCode.Error, message.encode("utf-8"))

    def to_bytes(self) -> bytes:
        tag_and_length = (self.status.value << 13) | len(self.payload)
        return struct.pack(">H", tag_and_length) + self.payload
