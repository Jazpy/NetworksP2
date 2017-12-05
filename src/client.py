#!/usr/bin/python

import socket

def main():
    s = socket.socket()
    host = socket.gethostname()
    port = 9999

    s.connect((host, port))

    while True:
        s.sendall((10).to_bytes(1, byteorder = 'big'))
        print(str(s.recv(1024)))

    s.close

if __name__ == '__main__': main()
