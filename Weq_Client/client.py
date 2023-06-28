import json
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from threading import Thread

BLOCK_SIZE = 16

class Client:
    def __init__(self, ip, port):
        self.session_key = ''
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.server.listen(5)

    def __del__(self):
        self.server.close()

    def send_msg(self, recv_ip, recv_port):
        while True:
            msg = input()
            key = self.session_key
            cipher = AES.new(key, AES.MODE_ECB)
            msg = cipher.encrypt(pad(msg.encode('utf-8'), BLOCK_SIZE))

            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect((recv_ip, recv_port))
            conn.send(msg)
            if msg == 'quit':
                print('退出聊天')
                break

    def recv_msg(self):
        while True:
            try:
                conn, addr = self.server.accept()
                msg = conn.recv(4096)
                key = self.session_key
                cipher = AES.new(key, AES.MODE_ECB)
                msg = unpad(cipher.decrypt(msg), BLOCK_SIZE).decode('utf-8', errors='ignore')
                if msg == 'quit':
                    print('对方退出聊天')
                    conn.close()
                    break
                else:
                    print(f'{addr} say:', msg)
                    conn.close()
            except Exception as e:
                print(e)
                exit()

    def chat(self, recv_ip, recv_port):
        t1 = Thread(target=self.recv_msg)
        t2 = Thread(target=self.send_msg, args=(recv_ip, recv_port))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
