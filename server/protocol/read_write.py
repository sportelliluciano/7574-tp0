class ReadWriteExact:
    """
    Interface for a stream that provides capabilities to write
    and read an exact number of bytes.
    """

    def read_exact(self, n: int) -> bytes:
        raise NotImplementedError

    def write_exact(self, payload: bytes):
        raise NotImplementedError
