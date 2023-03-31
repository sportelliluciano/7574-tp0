import struct

from dataclasses import dataclass

from protocol.response import Response, StatusCode


@dataclass
class WinnersCommand:
    @staticmethod
    def from_raw(raw_command):
        agency_id = int(raw_command.payload[0])
        return WinnersCommand(agency_id)

    agency_id: int


class WinnersResponse:
    @staticmethod
    def ok(winners: list):
        n_winners = struct.pack(">H", len(winners))
        payload = n_winners + b"".join(
            [struct.pack(">I", int(winner_id)) for winner_id in winners],
        )
        return Response(StatusCode.Ok, payload)

    @staticmethod
    def error(message: str):
        return Response(StatusCode.Error, message.encode("utf-8"))
