import socket
import sys
import random
import string
import os
import time

PATH = (sys.argv[3])

from watchdog.observers import Observer
from watchdog.events import FileSystemEvent Handler


def start_client(ip, port):
    HOST_IP = ip
    PORT = port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST_IP, PORT))
    return s

def create_folder(path):
    os.makedirs(PATH + "/" + path)

def create_file(user_code, path):
    if os.path.exists(PATH + "/" + path):
        os.remove(PATH + "/" + path)
    f = open(PATH + "/" + path, "w")
    f.close()

def append_data_to_file(path, data):
    f = open(PATH + "/" + path, "a")
    f.write(data)
    f.close()


def sync_new_user(s):
    s.send("new user:".encode('utf-8') + PATH.encode('utf-8'))
    for currentpath, folders, files in os.walk(PATH):
        for file in files:
            s.send("create file:".encode('utf-8') + (currentpath + file).encode('utf-8'))
            s.send("End of File".encode('utf-8'))
        for folder in folders:
            s.send("create folder:".encode('utf-8') + (currentpath + folder).encode('utf-8'))
    s.send("finished".encode('utf-8'))
    # recive user code from server
    code = s.recv(1024)
    return code.decode('utf-8')

def sync_old_user(s, user_code):
    s.send("old user:sync:".encode('utf-8') + user_code.encode('utf-8') + ":sync:".encode('utf-8'))
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    while(data != "all files sended") :
        command = data.split(":", 1)[0]
        if (command == "directory"):
            path = data.split(":", 1)[1]
            create_folder(user_code, path)
        if (command == "file") :
            path = data.split(":", 1)[1]
            create_file(user_code, path)
            data = connection.recv(1024)
            data = data.decode('utf-8')
            while  (data != "End of File"):
                append_data_to_file(user_code, path, data)
                data = connection.recv(1024)
                data = data.decode('utf-8')

        data = connection.recv(1024)
        data = data.decode('utf-8')

def on_created(event, s):
    s.send(user.encode('utf-8') + event.src_path.encode('utf-8'))

#def on_deleted(event):

#def on_modified(event, s_host):

#def on_moved(event):



if __name__ == "__main__":
    s = start_client(int(sys.argv[1]),sys.argv[2]);

    if len(sys.argv) <= 5:
        user_code = sync_new_user(s)
    else:
        user_code = sys.argv[5]
        sync_old_user(s, user_code)



    my_observer = Observer()
    #my_observer.schedule(my_event_handler, path, recursive=go_recursively)
    while True:
        conn, addr = s.accept()
        get_command(conn)
        conn.close()