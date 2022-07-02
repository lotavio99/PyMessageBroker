import socket
import time
from threading import Thread


class ClientPyBroker(object):
    def __init__(self, host='localhost', port=53):
        self.host = host
        self.port = port
        self.socket = None
        self.thread = None

    def connect(self):
        self.socket = socket.socket()
        self.socket.connect((self.host, self.port))

    def sub_channel(self, chl: str):
        self.socket.send(f'sub {chl}'.encode())
        time.sleep(1)

    def send_message(self, msg: str):
        self.socket.send(f'{msg}'.encode())
        pass

    def threading_loop(self):
        while True:
            msg = self.socket.recv(1024).decode()
            print(msg)

    def loop(self):
        self.thread = Thread(target=self.threading_loop, args=[])
        self.thread.start()


def cli(cpb: ClientPyBroker):
    while True:
        cmd = input('')
        if cmd == 'quit' or cmd == 'q':
            cpb.thread.join()
            quit()
        elif cmd == 'help':
            print('*'*20)
            print('1 - Op')
            print('2 - Op')
            print('*' * 20)
        else:
            cpb.send_message(cmd)
    pass


def main():
    cpb = ClientPyBroker()
    cpb.connect()
    cpb.sub_channel('teste')
    cpb.send_message('ok')
    cpb.loop()
    cli(cpb)

    pass


if __name__ == '__main__':
    main()