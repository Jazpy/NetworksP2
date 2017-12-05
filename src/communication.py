# Main logic for communication

def client_thread(connection, address):
    
    # Set initial state
    state = 0

    # Main thread loop
    while True:

        # Receive from client
        data = connection.recv(1024)
        code = int.from_bytes(data[:2], byteorder = 'big')

        reply = 'Received code: ' + str(code)

        # Check if connection ended
        if not data:
            break

        connection.sendall(reply.encode('utf-8'))

    connection.close()
    print('Closed connection to ' + address[0] + ':' + str(address[1]))
