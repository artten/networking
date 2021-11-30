import socket
import sys
import random
import string
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler

PATH = (sys.argv[3])


class MyEventHandler(FileSystemEventHandler):
    def dispatch(self, event):
        event.on_moved()
        if event.event_type == "created":
            self.on_created(event)
        if event.event_type == "modified":
            self.on_modified(event)
        if event.event_type == "deleted":
            self.on_deleted(event)
        if event.event_type == "moved":
            self.on_moved(event)

    def on_created(self, event):
        if event.is_directory:
             send_data(event.src_path, ":add new folder:")
        else:
            send_data(event.src_path, ":write to file:")
            send_file_data(event.src_path)

    def on_deleted(self, event):
        send_data(event.src_path, ":delete:")

    def on_modified(self, event):
        if event.is_directory:
            send_data(event.src_path, ":add new folder:")
        else:
            send_data(event.src_path, ":write to file:")
            send_file_data(event.src_path)

    def on_moved(self, event):
        send_data(event.src_path, ":delete:")
        if event.is_directory:
            send_data(event.dest_path, ":add new folder:")
        else:
            send_data(event.dest_path, ":write to file:")
            send_file_data(event.dest_path)


def start_client(ip, port):
    HOST_IP = ip
    PORT = port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST_IP, PORT))
    return s


def create_folder(path):
    os.makedirs(PATH + "/" + path)


def create_file(path):
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
            create_file(path)
            data = s.recv(1024)
            data = data.decode('utf-8')
            while  (data != "End of File"):
                append_data_to_file(path, data)
                data = s.recv(1024)
                data = data.decode('utf-8')

        data = s.recv(1024)
        data = data.decode('utf-8')




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


def send_file_data(path):
    f = open(path, "w")
    data = f.read(1024)
    while data:
        s.send(data)
        data = f.read(1024)
    s.send("End of File".encode('utf-8'))


def get_date_of_file(path):
    modified = time.ctime(os.path.getmtime(path)).split(" ")

    return modified[4] + str(time.strptime(modified[1],'%b').tm_mon) + modified[2] + modified[3].split(":")[0]
    + modified[3].split(":")[1] + modified[3].split(":")[2]


def check_for_updates():
    fileAndDirList = []
    for currentpath, folders, files in os.walk(PATH):
        for file in files:
            fileAndDirList.insert(currentpath + file)
        for folder in folders:
            fileAndDirList.insert(currentpath + folder)

    s.send("old user:sync:".encode('utf-8') + user_code.encode('utf-8') + ":sync:".encode('utf-8'))
    if not os.path.exists(PATH):
        os.makedirs(PATH)
    while (data != "all files sended"):
        command = data.split(":", 1)[0]
        if (command == "directory"):
            path = data.split(":", 1)[1]
            if not os.path.exists(PATH + "/" + path):
                create_folder(user_code, path)
            else:
                fileAndDirList.remove(PATH + "/" + path)

        if (command == "file"):
            path = data.split(":", 1)[1]
            date = data.split(":", 1)[2]
            update = False

            if os.path.exists(PATH + "/" + path):
                fileAndDirList.remove(PATH + "/" + path)
                if date > get_date_of_file(PATH + "/" + path):
                    update = True
            else:
                update = True
            if update:
                path = data.split(":", 1)[1]
                create_file(path)
                data = s.recv(1024)
                data = data.decode('utf-8')
                while (data != "End of File"):
                    append_data_to_file(path, data)
                    data = s.recv(1024)
                    data = data.decode('utf-8')
            else:
                while (data != "End of File"):
                    data = s.recv(1024)
                    data = data.decode('utf-8')

        data = s.recv(1024)
        data = data.decode('utf-8')

    remove_deleted(fileAndDirList)


def remove_deleted(filesAndDirs):
    for path in filesAndDirs:
        if os.path.isdir(path):
            os.rmdir(path)
        else:
            os.remove(path)


if __name__ == "__main__":
    s = start_client(int(sys.argv[1]), sys.argv[2])
    my_event_handler = PatternMatchingEventHandler("*", "", False, True)
    sleepTime = int(sys.argv[4])

    if len(sys.argv) <= 5:
        user_code = sync_new_user(s)
    else:
        user_code = sys.argv[5]
        sync_old_user(s, user_code)
    s.close()

    observer = Observer()
    observer.schedule(my_event_handler, PATH, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(sleepTime)
            s.connect(int(sys.argv[1]), sys.argv[2])
            check_for_updates()
            s.close()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    s.close()
