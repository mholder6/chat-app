#!/usr/bin/env python3

'''
The client that connects to the server.
'''
import socket
import os
import sys
import threading

__author__ = 'Mariah Holder'
__version__ = 'Dec 2023'
__pylint__ = 'v1.8.3.'

PORT = 3280


class SendingThread(threading.Thread):
    '''
    Sending thread subclassing Thread.
    Fields: connection and name.
    '''

    def __init__(self, conn, name):
        super().__init__()
        self.conn = conn
        self.name = name

    def run(self):
        '''
        Sends messages to the server.
        Typing 'bye' will close the connection and exit the application.
        '''
        while True:
            print(f'{self.name}: ', end='')
            sys.stdout.flush()
            message = sys.stdin.readline()[:-1]

            if message == 'bye':
                self.conn.sendall(f'{self.name}: {message}\n'.encode())
                self.conn.sendall(f'Server: {self.name} has left the chat room.'.encode())
                break
            else:
                self.conn.sendall(f'{self.name}: {message}'.encode())

        print('\nGood bye!')
        self.conn.close()
        os._exit(0)  # pylint: disable=protected-access


class ReceivingThread(threading.Thread):
    '''
    Receiving thread listens for incoming messages from the server.
    Fields: connection and name.
    '''
    def __init__(self, conn, name):
        super().__init__()
        self.conn = conn
        self.name = name

    def run(self):
        '''
        Receives and prints data from server.
        '''
        while True:
            message = self.conn.recv(1024).decode('ascii')
            if message:
                #print('\r{}\n{}: '.format(message, self.name), end = '')
                print(f'\r{message}\n{self.name}: ', end='')
            else:
                print('Server went offline.')
                self.conn.close()
                os._exit(0) # pylint: disable=protected-access

class Client: # pylint: disable=too-few-public-methods
    '''
    The client needs a thread for sending and one for receiving data.
    '''

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        '''
        Starts the client.
        '''

        print('Type \'bye\' at any time to leave the chat room...')
        self.client_socket.connect((self.host, self.port))
        name = input('Please type your name: ')
        sending = SendingThread(self.client_socket, name)
        receiving = ReceivingThread(self.client_socket, name)
        sending.start()
        receiving.start()
        self.client_socket.sendall(f'Server: {name} has joined the room. Say hi!'.encode())


def main():
    '''
    Lanuches the app.
    '''
    client = Client('localhost', PORT)
    try:
        client.start()
    except ConnectionRefusedError as err:
        print(f'Start the server first.{os.linesep}{err}')
    except KeyboardInterrupt:
        print(os.linesep + 'Interrupted by user. Good bye!')
        sys.exit(0)


if __name__ == '__main__':
    main()
