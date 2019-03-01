
#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from termcolor import colored
import os
import base64

# ?? Python has a tudip import style of relateive path
# import sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import lib.asciify as asciify

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(msg)
            # msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break

def handle_help():
    return """
Usage: \<command> [<args>]

Some useful pyenv commands are:
    commands    List all available pyenv commands
    help        show help information
    ping        Pong!
    quit        leave chat room
    """

# ----Now comes the sockets part----
# HOST = input('Enter host: ')
# PORT = input('Enter port: ')
# if not PORT:
#     PORT = 33000
# else:
#     PORT = int(PORT)

BUFSIZ = 1024*60 # TODO https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
# ADDR = (HOST, PORT)
ADDR = ('127.0.0.1', 33335)
# ADDR = ('10.20.0.100', 33335)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
receive_thread = Thread(target=receive)
receive_thread.start()

while True:
    msg = input().rstrip() # https://stackoverflow.com/questions/2372573/how-do-i-remove-whitespace-from-the-end-of-a-string-in-python
    if msg.endswith('.png') or msg.endswith('.jpg') or msg.endswith('.jpeg') or msg.endswith('.gif'):
        if os.path.isfile(msg):
          msg = asciify.runner(msg)
    if msg == '\help':
        print(handle_help())
        continue
    client_socket.send(bytes(msg, "utf-8"))
    if msg == "\quit":
        client_socket.close()
