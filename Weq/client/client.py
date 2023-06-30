# import json
import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from threading import Thread
import traceback
import time
BLOCK_SIZE = 16

class Client:
    def __init__(self,session_key ,port = 8888):
        self.session_key = session_key
        addrs = socket.getaddrinfo(socket.gethostname(), None)
        for item in [addr[4][0] for addr in addrs]:
            if item[:2] == '10':
                ip = item
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cnt = 0
        while cnt<3:
            try:
                self.server.bind((ip, port))
                break
            except OSError:
                time.sleep(3)
                cnt +=1
        self.server.listen(5)

    def __del__(self):
        self.server.close()

    def send_msg(self, recv_ip, msg,isByte = False, recv_port=8888):
        key = self.session_key
        cipher = AES.new(key, AES.MODE_ECB)
        if isByte:
            msg = cipher.encrypt(pad(msg, BLOCK_SIZE))
        else:
            msg = cipher.encrypt(pad(msg.encode('utf-8'), BLOCK_SIZE))
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn.connect((recv_ip, recv_port))
        # print((str(len(msg))).encode())
        conn.send((str(len(msg))).encode()+ b'\r\n\r\n' + msg)
        



    def recv_msg(self,isByte = True):
            try:
                conn, addr = self.server.accept()
                data = conn.recv(1024)
                # print(data.split(b'\r\n\r\n')[0])
                dataLen = int(data.split(b'\r\n\r\n')[0].decode())
                msg = data.split(b'\r\n\r\n')[1]
                Len = len(msg)
                while 1:
                    if  Len >= dataLen:
                        break
                    data = conn.recv(4096)
                    msg += data
                    Len += len(data)
                    

                # print(len(msg))
                key = self.session_key
                cipher = AES.new(key, AES.MODE_ECB)
                if isByte:
                    msg = unpad(cipher.decrypt(msg), BLOCK_SIZE)
                else:
                    msg = unpad(cipher.decrypt(msg), BLOCK_SIZE).decode('utf-8', errors='ignore')
                return msg,conn,self.server
                # if msg == 'quit':
                #     print('对方退出聊天')
                #     conn.close()
                #     break
                # else:
                #     print(f'{addr} say:', msg)
                #     conn.close()
            except Exception as e:
                print(e)
                traceback.print_exc()

    def chat(self, recv_ip, recv_port):
        t1 = Thread(target=self.recv_msg)
        t2 = Thread(target=self.send_msg, args=(recv_ip, recv_port))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
