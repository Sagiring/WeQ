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
        self.isFisrt = True
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
       
        port = self.send_port
        if msg != 'correct1\r\n' and msg != 'correct2\r\n':
           
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            key = self.session_key
            # self.send_port = 8888
            cipher = AES.new(key, AES.MODE_ECB)
            if isByte:
                msg = cipher.encrypt(pad(msg, BLOCK_SIZE))
            else:
                msg = cipher.encrypt(pad(msg.encode('utf-8'), BLOCK_SIZE))
           
            while 1:
                # try:
                    conn.connect((recv_ip,port))
                    self.send_port = port
                    break
                # except ConnectionRefusedError:
                #     time.sleep(0.1)
                #     port += 1
            # print((str(len(msg))).encode())
            # print(f'send_port:{self.send_port}')
            conn.send((str(len(msg))).encode()+ b'\r\n\r\n' + msg)
        else:
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(2)
            if msg == 'correct1\r\n':
                while self.isFisrt:
                    try:
                        conn.connect((recv_ip,self.send_port))
                        conn.settimeout(2)
                        conn.send((str(len(msg))).encode()+ b'\r\n\r\n' +msg.encode())
                        time.sleep(3)
                    except ConnectionRefusedError:
                        time.sleep(0.1)
                        self.send_port += 1
                    except TimeoutError:
                        time.sleep(0.1)
                        self.send_port += 1
                    except OSError:
                        conn.close()
                        self.send_port += 1
                        if self.send_port > 20000:
                            self.send_port = 8888
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
                    # msg = conn.recv(len(b'correct2\r\n'))
                    if msg == b'correct2\r\n':
                        print('已收到Correct2')
                        socket.setdefaulttimeout(None)
                        conn.settimeout(None)
                        self.isFisrt = False
   
                    return msg,conn,self.server
            except TimeoutError:
                pass
            except Exception as e:
                print(e)
                traceback.print_exc()

    def correct(self, ip):
        message = 'correct\r\n'
        frendip = ip
        self.send_msg(frendip, message)