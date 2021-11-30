import socket
import sys
import random
import string
import os
import time

USER_PATH = "./Users"

def start_server(port):
    PORT = port

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', PORT))
    s.listen(5)

    return s


def get_new_user_code(num):
        return ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=num))


def add_new_user(path):
    mode = 'w'
    if not os.path.exists(USER_PATH):
        os.mkdir("Users")
    open(USER_PATH + "/users.txt", 'a')
    if os.path.exists(USER_PATH + "/users.txt"):
        mode = 'a'
    with open(USER_PATH + "/users.txt", mode) as f:
        user_code = get_new_user_code(128)
        while (check_if_user_exist(user_code)):
            user_code = get_new_user_code(128)
        f.write(user_code + "\n")
    return user_code


def create_folder(user_code, path):
    if not os.path.exists(USER_PATH + "/" + user_code + "/" + path):
        os.makedirs(USER_PATH + "/" + user_code + "/" + path)


def create_file(user_code, path):
    if os.path.exists(USER_PATH + "/" + user_code + "/" + path):
        os.remove(USER_PATH + "/" + user_code + "/" + path)
    f = open(USER_PATH + "/" + user_code + "/" + path, "w")
    f.close()


def append_data_to_file(user_code, path, data):
    f = open(USER_PATH + "/" + user_code + "/" + path, "a")
    f.write(data)
    f.close()



def check_if_user_exist(user_code):
    with open(USER_PATH + "/users.txt", "r") as users:
        for line in users:
            if(user_code == line.split("\n")[0]):
                return 1
        users.close()
    return 0


def copy_files_from_user(user_code, connection) :
    if not os.path.exists(USER_PATH):
        os.makedirs(USER_PATH)
    if not os.path.exists(USER_PATH + user_code):
        os.makedirs(USER_PATH + "/" +user_code)
    data = connection.recv(1024)
    data = data.decode('utf-8')
    while(data != "finished") :
        command = data.split(":", 1)[0]
        if (command == "create folder"):
            path = data.split(":", 1)[1]
            create_folder(user_code, path)
        if (command == "create file") :
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


def get_date_of_file(path):
    modified = time.ctime(os.path.getmtime(path)).split(" ")

    return modified[4] + str(time.strptime(modified[1],'%b').tm_mon) + modified[2] + modified[3].split(":")[0] + modified[3].split(":")[1] + modified[3].split(":")[2]


def send_all_files_of_user(user_code, connection):
    if (check_if_user_exist(user_code)) :
        for currentpath, folders, files in os.walk(USER_PATH + "/" + user_code + "/"):
            try:
                path = currentpath.split(user_code + "/")[1]
            except:
                path = ""
            for file in files:
                connection.sendall("file:".encode('utf-8')
                + (path + "/" + file).encode('utf-8') + (":"
                + get_date_of_file(path + "/" + file)).encode('utf-8'))
                time.sleep(1)
            for folder in folders:
                connection.send("directory:".encode('utf-8') + (path + folder).encode('utf-8'))
                time.sleep(1)
        connection.send("all files sended".encode('utf-8'))
        time.sleep(1)
    else :
     print("no such user")


def send_file(user_code, connection, path):
    f = open(path, "r")
    data = f.read(1024)
    while data:
        connection.sendall(bytes(data,"utf-8"))
        time.sleep(1)
        data = f.read(1024)
    connection.send(bytes("End of File","utf-8"))
    time.sleep(1)

def delete_folder(user_code, path):
    os.rmdir(USER_PATH + "/" + user_code + "/" + path)

def delete_file(user_code, path):
    os.remove(USER_PATH + "/" + user_code + "/" + path)


def get_command(connection):
    data = connection.recv(1024)
    data = data.decode("utf-8")
    command = data.split(":", 1)[0]
    print(command)
    if (command == "new user") :
        path = data.split(":", 1)[1]
        user_code = add_new_user(path)
        copy_files_from_user(user_code, connection)
    if (command == "old user") :
        user_code = data.split(":")[1]
        command = data.split(":")[2]
        if (command == "add new folder") :
            path = data.split(":")[3]
            create_folder(user_code, path)

        if (command == "write to file") :
            path = data.split(":")[3]
            create_file(user_code, path)
            data = connection.recv(1024)
            data = data.decode('utf-8')
            while  (data != "End of File"):
                append_data_to_file(user_code, path, data)
                data = connection.recv(1024)
                data = data.decode('utf-8')

        if (command == "delete file"):
            path = data.split(":")[3]
            delete_file(user_code, path)

        if (command == "delete folder"):
            path = data.split(":")[3]
            delete_folder(user_code, path)

        if (command == "sync") :
            send_all_files_of_user(user_code, connection)
            data = connection.recv(1024)
            data = data.decode('utf-8')
            while (data == "all updated") :
                path = data
                send_file(user_code, connection, path)
                data = connection.recv(1024)
                data = data.decode('utf-8')



if __name__ == "__main__":
    s = start_server(int(sys.argv[1]));
    while True:
        conn, addr = s.accept()
        get_command(conn)
