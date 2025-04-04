import sys
from contextlib import contextmanager


class TeeOutput:
    def __init__(self, buffer):
        self.buffer = buffer

    def write(self, text):
        self.buffer.write(text)
        sys.__stdout__.write(text)

    def flush(self):
        self.buffer.flush()
        sys.__stdout__.flush()


class TeeInput:
    def __init__(self, buffer):
        self.buffer = buffer

    def readline(self, size=-1):
        line = sys.__stdin__.readline(size)
        self.buffer.write(line)
        self.buffer.flush()
        return line


@contextmanager
def redirect_stdin(new_input):
    original_stdin = sys.stdin
    try:
        sys.stdin = new_input
        yield
    finally:
        sys.stdin = original_stdin
