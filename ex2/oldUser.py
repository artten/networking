import socket
import time

if __name__ == '__main__':
    HOST = '127.0.0.1'  # The server's hostname or IP address
    PORT = 12345       # The port used by the server

    user_code = "66uIiaz0YKnXowlUpI1xJuwAY305quuIDvZWr2yNNW6RIWKYJ3UASRMo09lMJLnjdNDqjAVIqMImATKQdpAC2eXuCho0OeySWi5itT66NJYh2jYDnGkGu6I3d01KFQ3t"
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.connect((HOST, PORT))
    #     s.sendall(bytes("old user:" + user_code + ":add new folder:./test", "utf-8"))
    #     s.close()
    #     time.sleep(1)
    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.connect((HOST, PORT))
    #     s.sendall(bytes("old user:" + user_code + ":write to file:/test/test.txt", "utf-8"))
    #     time.sleep(1)
    #     s.sendall(bytes("Hi Saar", "utf-8"))
    #     time.sleep(1)
    #     s.sendall(bytes("End of File", "utf-8"))
    #     s.close()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(bytes("old user:" + user_code + ":sync", "utf-8"))
        data = s.recv(1024)
        data = data.decode('utf-8')
        while(data != "all files sended"):
            print(data)
            data = s.recv(1024)
            data = data.decode('utf-8')
        s.close()

    # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #     s.connect((HOST, PORT))
    #     s.sendall(bytes("old user:" + user_code + ":delete folder:./test", "utf-8"))
    #     s.close()
