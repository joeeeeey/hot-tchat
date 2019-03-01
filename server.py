#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from termcolor import colored
import lib.asciify as asciify
from art import text2art

clients = {}
addresses = {}
HOST = ''
PORT = 33335
BUFSIZ = 1024*60  # TODO https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes(text2art('STUDENT HOT CHAT\n\n\n') +
                          "Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = client.recv(BUFSIZ).decode("utf8")
    # welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    welcome = '\n Hello, ' + \
        colored(name, "yellow") + \
        '~ If you ever want to quit, type {quit} to exit.'
    # asciify

    client.send(bytes(welcome, "utf8"))
    # msg = "%s has joined the chat!" % name
    msg = colored(name, "yellow") + " has joined the chat!"
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    while True:
        try:
            msg = client.recv(BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                print('Begin sending msg is: ', msg)
                handle_msg(msg, name, client)
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                del clients[client]
                broadcast(bytes("%s has left the chat." % name, "utf8"))
                break
        except OSError:  # Possibly client has left the chat.
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

def handle_msg(msg, name, client):
    response_msg = None
    broadcast(msg, colored(name, "yellow")+": ", client)
    if (msg == b'/ping'):
        response_msg = b'Pong!'
    if (response_msg):
        broadcast(response_msg, colored('SYSTEM', "blue")+": ")

# prefix is for name identification.
def broadcast(msg, prefix="", currentClient=None):
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)
        # if(currentClient and currentClient == sock):
        #     pass
        # else:
        #     sock.send(bytes(prefix, "utf8")+msg)

if __name__ == "__main__":
    SERVER.listen(15)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SERVER.close()
