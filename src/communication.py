# Main logic for communication

def client_thread(connection, address):
    
    # Send initial message
    connection.sendall('Connection established\n'.encode('utf-8'))

    # Main thread loop
    while True:

        # Receive from client
        data = connection.recv(1024)
        reply = 'ACK' + str(data)

        # Check if connection ended
        if not data:
            break

        connection.sendall(reply.encode('utf-8'))

    connection.close()
    print('Closed connection to ' + address[0] + ':' + str(address[1]))
