#!/usr/bin/python
import socket
from select import select

def main():
    s = socket.socket()
    host = socket.gethostname()
    port = 9999

    s.connect((host, port))

    # Send the initial code
    print('Client:')
    print('Sending code: 10')
    reply = (10).to_bytes(1, byteorder = 'big')
    s.sendall(reply)

    # Persistent variables
    state = 1
    close_connection = False

    while True:
        
        # Clean our variable
        reply = b''

        # Get the server's response
        data = ''
        code = -1

        # Check to see if there is data to read
        r, _, _ = select([s], [], [])
        if r:
            print('e')
            data = s.recv(4096)
            code = int.from_bytes(data[:1], byteorder = 'big')
        print('Client:')
        print('Received code: ' + str(code))

        # Monster if to represent the FSM
        if state == 1 and code == 20:

            # Extract pokemon_id
            pokemon_id = int.from_bytes(data[1:2], byteorder = 'big')

            # Ask for user input
            to_catch = input('Catch pokemon with id ' + str(pokemon_id) + '?')

            # Build reply
            if to_catch == 'y':
                state = 3
                reply = (30).to_bytes(1, byteorder = 'big')
            else:
                state = 7
                reply = (31).to_bytes(1, byteorder = 'big')
        elif state == 3:

            # Check if we caught the pokemon
            if code == 22:
                pokemon_id = int.from_bytes(data[1:2], byteorder = 'big')
                image_size = int.from_bytes(data[2:3], byteorder = 'big')
                image = int.from_bytes(data[3:], byteorder = 'big')
                print('You caught the pokemon with code ' + str(pokemon_id))

                # Switch to termination state
                state = 7
            elif code == 21:
                pokemon_id = int.from_bytes(data[1:2], byteorder = 'big')
                attempts = int.from_bytes(data[2:3], byteorder = 'big')

                # Build reply
                print(str(attempts) + ' attempts remaining')
                to_catch = input('Keep trying to catch id ' + str(pokemon_id) + '?')

                if to_catch == 'y':
                    state = 3
                    reply = (30).to_bytes(1, byteorder = 'big')
                else:
                    state = 7
                    reply = (31).to_bytes(1, byteorder = 'big')

            elif code == 23:
                print('Failed to capture pokemon')

                # Switch to termination state
                state = 7
        elif state == 7:
            close_connection = True
            reply = (32).to_bytes(1, byteorder = 'big')

        s.sendall(reply)

        # Check if connection ended
        if close_connection or not data:
            break
        
    print('Client is closing connection')
    s.close

if __name__ == '__main__': main()
