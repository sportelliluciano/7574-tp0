import logging


from protocol.command import CommandHeader, RawCommand
from protocol.read_write import ReadWriteExact


class LotteryStream:
    def __init__(self, stream: ReadWriteExact):
        self.stream = stream

    def read_command(self) -> RawCommand:
        logging.info(
            "action: read_exact | result: in_progress | n_bytes: %r",
            CommandHeader.byte_length(),
        )
        data = self.stream.read_exact(CommandHeader.byte_length())
        header = CommandHeader.from_bytes(data)
        logging.info(
            "action: read_exact | result: success | result: %r",
            header,
        )
        logging.info(
            "action: read_exact | result: in_progress | n_bytes: %r",
            header.length,
        )
        payload = self.stream.read_exact(header.length)
        logging.info(
            "action: read_exact | result: success | result: %r",
            payload,
        )
        return RawCommand(header, payload)

    def write_response(self, response):
        self.stream.write_exact(response.to_bytes())
