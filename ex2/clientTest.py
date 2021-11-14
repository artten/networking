#!/usr/bin/env python3

import socket
import time
import sys

if __name__ == "__main__":

    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 65432        # The port used by the server
    print(bytes(sys.argv[1],'UTF-8'))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            s.sendall(bytes(sys.argv[1],'UTF-8'))
            time.sleep(1)


    print('Received', repr(data))
