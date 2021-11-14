import socket
import sys
import random
import string

HOST = "127.0.0.1"
PORT = 65432
USER_PATH = "./Users.txt"

def start_server(port, host):
    HOST = host
    PORT = port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)

    return s


def get_new_user_code(num):
        return ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=num))


def add_new_user(path):
    mode = 'a' if os.path.exists(USER_PATH + "/users.txt") else 'w'
    with open(USER_PATH + "/users.txt", mode) as f:
        user_code = get_new_user_code(128)
        while (check_if_user_exist(user_code)):
            user_code = get_new_user_code(128)
        f.write(user_code + "-" + path + "\n")
    return user_code


def create_folder(user_code, path):
    os.makedirs(USER_PATH + "/" + user_code + "/" + path)


def create_file(user_code, path):
    open(USER_PATH + "/" + user_code + "/" + path, "w")

def append_data_to_file(user_code, path, data):
    if os.path.exists(USER_PATH + "/" + user_code + "/" + path):
        os.remove(USER_PATH + "/" + user_code + "/" + path)
    f = open(USER_PATH + "/" + user_code + "/" + path, "a")
    f.write(data)
    f.close()



def check_if_user_exist(user_code):
    with open(USER_PATH + "/users.txt", "r") as users:
        for line in users:
             if(user_code == line.split("-")[0]):
                return 1
        users.close()
    return 0


def copy_files_from_user(user_code, connection) :
    if not os.path.exists(USER_PATH):
        os.makedirs(USER_PATH)
    if not os.path.exists(USER_PATH + user_code):
        os.makedirs(USER_PATH + user_code)
    data = connection.recv(1024)
    data = data.decode('utf-8')

    while(data != "finished") {
        command = data.split(":", 1)[0]
        if (command = "create folder"):
            path = data.split(":", 1)[1]
            create_folder(user_code, path)

        if (command = "create file") :
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


def send_all_files_of_user(user_code, connection):
    if (check_if_user_exist(user_code)) :
        for currentpath, folders, files in os.walk(USER_PATH + "/" + user_code):
            path = currentpath.split(user_code + "/")[1]
            for file in files:
                connection.send("file:".encode('utf-8') + (path + file).encode('utf-8'))
            for folder in folders:
                connection.send("directory:".encode('utf-8') + (path + folder).encode('utf-8'))
        connection.send("all files sended".encode('utf-8'))
    else :
     print("no such user")


def send_file(user_code, connection, path):
    f = open(USER_PATH + user_code + path, "w")
    data = f.read(1024)
    while data:
        connection.send(data)
        data = infile.read(1024)
    connection.send("Enf Of File".encode('utf-8'))


def get_command(connection):
    data = connection.recv(1024)
    data = data.decode("utf-8")
    command = data.split(":", 1)[0]
    if (command == "new user") :
        path = data.split(":", 1)[1]
        user_code = add_new_user(path)
        copy_files_from_user(user_code, connection)
    if (command = "old user") :
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
        if (command == "sync") :
            user_code = data.split(":")[2]
            send_all_files_of_user(user_code, connection)
            data = connection.recv(1024)
            data = data.decode('utf-8')
            while data != "all synced" :
                send_file(user_code, connection, data)
                data = connection.recv(1024)
                data = data.decode('utf-8')


if __name__ == "__main__":
    s = start_server(int(sys.argv[1]),"");
    while True:
        conn, addr = s.accept()
        get_command(conn)
        conn.close()
