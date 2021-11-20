import socket
import sys
import random
import string
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler

PATH = (sys.argv[3])




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
            data = s.recv(1024)
            data = data.decode('utf-8')
            while  (data != "End of File"):
                append_data_to_file(user_code, path, data)
                data = s.recv(1024)
                data = data.decode('utf-8')

        data = s.recv(1024)
        data = data.decode('utf-8')


def on_created(event):
    s.send(user_code.encode('utf-8') + event.src_path.encode('utf-8'))
    if event.is_directory:
        # send_directory(event.src_path)
        send_data(event.src_path, ":add new folder:")
    else:
        # send_file(event.src_path)
        send_data(event.src_path, ":write to file:")


# def on_deleted(event):


def on_modified(event):
    s.send(user_code.encode('utf-8') + event.src_path.encode('utf-8'))
    if event.is_directory:
        # send_directory(event.src_path)
        send_data(event.src_path, ":add new folder:")
    else:
        # send_file(event.src_path)
        send_data(event.src_path, ":write to file:")

# def on_moved(event):


def send_data(path, command):
    p = path.split(PATH + "/")[1]
    s.send("old user:".encode('utf-8') + user_code.encode('utf-8') + command.encode('utf-8') + p.encode('utf-8'))


def send_file(path):
    # is the actual file being sent?
    p = path.split(PATH + "/")[1]
    s.send("old user:".encode('utf-8') + user_code.encode('utf-8') + ":write to file:".encode('utf-8') + p.encode('utf-8'))


def send_directory(path):
    p = path.split(PATH + "/")[1]
    s.send("old user:".encode('utf-8') + user_code.encode('utf-8') + ":add new folder:".encode('utf-8') + p.encode('utf-8'))


if __name__ == "__main__":
    s = start_client(int(sys.argv[1]), sys.argv[2])
    my_event_handler = PatternMatchingEventHandler("*", "", False, True)

    if len(sys.argv) <= 5:
        user_code = sync_new_user(s)
    else:
        user_code = sys.argv[5]
        sync_old_user(s, user_code)

    observer = Observer()
    observer.schedule(my_event_handler, PATH, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    s.close()