#!/usr/bin/python

import socket
from _thread import *
from communication import client_thread

def main():
    host = ''
    port = 9999

    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket
    try:
        s.bind((host, port))
    except socket.error as err:
        print('Binding failed, code: ' + str(msg[0]) + ' message: ' + msg[1])
        return

    # Begin listening
    s.listen(5)

    # Main server loop
    while True:

        # Wait on new connection
        connection, address = s.accept()
        print('Connected to ' + address[0] + ':' + str(address[1]))

        # Start a new thread, using function in communication.py
        start_new_thread(client_thread, (connection, address))

if __name__ == '__main__': main()
