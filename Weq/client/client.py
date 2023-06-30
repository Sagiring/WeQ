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
        self.server_port = port
        self.send_port = port
        addrs = socket.getaddrinfo(socket.gethostname(), None)
        for item in [addr[4][0] for addr in addrs]:
            if item[:2] == '10':
                ip = item
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while 1:
            try:
                self.server.bind((ip, port))
                self.server_port = port
                break
            except OSError:
                time.sleep(0.1)
                port += 1
        self.server.listen(5)
        # print(f'recv_port:{self.server_port}')

    def __del__(self):
        self.server.close()

    def send_msg(self, recv_ip, msg,isByte = False):
        socket.setdefaulttimeout(2)
        conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = self.send_port
        if msg != 'correct1\r\n' and msg != 'correct2\r\n':
            key = self.session_key
            # self.send_port = 8888
            cipher = AES.new(key, AES.MODE_ECB)
            if isByte:
                msg = cipher.encrypt(pad(msg, BLOCK_SIZE))
            else:
                msg = cipher.encrypt(pad(msg.encode('utf-8'), BLOCK_SIZE))
           
            while 1:
                try:
                    conn.connect((recv_ip,port))
                    self.send_port = port
                    break
                except ConnectionRefusedError:
                    time.sleep(0.1)
                    port += 1
            # print((str(len(msg))).encode())
            # print(f'send_port:{self.send_port}')
            conn.send((str(len(msg))).encode()+ b'\r\n\r\n' + msg)
        else:
            
            if msg == 'correct1\r\n':
                while 1:
                    try:
                        conn.connect((recv_ip,port))
                        conn.settimeout(2)
                        conn.send((str(len(msg))).encode()+ b'\r\n\r\n' +msg.encode())
                        msg = conn.recv(1024)
                        if msg == b'correct2\r\n':
                            self.send_port = port
                            socket.setdefaulttimeout(None)
                            break
                    except ConnectionRefusedError or TimeoutError:
                        time.sleep(0.1)
                        port += 1
            else:
                conn.connect((recv_ip,port))
                conn.send((str(len(msg))).encode()+ b'\r\n\r\n' + msg.encode())
                
                    
        



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
                    
                if msg != b'correct1\r\n' and msg != b'correct2\r\n':
                    # print(len(msg))
                    key = self.session_key
                    cipher = AES.new(key, AES.MODE_ECB)
                    if isByte:
                        msg = unpad(cipher.decrypt(msg), BLOCK_SIZE)
                    else:
                        msg = unpad(cipher.decrypt(msg), BLOCK_SIZE).decode('utf-8', errors='ignore')
                    return msg,conn,self.server
                else:
                    return msg,conn,self.server
            except Exception as e:
                print(e)
                traceback.print_exc()

