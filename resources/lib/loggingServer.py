import logging
import pickle
import socketserver


class LogRecordStreamHandler(socketserver.StreamRequestHandler):
    def handle(self):
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = int.from_bytes(chunk, "big")
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = pickle.loads(chunk)
            record = logging.makeLogRecord(obj)
            logger = logging.getLogger(record.name)
            logger.handle(record)


def setup_logging_server():
    server = socketserver.TCPServer(("localhost", 9000), LogRecordStreamHandler)
    server.serve_forever()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    setup_logging_server()
