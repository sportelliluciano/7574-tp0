import struct

from protocol.response import Response, StatusCode


class WinnersCommand:
    @staticmethod
    def from_raw(_):
        return WinnersCommand()


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
