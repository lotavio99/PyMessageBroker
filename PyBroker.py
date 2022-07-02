from pprint import pprint
from threading import Thread
from hashlib import md5
import socket


class PyBroker(object):
    def __init__(self, host='localhost', port=53):
        self.hosts_for_broadcast = dict()
        self.connections = dict()
        self.socket = None
        self.host = host
        self.port = port

    def connect(self):
        self.socket = socket.socket()
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

    def threading_loop(self):
        while 1:
            conn, info = self.socket.accept()
            id_client = self.get_id(info)
            if id_client not in self.connections:
                self.connections[id_client] = {'socket': conn, 'chan': None}
            Thread(target=self.read_message, args=[conn, info]).start()

    def read_message(self, conn, info):
        while 1:
            try:
                msg = conn.recv(1024)
                msg = msg.decode()
            except ConnectionResetError:
                print(info, 'Desconectou-se')
                break
            client_id = self.get_id(info)
            if msg.startswith('sub') and len(msg.split(' ')) == 2:
                channel = msg.split(' ')[1]
                self.connections[client_id]['chan'] = channel
                if channel not in self.hosts_for_broadcast:
                    self.hosts_for_broadcast[channel] = [client_id]
                else:
                    self.hosts_for_broadcast[channel].append(client_id)
            else:
                for client in self.hosts_for_broadcast[self.connections[client_id]['chan']]:
                    if client in self.connections and conn != self.connections[client]['socket']:
                        try:
                            self.connections[client]['socket'].send(msg.encode())
                        except ConnectionResetError:
                            print(info, 'Desconectou-se')
                            del self.connections[client]

    def loop(self):
        Thread(target=self.threading_loop, args=[]).start()

    def broadcast(self):
        pass

    def get_id(self, info):
        return md5(str(info).encode()).hexdigest()


def cli(broker: PyBroker):
    while 1:
        cmd = input('..::')
        if cmd == 'list connections':
            pprint(broker.connections)

        if cmd == 'list hosts for broadcast':
            pprint(broker.hosts_for_broadcast)

        if cmd.startswith('send_message'):
            act, to, msg = cmd.split(' ')
            broker.connections[to]['socket'].send(msg.encode())


def iniciar_cli(broker):
    Thread(target=cli, args=[broker]).start()


def main():
    broker = PyBroker(port=53)
    iniciar_cli(broker)
    broker.connect()
    broker.loop()


if __name__ == '__main__':
    main()