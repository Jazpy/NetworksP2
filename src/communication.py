from random import randint
from select import select

# Aux functions
def list_to_bytes(l):
    ret = b''

    for n in l:
        ret = ret + n.to_bytes(1, byteorder = 'big')

    return ret

# Main logic for communication

def client_thread(connection, address):
    
    # Set persistent variables
    state = 0
    attempts = 3
    pokemon_id = 0
    close_connection = False

    # Main thread loop
    while True:

        # Receive from client, parse the code, and clean reply variable
        data = ''
        code = -1

        # Check to see if there is data to read
        r, _, _ = select([connection], [], [])
        if r:
            data = connection.recv(4096)
            code = int.from_bytes(data[:1], byteorder = 'big')

        reply = b''

        # Logging
        print('Server:')
        print('Received code:' + str(code))

        # Monster if to represent the FSM
        if state == 0 and code == 10:

            # Switch state
            state = 2

            # We pick a pokemon id at random and send that, along
            # with the corresponding code
            pokemon_id = randint(0, 9)
            reply = list_to_bytes([20, pokemon_id])

        elif (state == 2 or state == 4) and code == 30:

            # Check if client captured pokemon, 50% chance
            caught = True
            if randint(0, 9) >= 5:
                caught = False

            if caught:
                state = 5

                out_code = (22).to_bytes(1, byteorder = 'big')
                pokemon_id_code = pokemon_id.to_bytes(1, byteorder = 'big')
                image_size = 10
                image_size_code = image_size.to_bytes(4, byteorder = 'big')
                image_code = (0).to_bytes(image_size, byteorder = 'big')
                reply = out_code + pokemon_id_code + image_size_code + image_code

                # Cleanup
                attempts = 3
            else:
                # Check if user is out of attempts
                if attempts == 0:
                    state = 6
                    reply = list_to_bytes([23])

                    # Cleanup
                    attempts = 3
                else:
                    state = 4
                    reply = list_to_bytes([21, pokemon_id, attempts])

            attempts = attempts - 1
        elif (state == 2 or state == 4) and code == 31:
            state = 6
        elif (state == 5 or state == 6) and code == 32:
            close_connection = True
            reply = list_to_bytes([32])

        # Send the message
        print('Server:')
        print('Sending code: ' + str(reply))
        connection.sendall(reply)

        # Check if connection ended
        if close_connection or not data:
            break

    connection.close()
    print('Closed connection to ' + address[0] + ':' + str(address[1]))
