#!/usr/bin/env python3

import socket
import time
import sys

if __name__ == "__main__":

    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 12345       # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(bytes("new user:./", "utf-8"))
        time.sleep(1)
        s.sendall(bytes("create folder:client",'utf-8'))
        time.sleep(1)
        s.sendall(bytes("create file:client/client.txt",'utf-8'))
        time.sleep(1)
        s.sendall(bytes("non",'utf-8'))
        time.sleep(1)
        s.sendall(bytes(" of\n",'utf-8'))
        time.sleep(1)
        s.sendall(bytes(" your bisnuss",'utf-8'))
        time.sleep(1)
        s.sendall(bytes("End of File",'utf-8'))
        time.sleep(1)
        s.sendall(bytes("finished",'utf-8'))
        time.sleep(1)
        print("closed")

        s.close()
