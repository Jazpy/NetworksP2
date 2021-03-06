"""
This module handles server side logic, it implements the FSM and connects to
our database for data transmission.

    pydoc -w communication

"""
from random import randint
from select import select
import os, MySQLdb

# Aux functions
def list_to_bytes(l):
    """
    Transforms a list of strings or numbers into bytes for transmission.

    :param l: the list with objects to transform.
    :return: returns nothing
    """
    ret = b''

    for n in l:
        ret = ret + n.to_bytes(1, byteorder = 'big')

    return ret

# Main logic for communication
def client_thread(connection, address):
    """
    Implements the FSM with the app's logic, it also establishes connection to
    a database in order to obtain user information and send image data.

    :param connection: the python socket object, used for transmission.
    :param address: the client's address, used for diagnostics.
    :return: returns nothing
    """
    # Connect to database
    db = MySQLdb.connect(host = 'localhost', user = 'pokeuser',
            passwd = 'poke', db = 'pokedex')
    cursor = db.cursor()


    # Only one user, this can change to add functionality
    user_id = 1

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

        # Monster if to represent the FSM
        if state == 0 and code == 10:

            # Switch state
            state = 2

            # We pick a pokemon id at random and send that, along
            # with the corresponding code
            cursor.execute('SELECT * FROM pokemon')
            total_pokemon = len(cursor.fetchall())
            pokemon_id = randint(1, total_pokemon)

            reply = list_to_bytes([20, pokemon_id])

        elif (state == 2 or state == 4) and code == 30:
            # Reduce available attempts
            attempts = attempts - 1

            # Check if client captured pokemon, 50% chance
            caught = True
            if randint(0, 9) >= 5:
                caught = False

            if caught:
                state = 5

                out_code = (22).to_bytes(1, byteorder = 'big')
                pokemon_id_code = pokemon_id.to_bytes(1, byteorder = 'big')


                # Get image bytes, first, open the image using database info, store size
                cursor.execute('SELECT image_path FROM pokemon WHERE pokemon_id = ' +
                        str(pokemon_id))
                path = cursor.fetchall()[0][0]

                image_size = os.path.getsize(path)
                image_size_code = image_size.to_bytes(4, byteorder = 'big')

                # Open image and transform to bytes
                image_bytes = b''
                with open(path, 'rb') as image:
                    f = image.read()
                    image_bytes = bytes(f)

                reply = out_code + pokemon_id_code + image_size_code + image_bytes

                # Update the database if needed
                cursor.execute('SELECT * FROM caught WHERE user_id = ' + str(user_id) +
                        ' AND pokemon_id = ' + str(pokemon_id))

                if not cursor.fetchall():
                    cursor.execute('INSERT INTO caught(user_id, pokemon_id) VALUES (' +
                            str(user_id) + ', ' + str(pokemon_id) + ')')

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

        elif (state == 2 or state == 4) and code == 31:
            state = 6
        elif (state == 5 or state == 6) and code == 32:
            close_connection = True
            reply = list_to_bytes([32])

        # Send the message
        connection.sendall(reply)

        # Check if connection ended
        if close_connection or not data:
            break

    connection.close()
    db.commit()

    print('Closed connection to ' + address[0] + ':' + str(address[1]))
