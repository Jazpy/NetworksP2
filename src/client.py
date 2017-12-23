192#!/usr/bin/python
import socket
import sys
from io import BytesIO
from tkinter import Tk, Label, Button, StringVar
from PIL import Image, ImageTk
from select import select

# Aux function
def code_to_byte(n):
    return n.to_bytes(1, byteorder = 'big')

class poke_client:
    def __init__(self, master):
        # GUI stuff
        self.master = master
        master.title("Pokedex")
        master.minsize(width = 640, height = 480)

        self.poke_label = Label(master)
        self.poke_label.pack()

        self.server_msg = StringVar()
        self.server_msg.set('Connecting to server')
        self.label = Label(master, textvariable = self.server_msg)
        self.label.pack()

        self.yes_button = Button(master, text="Yes", command = self.yes)
        self.yes_button.pack()

        self.no_button = Button(master, text="No", command = self.no)
        self.no_button.pack()

        self.close_button = Button(master, text="Close", command = self.close)
        self.close_button.pack()

        # Socket and app stuff
        self.s = socket.socket()


        #lines added by Davif,

        dns = socket.gethostbyaddr(sys.argv[1])
        self.host = dns[0]
        #lines added by Davif


        self.port = 9999

        # Begin connection with server and change states
        self.s.connect((self.host, self.port))
        reply = code_to_byte(10)
        self.s.sendall(reply)
        self.state = 1

        # Call the server communication loop
        self.server_loop()

    def yes(self):
        if self.state == 1 or self.state == 3:
            self.state = 3
            reply = code_to_byte(30)
            self.s.sendall(reply)
            self.server_loop()

    def no(self):
        if self.state == 1 or self.state == 3:
            self.state = 7
            reply = code_to_byte(31)
            self.s.sendall(reply)
            self.server_loop()

    def close(self):
        self.state = 7
        self.server_loop()
        self.master.quit()

    def server_loop(self):

        # Clean variable
        reply = b''

        # Terminate before checking socket
        if self.state == 7:
            reply = code_to_byte(32)
            self.s.sendall(reply)
            self.s.close

            return

        # Get the server's response
        data = ''
        code = -1

        # Check to see if there is data to read
        r, _, _ = select([self.s], [], [])
        if r:
            data = self.s.recv(4096)
            code = int.from_bytes(data[:1], byteorder = 'big')

        # Monster if to represent the FSM
        if self.state == 1 and code == 20:

            # Extract pokemon_id
            pokemon_id = int.from_bytes(data[1:2], byteorder = 'big')

            # Show user, reply will be sent from yes or no functions, exit
            self.server_msg.set('Catch pokemon with id ' + str(pokemon_id) + '?')

            return

        elif self.state == 3:

            # Check if we caught the pokemon
            if code == 22:
                pokemon_id = int.from_bytes(data[1:2], byteorder = 'big')
                image_size = int.from_bytes(data[2:6], byteorder = 'big')

                # Begin reading image data
                # Read rest of buffer, and substract from total
                image_bytes = data[6:]
                read = len(image_bytes)

                # Read until we have read all bytes
                while read < image_size:
                    data = self.s.recv(4096)
                    image_bytes = image_bytes + data
                    read = len(image_bytes)

                # Display results
                image = Image.open(BytesIO(image_bytes))
                poke_image= ImageTk.PhotoImage(image)
                self.poke_label.configure(image = poke_image)
                self.poke_label.image = poke_image
                self.server_msg.set('You caught the pokemon with id ' + str(pokemon_id))

                # Switch to termination state
                self.state = 7
            elif code == 21:
                pokemon_id = int.from_bytes(data[1:2], byteorder = 'big')
                attempts = int.from_bytes(data[2:3], byteorder = 'big')

                # Show user, reply will be sent from yes or no functions, exit
                self.server_msg.set('Keep trying to catch id ' + str(pokemon_id) + '? ' +
                        str(attempts) + ' attempts remaining.')

                return

            elif code == 23:
                self.server_msg.set('Failed to capture pokemon')

                # Switch to termination state
                self.state = 7

        self.s.sendall(reply)

        # Terminate if needed
        if self.state == 7:
            reply = code_to_byte(32)
            self.s.sendall(reply)
            self.s.close

            return

        if not data:
            self.s.close
            return

root = Tk()
gui = poke_client(root)
root.mainloop()
