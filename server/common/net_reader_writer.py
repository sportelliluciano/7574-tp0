from protocol.read_write import ReadWriteExact


class NetReaderWriter(ReadWriteExact):
    def __init__(self, socket):
        self.socket = socket

    def read_exact(self, n: int) -> bytes:
        data = self.socket.recv(n)
        while len(data) != n:
            new_data = self.socket.recv(n - len(data))
            data = data + new_data
        return data

    def write_exact(self, payload: bytes):
        bytes_sent = self.socket.send(payload)
        while bytes_sent != len(payload):
            new_bytes_sent = self.socket.send(payload[bytes_sent:])
            bytes_sent += new_bytes_sent
